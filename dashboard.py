import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import psycopg2
import pandas as pd
import plotly.express as px

# PostgreSQL Connection
def get_data():
    conn = psycopg2.connect(
        dbname="sensor_db",
        user="postgres",
        password="nmt",
        host="localhost",
        port="5433"
    )
    query = "SELECT timestamp, temperature FROM temperature_data ORDER BY timestamp DESC LIMIT 50"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Real-Time OPC-UA Temperature Monitoring"),
    
    dcc.Graph(id="temperature-graph"),
    
    dcc.Interval(
        id="interval-component",
        interval=2000,  # Update every 2 seconds
        n_intervals=0
    )
])

@app.callback(
    Output("temperature-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    df = get_data()
    fig = px.line(df, x="timestamp", y="temperature", title="Temperature Data (Last 50 Entries)")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
