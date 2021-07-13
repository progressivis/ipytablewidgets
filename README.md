# ipytablewidgets
Traitlets and widgets to efficiently data tables (e.g. Pandas DataFrame) using the jupyter notebook


ipytablewidgets is a set of widgets and traitlets to reuse of large tables such as Pandas DataFrames
across different widgets, and different packages.


## Installation

A typical installation requires the following three commands to be run:

```bash
pip install ipytablewidgets
jupyter nbextension install --py [--sys-prefix|--user|--system] ipytablewidgets
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipytablewidgets
```

Or, if you use jupyterlab:

```bash
pip install ipytablewidgets
jupyter labextension install jupyterlab-tablewidgets
```

### Tables

The main widget for tables is the `TableWidget` class. It has a main trait: A
table. This table's main purpose is simply to be a standardized way of transmitting table
data from the kernel to the frontend, and to allow the data to be reused across
any number of other widgets, but with only a single sync across the network.

```python
import pandas as pd
from ipytableidgets import TableWidget

df = pd.DataFrame({'a': [1,2], 'b': [3.5, 4.5], 'c': ['foo','bar'])
tablewidget = TableWidget(PandasAdapter(df))

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
