# %% Code description
"""
My first app with Dash and Plotly.

Created: 16/04/2024
User: JT
Computer: On campus machine
Python v3.10
Conda environment: 
"""

# %% Python setup
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
import plotly.express as px

# %% Create data
df = pd.DataFrame(np.random.randint(low = 0, high = 100, size = (5,5)),
                  columns = ['A', 'B', 'C', 'D', 'E'],
                  index = ['I1', 'I2', 'I3', 'I4' ,'I5'])

# %% Create app
app = dash.Dash(__name__)

# %% Create graph to add to app
line_graph = px.line(data_frame = df,
                     x = df.index,
                     y = df.columns)
line_graph.show()

# %% Add graph to app
# Set up the layout using an overall div
app.layout = html.Div(
    children=[
  # Add a H1
  html.H1('Random data'),
  # Add graph
  dcc.Graph(id='line_graph', figure=line_graph)
  ])

if __name__ == '__main__':
    app.run_server(debug=True)

# %%
