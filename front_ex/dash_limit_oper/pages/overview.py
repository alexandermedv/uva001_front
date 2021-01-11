import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State

import pandas as pd
import os

import pyhdb
import datetime as dt
from datetime import datetime
import numpy as np

def create_layout(app, start_date = None, end_date=None, debug=False):  
    connection_hana = pyhdb.connect(
        host = "sap-db-s4q.sap.tc",
        port = 30115,
        user = "PGKAUDIT",
        password = "Rfh,jyfhf20"
        )
    print(connection_hana)

    return html.Div([html.H1('Page-4')])