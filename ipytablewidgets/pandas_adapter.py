# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import pandas as pd
from .source_adapter import SourceAdapter


class PandasAdapter(SourceAdapter):
    def __init__(self, source, *args, **kw):
        assert source is None or isinstance(source, pd.DataFrame)
        super().__init__(source, *args, **kw)

    @property
    def columns(self):
        return self._columns or self._source.columns.tolist()

    def to_array(self, col):
        return self._source[col].to_numpy()

    def equals(self, other):
        if isinstance(other, SourceAdapter):
            other = other._source
        if not isinstance(other, pd.DataFrame):
            other = pd.DataFrame(other)
        return self._source.equals(other)
