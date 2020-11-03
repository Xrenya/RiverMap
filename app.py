import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import plotly.graph_objs as go
from random import randint

PORT = 8051


df = pd.read_csv("Kamchatka.csv", encoding='utf8')
df.fillna(value=0, inplace=True)

num_cols = [
    "Latitude", "Longitude", "Азот_нитритный",
    "Азот_аммонийный", "Азот_нитратный", "Фенол", "Нефтепродукты",
    "Органические_вещества(по ХПК)", "Железо", "Медь", "Цинк", "Марганец",
    "БПК5", "Хлориды Сульфат-ион", "Аммоний-ион", "Нитрит-ион",
    "Нитратный азот", "Фосфат-ион", "АПАВ", "Цезий-137", "Цезий-134",
    "Йод-131", "Окраска", "Запахи", "Плавающие_примеси", "Нафталину",
    "антраценуА", "Бенз(а)перену", " Фенол", "Прозрачность", "Литий",
    "Цифлутрин", "Цинерметрин", "ор_ДДТ", "Спироксамин", "Сульфаты",
    "Сероводород", "Мышьяк", "Бор", "Хлороформ", "Свинец", "Ртуть",
    "Кадмий", "Тетрахлорметан", "Энтерококков", "Стафилококки", "Фосфор"
]
chem_cols = [
    "Азот_нитритный", "Азот_аммонийный", "Азот_нитратный", "Фенол", "Нефтепродукты",
    "Органические_вещества(по ХПК)", "Железо", "Медь", "Цинк", "Марганец",
    "БПК5", "Хлориды Сульфат-ион", "Аммоний-ион", "Нитрит-ион",
    "Нитратный азот", "Фосфат-ион", "АПАВ", "Цезий-137", "Цезий-134",
    "Йод-131", "Окраска", "Запахи", "Плавающие_примеси", "Нафталину",
    "антраценуА", "Бенз(а)перену", " Фенол", "Прозрачность", "Литий",
    "Цифлутрин", "Цинерметрин", "ор_ДДТ", "Спироксамин", "Сульфаты",
    "Сероводород", "Мышьяк", "Бор", "Хлороформ", "Свинец", "Ртуть",
    "Кадмий", "Тетрахлорметан", "Энтерококков", "Стафилококки", "Фосфор"
]
cat_cols = [
    "Объект_исследования",
    "Предмет_исследований"
]
date_col = "Предмет_исследований"

df_chem = pd.DataFrame(np.max(df[chem_cols], axis=0), columns=["chemicals"])
dff = pd.DataFrame(data={"chemicals": chem_cols, "values": np.max(df[chem_cols], axis=0)})


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Associating server
server = app.server
app.title = 'Pollution map'
app.config.suppress_callback_exceptions = True

df_chem = pd.DataFrame(np.max(df[chem_cols], axis=0), columns=["chemicals"])
dff = pd.DataFrame(data={"chemicals": chem_cols, "values": np.max(df[chem_cols], axis=0)})
fig_bar = px.bar(dff, x="chemicals", y="values", labels={'chemicals':'Химикаты', "values": "Превышения (раз)"}, color="values")


app.layout = html.Div([
    html.Div([html.H4("Ecological crisis in Kamchatka"),
              html.P("Pollution level")], 
              style = {'padding' : '2px' ,
                       'backgroundColor' : '#ECEFF1'}),
    dcc.Dropdown(
        id='chemicals_dropdown',
        options=[{'label' : i, 'value' : i} for i in chem_cols],
        multi=True,
        value=['Нефтепродукты']
    ),
    dcc.Graph(id='map'),
                       
    html.Div(children='Максимальное ПДК', style={
        'textAlign': 'center'
    }),

    dcc.Graph(
        figure=fig_bar
    )
                      
])

# Step 5. Add callback functions
@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('chemicals_dropdown', 'value')])
def update_graph(value):
    fig = px.scatter_mapbox(
    data_frame=df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Объект_исследования",
    hover_data=df[value],
    color="Предмет_исследований",
    animation_frame="Период_наблюдений",
    zoom=10,
    height=600,
    width=1500,
    size=np.sum(df[value], axis=1),
    center={"lat":52.94, "lon":158.68})
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="white")
    return fig

# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug=True, port=PORT)
