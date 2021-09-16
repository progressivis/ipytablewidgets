# Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import json
import pandas as pd

# from .compressors import *
from .serializers import serialization
from .traitlets import TableType
from ._frontend import npm_module_name, npm_package_version
#import numpy as np
from ipywidgets import DOMWidget
from traitlets import Unicode, Any, Instance
import ipywidgets as widgets

@widgets.register
class TableWidget(DOMWidget):
    """
    """
    _view_name = Unicode('').tag(sync=True)
    _model_name = Unicode('TableWidgetModel').tag(sync=True)
    #_view_module = Unicode('nbextensions/jupyter-tablewidgets').tag(sync=True)
    _model_module = Unicode(npm_module_name).tag(sync=True)
    _view_module_version = Unicode(npm_package_version).tag(sync=True)
    _model_module_version = Unicode(npm_package_version).tag(sync=True)
    compression = None
    _table = TableType(None).tag(sync=True, **serialization)

    def __init__(self, table=None, compression=None, **kwargs):
        self._table = table
        self.compression = compression
        super().__init__(**kwargs)

@widgets.register
class EchoTableWidget(DOMWidget):
    """
    """
    _view_name = Unicode('EchoTableWidgetView').tag(sync=True)
    _model_name = Unicode('EchoTableWidgetModel').tag(sync=True)
    _view_module = Unicode(npm_module_name).tag(sync=True)
    _model_module = Unicode(npm_module_name).tag(sync=True)
    _view_module_version = Unicode(npm_package_version).tag(sync=True)
    _model_module_version = Unicode(npm_package_version).tag(sync=True)
    data = Instance(TableWidget).tag(sync=True, **serialization)
    echo = Any([]).tag(sync=True)
    def __init__(self, wg, **kwargs):
        self.data = wg
        super().__init__(**kwargs)

