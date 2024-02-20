# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import pandas as pd
import numpy as np
from .source_adapter import SourceAdapter


class PandasAdapter(SourceAdapter):
    def __init__(self, df, *args, columns=None, **kw):
        assert df is None or isinstance(df, pd.DataFrame)
        self.column = {}
        # Synchronized with Altair sanitize_dataframe

        if isinstance(df.index, pd.MultiIndex):
            raise ValueError("Hierarchical indices not supported")
        if isinstance(df.columns, pd.MultiIndex):
            raise ValueError("Hierarchical columns not supported")

        if columns is None:
            columns = df.columns
            if isinstance(columns, pd.RangeIndex):
                columns = columns.astype(str)
            columns = columns.tolist()

        for col in columns:
            if not isinstance(col, str):
                raise ValueError(
                    "Dataframe contains invalid column name: {0!r}. "
                    "Column names must be strings".format(col)
                )

        def to_list_if_array(val):
            if isinstance(val, np.ndarray):
                return val.tolist()
            else:
                return val

        for col_name, dtype in df.dtypes.items():
            if str(dtype) == "category":
                # XXXX: work around bug in to_json for categorical types
                # https://github.com/pydata/pandas/issues/10778
                col = df[col_name].astype(object)
                self.column[col_name] = col.where(col.notnull(), None)
            elif str(dtype) == "string":
                # dedicated string datatype (since 1.0)
                # https://pandas.pydata.org/pandas-docs/version/1.0.0/whatsnew/v1.0.0.html#dedicated-string-data-type
                col = df[col_name].astype(object)
                self.column[col_name] = col.where(col.notnull(), None)
            # bool numpy array are fine
            # elif str(dtype) == "bool":
            #     # convert numpy bools to objects; np.bool is not JSON serializable
            #     df[col_name] = df[col_name].astype(object)
            elif str(dtype) == "boolean":
                # dedicated boolean datatype (since 1.0)
                # https://pandas.io/docs/user_guide/boolean.html
                col = df[col_name].astype(object)
                self.column[col_name] = col.where(col.notnull(), None)
            elif str(dtype).startswith("datetime"):
                # Convert datetimes to strings. This needs to be a full ISO string
                # with time, which is why we cannot use ``col.astype(str)``.
                # This is because Javascript parses date-only times in UTC, but
                # parses full ISO-8601 dates as local time, and dates in Vega and
                # Vega-Lite are displayed in local time by default.
                # (see https://github.com/altair-viz/altair/issues/1027)
                self.column[col_name] = (
                    df[col_name].apply(lambda x: x.isoformat()).replace("NaT", "")
                )
            elif str(dtype).startswith("timedelta"):
                raise ValueError(
                    'Field "{col_name}" has type "{dtype}" which is '
                    "not supported by Vega. Please convert to "
                    "either a timestamp or a numerical value."
                    "".format(col_name=col_name, dtype=dtype)
                )
            elif str(dtype).startswith("geometry"):
                # geopandas >=0.6.1 uses the dtype geometry. Continue here
                # otherwise it will give an error on np.issubdtype(dtype, np.integer)
                self.column[col_name] = df[col_name]
                continue
            elif str(dtype) in {
                "Int8",
                "Int16",
                "Int32",
                "Int64",
                "UInt8",
                "UInt16",
                "UInt32",
                "UInt64",
                "Float32",
                "Float64",
            }:  # nullable integer datatypes (since 24.0) and nullable float datatypes (since 1.2.0)
                # https://pandas.pydata.org/pandas-docs/version/0.25/whatsnew/v0.24.0.html#optional-integer-na-support
                # TODO Check if there are nulls before converting
                col = df[col_name].astype(object)
                self.column[col_name] = col.where(col.notnull(), None)
            # The 2 following cases are handled by our serialization of numpy arrays
            # elif np.issubdtype(dtype, np.integer):
            #     # convert integers to objects; np.int is not JSON serializable
            #     self.column[col_name] = df[col_name].astype(int)
            # elif np.issubdtype(dtype, np.floating):
            #     # For floats, convert to Python float: np.float is not JSON serializable
            #     # Also convert NaN/inf values to null, as they are not JSON serializable
            #     col = df[col_name]
            #     bad_values = col.isnull() | np.isinf(col)
            #     self.column[col_name] = col.astype(object).where(~bad_values, None)
            elif dtype == object:
                # Convert numpy arrays saved as objects to lists
                # Arrays are not JSON serializable
                col = df[col_name].astype(object).apply(to_list_if_array)
                self.column[col_name] = col.where(col.notnull(), None)
            else:
                self.column[col_name] = df[col_name]  # TODO check more

        super().__init__(df, *args, columns=columns, **kw)

    @property
    def columns(self):
        return self._columns

    def to_array(self, col):
        return self.column[col].to_numpy()

    def equals(self, other):
        if isinstance(other, SourceAdapter):
            other = other._source
        if not isinstance(other, pd.DataFrame):
            other = pd.DataFrame(other)
        return self._source.equals(other)
