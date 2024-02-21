# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: Mark.Sandan@teradata.com
Secondary Owner:

"""
#  This module deals with creating SQLEngine expressions
#  for tables and columns as well as sql for displaying 
#  the DataFrame. The objects in this module are internal 
#  and implement the interfaces in sql_interfaces.py
import warnings

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants, \
    SQLFunctionConstants, TDMLFrameworkKeywords, GeospatialConstants
from teradataml.options.configure import configure
from teradataml.options.display import display
from teradataml.utils.dtypes import _Dtypes
from teradataml.utils.validators import _Validators
from teradataml.dataframe.vantage_function_types import _get_function_expression_type
from teradatasqlalchemy.types import _TDType
from .sql_interfaces import TableExpression, ColumnExpression
from sqlalchemy.sql.elements import BinaryExpression, ClauseElement, Grouping, ClauseList
try:
    from sqlalchemy.sql.elements import ExpressionClauseList
except ImportError:
    pass
from sqlalchemy.sql.functions import GenericFunction, Function
from sqlalchemy import (Table, Column, literal, MetaData, func, or_, and_, literal_column, null)
from sqlalchemy.sql.expression import text, case as case_when
import functools
import sqlalchemy as sqlalc

import re

from teradatasqlalchemy.dialect import dialect as td_dialect, compiler as td_compiler
from teradatasqlalchemy import (INTEGER, SMALLINT, BIGINT, BYTEINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy import (DATE, TIME, TIMESTAMP)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
from teradatasqlalchemy import (INTERVAL_DAY, INTERVAL_DAY_TO_HOUR, INTERVAL_DAY_TO_MINUTE,
                                INTERVAL_DAY_TO_SECOND, INTERVAL_HOUR, INTERVAL_HOUR_TO_MINUTE,
                                INTERVAL_HOUR_TO_SECOND, INTERVAL_MINUTE, INTERVAL_MINUTE_TO_SECOND,
                                INTERVAL_MONTH, INTERVAL_SECOND, INTERVAL_YEAR,
                                INTERVAL_YEAR_TO_MONTH)
from teradatasqlalchemy import (PERIOD_DATE, PERIOD_TIME, PERIOD_TIMESTAMP)
from teradatasqlalchemy import XML, GEOMETRY
import decimal
import datetime as dt
from teradataml.dataframe.window import Window
from teradataml.common.bulk_exposed_utils import _validate_unimplemented_function
from teradataml.common.utils import UtilFuncs


def _resolve_value_to_type(value, **kw):
    """
    DESCRIPTION:
        Internal function for coercing python literals to sqlalchemy_terdata types
        or retrieving the derived type of ColumnExpression

    PARAMETERS:
        value: a python literal type or ColumnExpression instance
        **kw: optional parameters
            len_: a length for the str type

    RETURNS:
        result: sqlalchemy TypeEngine derived type or ColumnExpression derived type

    Note:
        - Currently the supported literal types are str/float/int/decimal
          since these are being rendered already by teradatasqlalchemy

        - Mainly used in assign when passing literal values to be literal columns
    """
    length = kw.get('len_', configure.default_varchar_size)

    type_map = {
        str: VARCHAR(length, charset = 'UNICODE'),
        bytes: VARBYTE(length),
        int: INTEGER(),
        float: FLOAT(),
        bool: BYTEINT(),
        decimal.Decimal: DECIMAL(38,37),
        dt.date: DATE(),
        dt.datetime: TIMESTAMP(),
        dt.time: TIME()
    }

    result = type_map.get(type(value))

    if isinstance(value, ColumnExpression):
        result = value.type
    return result

def _handle_sql_error(f):
    """
    DESCRIPTION:
        This decorator wraps python special methods that generate SQL for error handling.
        Any error messages or error codes involving sql generating methods
        can be considered here.

    PARAMETERS:
        A function or method that generates sql

    EXAMPLES:
        @_handle_sql_error
        def __and__(self, other)
    """
    @functools.wraps(f)
    def binary(*args, **kw):

        self_ = None
        other_ = None

        if len(args) == 2:
            self_, other_ = args

        # Used to determine whether multiple dataframes are given in _SQLColumnExpression.
        multiple_dataframes = False

        try:
            if self_ is not None and other_ is not None and\
                isinstance(self_, ColumnExpression) and\
                isinstance(other_, ColumnExpression) and\
                self_.table is not None and other_.table is not None:

                # If table names or schema names are different or has_multiple_dataframes flag
                # is True for any of the two _SQLColumnExpressions.
                if self_.table.name != other_.table.name or\
                    self_.table.schema != other_.table.schema or\
                    self_.get_flag_has_multiple_dataframes() == True or\
                    other_.get_flag_has_multiple_dataframes() == True:

                    multiple_dataframes = True

            # If _SQLColumnExpressions have NULL tables (ie at later levels of a multi level
            # expression).
            elif isinstance(self_, ColumnExpression) and\
                isinstance(other_, ColumnExpression) and\
                self_.table is None and other_.table is None:

                multiple_dataframes = self_.get_flag_has_multiple_dataframes() | \
                                      other_.get_flag_has_multiple_dataframes()

            res = f(*args, **kw)
            # Assign True or False to resultant _SQLColumnExpression based on previous two
            # _SQLColumnExpressions.
            res.set_flag_has_multiple_dataframes(multiple_dataframes)
            res.original_column_expr = [self_, other_]

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode) from err

        return res

    return binary

class _MetaExpression(object):
    """
    The _MetaExpression contains the TableExpression and provides the DataFrame with metadata
    from the underlying Table as well as methods for translating and generating SQL.

    The main responsibility of this class is to translate sql expressions internally in DataFrame.
    Other responsibilities are delegated to the underlying TableExpression.

    This class is internal.
    """

    def __init__(self, table, **kw):
        """
        PARAMETERS:
            table: the table to use for TableExpression

            kw: kwargs for implementation specific TableExpressions/ColumnExpressions
              - dialect: an implementation of a SQLAlchemy Dialect
        """

        self._dialect = kw.get('dialect', td_dialect())
        self.__t = _SQLTableExpression(table, **kw)
        self._is_persist = kw.get("is_persist", False)

    def __getattr__(self, key):
        """
        DESCRIPTION:
            Retrieve an attribute from _MetaExpression or the underlying TableExpression

        PARAMETERS:
            key: attribute name

        RAISES:
            AttributeError if attribute can't be found
        """

        res = getattr(self.__t, key, None)
        if res is None:
            raise AttributeError('Unable to find attribute: %s' % key)

        return res

    @property
    def _n_rows(self):
        return self.__t._n_rows

    @_n_rows.setter
    def _n_rows(self, value):
        """Use n number of rows for print() instead of display.max_rows for this metaexpr. If 0, display.max_rows is used"""
        if not isinstance(value, int) or value <= 0:
            raise ValueError('n_rows must be a positive int.')

        self.__t._n_rows = value

    def __repr__(self):
      return repr(self.__t)

class _PandasTableExpression(TableExpression):

    def _assign(self, drop_columns, **kw):
        """
        DESCRIPTION:
            Internal method for DataFrame.assign
            Generates the new select list ColumnExpressions and
            provides an updated _SQLTableExpression for the new _MetaExpression

        PARAMETERS:
            drop_columns (optional):  bool If True, drop columns that are not specified in assign. The default is False.
            kw: keyword, value pairs
                    - keywords are the column names.
                    - values can be column arithmetic expressions and int/float/string literals.

        RAISES:
            ValueError when a value that is callable is given in kwargs


        See Also
        --------
            DataFrame.assign


        Returns
        -------
        result : -Updated _SQLTableExpression
                 -list of compiled ColumnExpressions

        Note: This method assumes that the values in each key of kw
              are valid types (supported python literals or ColumnExpressions)
        """
        compiler = td_compiler(td_dialect(), None)
        current = {c.name for c in self.c}

        assigned_expressions = []

        existing = [(c.name, c) for c in self.c]
        new = [(label, expression) for label, expression in kw.items() if label not in current]
        new = sorted(new, key = lambda x: x[0])

        for alias, expression in existing + new:
            if drop_columns and alias not in kw:
                continue

            else:
                expression = kw.get(alias, expression)
                if isinstance(expression, ClauseElement):
                    expression = _SQLColumnExpression(expression)

                type_ = _resolve_value_to_type(expression)

                if not isinstance(expression, ColumnExpression):
                    # wrap literals. See DataFrame.assign for valid literal values
                    if expression == None:
                        expression = _SQLColumnExpression(null())
                    else:
                        expression = _SQLColumnExpression(literal(expression,
                                                                  type_=type_))

                aliased_expression = compiler.visit_label(expression.expression.label(alias),
                                                        within_columns_clause=True,
                                                        include_table = False,
                                                        literal_binds = True)
                assigned_expressions += [(alias, aliased_expression, type_)]

        if len(assigned_expressions) >= TeradataConstants['TABLE_COLUMN_LIMIT'].value:
            raise ValueError('Maximum column limit reached')

        cols = (Column(name, type_) for name, expression, type_ in assigned_expressions)
        t = Table(self.name, MetaData(), *cols)

        return (_SQLTableExpression(t), assigned_expressions)


    def _filter(self, axis, op, index_labels, **kw):
        """
        DESCRIPTION:
            Subset rows or columns of dataframe according to labels in the specified index.

        PARAMETERS:
            axis: int
                1 for columns to filter
                0 for rows to filter

            op: string
                A string representing the way to index.
                This parameter is used along with axis to get the correct expression.

            index_labels: list or iterable of string
                contains column names/labels of the DataFrame

            **kw: keyword arguments
                items: None or a list of strings
                like: None or a string representing a substring
                regex: None or a string representing a regex pattern

                optional keywords:
                match_args: string of characters to use for REGEXP_SUBSTR

        RETURNS:
            tuple of two elements:
                Either a tuple of (list of str, 'select') if axis == 1
                Or a tuple of (list of ColumnExpressions, 'where') if axis == 0

        Note:
            Implementation outline:

            axis == 1 (column based filter)

                items - [colname for colname in colnames if colname in items]
                like - [colname for colname in colnames if like in colname]
                regex - [colname for colname in colnames if re.search(regex, colname) is not None]

            axis == 0 (row value based filter on index)

                items - WHERE index IN ( . . . )
                like -  same as regex except the string (kw['like']) is a substring pattern
                regex - WHERE REGEXP_SUBSTR(index, regex, 1, 1, 'c')


        EXAMPLES:

            # self is a reference to DataFrame's _metaexpr.
            # This method is usually called from the DataFrame.
            # Suppose the DataFrame has columns ['a', 'b', 'c'] in its index:

            # select columns given in items list
            self._filter(1, 'items', ['a', 'b', 'c'], items = ['a', 'b'])

            # select columns matching like pattern (index_labels is ignored)
            self._filter(1, 'like', ['a', 'b', 'c'], like = 'substr')

            # select columns matching regex pattern (index_labels is ignored)
            self._filter(1, 'regex', ['a', 'b', 'c'], regex = '[0|1]')

            # select rows where index column(s) are in items list
            self._filter(0, 'items', ['a', 'b', 'c'], items = [('a', 'b', 'c')])

            # select rows where index column(s) match the like substring
            self._filter(0, 'like', ['a', 'b', 'c'], like = 'substr')

            # select rows where index column(s) match the regex pattern
            self._filter(0, 'regex', ['a', 'b', 'c'], regex = '[0|1]')
        """

        impls = dict({

            ('like', 1):  lambda col: kw['like'] in col.name,

            ('regex', 1): lambda col: re.search(kw['regex'], col.name) is not None,

            ('items', 0): lambda colexp, lst: colexp.in_(lst),

            ('like', 0):  lambda colexp: func.regexp_substr(colexp, kw['like'], 1, 1,
                                                            kw.get('match_arg', 'c')) != None,

            ('regex', 0): lambda colexp: func.regexp_substr(colexp, kw['regex'], 1, 1,
                                                            kw.get('match_arg', 'c')) != None
        }
        )

        filtered_expressions = []
        filter_ = impls.get((op, axis))
        is_char_like = lambda x: isinstance(x, CHAR) or\
                                 isinstance(x, VARCHAR) or\
                                 isinstance(x, CLOB)
        if axis == 1:

            # apply filtering to columns and then select()
            if op == 'items':
                for col in kw['items']:
                    filtered_expressions += [col]

            else:
                for col in self.c:
                    if filter_(col):
                        filtered_expressions += [col.name]

        else:
            # filter based on index values
            # apply filtering to get appropriate ColumnExpression then __getitem__()

            if op == 'items':

                if len(index_labels) == 1:

                    # single index case
                    for c in self.c:
                        if c.name in index_labels:

                            expression = c.expression
                            filtered_expressions += [filter_(expression, kw['items'])]

                else:

                    # multi index case
                    items_by_position = zip(*kw['items'])

                    # traverse in the order given by index_label
                    for index_col, item in zip(index_labels, items_by_position):
                        for c in self.c:
                            if c.name == index_col:
                                expression = c.expression
                                filtered_expressions += [filter_(expression, item)]

            else:

                var_size = kw.get('varchar_size', configure.default_varchar_size)
                for c in self.c:
                    if c.name in index_labels:

                        expression = c.expression
                        if not is_char_like(expression.type):
                            # need to cast to char-like operand for REGEXP_SUBSTR
                            expression = expression.cast(type_ = VARCHAR(var_size))

                        filtered_expressions += [filter_(expression)]

            if axis == 0:

                if op == 'items' and len(index_labels) > 1:

                    # multi index item case is a conjunction
                    filtered_expressions = _SQLColumnExpression(and_(*filtered_expressions))

                else:
                    filtered_expressions = _SQLColumnExpression(or_(*filtered_expressions))

        return filtered_expressions


class _SQLTableExpression(_PandasTableExpression):
    """
        This class implements TableExpression and is contained
        in the _MetaExpressions class

        It handles:
            - SQL generation for the table or all it's columns
            - DataFrame metadata access using a sqlalchemy.Table

      This class is internal.
    """
    def __init__(self, table, **kw):

        """
        DESCRIPTION:
            Initialize the _SQLTableExpression

        PARAMETERS:
            table : A sqlalchemy.Table
            kw**: a dict of optional parameters
                - column_order: a collection of string column names
                                in the table to be ordered in the c attribute
        """

        self.t = table
        if 'column_order' in kw:
            # Use DataFrame.columns to order the columns in the metaexpression
            columns = []
            for c in kw['column_order']:
                name = c.strip()
                col = table.c.get(name, table.c.get(name.lower(), table.c.get(name.upper())))

                if col is None:
                    raise ValueError('Reflected column names do not match those in DataFrame.columns')

                columns.append(_SQLColumnExpression(col))
            self.c = columns

        else:
            self.c = [_SQLColumnExpression(c) for c in table.c]

        self._n_rows = 0


    @property
    def c(self):
        """
        Returns the underlying collection of _SQLColumnExpressions
        """
        return self.__c

    @c.setter
    def c(self, collection):
        """
        Set the underlying map of _SQLColumnExpressions

        PARAMETERS:
            collection: a dict of _SQLColumnExpressions

        """
        is_sql_colexpression = lambda x: isinstance(x, _SQLColumnExpression)
        valid_collection = isinstance(collection, list) and\
                         len(collection) > 0 and\
                         all(map(is_sql_colexpression, collection))

        if (not valid_collection):
            raise ValueError("collection must be a non empty list of _SQLColumnExpression instances. Got {}".format(collection))


        self.__c = collection

    @property
    def name(self):
        """
        Returns the name of the underlying SQLAlchemy Table
        """
        return self.t.name

    @property
    def t(self):
        """
        Returns the underlying SQLAlchemy Table
        """
        return self.__t

    @t.setter
    def t(self, table):
        """
        Set the underlying SQLAlchemy Table

        PARAMETERS:
            table : A sqlalchemy.Table
        """
        if (not isinstance(table, Table)):
            raise ValueError("table must be a sqlalchemy.Table")

        self.__t = table

    def __repr__(self):
        """
        Returns a SELECT TOP string representing the underlying table.
        For representation purposes:
            - the columns are cast into VARCHAR
            - certain numeric columns are first rounded
            - character-like columns are unmodified
            - byte-like columns are called with from_bytes to show them as ASCII


        Notes:
            - The top integer is taken from teradataml.options
            - The rounding value for numeric types is taken from teradataml.options
            - from_bytes is called on byte-like columns to represent them as ASCII encodings
              See from_bytes for more info on different encodings supported:
              Teradata® Database SQL Functions, Operators, Expressions, and Predicates, Release 16.20

        """
        # TODO: refactor this to be in the ColumnExpression instances
        single_quote = literal_column("''''")
        from_bytes = lambda c: ('b' + single_quote + func.from_bytes(c, display.byte_encoding) + single_quote).label(c.name)
        display_decimal = lambda c: func.round(c, display.precision).cast(type_ = DECIMAL(38, display.precision)).label(c.name)
        display_number = lambda c: func.round(c, display.precision).label(c.name)

        # By default for BLOB data, display only first 10 characters following 3 dot characters.
        # If display option "blob_length" is set to None, then display all the data in the BLOB column.
        blob_substr = lambda c: func.substr(c, 0, display.blob_length)
        dots = "..."
        if display.blob_length is None:
            blob_substr = lambda c: func.substr(c, 0)
            dots = ""
        blob_expression = lambda c: func.from_bytes(blob_substr(c), display.byte_encoding) + dots
        display_blob = lambda c: ('b' + single_quote + blob_expression(c) + single_quote).label(c.name)

        compiler = td_compiler(td_dialect(), None)
        cast_expr = lambda c, var_size: c.cast(type_ = VARCHAR(var_size)).label(c.name)

        max_rows = display.max_rows
        if self._n_rows > 0:
            max_rows = self._n_rows

        res = 'select top {} '.format(max_rows)
        expressions = []
        interval_types= _Dtypes._get_interval_data_types()
        datetime_period_types = _Dtypes._get_datetime_period_data_types()

        for c in self.c:
            if isinstance(c.type, (CHAR, VARCHAR, CLOB, FLOAT, INTEGER, SMALLINT,
                                   BIGINT, BYTEINT, XML)):
                expression = c.expression.label(c.name)
            elif isinstance(c.type, (BYTE, VARBYTE)):
                expression = from_bytes(c.expression)
            elif isinstance(c.type, BLOB):
                expression = display_blob(c.expression)
            elif isinstance(c.type, DECIMAL):
                expression = display_decimal(c.expression)
            elif isinstance(c.type, NUMBER):
                expression = display_number(c.expression)
            elif isinstance(c.type, tuple(datetime_period_types)):
                expression = cast_expr(c.expression, 30)
            elif isinstance(c.type, tuple(interval_types)):
                expression = cast_expr(c.expression, 20)
            elif isinstance(c.type, GEOMETRY):
                expression = cast_expr(c.expression, display.geometry_column_length) if \
                    display.geometry_column_length is not None else c.expression.label(c.name)
            else:
                expression = cast_expr(c.expression,
                                       configure.default_varchar_size)

            expressions.append(compiler.visit_label(expression,
                                                within_columns_clause=True,
                                                include_table = False,
                                                literal_binds = True))

        return res + ', '.join(expressions)

class _LogicalColumnExpression(ColumnExpression):

    """
        The _LogicalColumnExpression implements the logical special methods
        for _SQLColumnExpression.
    """
    def __get_other_expr(self, other):
        """
        Internal function to get the SQL expression of the object.

        PARAMETERS:
            other:
                Required Argument.
                Specifies a python literal, ColumnExpression or GeometryType.
                Types: bool, float, int, str, ColumnExpression, GeometryType

        RETURNS:
            Expression as string

        RAISES:
            None

        EXAMPLES:
            expr = self.__get_other_expr(other)
        """
        from teradataml.geospatial.geometry_types import GeometryType
        from sqlalchemy import text
        if isinstance(other, _SQLColumnExpression):
            expr = other.expression
        elif isinstance(other, GeometryType):
            expr = text(other._vantage_str_())
        else:
            expr = other

        return expr

    def __coerce_to_text(self, other):
        """
        Internal function to coerce to text, using SQLAlchemy text(), a string literal passed as an argument.

        PARAMETERS:
            other: A python literal or another ColumnExpression.

        RETURNS:
            Python literal coerced to text if the input is a string literal, else the input argument itself.
        """
        if isinstance(other, str):
            return text(other)
        return other

    @_handle_sql_error
    def __and__(self, other):
        """
        Compute the logical AND between two ColumnExpressions using &.
        The logical AND operator is an operator that performs a logical
        conjunction on two statements.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students who got the admission (i.e., admitted = 1)
            #            and has GPA greater than 3.5.
            >>> df[(df.gpa > 3.5) & (df.admitted == 1)]
               masters   gpa     stats programming  admitted
            id
            21      no  3.87    Novice    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            3       no  3.70    Novice    Beginner         1
            20     yes  3.90  Advanced    Advanced         1
            37      no  3.52    Novice      Novice         1
            35      no  3.68    Novice    Beginner         1
            12      no  3.65    Novice      Novice         1
            18     yes  3.81  Advanced    Advanced         1
            17      no  3.83  Advanced    Advanced         1
            23     yes  3.59  Advanced      Novice         1


        """
        other = self.__coerce_to_text(other)
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression & expr)
        return res

    @_handle_sql_error
    def __rand__(self, other):
        """
        Compute the reverse of logical AND between two ColumnExpressions using &.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students who got the admission (i.e., admitted = 1)
            #            and has GPA greater than 3.5.
            >>> df[(df.gpa > 3.5) & (df.admitted == 1)]
               masters   gpa     stats programming  admitted
            id
            21      no  3.87    Novice    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            3       no  3.70    Novice    Beginner         1
            20     yes  3.90  Advanced    Advanced         1
            37      no  3.52    Novice      Novice         1
            35      no  3.68    Novice    Beginner         1
            12      no  3.65    Novice      Novice         1
            18     yes  3.81  Advanced    Advanced         1
            17      no  3.83  Advanced    Advanced         1
            23     yes  3.59  Advanced      Novice         1
        """
        return self & other

    @_handle_sql_error
    def __or__(self, other):
        """
        Compute the logical OR between two ColumnExpressions using |.
        The logical OR operator is an operator that performs a
        inclusive disjunction on two statements.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa greater than
            #            3.5 or 'Advanced' programming skills.
            >>> df[(df.gpa > 3.5) | (df.programming == "Advanced")]
               masters   gpa     stats programming  admitted
            id
            30     yes  3.79  Advanced      Novice         0
            40     yes  3.95    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            37      no  3.52    Novice      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            3       no  3.70    Novice    Beginner         1
            1      yes  3.95  Beginner    Beginner         0
            20     yes  3.90  Advanced    Advanced         1
            35      no  3.68    Novice    Beginner         1
            14     yes  3.45  Advanced    Advanced         0
        """
        other = self.__coerce_to_text(other)
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression | expr)
        return res

    @_handle_sql_error
    def __ror__(self, other):
        """
        Compute the reverse of logical OR between two ColumnExpressions using |.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa greater than
            #            3.5 or 'Advanced' programming skills.
            >>> df[(df.gpa > 3.5) | (df.programming == "Advanced")]
               masters   gpa     stats programming  admitted
            id
            30     yes  3.79  Advanced      Novice         0
            40     yes  3.95    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            37      no  3.52    Novice      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            3       no  3.70    Novice    Beginner         1
            1      yes  3.95  Beginner    Beginner         0
            20     yes  3.90  Advanced    Advanced         1
            35      no  3.68    Novice    Beginner         1
            14     yes  3.45  Advanced    Advanced         0
        """
        return self | other

    @_handle_sql_error
    def __invert__(self):
        """
        Compute the logical NOT of ColumnExpression using ~.

        PARAMETERS:
            None

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get the negation of gpa not equal to 3.44 or
            #            admitted equal to 1.
            >>> df[~((df.gpa != 3.44) | (df.admitted == 1))]
                         id masters   gpa   stats  admitted
            programming
            Novice        5      no  3.44  Novice         0
        """
        return _SQLColumnExpression(~self.expression)

    @_handle_sql_error
    def __gt__(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values greater than the other or not.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all the students with gpa greater than 3.
            >>> df[df.gpa > 3]
               masters   gpa     stats programming  admitted
            id
            14     yes  3.45  Advanced    Advanced         0
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            3       no  3.70    Novice    Beginner         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            37      no  3.52    Novice      Novice         1
            1      yes  3.95  Beginner    Beginner         0
            31     yes  3.50  Advanced    Beginner         1

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure greater than 400 and investment
            #            greater than 170.
            >>> df[(df.expenditure > 400) & (df.investment > 170)]
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        expr = self.__get_other_expr(other)
        res = _SQLColumnExpression(self.expression > expr)
        return res

    @_handle_sql_error
    def __lt__(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values less than the other or not.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa less than 3.
            >>> df[df.gpa < 3]
               masters   gpa     stats programming  admitted
            id
            24      no  1.87  Advanced      Novice         1
            19     yes  1.98  Advanced    Advanced         0
            38     yes  2.65  Advanced    Beginner         1
            7      yes  2.33    Novice      Novice         1

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure less than 440 and
            #            income greater than 180.
            >>> df[(df.expenditure < 440) & (df.income > 180)]
               start_time_column end_time_column  expenditure  income  investment
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0
        """
        expr = self.__get_other_expr(other)
        res = _SQLColumnExpression(self.expression < expr)
        return res

    @_handle_sql_error
    def __ge__(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values greater than or equal to the other or not.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa greater than
            #            or equal to 3.
            >>> df[df.gpa >= 3]
               masters   gpa     stats programming  admitted
            id
            30     yes  3.79  Advanced      Novice         0
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            3       no  3.70    Novice    Beginner         1
            1      yes  3.95  Beginner    Beginner         0
            37      no  3.52    Novice      Novice         1
            14     yes  3.45  Advanced    Advanced         0

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure greater than or equal to 450 and
            #            investment is greater than or equal to 200.
            >>> df[(df.expenditure >= 450) & (df.investment >= 200)]
               start_time_column end_time_column  expenditure  income  investment
            id
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        expr = self.__get_other_expr(other)
        res = _SQLColumnExpression(self.expression >= expr)
        return res

    @_handle_sql_error
    def __le__(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values less than or equal to the other or not.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa less than or
            #            equal to 3.
            >>> df[df.gpa <= 3]
               masters   gpa     stats programming  admitted
            id
            24      no  1.87  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            19     yes  1.98  Advanced    Advanced         0
            38     yes  2.65  Advanced    Beginner         1
            7      yes  2.33    Novice      Novice         1

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure less than or equal to
            #            500 and income less than or equal to 480.
            >>> df[(df.expenditure <= 500) & (df.income <= 480)]
               start_time_column end_time_column  expenditure  income  investment
            id
            2           67/06/30        07/07/10        421.0   465.0       179.0
            1           67/06/30        07/07/10        415.0   451.0       180.0
        """
        expr = self.__get_other_expr(other)
        res = _SQLColumnExpression(self.expression <= expr)
        return res

    @_handle_sql_error
    def __xor__(self, other):
        """
        Compute the logical XOR between two ColumnExpressions using ^.
        The logical XOR operator is an operator that performs a
        exclusive disjunction on two statements.

        PARAMETERS:
            other:
                Required Argument.
                Specifies another ColumnExpression.
                Types: ColumnExpression

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa is greater
            #            than 3.5 or programming skills are 'Advanced'.
            >>> df[(df.gpa > 3.5) ^ (df.programming == "Advanced")]
               masters   gpa     stats programming  admitted
            id
            14     yes  3.45  Advanced    Advanced         0
            40     yes  3.95    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            37      no  3.52    Novice      Novice         1
            3       no  3.70    Novice    Beginner         1
            1      yes  3.95  Beginner    Beginner         0
            2      yes  3.76  Beginner    Beginner         0
            35      no  3.68    Novice    Beginner         1
            29     yes  4.00    Novice    Beginner         0
            30     yes  3.79  Advanced      Novice         0
        """
        other = self.__coerce_to_text(other)
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression((self.expression | expr) & ~(self.expression & expr))
        return res

    @_handle_sql_error
    def __rxor__(self, other):
        """
        Compute the reverse of logical XOR between two ColumnExpressions using ^.

        PARAMETERS:
            other:
                Required Argument.
                Specifies another ColumnExpression.
                Types: ColumnExpression

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa greater than
            #            3.5 or programming skills are 'Advanced'.
            >>> df[(df.gpa > 3.5) ^ (df.programming == "Advanced")]
               masters   gpa     stats programming  admitted
            id
            14     yes  3.45  Advanced    Advanced         0
            40     yes  3.95    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            37      no  3.52    Novice      Novice         1
            3       no  3.70    Novice    Beginner         1
            1      yes  3.95  Beginner    Beginner         0
            2      yes  3.76  Beginner    Beginner         0
            35      no  3.68    Novice    Beginner         1
            29     yes  4.00    Novice    Beginner         0
            30     yes  3.79  Advanced      Novice         0
        """
        return self ^ other

    @_handle_sql_error
    def __eq__(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values equal to the other.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa equal to 3.44.
            >>> df[df.gpa == 3.44]
               masters   gpa   stats programming  admitted
            id
            5       no  3.44  Novice      Novice         0

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure equal to 415 or income equal to 509.
            >>> df[(df.expenditure == 415) | (df.income == 509)]
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        expr = self.__get_other_expr(other)
        res = _SQLColumnExpression(self.expression == expr)
        return res

    @_handle_sql_error
    def __ne__(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values not equal to the other.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            24      no  1.87  Advanced      Novice         1
            39     yes  3.75  Advanced    Beginner         0
            30     yes  3.79  Advanced      Novice         0

            # Example 1: Get all students with gpa not equal to 3.44.
            >>> df[df.gpa != 3.44]
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            24      no  1.87  Advanced      Novice         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            3       no  3.70    Novice    Beginner         1
            30     yes  3.79  Advanced      Novice         0

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure not equal to 415 or income
            #            not equal to 400.
            >>> df[(df.expenditure != 415) | (df.income != 400)]
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        expr = self.__get_other_expr(other)
        res = _SQLColumnExpression(self.expression != expr)
        return res


class _ArithmeticColumnExpression(ColumnExpression):

    """
        The _ArithmeticColumnExpression implements the arithmetic special methods
        for _SQLColumnExpression.
    """

    @_handle_sql_error
    def __add__(self, other):
        """
        Compute the sum between two ColumnExpressions using +.
        This is also the concatenation operator for string-like columns.

        PARAMETERS:
            other :
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Add 100 to the expenditure amount and assign the final amount
            #            to new column 'total_expenditure'.
            >>> df.assign(total_expenditure=df.expenditure + 100)
               start_time_column end_time_column  expenditure  income  investment  total_expenditure
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0              534.0
            2           67/06/30        07/07/10        421.0   465.0       179.0              521.0
            1           67/06/30        07/07/10        415.0   451.0       180.0              515.0
            5           67/06/30        07/07/10        459.0   509.0       211.0              559.0
            4           67/06/30        07/07/10        448.0   493.0       192.0              548.0

            # Example 2: Add expenditure amount to the investment amount and assign the
            #            final amount to new column 'total_investmet'.
            >>> df.assign(total_investmet=df.expenditure + df.investment)
               start_time_column end_time_column  expenditure  income  investment  total_investmet
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0                        619.0
            2           67/06/30        07/07/10        421.0   465.0       179.0                        600.0
            1           67/06/30        07/07/10        415.0   451.0       180.0                        595.0
            5           67/06/30        07/07/10        459.0   509.0       211.0                        670.0
            4           67/06/30        07/07/10        448.0   493.0       192.0                        640.0
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression + expr)
        return res

    @_handle_sql_error
    def __radd__(self, other):
        """
        Compute the rhs sum between two ColumnExpressions using +

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
            
            # Example 1: Add 100 to the expenditure amount and assign the final amount
            #            to new column 'total_expenditure'.
            >>> df.assign(total_expenditure=df.expenditure + 100)
               start_time_column end_time_column  expenditure  income  investment  total_expenditure
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0              534.0
            2           67/06/30        07/07/10        421.0   465.0       179.0              521.0
            1           67/06/30        07/07/10        415.0   451.0       180.0              515.0
            5           67/06/30        07/07/10        459.0   509.0       211.0              559.0
            4           67/06/30        07/07/10        448.0   493.0       192.0              548.0

            # Example 2: Add expenditure amount to the investment amount and assign the
            #            final amount to new column 'total_investmet'.
            >>> df.assign(total_investmet=df.expenditure + df.investment)
               start_time_column end_time_column  expenditure  income  investment  total_investmet
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0                        619.0
            2           67/06/30        07/07/10        421.0   465.0       179.0                        600.0
            1           67/06/30        07/07/10        415.0   451.0       180.0                        595.0
            5           67/06/30        07/07/10        459.0   509.0       211.0                        670.0
            4           67/06/30        07/07/10        448.0   493.0       192.0                        640.0
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(expr + self.expression)
        return res

    @_handle_sql_error
    def __sub__(self, other):
        """
        Compute the difference between two ColumnExpressions using -

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Subtract 100 from the income amount and assign the final amount
            #            to new column 'remaining_income'.
            >>> df.assign(remaining_income=df.income - 100)
               start_time_column end_time_column  expenditure  income  investment  remaining_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0             385.0
            2           67/06/30        07/07/10        421.0   465.0       179.0             365.0
            1           67/06/30        07/07/10        415.0   451.0       180.0             351.0
            5           67/06/30        07/07/10        459.0   509.0       211.0             409.0
            4           67/06/30        07/07/10        448.0   493.0       192.0             393.0

            # Example 2: Subtract investment amount from the income amount and assign the
            #            final amount to new column 'remaining_income'.
            >>> df.assign(remaining_income=df.income - df.investment)
               start_time_column end_time_column  expenditure  income  investment  remaining_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0             300.0
            2           67/06/30        07/07/10        421.0   465.0       179.0             286.0
            1           67/06/30        07/07/10        415.0   451.0       180.0             271.0
            5           67/06/30        07/07/10        459.0   509.0       211.0             298.0
            4           67/06/30        07/07/10        448.0   493.0       192.0             301.0
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression - expr)
        return res

    @_handle_sql_error
    def __rsub__(self, other):
        """
        Compute the difference between two ColumnExpressions using -.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Subtract 100 from the income amount and assign the final amount
            #            to new column 'remaining_income'.
            >>> df.assign(remaining_income=df.income - 100)
               start_time_column end_time_column  expenditure  income  investment  remaining_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0             385.0
            2           67/06/30        07/07/10        421.0   465.0       179.0             365.0
            1           67/06/30        07/07/10        415.0   451.0       180.0             351.0
            5           67/06/30        07/07/10        459.0   509.0       211.0             409.0
            4           67/06/30        07/07/10        448.0   493.0       192.0             393.0

            # Example 2: Subtract investment amount from the income amount and assign the
            #            final amount to new column 'remaining_income'.
            >>> df.assign(remaining_income=df.income - df.investment)
               start_time_column end_time_column  expenditure  income  investment  remaining_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0             300.0
            2           67/06/30        07/07/10        421.0   465.0       179.0             286.0
            1           67/06/30        07/07/10        415.0   451.0       180.0             271.0
            5           67/06/30        07/07/10        459.0   509.0       211.0             298.0
            4           67/06/30        07/07/10        448.0   493.0       192.0             301.0
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(expr - self.expression)
        return res

    @_handle_sql_error
    def __mul__(self, other):
        """
        Compute the product between two ColumnExpressions using *.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Increase the income for each id by 10 % and assign increased
            #            income to new column 'increased_income'.
            >>> df.assign(increased_income=df.income + df.income * 0.1)
               start_time_column end_time_column  expenditure  income  investment  increased_income
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0             496.1
            4           67/06/30        07/07/10        448.0   493.0       192.0             542.3
            2           67/06/30        07/07/10        421.0   465.0       179.0             511.5
            3           67/06/30        07/07/10        434.0   485.0       185.0             533.5
            5           67/06/30        07/07/10        459.0   509.0       211.0             559.9

            # Example 2: Filter out the rows after increasing the income by 10% is greater than 500.
            >>> df[(df.income + df.income * 0.1) > 500]
               start_time_column end_time_column  expenditure  income  investment
            id
            2           67/06/30        07/07/10        421.0   465.0       179.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression * expr)
        return res

    @_handle_sql_error
    def __rmul__(self, other):
        """
        Compute the product between two ColumnExpressions using *.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            # Example 1: Double the income and assign increased
            #            income to new column 'double_income'.
             >>> df.assign(double_income=df.income * 2)
               start_time_column end_time_column  expenditure  income  investment  double_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0          970.0
            2           67/06/30        07/07/10        421.0   465.0       179.0          930.0
            1           67/06/30        07/07/10        415.0   451.0       180.0          902.0
            5           67/06/30        07/07/10        459.0   509.0       211.0         1018.0
            4           67/06/30        07/07/10        448.0   493.0       192.0          986.0

            # Example 2: Filter out the rows after increasing the income by 10% is greater than 500.
            >>> df[(df.income + df.income * 0.1) > 500]
               start_time_column end_time_column  expenditure  income  investment
            id
            2           67/06/30        07/07/10        421.0   465.0       179.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        return self * other

    @_handle_sql_error
    def __truediv__(self, other):
        """
        Compute the division between two ColumnExpressions using /.

        PARAMETERS:
            other :
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

           # Example 1: Divide the income by 2 and assign the final amount to new column 'half_income'.
            >>> df.assign(half_income=df.income / 2)
               start_time_column end_time_column  expenditure  income  investment  half_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0        242.5
            2           67/06/30        07/07/10        421.0   465.0       179.0        232.5
            1           67/06/30        07/07/10        415.0   451.0       180.0        225.5
            5           67/06/30        07/07/10        459.0   509.0       211.0        254.5
            4           67/06/30        07/07/10        448.0   493.0       192.0        246.5

            # Example 2: Calculate the percent of investment of income and assign the
            #            final amount to new column 'percent_inverstment_'.
            >>> df.assign(percent_inverstment_=df.investment * 100 / df.income)
               start_time_column end_time_column  expenditure  income  investment  percent_inverstment_
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0             38.144330
            2           67/06/30        07/07/10        421.0   465.0       179.0             38.494624
            1           67/06/30        07/07/10        415.0   451.0       180.0             39.911308
            5           67/06/30        07/07/10        459.0   509.0       211.0             41.453831
            4           67/06/30        07/07/10        448.0   493.0       192.0             38.945233
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression / expr)
        return res

    @_handle_sql_error
    def __rtruediv__(self, other):
        """
        Compute the division between two ColumnExpressions using /.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

           # Example 1: Divide the income by 2 and assign the divided income to new column 'divided_income'.
            >>> df.assign(divided_income=df.income / 2)
               start_time_column end_time_column  expenditure  income  investment  divided_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0           242.5
            2           67/06/30        07/07/10        421.0   465.0       179.0           232.5
            1           67/06/30        07/07/10        415.0   451.0       180.0           225.5
            5           67/06/30        07/07/10        459.0   509.0       211.0           254.5
            4           67/06/30        07/07/10        448.0   493.0       192.0           246.5

            # Example 2: Calculate the percent of investment of income and assign the
            #            final amount to new column 'divided_income'.
            >>> df.assign(divided_income=df.investment * 100 / df.income)
               start_time_column end_time_column  expenditure  income  investment  divided_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0       38.144330
            2           67/06/30        07/07/10        421.0   465.0       179.0       38.494624
            1           67/06/30        07/07/10        415.0   451.0       180.0       39.911308
            5           67/06/30        07/07/10        459.0   509.0       211.0       41.453831
            4           67/06/30        07/07/10        448.0   493.0       192.0       38.945233
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(expr / self.expression)
        return res

    @_handle_sql_error
    def __floordiv__(self, other):
        """
        Compute the floor division between two ColumnExpressions using //.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Divide the income by 2 and assign the divided income to
            #            new column 'divided_income'.
            >>> df.assign(divided_income=df.income // 2)
               start_time_column end_time_column  expenditure  income  investment  divided_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0           242.0
            2           67/06/30        07/07/10        421.0   465.0       179.0           232.0
            1           67/06/30        07/07/10        415.0   451.0       180.0           225.0
            5           67/06/30        07/07/10        459.0   509.0       211.0           254.0
            4           67/06/30        07/07/10        448.0   493.0       192.0           246.0

            # Example 2: Calculate the percent of investment of income and assign the
            #            final amount to new column 'percent_inverstment'.
            >>> df.assign(percent_inverstment=df.investment * 100 // df.income)
               start_time_column end_time_column  expenditure  income  investment  percent_inverstment
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0                 38.0
            2           67/06/30        07/07/10        421.0   465.0       179.0                 38.0
            1           67/06/30        07/07/10        415.0   451.0       180.0                 39.0
            5           67/06/30        07/07/10        459.0   509.0       211.0                 41.0
            4           67/06/30        07/07/10        448.0   493.0       192.0                 38.0
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression // expr)
        return res

    @_handle_sql_error
    def __rfloordiv__(self, other):
        """
        Compute the floor division between two ColumnExpressions using //.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Divide the income by 2 and assign the divided income
            #            to new column 'divided_income'.
            >>> df.assign(divided_income=c1 // 2)
            
            # Example 2: Calculate the percent of investment of income and assign the
            #            final output to new column 'percent_inverstment_'.
            >>> df.assign(percent_inverstment_=df.investment * 100 // df.income)
        """
        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(expr // self.expression)
        return res

    @_handle_sql_error
    def __mod__(self, other):
        """
        Compute the MOD between two ColumnExpressions using %.

        PARAMETERS:
            other :
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Calculate the reminder by taking mod of 2 on income and assign the
            #            reminder to new column 'reminder'.
            >>> df.assign(reminder=df.income.mod(2))
               start_time_column end_time_column  expenditure  income  investment   reminder
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0        1.0
            2           67/06/30        07/07/10        421.0   465.0       179.0        1.0
            1           67/06/30        07/07/10        415.0   451.0       180.0        1.0
            5           67/06/30        07/07/10        459.0   509.0       211.0        1.0
            4           67/06/30        07/07/10        448.0   493.0       192.0        1.0
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other
        res = _SQLColumnExpression(self.expression % expr)
        return res

    @_handle_sql_error
    def __rmod__(self, other):
        """
        Compute the MOD between two ColumnExpressions using %.
        Note: string types already override the __mod__ . We cannot override it
              if the string type is the left operand.

        PARAMETERS:
            other :
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression

        RETURNS:
            ColumnExpression, Python literal

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression.

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Calculate the reminder by taking mod of 2 on income and assign the
            #            reminder to new column 'reminder'.
            >>> df.assign(reminder=df.income.mod(2))
               start_time_column end_time_column  expenditure  income  investment   reminder
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0        1.0
            2           67/06/30        07/07/10        421.0   465.0       179.0        1.0
            1           67/06/30        07/07/10        415.0   451.0       180.0        1.0
            5           67/06/30        07/07/10        459.0   509.0       211.0        1.0
            4           67/06/30        07/07/10        448.0   493.0       192.0        1.0
        """

        expr = other.expression if isinstance(other, _SQLColumnExpression) else other

        if type(expr) is str:
            raise ValueError('MOD with string literals as the left operand is unsupported')

        res = _SQLColumnExpression(expr % self.expression)
        return res

    @_handle_sql_error
    def __neg__(self):
        """
        Compute the unary negation of the ColumnExpressions using -.

        PARAMETERS:
            None

        RETURNS:
            _SQLColumnExpression

        RAISES:
            Exception
                A TeradataMlException gets thrown if SQLAlchemy
                throws an exception when evaluating the expression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Negate the values in the column 'gpa' and assign those
            #           values to new column 'negate_gpa'.
            >>> df.assign(negate_gpa=-df.gpa)
               masters   gpa     stats programming  admitted  negate_gpa
            id
            5       no  3.44    Novice      Novice         0       -3.44
            34     yes  3.85  Advanced    Beginner         0       -3.85
            13      no  4.00  Advanced      Novice         1       -4.00
            40     yes  3.95    Novice    Beginner         0       -3.95
            22     yes  3.46    Novice    Beginner         0       -3.46
            19     yes  1.98  Advanced    Advanced         0       -1.98
            36      no  3.00  Advanced      Novice         0       -3.00
            15     yes  4.00  Advanced    Advanced         1       -4.00
            7      yes  2.33    Novice      Novice         1       -2.33
            17      no  3.83  Advanced    Advanced         1       -3.83

            # Example 2: Filter out the rows by taking negation of gpa not equal to 3.44 or
            #            admitted equal to 1.
            >>> df[~((df.gpa != 3.44) | (df.admitted == 1))]
                         id masters   gpa   stats  admitted
            programming
            Novice        5      no  3.44  Novice         0

        """

        res = _SQLColumnExpression(-self.expression)
        return res


# Accessor classes
class _StringMethods(object):
    """
    A class for implementing string methods for string-like ColumnExpressions
    This accessor class should only be used from the str property of a ColumnExpression

    This class is internal.
    """
    def __init__(self, c):
        """
            PARAMETERS:
                c: A ColumnExpression instance

        """
        self.c = c

    def lower(self):
        """
        Convert character column values to lowercase.
        REFERENCE:
            SQL Functions, Operators, Expressions, and Predicates
            Chapter 26 String Operators and Functions

        PARAMETERS:
            None

        RETURNS:
            A str Series with values lowercased

        EXAMPLES:
            >>> load_example_data("dataframe", "sales")
            >>> df = DataFrame("sales")
            >>> df
                          Feb    Jan    Mar    Apr    datetime
            accounts
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017

            >>> accounts = df['accounts']

            # Example 1: Convert the 'account' column values to lower case.
            >>> df.assign(drop_columns = True, lower = df.accounts.str.lower())
                    lower
            0  orange inc
            1    blue inc
            2  yellow inc
            3     red inc
            4   jones llc
            5    alpha co
        """
        res = _SQLColumnExpression(
                func.lower(
                  self.c.expression,
                  type_ = self.c.type
                )
               )
        return res

    def contains(self, pattern, case = True, na = None, **kw):
        """
        Search the pattern or substring in a given string.
        REFERENCE:
            SQL Functions, Operators, Expressions, and Predicates
            Chapter 24: Regular Expression Functions

        PARAMETERS:
            pattern:
                Required Argument.
                Specifies a regex pattern
                Types: str

            case:
                Optional Argument.
                Specifies the case-sentivity match.
                When True, case-sensitive matches, otherwise case-sensitive does not matches.
                Default value: True
                Types: bool

            na:
                Optional Argument.
                Specifies an optional fill value for NULL values in the column
                Types: bool, str, or numeric python literal.

            **kw:
                Optional Argument.
                Specifies optional parameters to pass to regexp_substr
                match_arg:
                    A string of characters to use for the match_arg parameter for REGEXP_SUBSTR
                    See the Reference for more information about the match_arg parameter.
                Note:
                     Specifying match_arg overrides the case parameter


        RETURNS:
            A numeric Series of values where:
                - Nulls are replaced by the fill parameter
                - A 1 if the value matches the pattern or else 0
            The type of the series is upcasted to support the fill value, if specified.

        EXAMPLES:
            >>> load_example_data("sentimentextractor", "additional_table")
            >>> df = DataFrame("additional_table")
            >>> df
                            polarity_strength
            sentiment_word
            'integral'                      1
            'eagerness'                     1
            'fearfully'                    -1
            irregular'                     -1
            'upgradable'                    1
            'rupture'                      -1
            'imperfect'                    -1
            'rejoicing'                     1
            'comforting'                    1
            'obstinate'                    -1

            >>> sentiment_word = df["sentiment_word"]

            # Example 1: Check if 'in' string is present or not in values in
            #            column 'sentiment_word'.
            >>> df.assign(drop_columns = True,
                         Name = sentiment_word,
                         has_in = sentiment_word.str.contains('in'))
                       Name has_in
            0    'integral'      1
            1   'eagerness'      0
            2   'fearfully'      0
            3    irregular'      0
            4  'upgradable'      0
            5     'rupture'      0
            6   'imperfect'      0
            7   'rejoicing'      1
            8  'comforting'      1
            9   'obstinate'      1

             # Example 2: Check if accounts column contains 'Er' string by ignoring
             #            case sensitivity and specifying a literal for null values.
             >>> df.assign(drop_columns = True,
                           Name = sentiment_word,
                           has_er = sentiment_word.str.contains('ER', case=False, na = 'no value'))
                        Name has_er
             0    'integral'      0
             1   'eagerness'      1
             2   'fearfully'      0
             3    irregular'      0
             4  'upgradable'      0
             5     'rupture'      0
             6   'imperfect'      1
             7   'rejoicing'      0
             8  'comforting'      0
             9   'obstinate'      0
     
            >>> load_example_data("dataframe", "sales")
            >>> df = DataFrame("sales")
            >>> df
                          Feb    Jan    Mar    Apr    datetime
            accounts
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017

            # Example 3: Get the all the accounts where accounts has 'Inc' string.
            >>> df[accounts.str.contains('Inc') == True]
                          Feb    Jan    Mar    Apr    datetime
            accounts
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017

            # Example 4: Get all the accounts where accounts does not
            #            have 'Inc' string.
            >>> df[accounts.str.contains('Inc') == False]
                         Feb  Jan  Mar  Apr    datetime
            accounts
            Jones LLC  200.0  150  140  180  04/01/2017
            Alpha Co   210.0  200  215  250  04/01/2017

            # Example 5: Get all the accounts where accounts has 'Inc' by
            #            specifying numeric literals for True (1).
            >>> df[accounts.str.contains('Inc') == 1]
                          Feb    Jan    Mar    Apr    datetime
            accounts
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017

            #Example 6: Get all the accounts where accounts has 'Inc' by
            #           specifying numeric literals for False (0).
            >>> df[accounts.str.contains('Inc') == 0]
                         Feb  Jan  Mar  Apr    datetime
            accounts
            Jones LLC  200.0  150  140  180  04/01/2017
            Alpha Co   210.0  200  215  250  04/01/2017

        """
        if not isinstance(pattern, str):
            raise TypeError('str.contains requires the pattern parameter to be a string.')

        if not isinstance(case, bool):
            raise TypeError('str.contains requires the case parameter to be True or False.')

        match_arg = kw.get('match_arg', 'c' if case else 'i')
        regexp_substr = func.regexp_substr(
                           self.c.expression,
                           pattern, 1, 1,
                           match_arg)
        
        expr = case_when((regexp_substr == None, 0), else_ = 1)
        expr = case_when((self.c.expression == None, na), else_ = expr)

        if na is not None:

            # na should be numeric or string-like or bool
            if not isinstance(na, (str, float, int, decimal.Decimal, bool)):
                raise TypeError('str.contains requires the na parameter to be a numeric, string, or bool literal.')

            # the resulting type is the type of the na (if not None), otherwise BYTEINT
            type_ = _resolve_value_to_type(na, len_ = len(na) if isinstance(na, str) else None)
            expr.type = type_

        return _SQLColumnExpression(expr)

    def strip(self):
        """
        Remove leading and trailing whitespace.
        REFERENCE:
            SQL Functions, Operators, Expressions, and Predicates
            Chapter 26 String Operators and Functions

        PARAMETERS:
            None

        RETURNS:
            A str Series with leading and trailing whitespace removed

        EXAMPLES:
            >>> load_example_data("dataframe", "sales")
            >>> df = DataFrame("sales")
            >>> df
                          Feb    Jan    Mar    Apr    datetime
            accounts
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017

            >>> accounts = df['accounts']

            # create a column with some whitespace
            >>> wdf = df.assign(drop_columns = True,
                              accounts = accounts,
                              w_spaces = '\n ' + accounts + '\v\f \t')
            >>> wdf

                                  w_spaces
            accounts
            Blue Inc      \n Blue Inc

             \t
            Orange Inc  \n Orange Inc

             \t
            Red Inc        \n Red Inc

             \t
            Yellow Inc  \n Yellow Inc

             \t
            Jones LLC    \n Jones LLC

             \t
            Alpha Co      \n Alpha Co

             \t

            # Example 1: Strip the leading and trailing whitespace.
            >>> wdf.assign(drop_columns = True,
                         wo_wspaces = wdf.w_spaces.str.strip())

               wo_wspaces
            0    Blue Inc
            1  Orange Inc
            2     Red Inc
            3  Yellow Inc
            4   Jones LLC
            5    Alpha Co
        """
        whitespace = '\n \t\r\v\f'
        res = func.rtrim(
                func.ltrim(
                    self.c.expression,
                    whitespace
                ),
                whitespace, type_ = self.c.type
              )

        return _SQLColumnExpression(res)

class _SeriesColumnExpression(ColumnExpression):

    """
        The _SeriesColumnExpression implements the pandas.Series methods
        for _SQLColumnExpression.
    """

    @property # TODO: consider making this a cached property
    def str(self):
        """
        The string accessor.
        Upon validation, returns a reference to a _StringMethods instance
        """
        if not isinstance(self.type, (CHAR, VARCHAR, CLOB)):
            raise AttributeError('The str accessor is only valid for string-like columns (CHAR, VARCHAR, or CLOB).')

        elif isinstance(getattr(self, '_SeriesColumnExpression__str', None), _StringMethods):
            return self.__str

        # otherwise, initialize the accessor
        self.str = _StringMethods(self)
        return self.__str

    @str.setter
    def str(self, accessor):
        """
        """
        if isinstance(accessor, _StringMethods):
            self.__str = accessor

        # otherwise, just ignore

    def gt(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values greater than the other or not.

        PARAMETERS:
            other :
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Get all the students with gpa greater than 3.
            >>> df[df.gpa.gt(3)]
               masters   gpa     stats programming  admitted
            id
            3       no  3.70    Novice    Beginner         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            15     yes  4.00  Advanced    Advanced         1
            30     yes  3.79  Advanced      Novice         0
            14     yes  3.45  Advanced    Advanced         0
            31     yes  3.50  Advanced    Beginner         1
            37      no  3.52    Novice      Novice         1
            1      yes  3.95  Beginner    Beginner         0

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure greater than 400 and investment
            #            greater than 170.
            >>> df[(df.expenditure.gt(400)) & (df.investment.gt(170))]
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        return self > other

    def ge(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values greater than or equal to the other or not.

        PARAMETERS:
            other :
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Get all the students with gpa greater than
            #            or equal to 3.
            >>> df[df.gpa.ge(3)]
               masters   gpa     stats programming  admitted
            id
            3       no  3.70    Novice    Beginner         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            39     yes  3.75  Advanced    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            30     yes  3.79  Advanced      Novice         0
            14     yes  3.45  Advanced    Advanced         0
            37      no  3.52    Novice      Novice         1
            1      yes  3.95  Beginner    Beginner         0

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure greater than or equal to 450 and
            #            investment is greater than or equal to 200.
            >>> df[(df.expenditure.ge(450)) & (df.investment.ge(200))]
               start_time_column end_time_column  expenditure  income  investment
            id
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        return self >= other

    def lt(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values less than the other or not.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Get all the students with gpa less than 4.
            >>> df[df.gpa.lt(4)]
               masters   gpa     stats programming  admitted
            id
            5       no  3.44    Novice      Novice         0
            34     yes  3.85  Advanced    Beginner         0
            32     yes  3.46  Advanced    Beginner         0
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            19     yes  1.98  Advanced    Advanced         0
            36      no  3.00  Advanced      Novice         0
            30     yes  3.79  Advanced      Novice         0
            7      yes  2.33    Novice      Novice         1
            17      no  3.83  Advanced    Advanced         1

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure less than 440 and
            #            income greater than 180.
            >>> df[(df.expenditure.lt(440)) & (df.income.lt(180))]
               start_time_column end_time_column  expenditure  income  investment
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0
        """
        return self < other

    def le(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values less than or equal to other or not.

        PARAMETERS:
        other:
            Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Get all the students with gpa less than
            #              or equal to 3.
            >>> df[df.gpa.le(3)]
               masters   gpa     stats programming  admitted
            id
            36      no  3.00  Advanced      Novice         0
            24      no  1.87  Advanced      Novice         1
            38     yes  2.65  Advanced    Beginner         1
            19     yes  1.98  Advanced    Advanced         0
            7      yes  2.33    Novice      Novice         1

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure less than or equal to
            #            500 and income less than or equal to 480.
            >>> df[(df.expenditure.le(500)) & (df.income.le(480))]
               start_time_column end_time_column  expenditure  income  investment
            id
            2           67/06/30        07/07/10        421.0   465.0       179.0
            1           67/06/30        07/07/10        415.0   451.0       180.0
        """
        return self <= other

    def eq(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values equal to other or not.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Get all the students with gpa equal to 3.
            >>> df[df.gpa.eq(3)]
               masters  gpa     stats programming  admitted
            id
            36      no  3.0  Advanced      Novice         0

            # Example 2: Get all the students with gpa equal to 3 and
            #            admitted values equal to 0.
            >>> df[c1.eq(3) & c2.eq(0)]
               masters  gpa     stats programming  admitted
            id
            36      no  3.0  Advanced      Novice         0

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure equal to 415 or income equal to 509.
            >>> df[(df.expenditure.eq(415)) | (df.income.eq(509))]
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        return self == other

    def ne(self, other):
        """
        Compare the ColumnExpressions to check if one ColumnExpression
        has values not equal to other.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Get all the students with gpa values not equal to 3.44.
            >>> df[df.gpa.ne(3.44)]
               masters   gpa     stats programming  admitted
            id
            24      no  1.87  Advanced      Novice         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            19     yes  1.98  Advanced    Advanced         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            7      yes  2.33    Novice      Novice         1
            17      no  3.83  Advanced    Advanced         1

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Get all rows with expenditure not equal to 415 or income
            #            not equal to 400.
            >>> df[(df.expenditure.ne(415)) | (df.income.ne(400))]
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        return self != other

    def add(self, other):
        """
        Compute the addition between two ColumnExpressions.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Add 100 to the expenditure amount and assign the final amount
            #            to new column 'total_expenditure'.
            >>> df.assign(total_expenditure=df.expenditure.add(100))
               start_time_column end_time_column  expenditure  income  investment  total_expenditure
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0              534.0
            2           67/06/30        07/07/10        421.0   465.0       179.0              521.0
            1           67/06/30        07/07/10        415.0   451.0       180.0              515.0
            5           67/06/30        07/07/10        459.0   509.0       211.0              559.0
            4           67/06/30        07/07/10        448.0   493.0       192.0              548.0

            # Example 2: Filter the rows where the income left after the investment is more than 300.
            >>> df[df.income.sub(df.investment) > 300]
               start_time_column end_time_column  expenditure  income  investment
            id
            4           67/06/30        07/07/10        448.0   493.0       192.0        """
        return self + other

    def sub(self, other):
        """
        Compute the subtraction between two ColumnExpressions.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Subtract 100 from the income amount and assign the final amount
            #            to new column 'remaining_income'.
            >>> df.assign(remaining_income=df.income - 100)
               start_time_column end_time_column  expenditure  income  investment  remaining_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0             385.0
            2           67/06/30        07/07/10        421.0   465.0       179.0             365.0
            1           67/06/30        07/07/10        415.0   451.0       180.0             351.0
            5           67/06/30        07/07/10        459.0   509.0       211.0             409.0
            4           67/06/30        07/07/10        448.0   493.0       192.0             393.0

            # Example 2: Filter the rows where the income left after the investment is more than 300.
            >>> df[df.income.sub(df.investment) > 300]
               start_time_column end_time_column  expenditure  income  investment
            id
            4           67/06/30        07/07/10        448.0   493.0       192.0
        """
        return self - other

    def mul(self, other):
        """
        Compute the multiplication between two ColumnExpressions.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            7      yes  2.33    Novice      Novice         1
            19     yes  1.98  Advanced    Advanced         0

            # Example 1: Increase the GPA for each student by 10 % and assign
            #            increased income to new column 'increased_gpa'.
            >>> df.assign(increased_gpa=df.gpa + df.gpa.mul(0.1))
               masters   gpa     stats programming  admitted  increased_gpa
            id
            22     yes  3.46    Novice    Beginner         0          3.806
            26     yes  3.57  Advanced    Advanced         1          3.927
            5       no  3.44    Novice      Novice         0          3.784
            17      no  3.83  Advanced    Advanced         1          4.213
            13      no  4.00  Advanced      Novice         1          4.400
            19     yes  1.98  Advanced    Advanced         0          2.178
            36      no  3.00  Advanced      Novice         0          3.300
            15     yes  4.00  Advanced    Advanced         1          4.400
            34     yes  3.85  Advanced    Beginner         0          4.235
            38     yes  2.65  Advanced    Beginner         1          2.915

            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 2: Calculate the percent of investment done of total income and assign the
            #            final amount to new column 'percentage_investment'.
            >>> df.assign(percentage_investment=(df.investment.mul(100)).div(df.income))
               start_time_column end_time_column  expenditure  income  investment  percentage_investment
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0              38.144330
            2           67/06/30        07/07/10        421.0   465.0       179.0              38.494624
            1           67/06/30        07/07/10        415.0   451.0       180.0              39.911308
            5           67/06/30        07/07/10        459.0   509.0       211.0              41.453831
            4           67/06/30        07/07/10        448.0   493.0       192.0              38.945233

            # Example 3: Filter out the rows after doubling income is greater than 1000.
            >>> df[(df.income * 2) > 1000]
               start_time_column end_time_column  expenditure  income  investment  double_income
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0          970.0
            2           67/06/30        07/07/10        421.0   465.0       179.0          930.0
            1           67/06/30        07/07/10        415.0   451.0       180.0          902.0
            5           67/06/30        07/07/10        459.0   509.0       211.0         1018.0
            4           67/06/30        07/07/10        448.0   493.0       192.0          986.0
        """
        return self * other

    def div(self, other):
        """
        Compute the division between two ColumnExpressions.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Calculate the percent of investment of income and assign the
            #            divided amount to new column 'percentage_investment'.
            >>> df.assign(percentage_investment=(df.investment.mul(100)).truediv(df.income))
               start_time_column end_time_column  expenditure  income  investment  percentage_investment
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0              38.144330
            2           67/06/30        07/07/10        421.0   465.0       179.0              38.494624
            1           67/06/30        07/07/10        415.0   451.0       180.0              39.911308
            5           67/06/30        07/07/10        459.0   509.0       211.0              41.453831
            4           67/06/30        07/07/10        448.0   493.0       192.0              38.945233

            # Example 2: Filter out the rows after diving income amount by 2 is less than 240.
            >>> df[(df.income.div(2)) < 240]
               start_time_column end_time_column  expenditure  income  investment
            id
            2           67/06/30        07/07/10        421.0   465.0       179.0
            1           67/06/30        07/07/10        415.0   451.0       180.0
        """
        return self.truediv(other)

    def truediv(self, other):
        """
        Compute the true-division between two ColumnExpressions.

        PARAMETERS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Calculate the percent of investment of income and assign the
            #            final amount to new column 'percentage_investment'.
            >>> df.assign(percentage_investment=(df.investment.mul(100)).truediv(df.income))
               start_time_column end_time_column  expenditure  income  investment  percentage_investment
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0              38.144330
            2           67/06/30        07/07/10        421.0   465.0       179.0              38.494624
            1           67/06/30        07/07/10        415.0   451.0       180.0              39.911308
            5           67/06/30        07/07/10        459.0   509.0       211.0              41.453831
            4           67/06/30        07/07/10        448.0   493.0       192.0              38.945233

            # Example 2: Filter out the rows after diving income amount by 2 is less than 240.
            >>> df[(df.income.truediv(2)) < 240]
               start_time_column end_time_column  expenditure  income  investment
            id
            2           67/06/30        07/07/10        421.0   465.0       179.0
            1           67/06/30        07/07/10        415.0   451.0       180.0
        """
        return self / other

    def floordiv(self, other):
        """
        Compute the floor-division between two ColumnExpressions.

        PARAMETRS:
            other:
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Calculate the percent of investment of income and assign the
            #            final amount to new column 'percentage_investment'.
            >>> df.assign(percentage_investment=(df.investment.mul(100)).floordiv(df.income))
               start_time_column end_time_column  expenditure  income  investment  percentage_investment
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0                   38.0
            2           67/06/30        07/07/10        421.0   465.0       179.0                   38.0
            1           67/06/30        07/07/10        415.0   451.0       180.0                   39.0
            5           67/06/30        07/07/10        459.0   509.0       211.0                   41.0
            4           67/06/30        07/07/10        448.0   493.0       192.0                   38.0

            # Example 2: Filter out the rows after diving income amount by 2 is less than 240.
            >>> df[(df.income.floordiv(2)) < 240]
               start_time_column end_time_column  expenditure  income  investment
            id
            2           67/06/30        07/07/10        421.0   465.0       179.0
            1           67/06/30        07/07/10        415.0   451.0       180.0
        """
        return self // other

    def mod(self, other):
        """
        Compute the mod between two ColumnExpressions.

        PARAMETERS:
            other :
                Required Argument.
                Specifies Python literal or another ColumnExpression.
                Types: ColumnExpression, Python literal

        RETURNS:
            ColumnExpression

        EXAMPLES:
            >>> load_example_data("burst", "finance_data")
            >>> df = DataFrame("finance_data")
            >>> df
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0

            # Example 1: Calculate the reminder by taking mod of 2 on income and assign the
            #            reminder to new column 'reminder_'.
            >>> df.assign(reminder_=df.income.mod(2))
               start_time_column end_time_column  expenditure  income  investment  reminder_
            id
            3           67/06/30        07/07/10        434.0   485.0       185.0        1.0
            2           67/06/30        07/07/10        421.0   465.0       179.0        1.0
            1           67/06/30        07/07/10        415.0   451.0       180.0        1.0
            5           67/06/30        07/07/10        459.0   509.0       211.0        1.0
            4           67/06/30        07/07/10        448.0   493.0       192.0        1.0

            Example 2: Filter out the rows where left over reminder of income is greater than 0.
            >>> df[df.income.mod(2) > 0]
               start_time_column end_time_column  expenditure  income  investment
            id
            1           67/06/30        07/07/10        415.0   451.0       180.0
            4           67/06/30        07/07/10        448.0   493.0       192.0
            2           67/06/30        07/07/10        421.0   465.0       179.0
            3           67/06/30        07/07/10        434.0   485.0       185.0
            5           67/06/30        07/07/10        459.0   509.0       211.0
        """
        return self % other

    def isna(self):
        """
        Test for NA values

        PARAMETERS:
            None

        RETURNS:
            When used with assign() function, newly assigned column contains
            A boolean Series of numeric values:
              - 1 if value is NA (None)
              - 0 if values is not NA
            Otherwise returns ColumnExpression, also known as, teradataml DataFrameColumn.

        EXAMPLES:
            >>> load_example_data("dataframe", "sales")
            >>> df = DataFrame("sales")

            # Example 1: Filter out the NA values from 'Mar' column.
            >>> df[df.Mar.isna() == 1]
                          Feb   Jan   Mar    Apr    datetime
            accounts
            Orange Inc  210.0  None  None  250.0  04/01/2017
            Yellow Inc   90.0  None  None    NaN  04/01/2017

            # Filter out the non-NA values from 'Mar' column.
            >>> df[df.Mar.isna() == 0]
                         Feb  Jan  Mar    Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101.0  04/01/2017
            Red Inc    200.0  150  140    NaN  04/01/2017
            Jones LLC  200.0  150  140  180.0  04/01/2017
            Alpha Co   210.0  200  215  250.0  04/01/2017

            # Example 2: Filter out the NA values from 'Mar' column using boolean True.
            >>> df[df.Mar.isna() == True]
                          Feb   Jan   Mar    Apr    datetime
            accounts
            Orange Inc  210.0  None  None  250.0  04/01/2017
            Yellow Inc   90.0  None  None    NaN  04/01/2017

            # Filter out the non-NA values from 'Mar' column using boolean False.
            >>> df[df.Mar.isna() == False]
                         Feb  Jan  Mar    Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101.0  04/01/2017
            Red Inc    200.0  150  140    NaN  04/01/2017
            Jones LLC  200.0  150  140  180.0  04/01/2017
            Alpha Co   210.0  200  215  250.0  04/01/2017

            # Example 3: Assign the tested values to dataframe as a column.
            >>> df.assign(isna_=df.Mar.isna())
                          Feb    Jan    Mar    Apr    datetime isna_
            accounts
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017     0
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017     1
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017     0
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017     1
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017     0
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017     0

        """
        res = _SQLColumnExpression(
                case_when(
                        (self.expression != None, 0),
                        else_ = 1
                )
            )
        return res

    def isnull(self):
        """
        Test for NA values. Alias for isna()

        PARAMETERS:
            None

        RETURNS:
            When used with assign() function, newly assigned column contains
            A boolean Series of numeric values:
              - 1 if value is NA (None)
              - 0 if values is not NA
            Otherwise returns ColumnExpression, also known as, teradataml DataFrameColumn.

        EXAMPLES:
            >>> load_example_data("dataframe", "sales")
            >>> df = DataFrame("sales")

            # Example 1: Filter out the NA values from 'Mar' column.
            >>> df[df.Mar.isnull() == 1]
                          Feb   Jan   Mar    Apr    datetime
            accounts
            Orange Inc  210.0  None  None  250.0  04/01/2017
            Yellow Inc   90.0  None  None    NaN  04/01/2017

            # Filter out the non-NA values from 'Mar' column.
            >>> df[df.Mar.isnull() == 0]
                         Feb  Jan  Mar    Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101.0  04/01/2017
            Red Inc    200.0  150  140    NaN  04/01/2017
            Jones LLC  200.0  150  140  180.0  04/01/2017
            Alpha Co   210.0  200  215  250.0  04/01/2017

            # Example 2: Filter out the NA values from 'Mar' column using boolean True.
            >>> df[df.Mar.isnull() == True]
                          Feb   Jan   Mar    Apr    datetime
            accounts
            Orange Inc  210.0  None  None  250.0  04/01/2017
            Yellow Inc   90.0  None  None    NaN  04/01/2017

            # Filter out the non-NA values from 'Mar' column using boolean False.
            >>> df[df.Mar.isnull() == False]
                         Feb  Jan  Mar    Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101.0  04/01/2017
            Red Inc    200.0  150  140    NaN  04/01/2017
            Jones LLC  200.0  150  140  180.0  04/01/2017
            Alpha Co   210.0  200  215  250.0  04/01/2017

            # Example 3: Assign the tested values to dataframe as a column.
            >>> df.assign(isnull_=df.Mar.isnull())
                          Feb    Jan    Mar    Apr    datetime isnull_
            accounts
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017     0
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017     1
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017     0
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017     1
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017     0
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017     0
        """
        return self.isna()

    def notna(self):
        """
        Test for non NA values
        The boolean complement of isna()

        PARAMETERS:
            None

        RETURNS:
            When used with assign() function, newly assigned column contains
            A boolean Series of numeric values:
              - 1 if value is NA (None)
              - 0 if values is not NA
            Otherwise returns ColumnExpression, also known as, teradataml DataFrameColumn.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")

            # Test for NA values on dataframe by using 0 and 1.
            >>> df[df.gpa.notna() == 1]
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0

            >>> df[df.gpa.notna() == 0]
            Empty DataFrame
            Columns: [masters, gpa, stats, programming, admitted]
            Index: []

            # Test for NA values on dataframe by using False and True.
            >>> df[df.gpa.notna() == True]
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0

            >>> df[df.gpa.notna() == False]
            Empty DataFrame
            Columns: [masters, gpa, stats, programming, admitted]
            Index: []

            # Assign the tested values to dataframe as a column.
            >>> df.assign(notna_=df.gpa.notna())
               masters   gpa     stats programming  admitted notna_
            id
            22     yes  3.46    Novice    Beginner         0      1
            36      no  3.00  Advanced      Novice         0      1
            15     yes  4.00  Advanced    Advanced         1      1
            38     yes  2.65  Advanced    Beginner         1      1
            5       no  3.44    Novice      Novice         0      1
            17      no  3.83  Advanced    Advanced         1      1
            34     yes  3.85  Advanced    Beginner         0      1
            13      no  4.00  Advanced      Novice         1      1
            26     yes  3.57  Advanced    Advanced         1      1
            19     yes  1.98  Advanced    Advanced         0      1
        """
        res = _SQLColumnExpression(
                case_when(
                        (self.expression != None, 1),
                        else_ = 0
                )
            )

        return res

    def notnull(self):
        """
        Alias for notna().Test for non NA values
        The boolean complement of isna()

        PARAMETERS:
            None

        RETURNS:
            When used with assign() function, newly assigned column contains
            A boolean Series of numeric values:
              - 1 if value is NA (None)
              - 0 if values is not NA
            Otherwise returns ColumnExpression, also known as, teradataml DataFrameColumn.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")

            >>> df[df.gpa.notnull() == 1]
               masters   gpa     stats programming  admitted
            id
            5       no  3.44    Novice      Novice         0
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            40     yes  3.95    Novice    Beginner         0
            22     yes  3.46    Novice    Beginner         0
            19     yes  1.98  Advanced    Advanced         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            7      yes  2.33    Novice      Novice         1
            17      no  3.83  Advanced    Advanced         1

            >>> df[df.gpa.notnull() == 0]
            Empty DataFrame
            Columns: [masters, gpa, stats, programming, admitted]
            Index: []

            # alternatively, True and False can be used
            >>> df[df.gpa.notnull() == True]
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            13      no  4.00  Advanced      Novice         1
            19     yes  1.98  Advanced    Advanced         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            38     yes  2.65  Advanced    Beginner         1

            >>> df[df.gpa.notnull() == False]
            Empty DataFrame
            Columns: [masters, gpa, stats, programming, admitted]
            Index: []

            # Assign the tested values to dataframe as a column.
            >>> df.assign(notnull_=df.gpa.notnull())
               masters   gpa     stats programming  admitted notnull_
            id
            22     yes  3.46    Novice    Beginner         0       1
            26     yes  3.57  Advanced    Advanced         1       1
            5       no  3.44    Novice      Novice         0       1
            17      no  3.83  Advanced    Advanced         1       1
            13      no  4.00  Advanced      Novice         1       1
            19     yes  1.98  Advanced    Advanced         0       1
            36      no  3.00  Advanced      Novice         0       1
            15     yes  4.00  Advanced    Advanced         1       1
            34     yes  3.85  Advanced    Beginner         0       1
            38     yes  2.65  Advanced    Beginner         1       1
        """
        return self.notna()

    def _unique(self):
        """
        Private method to return _SQLColumnExpression with DISTINCT applied on it.

        NOTE : This operation is valid only when the resultant _MetaExpression has
               just this one _SQLColumnExpression. All other operations will fail with
               a database error given the nature of the DISTINCT keyword.

               For example:
               >>> df = DataFrame("admissions_train") # a multi-column table
               >>> # Filter operations will fail
               >>> df = df[df.gpa._unique() > 2.00]
               >>> # Assign operations resulting in multiple columns
               >>> df.assign(x = df.gpa._unique())

               The following however is fine since it return only the one column
               with DISTINCT applied to it

               >>> df.assign(drop_columns = True, x = df.gpa._unique())

        PARAMETERS:
            None

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame(...)
            c1 = df.c1
            c1.unique()
        """
        res = _SQLColumnExpression(
                    self.expression.distinct()
              )

        return res

    def isin(self, values=None):
        """
        Function to check for the presence of values in a column.

        PARAMETERS:
            values:
                Required Argument.
                Specifies the list of values to check for their presence in the column.
                in the provided set of values.
                Types: list

        RETURNS:
            _SQLColumnExpression

        RAISES:
            TypeError - If invalid type of values are passed to argument 'values'.
            ValueError - If None is passed to argument 'values'.

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            17      no  3.83  Advanced    Advanced         1
            13      no  4.00  Advanced      Novice         1
            38     yes  2.65  Advanced    Beginner         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            34     yes  3.85  Advanced    Beginner         0
            40     yes  3.95    Novice    Beginner         0
            >>>

            # Example 1: Filter results where gpa values are in any of these following values:
            #            4.0, 3.0, 2.0, 1.0, 3.5, 2.5, 1.5
            >>> df[df.gpa.isin([4.0, 3.0, 2.0, 1.0, 3.5, 2.5, 1.5])]
               masters  gpa     stats programming  admitted
            id
            31     yes  3.5  Advanced    Beginner         1
            6      yes  3.5  Beginner    Advanced         1
            13      no  4.0  Advanced      Novice         1
            4      yes  3.5  Beginner      Novice         1
            29     yes  4.0    Novice    Beginner         0
            15     yes  4.0  Advanced    Advanced         1
            36      no  3.0  Advanced      Novice         0
            >>>

            # Example 2: Filter results where stats values are neither 'Novice' nor 'Advanced'
            >>> df[~df.stats.isin(['Novice', 'Advanced'])]
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0
            2      yes  3.76  Beginner    Beginner         0
            8       no  3.60  Beginner    Advanced         1
            4      yes  3.50  Beginner      Novice         1
            6      yes  3.50  Beginner    Advanced         1
            >>>
        """
        # If 'values' is None or not specified, raise an Exception
        if values is None:
            raise ValueError(Messages.get_message(MessageCodes.MISSING_ARGS, 'values'))

        if not isinstance(values, list):
            raise TypeError(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, 'values', 'list'))

        return _SQLColumnExpression(self.expression.in_(values))


class _AggregateColumnExpresion(ColumnExpression):
    """
    A class for implementing aggregate methods for ColumnExpressions.
    This class contains several methods that can work as regular aggregates as well as
    time series aggregates.
    This class is internal.
    """

    original_expressions = []

    def __validate_operation(self, name, as_time_series_aggregate=False, describe_op=False,
                                   **kwargs):
        """
        DESCRIPTION:
            Internal function used by aggregates to validate whether column supports
            the aggregate operation or not.

        PARAMETERS:
            name:
                Required Argument.
                Specifies the name of the aggregate function/operation.
                Types: str

            as_time_series_aggregate:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation is time
                series aggregate or regular aggregate.
                Default Values: False (Regular Aggregate)
                Types: bool

            describe_op:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation being
                run is for describe operation or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
            None.

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            self.__validate_operation(func_obj.name, describe_op=describe_op, **kwargs)
        """
        is_window_aggregate = kwargs.get("window_properties", {})

        # sqlalchemy func.any_func().name returns different results for
        # different functions i.e.
        # >>> func.count().name
        # 'count'
        # >>> func.COUNT().name
        # 'count'
        # >>> func.msum().name
        # 'msum'
        # >>> func.MSUM().name
        # 'MSUM'
        # >>>
        # Since unsupported types mapper looks for lowercase names, converting
        # all to lowercase.
        name = name.lower()
        if not describe_op:
            unsupported_types = _Dtypes._get_unsupported_data_types_for_aggregate_operations(name,
                                                                                             as_time_series_aggregate,
                                                                                             is_window_aggregate)
        else:
            unsupported_types = _Dtypes._get_unsupported_data_types_for_describe_operations(name)
        if type(self.type) in unsupported_types:
            raise RuntimeError(
                "Unsupported operation '{}' on column '{}' of type '{}'".format(name, self.name, str(self.type)))

    def __generate_function_call_object(self, func_obj, *args, **kwargs):
        """
        DESCRIPTION:
            Internal function used by aggregates to generate actual function call using
            sqlalchemy FunctionGenerator.

        PARAMETERS:
            func_obj:
                Required Argument.
                Specifies the sqlalchemy FunctionGenerator object to be used generate
                actual function call.
                Types: sqlalchemy FunctionGenerator

            distinct:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation should consider
                duplicate rows or not.
                Default Values: False
                Types: bool

            skipna:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation should skip
                null values or not.
                Default Values: False
                Types: bool

            describe_op:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation being
                run is for describe operation or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
            _SQLColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            self.__generate_function_call_object(func.count, distinct=distinct, skipna=skipna, **kwargs)
        """

        from teradataml.dataframe.sql_function_parameters import NO_DEFAULT_PARAM_FUNCTIONS

        expr = self

        if kwargs.pop("skipna", False):
            expr = self.notna()

        default_args = [expr.expression]
        if kwargs.pop("distinct", False):
            default_args = [expr.expression.distinct()]

        # Most of the Aggregate functions take first parameter as, the column
        # on which the Aggregate function is being applied. However, few
        # functions (e.g. rank, quantile) do not accept first parameter as
        # corresponding column. So, if the function is of such type, do not
        # pass the column expression as first argument.
        if func_obj().name.upper() in NO_DEFAULT_PARAM_FUNCTIONS:
            default_args = []

        args = default_args + [arg.expression if isinstance(arg, _SQLColumnExpression)
                                     else arg for arg in args]

        # Check for window parameters in kwargs.
        window_properties = kwargs.get("window_properties", {})

        # Check within_group parameters in kwargs.
        within_group_properties = kwargs.get("within_group", {})

        get_quoted_cols = UtilFuncs._process_for_teradata_keyword
        if window_properties:
            func_obj = func_obj(*args).over(partition_by=get_quoted_cols(window_properties.get("partition_by")),
                                            rows=window_properties.get("rows"),
                                            order_by=get_quoted_cols(window_properties.get("order_by"))
                                            )
        elif within_group_properties:
            func_obj = func_obj(*args).within_group(get_quoted_cols(within_group_properties.get("order_by")))
        else:
            func_obj = func_obj(*args)

        # Remove describe_op from kwargs as it will passed as positional
        # argument.
        describe_op = kwargs.pop("describe_op", False)
        return self.__process_function_call_object(func_obj, describe_op, **kwargs)

    def __process_function_call_object(self, func_obj, describe_op=False, **kwargs):
        """
        DESCRIPTION:
            Internal function used by aggregates to process actual function call generated
            using sqlalchemy FunctionGenerator.
            This functions:
                1. Validates whether aggregate operation for the column is supported or not.
                2. Creates a new _SQLColumnExpression.
                3. Identifies the output column type for the aggregate function.

        PARAMETERS:
            func_obj:
                Required Argument.
                Specifies the sqlalchemy FunctionGenerator object to be used generate
                actual function call.
                Types: sqlalchemy FunctionGenerator

            describe_op:
                Optional Argument.
                Specifies a flag that decides whether the aggregate operation being
                run is for describe operation or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
            _SQLColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            self.__process_function_call_object(func_obj, describe_op, **kwargs)
        """
        # Perform validations for the function to check if operation is valid or not.
        if isinstance(func_obj, sqlalc.sql.elements.Over) or \
                isinstance(func_obj, sqlalc.sql.elements.WithinGroup):
            func_name = func_obj.element.name
        else:
            func_name = func_obj.name
        self.__validate_operation(func_name, describe_op=describe_op, **kwargs)

        # Add self to original expression lists.
        self.original_expressions.append(self)

        # Set _SQLColumnExpression type
        new_expression_type = _get_function_expression_type(func_obj, self.expression, **kwargs)
        columnExpression = _SQLColumnExpression(func_obj, type=new_expression_type)
        if describe_op:
            columnExpression = columnExpression.cast(NUMBER())
        return columnExpression

    def __process_column_expression(self, func_name, *args, **kwargs):
        """
        Description:
            Function to process the aggregate expression. This function first
            checks the argument types passed to aggregate function is expected
            or not. If the argument types are expected, then this function combines
            positional arguments and keyword arguments to positional arguments,
            and then pass to the sql aggregate function.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the name of the aggregate function.
                Types: str

            args:
                Optional Argument.
                Specifies the positional arguments to be passed to the aggregate function.
                Types: Tuple

            kwargs:
                Optional Argument.
                Specifies the keyword arguments to be passed to the aggregate function.
                Types: Dictionary

        RETURNS:
            An _SQLColumnExpression.

        EXAMPLES:
            # Create a Window from a teradataml DataFrame.
            from teradataml import *
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            df.Feb.__process_column_expression("corr", df.Feb.Mar)
        """

        from teradataml.dataframe.sql_function_parameters import SQL_AGGREGATE_FUNCTION_ADDITIONAL_PARAMETERS, \
            SQL_FUNCTION_ADDITIONAL_PARAMETERS, SINGLE_QUOTE_FUNCTIONS
        from teradataml.common.utils import UtilFuncs

        func_params = []
        if func_name in SQL_AGGREGATE_FUNCTION_ADDITIONAL_PARAMETERS:
            func_params = SQL_AGGREGATE_FUNCTION_ADDITIONAL_PARAMETERS.get(func_name)
        elif func_name in SQL_FUNCTION_ADDITIONAL_PARAMETERS:
            func_params = SQL_FUNCTION_ADDITIONAL_PARAMETERS.get(func_name)

        # Validation should be done against user passed function name i.e., on
        # Python function name, not on SQL function name.
        python_func_name = kwargs.pop("python_func_name")

        # If the call is from DataFrame, i.e., df.col.aggregate_function(),
        # then argument check would have happened at DataFrame itself. So,
        # argument type check can be skipped and all the function parameters will
        # be available in kwargs.
        if kwargs.get("call_from_df"):
            kw = kwargs
        else:
            # Validate the arguments before proceeding further and convert the
            # positional arguments and keyword arguments to keyword arguments.
            kw = _validate_unimplemented_function(python_func_name, func_params, *args, **kwargs)

        args_ = tuple()
        awu_matrix = []
        for func_param in func_params:
            arg = kw[func_param["arg_name"]]
            # If default_value available, then parameter is Optional. For Optional
            # parameter, 3rd argument in "awu_matrix" should be True.
            is_optional = "default_value" in func_param
            awu_matrix.append([func_param["arg_name"],
                               arg,
                               is_optional,
                               func_param["exp_types"]]
                              )


            arg = UtilFuncs._as_list(arg)

            expression = lambda col: text(col) if isinstance(col, str) else col

            if func_name in SINGLE_QUOTE_FUNCTIONS:
                # Certain string functions, require the str argument to be quoted so that it is
                # treated as a str in sql query.
                expression = lambda col: '{0}'.format(text(col)) if isinstance(col, str) else col

            for a in arg:
                args_ = args_ + (expression(a), )

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        func_obj = getattr(func, func_name)

        return self.__generate_function_call_object(func_obj, *args_, **kwargs)

    def __getattr__(self, func_name):
        """
        DESCRIPTION:
            Magic Method to call the corresponding aggregate function.

        PARAMETERS:
            func_name:
                Required Argument.
                Name of the aggregate function.
                Types: str

        RETURNS:
            A function, which actually process the corresponding aggregate function.

        EXAMPLES:
            # Create a window from a teradataml DataFrame.
            from teradataml import *
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            df.Feb.corr(df.Feb.Mar)
        """
        # Check aggregate function is available or not. If available, process the corresponding
        # function. Else, let python decide what to do, using __getattribute__.
        sql_func_name = ""
        if func_name in SQLFunctionConstants.AGGREGATE_FUNCTION_MAPPER.value:
            sql_func_name = SQLFunctionConstants.AGGREGATE_FUNCTION_MAPPER.value.get(func_name)
        else:
            sql_func_name = SQLFunctionConstants.SQL_FUNCTION_MAPPER.value.get(func_name)

        if not sql_func_name:
            return self.__getattribute__(func_name)

        return lambda *args, **kwargs:\
            self.__process_column_expression(sql_func_name, *args, python_func_name=func_name, **kwargs)

    def count(self, distinct=False, skipna=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the number of values in a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            skipna:
                Optional Argument.
                Specifies a flag that decides whether to skip null values or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the count of the values in 'gpa' column.
            # Execute count() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> count_column = admissions_train.gpa.count()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, count_=count_column)
            >>> df
               count_
            0      40
            >>>

            # Example 2: Get the count of the distinct values in 'gpa' column
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute count() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> count_column = admissions_train.gpa.count(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(count_=count_column)
            >>> df
              programming  count_
            0    Advanced      15
            1      Novice      11
            2    Beginner      11
            >>>
        """
        return self.__generate_function_call_object(func.count, distinct=distinct, skipna=skipna, **kwargs)

    def kurtosis(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function returns kurtosis value for a column.
            Kurtosis is the fourth moment of the distribution of the standardized
            (z) values. It is a measure of the outlier (rare, extreme observation)
            character of the distribution as compared with the normal, Gaussian
            distribution.
                * The normal distribution has a kurtosis of 0.
                * Positive kurtosis indicates that the distribution is more
                  outlier-prone than the normal distribution.
                * Negative kurtosis indicates that the distribution is less
                  outlier-prone than the normal distribution.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the kurtosis of the values in 'gpa' column.
            # Execute kurtosis() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> kurtosis_column = admissions_train.gpa.kurtosis()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, kurtosis_=kurtosis_column)
            >>> df
               kurtosis_
            0   4.052659
            >>>

            # Example 2: Get the kurtosis of the distinct values in 'gpa' column
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute kurtosis() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> kurtosis_column = admissions_train.gpa.kurtosis(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(kurtosis_=kurtosis_column)
            >>> df
              programming  kurtosis_
            0    Advanced   8.106762
            1      Novice   1.420745
            2    Beginner   5.733691
            >>>
        """
        return self.__generate_function_call_object(func.kurtosis, distinct=distinct, **kwargs)

    def first(self, **kwargs):
        """
        DESCRIPTION:
            Function returns oldest value, determined by the timecode, for each group
            in a column.
            Note:
                This can only be used as Time Series Aggregate function.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")

            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cd",
            ...                                               value_expression="buoyid", fill="NULLS")

            >>> ocean_buoys_grpby1.temperature.first()
        """
        return self.__generate_function_call_object(func.first)

    def last(self, **kwargs):
        """
        DESCRIPTION:
            Function returns newest value, determined by the timecode, for each group
            in a column.
            Note:
                This can only be used as Time Series Aggregate function.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys"])

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")

            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="2cd",
            ...                                               value_expression="buoyid", fill="NULLS")

            >>> ocean_buoys_grpby1.temperature.last()
        """
        return self.__generate_function_call_object(func.last)

    def mad(self, constant_multiplier=None, **kwargs):
        """
        DESCRIPTION:
            Function returns the median of the set of values defined as the
            absolute value of the difference between each value and the median
            of all values in each group.

            Formula for computing MAD is as follows:
                MAD = b * Mi(|Xi - Mj(Xj)|)

                Where,
                    b       = Some numeric constant. Default value is 1.4826.
                    Mj(Xj)  = Median of the original set of values.
                    Xi      = The original set of values.
                    Mi      = Median of absolute value of the difference between
                              each value in Xi and the Median calculated in Mj(Xj).

            Note:
                1. This function is valid only on columns with numeric types.
                2. Null values are not included in the result computation.
                3. This can only be used as Time Series Aggregate function.

        PARAMETERS:
            constant_multiplier:
                Optional Argument.
                Specifies a numeric values to be used as constant multiplier
                (b in the above formula). It should be any numeric value
                greater than or equal to 0.
                Note:
                    When this argument is not used, Vantage uses 1.4826 as
                    constant multiplier.
                Default Values: None
                Types: int or float

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])

            # Example 1: Calculate Median Absolute Deviation for all columns over 1 calendar day of
            #            timebucket duration. Use default constant multiplier.
            #            No need to pass any arguments.

            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")

            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="1cd",value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.temperature.mad()

            # Example 2: Calculate MAD values using 2 as constant multiplier for all the columns
            #            in ocean_buoys_seq DataFrame on sequenced PTI table.

            >>> # DataFrame on sequenced PTI table
            ... ocean_buoys_seq = DataFrame("ocean_buoys_seq")

            >>> ocean_buoys_seq_grpby1 = ocean_buoys_seq.groupby_time(timebucket_duration="CAL_DAYS(2)", value_expression="buoyid", fill="NULLS")
            >>> constant_multiplier_columns = {2: "*"}
            >>> ocean_buoys_seq_grpby1.temperature.mad(constant_multiplier_columns)

        """
        if constant_multiplier:
            func_obj = func.mad(constant_multiplier, self.expression)
        else:
            func_obj = func.mad(self.expression)
        return self.__process_function_call_object(func_obj)

    def max(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the maximum value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the maximum value in 'gpa' column.
            # Execute max() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> max_column = admissions_train.gpa.max()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, max_=max_column)
            >>> df
               max_
            0   4.0
            >>>

            # Example 2: Get the maximum value from the distinct values in 'gpa' column
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute max() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> max_column = admissions_train.gpa.max(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(max_=max_column)
            >>> df
              programming  max_
            0    Beginner   4.0
            1    Advanced   4.0
            2      Novice   4.0
            >>>
        """
        return self.__generate_function_call_object(func.max, distinct=distinct, **kwargs)

    def mean(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the average value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the mean value of 'gpa' column.
            # Execute mean() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> mean_column = admissions_train.gpa.mean()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, mean_=mean_column)
            >>> df
                mean_
            0  3.54175
            >>>

            # Example 2: Get the mean of the distinct values in 'gpa' column
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute mean() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> mean_column = admissions_train.gpa.mean(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(mean_=mean_column)
            >>> df
              programming     mean_
            0    Beginner  3.651818
            1    Advanced  3.592667
            2      Novice  3.294545
            >>>
        """
        # TODO:: Validate if below lines of code is needed or not.
        if self.type in [INTEGER, DECIMAL]:
            return _SQLColumnExpression(self).cast(FLOAT).mean()

        return self.__generate_function_call_object(func.avg, distinct=distinct, **kwargs)

    def median(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the median value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the median value of 'gpa' column.
            # Execute median() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> median_column = admissions_train.gpa.median()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, median_=median_column)
            >>> df
               min_
            0  3.69

            # Example 2: Get the median of the distinct values in 'gpa' column.
            # Execute median() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> median_column = admissions_train.gpa.median(distict=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, median_=median_column)
            >>> df
               median_
            0     3.69

            # Example 3: Get the median value in 'gpa' column for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute median() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> median_column = admissions_train.gpa.median()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(median_=median_column)
            >>> df
              programming  median_
            0    Advanced     3.76
            1      Novice     3.52
            2    Beginner     3.75
            >>>
        """
        return self.__generate_function_call_object(func.median, distinct=distinct, **kwargs)

    def min(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the minimum value for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the minimum value in 'gpa' column.
            # Execute min() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> min_column = admissions_train.gpa.min()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, min_=min_column)
            >>> df
               min_
            0  1.87

            # Example 2: Get the minimum value from the distinct values in 'gpa' column
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute min() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> min_column = admissions_train.gpa.min(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(min_=min_column)
            >>> df
              programming  min_
            0    Advanced  1.98
            1      Novice  1.87
            2    Beginner  2.65
            >>>
        """
        return self.__generate_function_call_object(func.min, distinct=distinct, **kwargs)

    def mode(self, **kwargs):
        """
        DESCRIPTION:
            Function to get the mode value for a column.
            Note:
                This can only be used as Time Series Aggregate function.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            >>> # Load the example datasets.
            ... load_example_data("dataframe", ["ocean_buoys", "ocean_buoys_seq", "ocean_buoys_nonpti"])

            # Example 1: Executing mode function on DataFrame column created on non-sequenced PTI table.
            >>> # Create the required DataFrames.
            ... # DataFrame on non-sequenced PTI table
            ... ocean_buoys = DataFrame("ocean_buoys")

            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="10m",
            ...                                               value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.temperature.mode()

        """
        return self.__generate_function_call_object(func.mode)

    def percentile(self, percentile, distinct=False, interpolation="LINEAR",
                   as_time_series_aggregate=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the percentile values for a column.

        PARAMETERS:
            percentile:
                Required Argument.
                Specifies the desired percentile value to calculate.
                It should be between 0 and 1, both inclusive.
                Types: float

            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Note: "distinct" is insignificant if percentile is calculated
                      as regular aggregate i.e., "as_time_series_aggregate" is
                      set to False.
                Default Values: False
                Types: bool

            interpolation:
                Optional Argument.
                Specifies the interpolation type to use to interpolate the result value when the
                desired result lies between two data points.
                The desired result lies between two data points, i and j, where i<j. In this case,
                the result is interpolated according to the permitted values.
                Permitted Values for time series aggregate:
                    * LINEAR: Linear interpolation.
                        The result value is computed using the following equation:
                            result = i + (j - i) * (di/100)MOD 1
                        Specify by passing "LINEAR" as string to this parameter.
                    * LOW: Low value interpolation.
                        The result value is equal to i.
                        Specify by passing "LOW" as string to this parameter.
                    * HIGH: High value interpolation.
                        The result value is equal to j.
                        Specify by passing "HIGH" as string to this parameter.
                    * NEAREST: Nearest value interpolation.
                        The result value is i if (di/100 )MOD 1 <= .5; otherwise, it is j.
                        Specify by passing "NEAREST" as string to this parameter.
                    * MIDPOINT: Midpoint interpolation.
                         The result value is equal to (i+j)/2.
                         Specify by passing "MIDPOINT" as string to this parameter.
                Permitted Values for regular aggregate:
                    * LINEAR: Linear interpolation.
                        Percentile is calculated after doing linear interpolation.
                    * None:
                        Percentile is calculated with no interpolation.
                Default Values: "LINEAR"
                Types: str

            as_time_series_aggregate:
                Optional Argument.
                Specifies a flag that decides whether percentiles are being calculated
                as regular aggregate or time series aggregate. When it is set to False, it'll
                be executed as regular aggregate, if set to True; then it is used as time series
                aggregate.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", ["admissions_train", "ocean_buoys"])
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>
            # Create a DataFrame on 'ocean_buoys' table.
            >>> ocean_buoys = DataFrame("ocean_buoys")
            >>> ocean_buoys
                                   TD_TIMECODE  salinity  temperature
            buoyid
            1       2014-01-06 09:02:25.122200        55         78.0
            44      2014-01-06 10:00:24.333300        55         43.0
            44      2014-01-06 10:00:25.122200        55         43.0
            2       2014-01-06 21:01:25.122200        55         80.0
            2       2014-01-06 21:03:25.122200        55         82.0
            0       2014-01-06 08:00:00.000000        55         10.0
            0       2014-01-06 08:08:59.999999        55          NaN
            0       2014-01-06 08:09:59.999999        55         99.0
            2       2014-01-06 21:02:25.122200        55         81.0
            44      2014-01-06 10:00:24.000000        55         43.0
            >>>

            # Example 1: Calculate the 25th percentile of temperature in ocean_buoys table,
            #            with LINEAR interpolation.
            >>> ocean_buoys_grpby1 = ocean_buoys.groupby_time(timebucket_duration="10m", value_expression="buoyid", fill="NULLS")
            >>> ocean_buoys_grpby1.assign(True, temperature_percentile_=ocean_buoys_grpby1.temperature.percentile(0.25))
               temperature_percentile_
            0                       43
            >>>

            # Example 2: Calculate the 35th percentile of gpa in admissions_train table,
            #            with LINEAR interpolation.
            >>> admissions_train_grpby = admissions_train.groupby("admitted")
            >>> admissions_train_grpby.assign(True, percentile_cont_=admissions_train_grpby.gpa.percentile(0.35))
               admitted  percentile_cont_
            0         0             3.460
            1         1             3.565
            >>>

            # Example 3: Calculate the 45th percentile of gpa in admissions_train table,
            #            with no interpolation.
            >>> admissions_train_grpby = admissions_train.groupby("admitted")
            >>> admissions_train_grpby.assign(True, percentile_disc_=admissions_train_grpby.gpa.percentile(0.35, interpolation=None))
               admitted  percentile_disc_
            0         0              3.46
            1         1              3.57
            >>>
        """
        # Argument validations
        awu_matrix = []
        awu_matrix.append(["percentile", percentile, False, (int, float)])
        awu_matrix.append(["distinct", distinct, True, (bool)])

        # "interpolation" expected values are different for regular aggregates
        # and time series aggregates. So, creating a seperate validation
        # parameters.
        if as_time_series_aggregate:
            awu_matrix.append(["interpolation", interpolation, True, (str), True,
                              ["LINEAR", "LOW", "HIGH", "NEAREST", "MIDPOINT"]])
        else:
            awu_matrix.append(["interpolation", interpolation, True, (str, type(None)), True,
                               ["LINEAR", None]])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        _Validators._validate_argument_range(
            percentile, "percentile", lbound=0, ubound=1, lbound_inclusive=True, ubound_inclusive=True)

        # Performing percentile for Regular Aggregate.
        # SQL Equivalent: """percentile_cont({}) within group order by {}"""
        if not as_time_series_aggregate:

            # Since default value for interpolation is LINEAR, Perform
            # PERCENTILE_CONT by default. If no interpolation specified, then
            # perform PERCENTILE_DISC.
            percentile_func = func.percentile_cont
            if interpolation is None:
                percentile_func = func.percentile_disc

            order_by = self.expression
            # Cast order by column to Number for Describe operation.
            if kwargs.get("describe_op"):
                order_by = self.cast(NUMBER()).expression

            return self.__generate_function_call_object(
                percentile_func, percentile, within_group={"order_by": order_by}, **kwargs)

        # Performing percentile for Time Series Aggregate.
        # SQL Equivalent: """percentile([DISTINCT] column, percentile [interpolation])"""
        return self.__generate_function_call_object(
            func.percentile, percentile*100, text(interpolation), distinct=distinct)

    def skew(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the skewness of the distribution for a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Calculate the skewness of the distribution for values in 'gpa' column.
            # Execute skew() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> skew_column = admissions_train.gpa.skew()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, skew_=skew_column)
            >>> df
                  skew_
            0 -2.058969
            >>>

            # Example 2: Calculate the skewness of the distribution for distinct values in
            #            'gpa' column for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute skew() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> skew_column = admissions_train.gpa.skew(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(skew_=skew_column)
            >>> df
              programming     skew_
            0    Beginner -2.197710
            1    Advanced -2.647604
            2      Novice -1.459620
            >>>
        """
        return self.__generate_function_call_object(func.skew, distinct=distinct, **kwargs)

    def sum(self, distinct=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the sum of values in a column.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Calculate the sum of the values in 'gpa' column.
            # Execute sum() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> sum_column = admissions_train.gpa.sum()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, sum_=sum_column)
            >>> df
                sum_
            0  141.67
            >>>

            # Example 2: Calculate the sum of the distinct values in'gpa' column
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute sum() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> sum_column = admissions_train.gpa.sum(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(sum_=sum_column)
            >>> df
              programming   sum_
            0    Beginner  40.17
            1    Advanced  53.89
            2      Novice  36.24
            >>>
        """
        return self.__generate_function_call_object(func.sum, distinct=distinct, **kwargs)

    def std(self, distinct=False, population=False, **kwargs):
        """
        DESCRIPTION:
            Function to get the sample or population standard deviation for values in a column.
            The standard deviation is the second moment of a distribution.
                * For a sample, it is a measure of dispersion from the mean of that sample.
                * For a population, it is a measure of dispersion from the mean of that population.
            The computation is more conservative for the population standard deviation
            to minimize the effect of outliers on the computed value.
            Note:
                1. When there are fewer than two non-null data points in the sample used
                   for the computation, then std returns None.
                2. Null values are not included in the result computation.
                3. If data represents only a sample of the entire population for the
                   column, Teradata recommends to calculate sample standard deviation,
                   otherwise calculate population standard deviation.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            population:
                Optional Argument.
                Specifies whether to calculate standard deviation on entire population or not.
                Set this argument to True only when the data points represent the complete
                population. If your data represents only a sample of the entire population for the
                column, then set this variable to False, which will compute the sample standard
                deviation. As the sample size increases, even though the values for sample
                standard deviation and population standard deviation approach the same number,
                you should always use the more conservative sample standard deviation calculation,
                unless you are absolutely certain that your data constitutes the entire population
                for the column.
                Default Value: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the sample standard deviation for values in 'gpa' column.
            # Execute std() function on teradataml DataFrameColumn to generate the ColumnExpression.
            >>> std_column = admissions_train.gpa.std()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, std_=std_column)
            >>> df
                   std_
            0  0.513764
            >>>

            # Example 2: Get the population standard deviation for values in 'gpa' column.
            # Execute std() function on teradataml DataFrameColumn to generate the ColumnExpression.
            # To calculate population standard deviation we must set population=True.
            >>> std_column = admissions_train.gpa.std(population=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, std_=std_column)
            >>> df
                   std_
            0  0.507301
            >>>

            # Example 3: Get the sample standard deviation for distinct values in 'gpa' column
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute std() function on teradataml DataFrameColumn to generate the ColumnExpression.
            # We will consider DISTINCT values for the columns while calculating the standard deviation value.
            >>> std_column = admissions_train.gpa.std(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(std_=std_column)
            >>> df
              programming      std_
            0    Beginner  0.372151
            1    Advanced  0.502415
            2      Novice  0.646736
            >>>
        """
        if population:
            return self.__generate_function_call_object(func.stddev_pop, distinct=distinct, **kwargs)
        else:
            return self.__generate_function_call_object(func.stddev_samp, distinct=distinct, **kwargs)

    def unique(self, **kwargs):
        """
        DESCRIPTION:
            Function to get the number of unique values in a column.

        PARAMETERS:
            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> s1 = df.select(['gpa']).squeeze()
            >>> s1
            0    4.00
            1    3.57
            2    3.44
            3    1.98
            4    4.00
            5    3.95
            6    2.33
            7    3.46
            8    3.00
            9    2.65

            >>> s1.unique()
            0    3.65
            1    1.98
            2    3.55
            3    3.71
            4    3.13
            5    1.87
            6    3.44
            7    4.00
            8    3.96
            9    3.46
            Name: gpa, dtype: float64
        """
        # Check if it is describe operation or not.
        describe_op = False
        if "describe_op" in kwargs.keys():
            describe_op = kwargs["describe_op"]

        if describe_op:
            # If a describe operation function name is used as "unique" to retrieve unsupported types.
            self.__validate_operation(name="unique", describe_op=describe_op)
        return self.count(True)

    def var(self, distinct=False, population=False, **kwargs):
        """
        DESCRIPTION:
            Returns sample or population variance for values in a column.
                * The variance of a population is a measure of dispersion from the
                  mean of that population.
                * The variance of a sample is a measure of dispersion from the mean
                  of that sample. It is the square of the sample standard deviation.
            Note:
                1. When there are fewer than two non-null data points in the sample used
                   for the computation, then var returns None.
                2. Null values are not included in the result computation.
                3. If data represents only a sample of the entire population for the
                   columns, Teradata recommends to calculate sample variance,
                   otherwise calculate population variance.

        PARAMETERS:
            distinct:
                Optional Argument.
                Specifies a flag that decides whether to consider duplicate values in
                a column or not.
                Default Values: False
                Types: bool

            population:
                Optional Argument.
                Specifies whether to calculate variance on entire population or not.
                Set this argument to True only when the data points represent the complete
                population. If your data represents only a sample of the entire population
                for the columns, then set this variable to False, which will compute the
                sample variance. As the sample size increases, even though the values for
                sample variance and population variance approach the same number, but you
                should always use the more conservative sample standard deviation calculation,
                unless you are absolutely certain that your data constitutes the entire
                population for the columns.
                Default Value: False
                Types: bool

            kwargs:
                Specifies optional keyword arguments.

        RETURNS:
             ColumnExpression, also known as, teradataml DataFrameColumn.

        NOTES:
             * One must use DataFrame.assign() when using the aggregate functions on
               ColumnExpression, also known as, teradataml DataFrameColumn.
             * One should always use "drop_columns=True" in DataFrame.assign(), while
               running the aggregate operation on teradataml DataFrame.
             * "drop_columns" argument in DataFrame.assign() is ignored, when aggregate
               function is operated on DataFrame.groupby().

        RAISES:
            RuntimeError - If column does not support the aggregate operation.

        EXAMPLES:
            # Load the data to run the example.
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            # Create a DataFrame on 'admissions_train' table.
            >>> admissions_train = DataFrame("admissions_train")
            >>> admissions_train
               masters   gpa     stats programming  admitted
            id
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            15     yes  4.00  Advanced    Advanced         1
            38     yes  2.65  Advanced    Beginner         1
            5       no  3.44    Novice      Novice         0
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            19     yes  1.98  Advanced    Advanced         0
            >>>

            # Example 1: Get the sample variance for values in 'gpa' column.
            # Execute var() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> var_column = admissions_train.gpa.var()
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, var_=var_column)
            >>> df
                   var_
            0  0.263953

            # Example 2: Get the population variance for values in 'gpa' column.
            # Execute var() function on teradataml DataFrameColumn to generate the ColumnExpression.
            # To calculate population variance we must set population=True.
            >>> var_column = admissions_train.gpa.var(population=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df = admissions_train.assign(True, var_=var_column)
            >>> df
                   var_
            0  0.257354
            >>>

            # Example 3: Get the sample variance for distinct values in 'gpa' column.
            #            for each level of programming.
            # Note:
            #   When assign() is run after DataFrame.groupby(), the function ignores
            #   the "drop_columns" argument.
            # Execute var() function using teradataml DataFrameColumn to generate the ColumnExpression.
            >>> var_column = admissions_train.gpa.var(distinct=True)
            # Pass the generated ColumnExpression to DataFrame.assign(), to run and produce the result.
            >>> df=admissions_train.groupby("programming").assign(var_=var_column)
            >>> df
              programming      var_
            0    Advanced  0.252421
            1      Novice  0.418267
            2    Beginner  0.138496
            >>>
        """
        if population:
            return self.__generate_function_call_object(func.var_pop, distinct=distinct, **kwargs)
        else:
            return self.__generate_function_call_object(func.var_samp, distinct=distinct, **kwargs)


class _SQLColumnExpression(_LogicalColumnExpression,
                           _ArithmeticColumnExpression,
                           _SeriesColumnExpression,
                           _AggregateColumnExpresion):
    """
    _SQLColumnExpression is used to build Series/Column manipulations into SQL.
    It represents a column from a Table or an expression involving some operation
    between columns and other literals.

    These objects are created from _SQLTableExpression or from operations
    involving other _SQLColumnExpressions.

    They behave like sqlalchemy.Column objects when accessed from the SQLTableExpression.
    Thus you can access certain common attributes (decorated with property) specified by
    the ColumnExpression interface. Otherwise, the attributes refer to expressions.
    In this case, None is returned if an attribute is not found in the expression.

    This class is internal.
    """

    def __init__(self, expression, **kw):
        """
        Initialize the ColumnExpression

        PARAMETERS:
            expression : Required Argument.
                         A sqlalchemy.ClauseElement instance.

        """
        if isinstance(expression, str):
            expression = literal_column(expression)
        self.kw = kw
        self.expression = expression
        self.type = kw.get("type", expression.type)
        # Initial ColumnExpression has only one dataframe and hence
        # __has_multiple_dataframes = False.
        # eg: df1.col1, df2.col2
        self.__has_multiple_dataframes = False
        self.__names = []

    @property
    def expression(self):
        """
        A reference to the underlying column expression.

        PARAMETERS:
            None

        RETURNS:
            sqlalchemy.sql.elements.ColumnClause

        RAISE:
            None

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.gpa.expression
            Column('gpa', FLOAT(), table=<admissions_train>, nullable=False)
        """
        return self.__expression

    @expression.setter
    def expression(self, expression):
        """
        Sets a reference to the underlying column expression.
        """
        self.__expression = expression

    def get_flag_has_multiple_dataframes(self):
        """
        Returns whether the underlying column expression uses multiple dataframes or not.
        If column expression has only one dataframe, this function returns False; otherwise True.
        """
        return self.__has_multiple_dataframes

    def set_flag_has_multiple_dataframes(self, has_multiple_dataframes):
        """
        Sets __has_multiple_dataframes True or False based on the argument has_multiple_dataframes.
        """
        if (not isinstance(has_multiple_dataframes, bool)):
            raise ValueError('_SQLColumnExpression requires a boolean type argument '
                         'has_multiple_dataframes')
        self.__has_multiple_dataframes = has_multiple_dataframes

    @property
    def original_column_expr(self):
        """
        Returns a list of original ColumnExpression.
        """
        return self.original_expressions

    @original_column_expr.setter
    def original_column_expr(self, expression):
        """
        Sets the original_column_expr property to a list of ColumnExpressions.
        """
        if not isinstance(expression, list):
            raise ValueError('_SQLColumnExpression requires a list type argument '
                         'expression')
        self.original_expressions = expression

    @property
    def type(self):
        """
        Returns the underlying sqlalchemy type of the current expression.

        PARAMETERS:
            None

        RETURNS:
            teradatasqlalchemy.types

        RAISE:
            None

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.gpa.type
            FLOAT()
        """
        if self._type is not None:
            return self._type
        else:
            return self.expression.type

    @type.setter
    def type(self, value):
        """
        Setter for type property of _SQLColumnExpression.
        Allows to set the column expression type.
        """
        if value is None:
            self._type = self.expression.type
        else:
            self._type = value

        from teradataml.dataframe.vantage_function_types import \
            _retrieve_function_expression_type

        # If user passes a sqlalchemy expression, then teradataml do not know the type and
        # so self.kw do not have the expected type. Only then, the type should be derived
        # from  _retrieve_function_expression_type. Other wise, do not do any thing.
        #   Ex - when expression is res_col=df[col].sum(), teradataml is intelligent enough to
        #        predict the output type and corresponding type will be available in self.kw.
        #        If expression is func.sum(df[col].expression), teradataml do not know the type
        #        so retrieve it using _retrieve_function_expression_type
        if isinstance(self.expression, sqlalc.sql.functions.sum) and "type" not in self.kw:
            self._type = _retrieve_function_expression_type(self.expression)

        if not isinstance(self._type, _TDType):
            # If value is either SQLAlchemy NullType or any of SQLAlchemy type, then retrieve the
            # type for function expression from SQLAlchemy expression and input arguments.
            # sqlalc.sql.type_api.TypeEngine is grand parent class to all SQLAlchemy data types.
            # Hence checking if self._type is instance of that class.
            if isinstance(self._type, sqlalc.sql.sqltypes.NullType) or \
                    isinstance(self._type, sqlalc.sql.type_api.TypeEngine):
                if isinstance(self.expression, sqlalc.sql.elements.Over) \
                        or isinstance(self.expression, sqlalc.sql.functions.Function):
                    self._type = _retrieve_function_expression_type(self.expression)

    @property
    def name(self):
        """
        Returns the underlying name attribute of self.expression or None
        if the expression has no name. Note that the name may also refer to
        an alias or label() in sqlalchemy

        PARAMETERS:
            None

        RETURNS:
            str

        RAISE:
            None

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.gpa.name
            gpa
        """
        return getattr(self.expression, 'name', None)

    @property
    def table(self):
        """
        Returns the underlying table attribute of the sqlalchemy.Column

        PARAMETERS:
            None

        RETURNS:
            str

        RAISE:
            None

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.gpa.table
            Table('admissions_train', MetaData(bind=Engine(teradatasql://alice:***@sdt61582.labs.teradata.com)),
            Column('id', INTEGER(), table=<admissions_train>, nullable=False), Column('masters', VARCHAR(length=5,
            charset='LATIN'), table=<admissions_train>, nullable=False), Column('gpa', FLOAT(), table=<admissions_train>,
            nullable=False), Column('stats', VARCHAR(length=30, charset='LATIN'), table=<admissions_train>, nullable=False),
            Column('programming', VARCHAR(length=30, charset='LATIN'), table=<admissions_train>, nullable=False),
            Column('admitted', INTEGER(), table=<admissions_train>, nullable=False), schema=None)

        """
        return getattr(self.expression, 'table', None)

    def compile(self, *args, **kw):
        """
        Calls the compile method of the underlying sqlalchemy.Column
        """
        if len(kw) == 0:
            kw = dict({'dialect': td_dialect(),
                'compile_kwargs':
                    {
                        'include_table': False,
                        'literal_binds': True
                    }
                })

        return str(self.expression.compile(*args, **kw))

    def compile_label(self, label):
        """
        DESCRIPTION:
            Compiles expression with label, by calling underlying sqlalchemy methods.

        PARAMETES:
            label:
                Required Argument.
                Specifies the label to be used to alias the compiled expression.
                Types: str

        RAISES:
            None.

        RETURNS:
            string - compiled expression.

        EXAMPLES:
            self.compile_label("col1")
        """
        compiler = td_compiler(td_dialect(), None)
        aliased_expression = compiler.visit_label(self.expression.label(label),
                                                  within_columns_clause=True,
                                                  include_table=False,
                                                  literal_binds=True)
        return aliased_expression

    def cast(self, type_ = None):
        """
        DESCRIPTION:
            Apply the CAST SQL function to the column with the type specified.

            NOTE: This method can currently be used only with 'filter' and
                  'assign' methods of teradataml DataFrame.

        PARAMETERS:
            type_:
                Required Argument.
                Specifies a teradatasqlalchemy type or an object of a teradatasqlalchemy type
                that the column needs to be cast to.
                Default value: None
                Types: teradatasqlalchemy type or object of teradatasqlalchemy type

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming  admitted
            id
            13      no  4.00  Advanced      Novice         1
            26     yes  3.57  Advanced    Advanced         1
            5       no  3.44    Novice      Novice         0
            19     yes  1.98  Advanced    Advanced         0
            15     yes  4.00  Advanced    Advanced         1
            40     yes  3.95    Novice    Beginner         0
            7      yes  2.33    Novice      Novice         1
            22     yes  3.46    Novice    Beginner         0
            36      no  3.00  Advanced      Novice         0
            38     yes  2.65  Advanced    Beginner         1
            >>> df.dtypes
            id               int
            masters          str
            gpa            float
            stats            str
            programming      str
            admitted         int

            >>> # Let's try creating a new DataFrame casting 'id' column (of type INTEGER) to VARCHAR(5),
            >>> # an object of a teradatasqlalchemy type.
            >>> from teradatasqlalchemy import VARCHAR
            >>> new_df = df.assign(char_id = df.id.cast(type_=VARCHAR(5)))
            >>> new_df
               masters   gpa     stats programming  admitted char_id
            id
            5       no  3.44    Novice      Novice         0       5
            34     yes  3.85  Advanced    Beginner         0      34
            13      no  4.00  Advanced      Novice         1      13
            40     yes  3.95    Novice    Beginner         0      40
            22     yes  3.46    Novice    Beginner         0      22
            19     yes  1.98  Advanced    Advanced         0      19
            36      no  3.00  Advanced      Novice         0      36
            15     yes  4.00  Advanced    Advanced         1      15
            7      yes  2.33    Novice      Novice         1       7
            17      no  3.83  Advanced    Advanced         1      17
            >>> new_df.dtypes
            id               int
            masters          str
            gpa            float
            stats            str
            programming      str
            admitted         int
            char_id          str

            >>> # Now let's try creating a new DataFrame casting 'id' column (of type INTEGER) to VARCHAR,
            >>> # a teradatasqlalchemy type.
            >>> new_df_2 = df.assign(char_id = df.id.cast(type_=VARCHAR))
            >>> new_df_2
               masters   gpa     stats programming  admitted char_id
            id
            5       no  3.44    Novice      Novice         0       5
            34     yes  3.85  Advanced    Beginner         0      34
            13      no  4.00  Advanced      Novice         1      13
            40     yes  3.95    Novice    Beginner         0      40
            22     yes  3.46    Novice    Beginner         0      22
            19     yes  1.98  Advanced    Advanced         0      19
            36      no  3.00  Advanced      Novice         0      36
            15     yes  4.00  Advanced    Advanced         1      15
            7      yes  2.33    Novice      Novice         1       7
            17      no  3.83  Advanced    Advanced         1      17
            >>> new_df_2.dtypes
            id               int
            masters          str
            gpa            float
            stats            str
            programming      str
            admitted         int
            char_id          str

            >>> # Let's try filtering some data with a match on a column cast to another type,
            >>> # an object of a teradatasqlalchemy type.
            >>> df[df.id.cast(VARCHAR(5)) == '1']
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0

            >>> # Now let's try the same, this time using a teradatasqlalchemy type.
            >>> df[df.id.cast(VARCHAR) == '1']
               masters   gpa     stats programming  admitted
            id
            1      yes  3.95  Beginner    Beginner         0

        RETURNS:
            _SQLColumnExpression

        RAISES:
            TeradataMlException
        """
        # If type_ is None or not specified, raise an Exception
        if type_ is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS, 'type_'),
                                      MessageCodes.MISSING_ARGS)

        # Check that the type_ is a valid teradatasqlalchemy type
        if not UtilFuncs._is_valid_td_type(type_):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, 'type_',
                                                           'a valid teradatasqlalchemy type'),
                                      MessageCodes.UNSUPPORTED_DATATYPE)

        expression = func.cast(self.expression, type_=type_).label(self.name)
        return _SQLColumnExpression(expression)

    def __hash__(self):
        return hash(self.expression)

    def __dir__(self):
        # currently str is the only accessor
        # if we end up adding more, consider making this
        # list an instance attribute (i.e self._accessors) of the class
        accessors = ['str']
        attrs = {x for x in dir(type(self)) if not x.startswith('_') and x not in accessors}

        if isinstance(self.type, (CLOB, CHAR, VARCHAR)):
            return attrs | set(['str']) # str accessor is only visible for string-like columns

        return attrs

    # TODO - For future to enable execution of other functions with bulk exposure approach.
    '''
    def __getattr__(self, item):
        """
        Returns an attribute of the _SQLColumnExpression.

        PARAMETERS:
            name: the name of the attribute.

        RETURNS:
            _SQLColumnExpression

        EXAMPLES:
            df = DataFrame('table')
            df.column.lead()
        """
        # We can implement this logic in _SQLColumnExpression, that will allow
        # us to achieve "Generic Vantage SQL Function Support".
        # TODO::
        #   Add a check that skips executing Aggregate functions via this.
        return lambda *args, **kwargs: \
            self.__process_unimplemented_functions(item, *args, **kwargs)
    '''

    def _generate_vantage_function_call(self, func_name, col_name=None,
                                        type_=None, column_function=True,
                                        property=False, return_func=False,
                                        *args):
        """
        Internal function that generates a Vantage SQL function call.
        Function makes use of GenericFunciton from sqlalchemy to generate
        the function call.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the SQL function name to be executed.
                Types: str

            col_name:
                Optional Argument.
                Specifies the column name to use for executing the function.
                Types: str

            type_:
                Optional Argument.
                Specifies the output type of the function that it'll result
                in when executed.
                Types: teradatasqlalchemy.types

            column_function:
                Optional Argument.
                Specifies whether the SQL function is executed as
                'column.func_name()' or 'func_name(column)'. This parameter
                must be set to True, is SQL function syntax is
                'column.func_name()', otherwise must be set to False.
                Default Value: True
                Types: bool

            property:
                Optional Argument.
                Specifies whether the function being executed is exposed as
                property or method of a class. When set to True, it is
                exposed as property, otherwise method.
                Default Value: False
                Types: bool

            return_func:
                Optional Argument.
                Specifies whether to return the function object or not,
                instead of returning the _SQLColumnExpression.
                When set to True, returns the Function object (sqlalchemy).
                Default Value: False
                Types: bool

            *args:
                Specifies the SQL function function arguments.

        Returns:
            _SQLColumnExpression when "return_func" is False, otherwise
            sqlalchemy.sql.elements.Function object is returned.

        RAISES:
            None

        EXAMPLES:
            self._generate_vantage_function_call(
                func_name="function_name", col_name="col_name", return_func=True,
                type_=INTEGER())
        """
        from sqlalchemy.sql.functions import GenericFunction
        from sqlalchemy.sql.elements import quoted_name
        from sqlalchemy.exc import SAWarning

        # Catch and ignore SAWarning from sqlalchemy, which is thrown for
        # registering the function again with Generic function.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=SAWarning)

            # A class that allows us to create a GenericFunction and
            # it's associated attributes.
            class VantageGeneric(GenericFunction):
                # Set the output type for the function.
                if type_ is not None:
                    type = type_
                else:
                    # If user has not passed any type, then set it to
                    # NullType().
                    type = sqlalc.sql.sqltypes.NullType()

                # Generate the function syntax based on whether the
                # function is column function or not.
                if column_function:
                    name = quoted_name("{}.{}".format(col_name, func_name),
                                       False)
                else:
                    name = quoted_name(func_name, False)

                # Identifier to access the function with.
                identifier = func_name
                package = "vantage"

        # Invoke the function and return the results.
        if property:
            return self._wrap_as_column_expression(getattr(func.vantage,
                                                           func_name)())
        else:
            if return_func:
                #return getattr(func.vantage, func_name)
                return self._wrap_as_column_expression(getattr(func.vantage,
                                                               func_name))
            else:
                return self._wrap_as_column_expression(getattr(func.vantage,
                                                               func_name)(*args))

    def _wrap_as_column_expression(self, new_expression):
        """
        Internal function that wraps the provided expression as
        _SQLColumnExpression.

        PARAMETERS:
            new_expression:
                 Required Argument.
                 Specifies the expression to be returned.
                 Types: Any expression.

        RETURNS:
            _SQLColumnExpression.

        RAISES:
            None.

        EXAMPLES:
            self._wrap_as_column_expression(getattr(func.vantage,
                                                    func_name)(*args))
        """
        return _SQLColumnExpression(new_expression)

    '''
    def __process_unimplemented_functions(self, *c, **kwargs):
        """ TODO: Execute function that are not implemented. Future. """

        # Process the positional arguments passed in *c.
        new_c = [item.expression if isinstance(item, _SQLColumnExpression)
                 else item for item in c]

        # Extract the "type_" argument, if it is given, else set it to None.
        t_ = kwargs.get("type_", None)
        if t_ is None:
            # If "type_" is not passed, let's extract from the function name
            # and expression using the pre-defined vantage function output
            # type mappers.
            from teradataml.dataframe.vantage_function_types import \
                _retrieve_function_expression_type
            t_ = _retrieve_function_expression_type(self.expression)

        # Set some parameters to be passed to
        # '_generate_vantage_function_call()' function.
        cname = None
        cfunction = False
        new_c = (self.expression,) + tuple(new_c)

        # This returns quoted name, we should use quoted_name = False while
        # generating call.
        fname = ".".join(self.__names)

        # Generate the SQL function call.
        return self._generate_vantage_function_call(fname, cname, t_, cfunction,
                                                    False, False, *new_c)
    '''

    def __getitem__(self, key):
        """ Function to make _SQLColumnExpression subscriptable. """
        if isinstance(key, str):
            return getattr(self, key)

    def window(self,
               partition_columns=None,
               order_columns=None,
               sort_ascending=True,
               nulls_first=None,
               window_start_point=None,
               window_end_point=None,
               ignore_window=False):
        """
        DESCRIPTION:
            This function generates Window object on a teradataml DataFrame Column to run
            window aggregate functions.
            Function allows user to specify window for different types of
            computations:
                * Cumulative
                * Group
                * Moving
                * Remaining
            By default, window with Unbounded Preceding and Unbounded following
            is considered for calculation.
            Note:
                If both "partition_columns" and "order_columns" are None, then
                Window cannot be created on CLOB and BLOB type of columns.

        PARAMETERS:
            partition_columns:
                Optional Argument.
                Specifies the name(s) of the column(s) over which the ordered
                aggregate function executes by partitioning the rows. Such a
                grouping is static.
                Notes:
                     1. If this argument is not specified, then the entire data
                        from teradataml DataFrame, constitutes a single
                        partition, over which the ordered aggregate function
                        executes.
                     2. "partition_columns" does not support CLOB and BLOB type
                        of columns.
                        Refer 'DataFrame.tdtypes' to get the types of the
                        columns of a teradataml DataFrame.
                     3. "partition_columns" supports only columns specified in
                        groupby function, if Column is from DataFrameGroupBy.
                Types: str OR list of Strings (str)

            order_columns:
                Optional Argument.
                Specifies the name(s) of the column(s) to order the rows in a
                partition, which determines the sort order of the rows over
                which the function is applied.
                Notes:
                    1. "order_columns" does not support CLOB and BLOB type of
                       columns.
                       Refer 'DataFrame.tdtypes' to get the types of the columns
                       of a teradataml DataFrame.
                    2. "order_columns" supports only columns specified in
                        groupby function, if Column is from DataFrameGroupBy.
                Types: str OR list of Strings (str)

            sort_ascending:
                Optional Argument.
                Specifies whether column ordering should be in ascending or
                descending order.
                Default Value: True (ascending)
                Note:
                    When "order_columns" argument is not specified, argument
                    is ignored.
                Types: bool

            nulls_first:
                Optional Argument.
                Specifies whether null results are to be listed first or last
                or scattered.
                Default Value: None
                Note:
                    When "order_columns" argument is not specified, argument
                    is ignored.
                Types: bool

            window_start_point:
                Optional Argument.
                Specifies a starting point for a window. Based on the integer
                value, n, starting point of the window is decided.
                    * If 'n' is negative, window start point is n rows
                      preceding the current row/data point.
                    * If 'n' is positive, window start point is n rows
                      following the current row/data point.
                    * If 'n' is 0, window start at current row itself.
                    * If 'n' is None, window start as Unbounded preceding,
                      i.e., all rows before current row/data point are
                      considered.
                Notes:
                     1. Value passed to this should always satisfy following condition:
                        window_start_point <= window_end_point
                     2. Following functions does not require any window to
                        perform window aggregation. So, "window_start_point" is
                        insignificant for below functions:
                        * cume_dist
                        * rank
                        * dense_rank
                        * percent_rank
                        * row_number
                        * lead
                        * lag
                Default Value: None
                Types: int

            window_end_point:
                Optional Argument.
                Specifies an end point for a window. Based on the integer value,
                n, starting point of the window is decided.
                    * If 'n' is negative, window end point is n rows preceding
                      the current row/data point.
                    * If 'n' is positive, window end point is n rows following
                      the current row/data point.
                    * If 'n' is 0, window end's at current row itself.
                    * If 'n' is None, window end's at Unbounded following,
                      i.e., all rows before current row/data point are
                      considered.
                Notes:
                     1. Value passed to this should always satisfy following condition:
                        window_start_point <= window_end_point
                     2. Following functions does not require any window to
                        perform window aggregation. So, "window_end_point" is
                        insignificant for below functions:
                        * cume_dist
                        * rank
                        * dense_rank
                        * percent_rank
                        * row_number
                        * lead
                        * lag
                Default Value: None
                Types: int

            ignore_window:
                Optional Argument.
                Specifies a flag to ignore parameters related to creating
                window ("window_start_point", "window_end_point") and use other
                arguments, if specified.
                When set to True, window is ignored, i.e., ROWS clause is not
                included.
                When set to False, window will be created, which is specified
                by "window_start_point" and "window_end_point" parameters.
                Default Value: False
                Types: bool

        RAISES:
            TypeError, ValueError

        RETURNS:
            An object of type Window.

        EXAMPLES:
            # Example 1: Create a window on a teradataml DataFrame column.
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> window = df.Feb.window()
            >>>

            # Example 2: Create a cumulative (expanding) window with rows
            #            between unbounded preceding and 3 preceding with
            #            "partition_columns" and "order_columns" argument with
            #            default sorting.
            >>> window = df.Feb.window(partition_columns="Feb",
            ...                        order_columns=["Feb", "datetime"],
            ...                        window_start_point=None,
            ...                        window_end_point=-3)
            >>>

            # Example 3: Create a moving (rolling) window with rows between
            #            current row and 3 following with sorting done on 'Feb',
            #            'datetime' columns in descending order and
            #            "partition_columns" argument.
            >>> window = df.Feb.window(partition_columns="Feb",
            ...                        order_columns=["Feb", "datetime"],
            ...                        sort_ascending=False,
            ...                        window_start_point=0,
            ...                        window_end_point=3)
            >>>

            # Example 4: Create a remaining (contracting) window with rows
            #            between current row and unbounded following with
            #            sorting done on 'Feb', 'datetime' columns in ascending
            #            order and NULL values in 'Feb', 'datetime'
            #            columns appears at last.
            >>> window = df.Feb.window(partition_columns="Feb",
            ...                        order_columns=["Feb", "datetime"],
            ...                        nulls_first=False,
            ...                        window_start_point=0,
            ...                        window_end_point=None
            ...                        )
            >>>

            # Example 5: Create a grouping window, with sorting done on 'Feb',
            #            'datetime' columns in ascending order and NULL values
            #            in 'Feb', 'datetime' columns appears at last.
            >>> window = df.Feb.window(partition_columns="Feb",
            ...                        order_columns=["Feb", "datetime"],
            ...                        sort_ascending=False,
            ...                        nulls_first=False,
            ...                        window_start_point=None,
            ...                        window_end_point=None
            ...                        )
            >>>

            # Example 6: Create a window on a teradataml DataFrame column, which
            #            ignores all the parameters while creating window.
            >>> window = df.Feb.window(partition_columns="Feb",
            ...                        order_columns=["Feb", "datetime"],
            ...                        sort_ascending=False,
            ...                        nulls_first=False,
            ...                        ignore_window=True
            ...                        )
            >>>

            # Example 7: Perform sum of Feb and attach new column to the
            # DataFrame.
            >>> window = df.Feb.window()
            >>> df.assign(feb_sum=window.sum())
                          Feb    Jan    Mar    Apr    datetime  feb_sum
            accounts
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017   1000.0
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017   1000.0
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017   1000.0
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017   1000.0
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017   1000.0
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017   1000.0
            >>>

            # Example 8: Perform min and max operations on column Apr and
            # attach both the columns to the DataFrame.
            >>> window = df.Apr.window()
            >>> df.assign(apr_min=window.min(), apr_max=window.max())
                          Feb    Jan    Mar    Apr    datetime  apr_max  apr_min
            accounts
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017      250      101
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017      250      101
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017      250      101
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017      250      101
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017      250      101
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017      250      101
            >>>

            # Example 9: Perform count and max operations on column accounts in
            # teradataml DataFrame, which is grouped by 'accounts', and attach
            # column to DataFrame.
            >>> df = df.groupby("accounts")
            >>> window = df.accounts.window()
            >>> df.assign(accounts_max=window.max(), accounts_count=window.count())
                 accounts  accounts_count accounts_max
            0   Jones LLC               6   Yellow Inc
            1     Red Inc               6   Yellow Inc
            2  Yellow Inc               6   Yellow Inc
            3  Orange Inc               6   Yellow Inc
            4    Blue Inc               6   Yellow Inc
            5    Alpha Co               6   Yellow Inc
            >>>
        """
        return Window(object=self,
                        partition_columns=partition_columns,
                        order_columns=order_columns,
                        sort_ascending=sort_ascending,
                        nulls_first=nulls_first,
                        window_start_point=window_start_point,
                        window_end_point=window_end_point,
                        ignore_window=ignore_window)

    def desc(self):
        """
        DESCRIPTION:
            Generates a new _SQLColumnExpression which sorts the actual
            expression in Descending Order.
            Note:
                This function is supported only while sorting the Data. This
                function is neither supported in projection nor supported in
                filtering the Data.

        RAISES:
            None

        RETURNS:
            An object of type _SQLColumnExpression.

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')

            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')

            # Sorts the Data on column accounts in ascending order and column
            # Feb in descending order, then calculates moving average by dropping
            # the input DataFrame columns on the window of size 2.
            >>> df.mavg(width=2, sort_columns=[df.accounts, df.Feb.desc()], drop_columns=True)
               mavg_Feb  mavg_Jan  mavg_Mar  mavg_Apr mavg_datetime
            0     145.0     100.0     117.5     140.5    04/01/2017
            1     205.0     150.0     140.0     250.0    04/01/2017
            2     145.0     150.0     140.0       NaN    04/01/2017
            3     205.0     150.0     140.0     215.0    04/01/2017
            4     150.0     125.0     155.0     175.5    04/01/2017
            5     210.0     200.0     215.0     250.0    04/01/2017
        """
        return _SQLColumnExpression(self.expression.desc().label(self.name))

    def asc(self):
        """
        DESCRIPTION:
            Generates a new _SQLColumnExpression which sorts the actual
            expression in Ascending Order.
            Note:
                This function is supported only while sorting the Data. This
                function is neither supported in projection nor supported in
                filtering the Data.

        RAISES:
            None

        RETURNS:
            An object of type _SQLColumnExpression.

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')

            # Sorts the Data on column accounts in ascending order and column
            # Feb in descending order, then calculates moving average by dropping
            # the input DataFrame columns on the window of size 2.
            >>> df.mavg(width=2, sort_columns=[df.accounts, df.Feb.desc()], drop_columns=True)
               mavg_Feb  mavg_Jan  mavg_Mar  mavg_Apr mavg_datetime
            0     145.0     100.0     117.5     140.5    04/01/2017
            1     205.0     150.0     140.0     250.0    04/01/2017
            2     145.0     150.0     140.0       NaN    04/01/2017
            3     205.0     150.0     140.0     215.0    04/01/2017
            4     150.0     125.0     155.0     175.5    04/01/2017
            5     210.0     200.0     215.0     250.0    04/01/2017
        """
        return _SQLColumnExpression(self.expression.asc().label(self.name))

    def nulls_first(self):
        """
        DESCRIPTION:
            Generates a new _SQLColumnExpression which displays NULL values first.
            Note:
                The function can be applied only in conjunction with "asc" or "desc".

        RAISES:
            None

        RETURNS:
            An object of type _SQLColumnExpression.

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')

            # Sorts the Data on column accounts in ascending order and column
            # Feb in descending order, then calculates moving average by dropping
            # the input DataFrame columns on the window of size 2.
            >>> df.mavg(width=2, sort_columns=[df.accounts.desc().nulls_first()], drop_columns=True)
               mavg_Feb  mavg_Jan  mavg_Mar  mavg_Apr mavg_datetime
            0     145.0     100.0     117.5     140.5    04/01/2017
            1     205.0     150.0     140.0     250.0    04/01/2017
            2     145.0     150.0     140.0       NaN    04/01/2017
            3     205.0     150.0     140.0     215.0    04/01/2017
            4     150.0     125.0     155.0     175.5    04/01/2017
            5     210.0     200.0     215.0     250.0    04/01/2017
        """
        return _SQLColumnExpression(self.expression.nulls_first().label(self.name))

    def nulls_last(self):
        """
        DESCRIPTION:
            Generates a new _SQLColumnExpression which displays NULL values last.
            Note:
                The function can be applied only in conjunction with "asc" or "desc".

        RAISES:
            None

        RETURNS:
            An object of type _SQLColumnExpression.

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')

            # Sorts the Data on column accounts in ascending order and column
            # Feb in descending order, then calculates moving average by dropping
            # the input DataFrame columns on the window of size 2.
            >>> df.mavg(width=2, sort_columns=[df.accounts.asc().nulls_last(), df.Feb.desc().nulls_last()], drop_columns=True)
               mavg_Feb  mavg_Jan  mavg_Mar  mavg_Apr mavg_datetime
            0     145.0     100.0     117.5     140.5    04/01/2017
            1     205.0     150.0     140.0     250.0    04/01/2017
            2     145.0     150.0     140.0       NaN    04/01/2017
            3     205.0     150.0     140.0     215.0    04/01/2017
            4     150.0     125.0     155.0     175.5    04/01/2017
            5     210.0     200.0     215.0     250.0    04/01/2017
        """
        return _SQLColumnExpression(self.expression.nulls_last().label(self.name))

    def distinct(self):
        """
        DESCRIPTION:
            Generates a new _SQLColumnExpression which removes the duplicate
            rows while processing the function.
            Note:
                This function is supported only in Projection. It is neither
                supported in sorting the records nor supported in filtering
                the records.

        RAISES:
            None

        RETURNS:
            An object of type _SQLColumnExpression.

        EXAMPLES:
            >>> from teradataml import *
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df
                          Feb    Jan    Mar    Apr    datetime
            accounts
            Blue Inc     90.0   50.0   95.0  101.0  04/01/2017
            Alpha Co    210.0  200.0  215.0  250.0  04/01/2017
            Jones LLC   200.0  150.0  140.0  180.0  04/01/2017
            Yellow Inc   90.0    NaN    NaN    NaN  04/01/2017
            Orange Inc  210.0    NaN    NaN  250.0  04/01/2017
            Red Inc     200.0  150.0  140.0    NaN  04/01/2017
            >>>
            >>> df.assign(drop_columns=True, distinct_feb=df.Feb.distinct())
               distinct_feb
            0         210.0
            1          90.0
            2         200.0
            >>>
        """
        return _SQLColumnExpression(self.expression.distinct().label(self.name))

    def __get_columns(self, col_expr):
        """
        DESCRIPTION:
            Function to get the columns involved in a sqlalchemy expression.

        PARAMETERS:
            col_expr:
                Required Argument.
                Specifies the sqlalchemy expression.
                Types: BinaryExpression OR Grouping OR GenericFunction OR ClauseList OR Column

        RAISES:
            None

        RETURNS:
            list

        EXAMPLES:
            >>> self.__get_columns(self.expression)
        """
        # If it is a column, return the name of the column.
        if isinstance(col_expr, Column):
            return [col_expr.name]

        # Every other type exposes a method to retrieve the children. Recursively, walk through all
        # the childs till a Column or a Bind Parameter is reached.
        elif isinstance(col_expr, (BinaryExpression, Grouping, GenericFunction, ClauseList, Function)):
            res = []
            for c in col_expr.get_children():
                res = res + self.__get_columns(c)
            return res
        else:
            try:
                if isinstance(col_expr, ExpressionClauseList):
                    res = []
                    for c in col_expr.get_children():
                        res = res + self.__get_columns(c)
                    return res
            except NameError:
                pass
        # If the child is a Bind Parameter, return empty string.
        return []

    @property
    def _all_columns(self):
        """
        DESCRIPTION:
            A property to get the columns involved in ColumnExpression.

        RAISES:
            None

        RETURNS:
            list

        EXAMPLES:
            >>> self._all_columns
        """
        return list(set(self.__get_columns(self.expression)))

