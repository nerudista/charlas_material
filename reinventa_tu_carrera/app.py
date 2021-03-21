import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_alternative_viz as dav
import flask

from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

import pandas as pd

from plotly.tools import mpl_to_plotly
import matplotlib.pyplot as plt
from pywaffle import Waffle


server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.config.suppress_callback_exceptions = True

print("Starting again")

df = pd.read_csv("./historia.csv",
parse_dates=['Fecha'])

#print (df)


df['DiaNombre']= pd.to_datetime(df['Fecha']).dt.day_name()
df['Año'] = df['Fecha'].dt.year
df['DiaNumero'] = df['Fecha'].dt.dayofweek
df['Semana'] = df['Fecha'].dt.isocalendar().week


#print(df)

#print(df["Dia_Semana"].unique())


fig_heat = px.density_heatmap(
    df,
    x="DiaNombre",
    y="Semana",
    z="TipoCodigo",
    facet_col="Año",
    hover_name="Fecha",
    hover_data=["Hito", "Tipo"],
    
    #labels=dict(x="Day of Week", y="Semana", color="Tipo"),
)


fig_vega = alt.Chart(df).mark_rect().encode(
    x='DiaNombre:N',
    y='Semana:O',
    color='TipoCodigo:N'
)


def altair_fig():
    return ( alt.Chart(df).mark_rect()
        .encode(
            alt.X("DiaNombre:N",
            sort=['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday','Sunday']),
            alt.Y("Semana:O"),
            color="TipoCodigo:N",
            order=alt.Order("Semana", sort="descending"),
            tooltip=["Fecha","Hito"],
            facet=alt.Facet('Año:N', columns=8)
        )
        .properties(title="Mi carrera"
        ).interactive().to_dict() )
###


spec=altair_fig()


### plotly figure

go_heat = go.Figure(data=go.Heatmap(
                   z=df['TipoCodigo'],
                    x=df['DiaNombre'],
                   y=df['Semana'],
                   colorbar={'bordercolor':'#ffFF00'},
                   xgap=0.3,
                   hoverongaps = False),
                   )

### layout
app.layout = html.Div(
    children=[
        html.Div(children=""""""),
        html.H1(children="""Reinventa tu carrera con Python"""),
        html.H2(children="Python Panama"),        
        dcc.Graph(figure= go_heat),
        dcc.Graph(figure= fig_heat),
        html.Div([dav.VegaLite(id="vega",spec=spec)])
    ]
)




if __name__ == "__main__":
    import os

   # debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    app.run_server(host="0.0.0.0", port=8030, debug=True)