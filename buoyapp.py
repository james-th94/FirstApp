#%% Code description
"""
"""
# Data science imports
import pandas as pd
import numpy as np
import plotly.express as px
# Dashboard imports
import dash
from dash import dcc, html, Input, Output, callback
# Buoy data
data_link = "https://www.data.qld.gov.au/datastore/dump/2bbef99e-9974-49b9-a316-57402b00609c?bom=True"
# Open buoy data
dfRaw = pd.read_csv(data_link)
df = dfRaw.copy(deep=True)
df = df.replace(-99.9, np.NaN)
# Subset to SEQ
SEQ_sites = ['Noosa', 'Mooloolaba', 'Caloundra', 'North Moreton Bay', 'Brisbane Mk4', 
             'Gold Coast Mk4', 'Palm Beach Mk4', 'Bilinga', 'Tweed Heads Mk4', 'Tweed Offshore', ]
df = df[df["Site"].isin(SEQ_sites)]
# Convert format to grouped (g) data for plotting
hs_bins = np.linspace(start = 0, stop = 10, num = 21)
dir_bins = np.arange(start = -11.25, stop = 380, step = 22.5)
height_ranges = pd.cut(df["Hsig"], hs_bins)
df["Mag_bin"] = [f"{i.left}-{i.right}" for i in height_ranges]
df["Dir_bin"] = pd.cut(df.Direction, dir_bins, 
                   labels = ["N1", "NNE", "NE", "ENE", 
                             "E", "ESE", "SE", "SSE", 
                             "S", "SSW", "SW", "WSW",
                             "W", "WNW", "NW", "NNW", "N2"])
df["Dir_bin"] = df["Dir_bin"].replace(["N1","N2"], "N")
df["Count"] = np.zeros(len(df))
df.index = pd.to_datetime(df["DateTime"], format = "%Y-%m-%dT%H:%M:%S")

line_plot_Hs = px.line(df,
                 x = df.index,
                 y = ['Hsig','Hmax'],
                 color = 'Site',
                 template = 'plotly_dark')
line_plot_Hs.update_layout(yaxis_title = "Height (m)",xaxis_title = "Datetime (local)")


#%% Create Dash app
app = dash.Dash()
# Write to the Dash app
app.layout = html.Div(
    children=[
        # Add a header
        html.H1(f'Qld wave data for last 7 days'),
        html.P(f'From {df.index[0]} to {df.index[-1]} (Qld local time)'),
        # Add graph
        dcc.Graph(id='Timeseries_Hs_All', figure=line_plot_Hs),
        # Give user choice for site:
        html.H2('Choose a Qld buoy:'),
        dcc.Dropdown(id = 'Site selection',
                     options = SEQ_sites,
                     value = 'Gold Coast Mk4'),
        # Plot resulting graphs from dropdown result
        dcc.Graph(id='Timeseries_Hs'),        
        dcc.Graph(id='Timeseries_Tp'),
        dcc.Graph(id='Timeseries_Dir'),
        dcc.Graph(id='Waverose', style={'width': '1280px', 'height': '1280px'}),
        ])

@callback(
    Output("Waverose", "figure"), # Output is the figure property of the Waverose dcc.Graph
    Output("Timeseries_Hs", "figure"),
    Output("Timeseries_Tp", "figure"),
    Output("Timeseries_Dir", "figure"),
    Input("Site selection", "value")
)
def update_waverose(site_value):
    # Subset data by site (chosen by user in dropdown)
    site = site_value
    df1 = df[df['Site'] == site]
    df1 = df1.sort_index()
    # Plot timeseries of data
    fig_Hs = px.line(df1,
                    x = df1.index,
                    y = ['Hsig','Hmax'],
                    template = 'plotly_dark')
    fig_Hs.update_layout(yaxis_title = "Height (m)",xaxis_title = None)
    fig_Tp = px.line(df1,
                    x = df1.index,
                    y = ['Tp','Tz'],
                    template = 'plotly_dark')
    fig_Tp.update_layout(yaxis_title = "Period (s)", xaxis_title = None)
    fig_Dir = px.line(df1,
                    x = df1.index,
                    y = ['Direction'],
                    template = 'plotly_dark')
    fig_Dir.update_layout(yaxis_title = "Direction (deg. True)", 
                          xaxis_title = "Datetime (local)",)
    # Convert to binned data for waverose plotting
    df2 = df1[["Mag_bin", "Dir_bin", "Count"]].copy(deep = True)
    g = df2.groupby(["Mag_bin", "Dir_bin"]).count()
    g.reset_index(inplace = True)
    g['Percentage (%)'] = 100*g["Count"]/g["Count"].sum()
    g['Significant wave height (m)'] = g['Mag_bin']
    g['Direction'] = g['Dir_bin']
    # Wave rose
    polar_fig = px.bar_polar(g,
                        r = "Percentage (%)",
                        theta = "Direction",
                        color = "Significant wave height (m)",
                        template="plotly_dark",
                        color_discrete_sequence= px.colors.sequential.Plasma_r,
                        )

    return polar_fig, fig_Hs, fig_Tp, fig_Dir

if __name__ == '__main__':
    app.run_server(debug=True)

# %%
