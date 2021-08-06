from .source_adapter import SourceAdapter
from .pandas_adapter import PandasAdapter
from .numpy_adapter import NumpyAdapter
from .widgets import TableWidget, EchoTableWidget
from .traitlets import TableType
from .serializers import table_to_json, table_from_json, serialization
from .compressors import ZLibCompressor, LZ4Compressor, DEFAULT_COMPRESSORS

__version__ = '0.1.0'


def _jupyter_nbextension_paths():
    """Return metadata for the ipytablewidgets nbextension."""
    return [dict(
        section="notebook",
        # the path is relative to the inner `ipytablewidgets` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="jupyter-tablewidgets",
        # _also_ in the `nbextension/` namespace
        require="jupyter-tablewidgets/extension")]


def find_static_assets():
    warn("""To use the ipytablewidgets nbextension, you'll need to update
    the Jupyter notebook to version 4.2 or later.""")
    return []
