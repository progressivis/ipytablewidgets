# ipytablewidgets

![Python tests](https://github.com/progressivis/ipytablewidgets/actions/workflows/python.yml/badge.svg)

![Typescript tests](https://github.com/progressivis/ipytablewidgets/actions/workflows/ts.yml/badge.svg)

![End to end tests](https://github.com/progressivis/ipytablewidgets/actions/workflows/e2e.yml/badge.svg)

**NB:** End to end tests use [Galata]() framework.

Traitlets and widgets to efficiently data tables (e.g. Pandas DataFrame) using the jupyter notebook


ipytablewidgets is a set of widgets and traitlets to reuse of large tables such as Pandas DataFrames
across different widgets, and different packages.


## Installation

Using pip:

```bash
pip install ipytablewidgets
```

## Development installation

The first step requires the following three commands to be run (requires yarn and jupyterlab>=3):

```bash
$ git clone https://github.com/progressivis/ipytablewidgets.git
$ cd ipytablewidgets
$ pip install -e .
```
The development of extensions for **jupyter notebook** and **jupyter lab** requires **JavaScript** code to be modified in-place. For this reason, _lab_ and _notebook_ extensions need to be configured this way:

* For **jupyter notebook:**
    ```bash
    $ jupyter nbextension install --py --overwrite --symlink --sys-prefix ipytablewidgets
    $ jupyter nbextension enable --py --sys-prefix ipytablewidgets
    ```
* For **jupyter lab:**
    ```bash
    $ jupyter labextension develop . --overwrite
    ```

### Tables

The main widget for tables is the `TableWidget` class. It has a main trait: A
table. This table's main purpose is simply to be a standardized way of transmitting table
data from the kernel to the frontend, and to allow the data to be reused across
any number of other widgets, but with only a single sync across the network.

```python
import pandas as pd
from ipytableidgets import TableWidget, PandasAdapter, serialization

@widgets.register
class MyWidget(DOMWidget):
    """
    My widget needing a table
    """
    _view_name = Unicode('MyWidgetView').tag(sync=True)
    _model_name = Unicode('MyWidgetModel').tag(sync=True)
    ...
    data = Instance(TableWidget).tag(sync=True, **serialization)
    def __init__(self, wg, **kwargs):
        self.data = wg
        super().__init__(**kwargs)

df = pd.DataFrame({'a': [1,2], 'b': [3.5, 4.5], 'c': ['foo','bar'])
table_widget = TableWidget(PandasAdapter(df))
my_widget = MyWidget(table_widget)
```

You can see [EchoTableWidget](https://github.com/progressivis/ipytablewidgets/blob/main/ipytablewidgets/widgets.py) which is a more realistic example, currently used for end to end testing and [demo](https://github.com/progressivis/ipytablewidgets/blob/main/notebooks/plain.ipynb).

Or, if you prefer to use the **TableType** traitlet directly:
```python
from ipytablewidgets import serialization, TableType

@widgets.register
class MyWidget(DOMWidget):
    """
    My widget needing a table
    """
    ...
    data = TableType(None).tag(sync=True, **serialization)
```


## Developers

Developers should consider using ipytablewidgets because:

- It gives readily accessible syncing of table data using the binary transfer
  protocol of ipywidgets.
- It gives compression methods speifically suited for columnar data.
- It avoids duplication of common code among different extensions, ensuring
  that bugs discovered for one extension gets fixed in all.


### Overview

The major parts of ipyablewidgets are:

- Traits/Widgets definitions
- Adapters to convert tables to those traits
- Serializers/deserializers to send the data across the network
- Apropriate javascript handling and representation of the data