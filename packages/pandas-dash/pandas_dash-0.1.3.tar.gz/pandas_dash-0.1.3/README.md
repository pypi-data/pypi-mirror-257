# Pandas Dash

![Python version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg)
[![PyPI version](https://badge.fury.io/py/pandas-dash.svg)](https://pypi.org/project/pandas-dash/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/lucasjamar/pandas-dash/blob/main/LICENSE.md)

Tools for working with Pandas, Plotly, and Dash.

[See examples](https://github.com/lucasjamar/pandas-dash/blob/main/examples/app.py)

## Available extensions for `Dash`
* `df.dash.to_dash_table()` for getting the `data` and `columns` for `dash_table` from a flat or multi-index `pd.DataFrame`.
* `df.dash.to_options("my_column")` for creating `dcc.Dropdown` options from the column of a `pd.DataFrame`.
* `df.dash.to_pivot_table()` for creating the date necessary for `dash_pivottable.PivotTable`.

## Extensions for `Plotly` coming soon.