"""
Generic reusable data table component.
Wraps Dash AG Grid or Dash DataTable.
"""

from typing import Optional
import pandas as pd
from dash import dash_table, html
import dash_bootstrap_components as dbc


def create_data_table_block(
    table_id: str,
    df: pd.DataFrame = pd.DataFrame(),
    title: Optional[str] = None,
    page_size: int = 10,
    virtualization: bool = True,
) -> dbc.Card:
    """
    Creates a styled data table within a Card.

    Args:
        table_id: Unique identifier for the table.
        df: Data to display.
        title: Table title.
        page_size: Number of rows per page.

    Returns:
        dbc.Card: Data table component wrapped in a Card.
    """
    table = dash_table.DataTable(
        id={"type": "data-table", "index": table_id},
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        page_size=page_size,
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "left",
            "padding": "10px",
            "fontFamily": "inherit",
        },
        style_header={
            "backgroundColor": "#f8f9fa",
            "fontWeight": "bold",
            "border": "none",
        },
        style_data={
            "border": "none",
        },
        filter_action="native",
        sort_action="native",
        virtualization=virtualization,
    )

    return dbc.Card(
        [
            dbc.CardHeader(html.H5(title, className="mb-0")) if title else None,
            dbc.CardBody(table, className="p-0"),
        ],
        className="mb-4 shadow-sm",
    )
