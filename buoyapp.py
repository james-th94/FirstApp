# Data science imports
import pandas as pd
import numpy as np
import plotly.express as px
# Dashboard imports
import dash
from dash import dcc, html
# Buoy data
data_link = "https://www.data.qld.gov.au/datastore/dump/2bbef99e-9974-49b9-a316-57402b00609c?bom=True"
# Open buoy data
df = pd.read_csv(data_link)
# Bin wave data
bins = np.linspace(start = 0, stop = 5, num = 11)
df["Wave_Freq"] = pd.cut(df["Hsig"], bins)
# Choose site of interest (user choice)
sites = df.Site.unique()
site = "Brisbane Mk4"
if site in sites:
    # Plot data
    polar_plot = px.bar_polar(df[df['Site'] == site],
                            r = "Wave_Freq",
                            theta = "Direction",
                            color = "Hsig",)
    # Create Dash app
    app = dash.Dash(__name__)
    # Write to the Dash app
    app.layout = html.Div(
        children=[
    # Add a header
    html.H1(f'Wave data for {site} buoy'),
    # Add graph
    dcc.Graph(id='Waverose', figure=polar_plot)
    ])
    if __name__ == '__main__':
        app.run_server(debug=True)
else:
        # Create Dash app
    app = dash.Dash(__name__)
    # Write to the Dash app
    app.layout = html.Div(
        children=[
    # Add a header
    html.H1(f'Wave data for {site} buoy'),
    # Add paragraph
    html.P('Site does not exist in data. Check site name.')
    ])
    if __name__ == '__main__':
        app.run_server(debug=True)
