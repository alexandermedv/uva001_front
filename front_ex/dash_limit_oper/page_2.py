# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State

import pandas as pd
import os
import datetime as dt  

def create_layout(app, start_date = None, end_date=None, debug=False):  
    return None