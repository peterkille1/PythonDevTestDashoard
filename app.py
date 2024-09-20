import os
from dotenv import load_dotenv

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go

from proj_utils import readable_time, get_data

# Load environment variables
load_dotenv()

debug = False
ds = get_data(os.getenv("DATA_PATH"))

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="Windspeed Dashboard"
)

app.layout = html.Div([
    html.H1(id="windspeed-title"),
    html.Div(id="highest-windspeed"),
    html.Div(id="clicked-windspeed"),

    # Dropdown to select the time step
    html.Div([
        html.Div("Time: "),
        dcc.Dropdown(
            id="step-selector",
            options=[{
                'label': f'{readable_time(step)}',
                'value': i
            } for i, step in enumerate(ds.step.values)],
            value=0,
            style={
                'width': '30vw',
                "color": "black"
            },
        ),
        html.Br(),
        html.Br(),
        html.Div("Windspeed opacity: "),
        dcc.Dropdown(
            id="windspeed-opacity",
            options=[round(i, 2) for i in np.arange(0, 1.1, 0.1)],
            value=1,
            style={
                'width': '30vw',
                "color": "black"
            },
        ),
    ], style={"display": "inline-flex"}),

    dcc.Graph(
        id="windspeed-plot",
        style={"height": "80vh"}
    ),
])


@app.callback(
    Output("windspeed-plot", "figure"),
    Output("highest-windspeed", "children"),
    Output("windspeed-title", "children"),
    Input("step-selector", "value"),
    Input("windspeed-opacity", "value"),
)
def update_windspeed_plot(step, opacity):
    wind_speed = ds.ws
    lat = ds.latitude.values
    lon = ds.longitude.values

    ws_data = wind_speed.isel(step=step).values
    lat_flat = np.repeat(lat, len(lon))
    lon_flat = np.tile(lon, len(lat))
    ws_flat = ws_data.flatten()
    valid_mask = ~np.isnan(ws_flat)
    lat_filtered = lat_flat[valid_mask]
    lon_filtered = lon_flat[valid_mask]
    ws_filtered = ws_flat[valid_mask]

    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            lat=lat_filtered,
            lon=lon_filtered,
            mode='markers',
            marker=dict(
                size=8,
                color=ws_filtered,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Windspeed (m/s)"),
                opacity=opacity,
            ),
            text=ws_filtered
        )
    )

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            bounds=dict(
                west=-120,
                east=-20,
                south=-5,
                north=40
            ),
        ),
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
    )

    windspeed_title = (
        f"Windspeeds at {readable_time(ds.step[step].values)}"
    )

    highest_lon, highest_lat, highest_speed = sorted(
        [(lon, lat, speed) for lon, lat, speed in zip(
            lon_filtered, lat_filtered, ws_filtered
        )],
        key=lambda x: x[2]
    )[-1]

    rounded_windspeed = round(float(highest_speed), 2)

    highest_windspeed = (
        f"Highest windspeed at Lat: {highest_lat} "
        f"Lon: {highest_lon} Speed: {rounded_windspeed}"
    )

    return fig, highest_windspeed, windspeed_title


@app.callback(
    Output("clicked-windspeed", "children"),
    Input("windspeed-plot", "clickData"),
)
def clicked_windspeed(clickData):
    if not clickData:
        return "Click on graph to show location windspeed"

    data = clickData["points"][0]
    windspeed = round(data["marker.color"], 2)
    clicked_lat = data["lat"]
    clicked_lon = data["lon"]

    return (
        f"Clicked windspeed at Lat: {clicked_lat} "
        f"Lon: {clicked_lon} Speed: {windspeed}"
    )


if __name__ == '__main__':
    app.run_server(debug=debug)
