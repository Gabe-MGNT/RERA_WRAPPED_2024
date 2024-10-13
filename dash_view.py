import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from PIL import Image
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize, LinearSegmentedColormap
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from PIL import Image
from matplotlib.colors import Normalize, LinearSegmentedColormap
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback


stations_rer_a_constant_dict = {
    "Achères Grand Cormier":["Achères Grand Cormier"],
    "Achères Ville" : ["Achères Ville"],
    "Auber" : ["Auber"],
    "Boissy-Saint-Léger" : ["Boissy-Saint-Léger", "Boissy-St-Léger", "Boissy", "Poissy Saint Léger"],
    "Bry-sur-Marne": ["Bry-sur-Marne"],
    "Bussy-Saint-Georges": ["Bussy-Saint-Georges", "Bussy-St-Georges"],
    "Cergy le Haut" : ["Cergy le Haut", "Cergy"],
    "Cergy Préfecture" : ["Cergy Préfecture"],
    "Cergy Saint-Christophe" : ["Cergy Saint-Christophe", "Cergy St-Christophe"],
    "Champigny": ["Champigny"],
    "Charles de Gaulle-Etoile" : ["Charles de Gaulle-Etoile"],
    "Châtelet les Halles" : ["Châtelet les Halles"],
    "Chatou-Croissy" : ["Chatou-Croissy"],
    "Conflans Fin d'Oise" : ["Conflans Fin d'Oise", "Conflans – Fin d’Oise"],
    "Fontenay-sous-Bois" : ["Fontenay-sous-Bois", "Fontenay"],
    "Gare de Lyon" : ["Gare de Lyon"],
    "Houilles-Carrières-sur-Seine" : ["Houilles-Carrières-sur-Seine", "Houilles"],
    "Joinville-le-Pont" : ["Joinville-le-Pont"],
    "La Défense" : ["La Défense", "Défense"],
    "La Varenne-Chennevières" :["La Varenne-Chennevières", "Varenne-Chennevières", "Varennes Chennevieres"],
    "Parc de Saint-Maur" : ["Parc de Saint-Maur", "Parc de St-Maur", "Parc Saint-Maur", "Parc St-Maur"],
    "Le Vésinet-Centre" : ["Le Vésinet-Centre", "Vésinet-Centre"],
    "Le Vésinet-Le Pecq" : ["Le Vésinet-Le Pecq", "Vésinet-Le Pecq"],
    "Lognes": ["Lognes"],
    "Maisons-Laffitte" : ["Maisons-Laffitte", "Maison-Laffitte", "Maisons-Laffite", "Maison-Laffite"],
    "Marne-la-Vallée-Chessy" : ["Marne-la-Vallée-Chessy", "MLV-Chessy", "Marne la Vallée", "Chessy"],
    "Nanterre Préfecture" : ['Nanterre Préfecture', "Nantere Pref", "Nanterre-P"],
    "Nanterre Université" : ["Nanterre Université"],
    "Nanterre Ville" : ["Nanterre Ville"],
    "Nation" : ["Nation"],
    "Neuilly-Plaisance" : ["Neuilly-Plaisance"],
    "Neuville Université": ["Neuville Université"],
    "Nogent-sur-Marne" : ["Nogent-sur-Marne"],
    "Noisiel" : ["Noisiel"],
    "Noisy-Champs" : ["Noisy-Champs"],
    "Noisy-le-Grand-Mont d'Est" : ["Noisy-le-Grand-Mont d'Est", "Noisy-le-Grand"],
    "Poissy" : ["Poissy"],
    "Rueil-Malmaison" : ["Rueil-Malmaison"],
    "Saint-Germain-en-Laye" : ["Saint-Germain-en-Laye", "St-Germain-En-Laye", "St Germain", "Saint Germain"],
    "Saint-Maur-Créteil" : ["Saint-Maur-Créteil", "St-Maur-Créteil"],
    "Sartrouville" : ["Sartrouville"],
    "Sucy-Bonneuil" : ["Sucy-Bonneuil"],
    "Torcy" : ["Torcy"],
    "Val d'Europe" : ["Val d'Europe"],
    "Val de Fontenay" : ["Val de Fontenay"],
    "Vincennes" : ["Vincennes"],
}


month_dict = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre"
}

max_day_per_month = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

df_f = pd.read_csv("to_exploite.csv")
pb_resolve_df = pd.read_csv("pb_resolve.csv", parse_dates=['begin_date', 'end_date'])
pb_resolve_df['duration'] = pd.to_timedelta(pb_resolve_df['duration'])

df_f['date'] = pd.to_datetime(df_f['time_posted'])

# Ajouter des colonnes pour le mois et l'année
df_f['month'] = df_f['date'].dt.month
df_f['year'] = df_f['date'].dt.year

all_types = df_f['label'].fillna('')
all_types = all_types.values

all_types_split = [a.split(',') for a in all_types]
all_types_split_flat = [item for sublist in all_types_split for item in sublist if item]
all_types_split_unique = list(set(all_types_split_flat))

gare_list = list(stations_rer_a_constant_dict.keys())

line_y_1 = 514
line_y_2 = 342
line_y_3 = 173


x_beginning = 435
x_end = 5576
x_gap_space = 132
x_gare_lyon = x_beginning+(x_gap_space*17) + 2*197

gares = [
    {"name": "Cergy le Haut", "location": [x_beginning, line_y_1], "size": 3},
    {"name": "Cergy Saint-Christophe", "location": [x_beginning+x_gap_space, line_y_1], "size": 3},
    {"name": "Cergy Préfecture", "location": [x_beginning+(x_gap_space*2), line_y_1], "size": 3},
    {"name": "Neuville Université", "location": [x_beginning+(x_gap_space*3), line_y_1], "size": 3},
    {"name": "Conflans Fin d'Oise", "location": [x_beginning+(x_gap_space*4), line_y_1], "size": 3},
    {"name": "Achères Ville", "location": [x_beginning+(x_gap_space*5), line_y_1], "size": 3},
    {"name": "Maisons-Laffitte", "location": [x_beginning+(x_gap_space*7), line_y_1], "size": 3},
    {"name": "Sartrouville", "location": [x_beginning+(x_gap_space*8), line_y_1], "size": 3},
    {"name": "Houilles-Carrières-sur-Seine", "location": [x_beginning+(x_gap_space*9), line_y_1], "size": 3},

    {"name": "Poissy", "location": [x_beginning+(x_gap_space*2), line_y_2], "size": 3},
    {"name": "Achères Grand Cormier", "location": [x_beginning+(x_gap_space*3), line_y_2], "size": 3},

    {"name": "Saint-Germain-en-Laye", "location": [x_beginning+(x_gap_space*4), line_y_3], "size": 3},
    {"name": "Le Vésinet-Le Pecq", "location": [x_beginning+(x_gap_space*5), line_y_3], "size": 3},
    {"name": "Le Vésinet-Centre", "location": [x_beginning+(x_gap_space*6), line_y_3], "size": 3},
    {"name": "Chatou-Croissy", "location": [x_beginning+(x_gap_space*7), line_y_3], "size": 3},
    {"name": "Rueil-Malmaison", "location": [x_beginning+(x_gap_space*8), line_y_3], "size": 3},
    {"name": "Nanterre Ville", "location": [x_beginning+(x_gap_space*9), line_y_3], "size": 3},
    {"name": "Nanterre Université", "location": [x_beginning+(x_gap_space*10), line_y_3], "size": 3},


    {"name": "Nanterre Préfecture", "location": [x_beginning+(x_gap_space*13), line_y_2], "size": 3},
    {"name": "La Défense", "location": [x_beginning+(x_gap_space*14), line_y_2], "size": 3},

    {"name": "Charles de Gaulle-Etoile", "location": [x_beginning+(x_gap_space*16), line_y_2], "size": 3},
    {"name": "Auber", "location": [x_beginning+(x_gap_space*17), line_y_2], "size": 3},
    {"name": "Châtelet les Halles", "location": [x_beginning+(x_gap_space*17) + 198, line_y_2], "size": 3},
    {"name": "Gare de Lyon", "location": [x_gare_lyon, line_y_2], "size": 3},
    {"name": "Nation", "location": [x_gare_lyon+(x_gap_space*1), line_y_2], "size": 3},
    {"name": "Vincennes", "location": [x_gare_lyon+(x_gap_space*2), line_y_2], "size": 3},


    {"name": "Val de Fontenay", "location": [x_gare_lyon+(x_gap_space*5), line_y_1], "size": 3},
    {"name": "Neuilly-Plaisance", "location": [x_gare_lyon+(x_gap_space*7), line_y_1], "size": 3},
    {"name": "Bry-sur-Marne", "location": [x_gare_lyon+(x_gap_space*8), line_y_1], "size": 3},
    {"name": "Noisy-le-Grand-Mont d'Est", "location": [x_gare_lyon+(x_gap_space*10), line_y_1], "size": 3},
    {"name": "Noisy-Champs", "location": [x_gare_lyon+(x_gap_space*11), line_y_1], "size": 3},
    {"name": "Noisiel", "location": [x_gare_lyon+(x_gap_space*13), line_y_1], "size": 3},
    {"name": "Lognes", "location": [x_gare_lyon+(x_gap_space*14), line_y_1], "size": 3},
    {"name": "Torcy", "location": [x_gare_lyon+(x_gap_space*15), line_y_1], "size": 3},
    {"name": "Bussy-Saint-Georges", "location": [x_gare_lyon+(x_gap_space*16), line_y_1], "size": 3},
    {"name": "Val d'Europe", "location": [x_gare_lyon+(x_gap_space*17), line_y_1], "size": 3},
    {"name": "Marne-la-Vallée-Chessy", "location": [x_gare_lyon+(x_gap_space*19), line_y_1], "size": 3},


    {"name": "Fontenay-sous-Bois", "location": [x_gare_lyon+(x_gap_space*5), line_y_3], "size": 3},
    {"name":  "Nogent-sur-Marne", "location": [x_gare_lyon+(x_gap_space*6), line_y_3], "size": 3},
    {"name": "Joinville-le-Pont", "location": [x_gare_lyon+(x_gap_space*7), line_y_3], "size": 3},
    {"name": "Saint-Maur-Créteil", "location": [x_gare_lyon+(x_gap_space*8), line_y_3], "size": 3},
    {"name": "Parc de Saint-Maur", "location": [x_gare_lyon+(x_gap_space*9), line_y_3], "size": 3},
    {"name": "Champigny", "location": [x_gare_lyon+(x_gap_space*10), line_y_3], "size": 3},
    {"name": "La Varenne-Chennevières", "location": [x_gare_lyon+(x_gap_space*11), line_y_3], "size": 3},
    {"name": "Sucy-Bonneuil", "location": [x_gare_lyon+(x_gap_space*13), line_y_3], "size": 3},
    {"name": "Boissy-Saint-Léger", "location": [x_gare_lyon+(x_gap_space*14), line_y_3], "size": 3},

]


colorscales = px.colors.named_colorscales()

# Charger l'image de la ligne de métro
image_path = 'plan_rer__a.png'
img = Image.open(image_path)
img_width, img_height = img.size


# Créer l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Obtenir les années uniques pour le slider
years = df_f['year'].unique()
years.sort()
months = df_f['month'].unique()
months.sort()

problem_types = df_f['label'].unique()


app.layout = html.Div([
    html.Div([
        html.Img(src='/assets/IDF_RER_A_logo.svg', style={'width': '12%', 'margin-right': '20px', 'margin-left':'10px'}),
        html.H1('Dashboard du RER A', style={"justifyContent": "center", "display": "flex", "alignItems": "center", "margin-bottom": "20px", "margin-top": "20px"})
    ], style={'display': 'flex', 'textAlign': 'left', 'margin-bottom': '20px', 'margin-top':'20px'}),   
    html.Div(className='separator'),
    dcc.Tabs(id="multiple_tabs", value="accueil", children=[
        dcc.Tab(label="Vue générale", 
                value='ligne_rer_a', 
                style={
                    'width': '30%', 
                    'margin': '0 10px',  # Ajouter une marge pour séparer les onglets
                    'border-radius': '10px',  # Coins arrondis
                    'border':'2px solid', 
                    "box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 15px",
                    'justifyContent': 'center'
                    }, 
                    selected_style={
                        'backgroundColor': '#E30418', 
                        'border':'2px solid', 
                        'color':'white',  
                        'width': '30%', 
                        'margin': '0 10px',  # Ajouter une marge pour séparer les onglets
                        'border-radius': '10px',  # Coins arrondis
                        "box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 15px",
                        'justifyContent': 'center'
                        }),
        dcc.Tab(label="Temps réponse à incident", 
                value='temps_reponse_incidents', 
                style={
                    'width': '30%',  
                    'border':'2px solid',
                    'margin': '0 10px',  # Ajouter une marge pour séparer les onglets
                    'border-radius': '10px',  # Coins arrondis  
                    "box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 15px",
                    'justifyContent': 'center'
                    }, 
                    selected_style={
                        'backgroundColor': '#E30418', 
                        'border':'2px solid', 
                        'color':'white',  
                        'width': '30%', 
                        'margin': '0 10px',  # Ajouter une marge pour séparer les onglets
                        'border-radius': '10px',  # Coins arrondis
                        "box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 15px",
                        'justifyContent': 'center'
                        }),
        dcc.Tab(label="Détails par gare", 
                value='details_par_gare', 
                style={
                    'width': '30%',  
                    'border':'2px solid',
                    'margin': '0 10px',  # Ajouter une marge pour séparer les onglets
                    'border-radius': '10px',  # Coins arrondis  
                    "box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 15px",
                    'justifyContent': 'center'
                    }, 
                    selected_style={
                        'backgroundColor': '#E30418', 
                        'border':'2px solid', 
                        'color':'white',  
                        'width': '30%', 
                        'margin': '0 10px',  # Ajouter une marge pour séparer les onglets
                        'border-radius': '10px',  # Coins arrondis
                        "box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 15px",
                        'justifyContent': 'center'
                        }),
    ], style={'display': 'flex', 'flex-direction':'row', 'justifyContent': 'center'}),
    html.Div(className='separator'),
    html.Div(id='tabs-content-example-graph', style={"margin-left":"10px", "margin-right":"10px"})
])

"""
app.layout = html.Div([

    html.Div([
        html.H2("Nombre d'incidents par gare", style={'textAlign': 'center'}),
        html.Label("Sélectionnez l'année :"),
        dcc.Slider(
        id='year-slider',
        min=years.min(),
        max=years.max(),
        value=years.max(),
        marks={str(year): str(year) for year in years},
        step=None
    ),
    html.Label("Sélectionnez le mois :"),
    dcc.Slider(
        id='month-slider',
        min=months.min(),
        max=months.max(),
        value=months.max(),
        marks={str(month): str(month) for month in months},
        step=None
    ),
        dcc.Graph(id='incident-graph')
    ])
])
"""

@callback(Output('tabs-content-example-graph', 'children'),Input('multiple_tabs', 'value'))
def render_content(tab):
    if tab == 'ligne_rer_a':
        return html.Div([
            html.H2("Nombre d'incidents par gare", style={'textAlign': 'center'}),

            html.Div([
            html.Label("Sélectionnez le type de problème :"),
            dcc.Dropdown(
                id='problem-dropdown',
                options=[{'label': 'Tous les problèmes', 'value': 'all'}] +[{'label': problem.capitalize(), 'value': problem} for problem in all_types_split_unique],
                value=['all'],  # Sélectionner tous les types par défaut
                multi=True,
                style={'width': '98%',},
            ),
            ], style={'margin-left':'auto', 'margin-right':'auto', 'border': '1px solid #ccc', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '20px', 'width': '95%'}),
            dcc.Graph(id='incident-graph', config={"displayModeBar": False}),
            html.Div([
                html.Label("Sélectionnez l'année :"),
                dcc.Slider(
                id='year-slider',
                min=years.min(),
                max=years.max(),
                value=years.max(),
                marks={str(year): str(year) for year in years},
                step=None,
                className='custom-slider'
            ),
            html.Label("Sélectionnez le mois :"),
            dcc.RangeSlider(
                id='month-slider',
                min=months.min(),
                max=months.max(),
                value=[months.min(), months.max()],
                marks={str(month): month_dict[month] for month in months},
                step=None,
                className='custom-range-slider'
            ),
            html.Div(className='separator'),
            html.H2("Nombre d'incidents par typologie sélectionnées", style={'textAlign': 'center'}),
            html.Div([ 
            html.Label("Sélectionnez le type de tri :", style={'display': 'block', 'textAlign': 'center', 'marginBottom': '10px'}),
            dcc.RadioItems(
                        id='sort_type1',
                        options=[
                            {'label': 'Non triés', 'value': 'no_sort'},
                            {'label': 'Croissant', 'value': 'asc_sort'},
                            {'label': 'Décroissant', 'value': 'desc_sort'},

                        ],
                        value='no_sort',
                        labelStyle={'display': 'inline-block', 'marginRight': '20px'}  # Espacer les boutons radio
                    ),
            ], style={'margin-left':'auto', 'margin-right':'auto', 'border': '1px solid #ccc', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '20px', 'width': '60%'}),
            dcc.Graph(id='incident-bar', config={"displayModeBar": False})
            ])
        ])
    elif tab == 'temps_reponse_incidents':
        return html.Div([
            html.H1("Temps de réponse aux incidents", style={'textAlign': 'center'}),
            html.Label("Sélectionnez le type d'incident :"),
            dcc.Dropdown(
                id='incident-type-dropdown',
                options=[{'label': html.Span(
                    [
                        html.Span(problem.capitalize(), className='dropdown-item')
                    ], style={}), 'value': problem} for problem in all_types_split_unique],
                value=all_types_split_unique,  # Sélectionner le premier type par défaut
                multi=True,
                optionHeight=50,
                placeholder="Sélectionnez un type d'incident",
                searchable=True,
            ),
            html.Div([
            html.Div(id='average-response-time'),
                ], style={'margin-top':'40px', 'margin-left':'auto', 'margin-right':'auto', 'border': '5px solid black', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '20px', 'width': '100%'
                          }),
            html.Div(className='separator'),
            html.H1("Vue complète", style={'textAlign': 'center'}),

                html.Div([
                    html.Label("Sélectionnez le type de graphique :", style={'display': 'block', 'textAlign': 'center', 'marginBottom': '10px'}),
                    dcc.RadioItems(
                        id='graph-type',
                        options=[
                            {'label': 'Simplifié', 'value': 'bar'},
                            {'label': 'Détaillé', 'value': 'box'}
                        ],
                        value='bar',
                        labelStyle={'display': 'inline-block', 'marginRight': '20px'}  # Espacer les boutons radio
                    )
                ], style={'margin-left':'auto', 'margin-right':'auto', 'border': '1px solid #ccc', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '20px', 'width': '50%'}),

                dcc.Graph(id='time_solve_graph', config={"displayModeBar": False}),
                dcc.RangeSlider(
                    id='month-slider_time',
                    min=months.min(),
                    max=months.max(),
                    value=[months.min(), months.max()],
                    marks={str(month): month_dict[month] for month in months},
                    step=None,
                    className='custom-range-slider'
                ),
                dcc.Slider(
                id='year-slider_time',
                min=years.min(),
                max=years.max(),
                value=years.max(),
                marks={str(year): str(year) for year in years},
                step=None,
                className='custom-slider'
                ),

                html.Div(className='separator'),
                html.H1("Problèmes les plus courants", style={'textAlign': 'center'}),
                dcc.Graph(id='incidents_occurences', config={"displayModeBar": False}),
                dcc.RangeSlider(
                    id='month-slider_time_occurences',
                    min=months.min(),
                    max=months.max(),
                    value=[months.min(), months.max()],
                    marks={str(month): month_dict[month] for month in months},
                    step=None,
                    className='custom-range-slider'

                ),
                dcc.Slider(
                id='year-slider_time_occurences',
                min=years.min(),
                max=years.max(),
                value=years.max(),
                marks={str(year): str(year) for year in years},
                step=None,
                className='custom-slider'
                ),

                html.Div(className='separator'),
                html.H1("Par typologie spécifique", style={'textAlign': 'center'}),

                html.Div([
                    html.Label("Sélectionnez la typologie d'incidents", style={'display': 'block', 'textAlign': 'center', 'marginBottom': '10px'}),
                    dcc.Dropdown(
                    id='typology-dropdown-1',
                    options=[{'label': typology.upper(), 'value': typology} for typology in all_types_split_unique],
                    value=all_types_split_unique[0],  # Valeur par défaut
                    style={'width': '100%', 'display': 'inline-block', 'marginRight': '4%'}
                    ),
                ], style={'margin-left':'auto', 'margin-right':'auto', 'border': '1px solid #ccc', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '20px', 'width': '80%'}),


                dcc.Graph(id='incidents_details', config={"displayModeBar": False}),
                dcc.RangeSlider(
                    id='month-slider_time_incidents_details',
                    min=months.min(),
                    max=months.max(),
                    value=[months.min(), months.max()],
                    marks={str(month): month_dict[month] for month in months},
                    step=None,
                    className='custom-range-slider'
                ),
                dcc.Slider(
                id='year-slider_time_incidents_details',
                min=years.min(),
                max=years.max(),
                value=years.max(),
                marks={str(year): str(year) for year in years},
                step=None,
                className='custom-slider'
                ),


                                            
                   
        ])
    elif tab == 'details_par_gare':
        return html.Div([  
            html.H1("Sélectionnez une gare"),
            dcc.Dropdown(
                id='gare-dropdown_details_gare',
                options=[{'label': gare, 'value': gare} for gare in df_f['gare_source'].dropna().unique()],
                multi=False,
                value='Poissy',
                placeholder="Sélectionnez une ou plusieurs gares",
                style={'width': '90%', 'margin': 'auto'}
            ),
            dcc.Slider(
                id='year-dropdown_gare',
                min=years.min(),
                max=years.max(),
                value=years.max(),
                marks={str(year): str(year) for year in years},
                step=None
            ),
            dcc.RangeSlider(
                id='month-dropdown_gare',
                    min=months.min(),
                    max=months.max(),
                    value=[months.min(), months.max()],
                    marks={str(month): month_dict[month] for month in months},
                    step=None,
                    className='custom-range-slider'
            ),
            html.Div(id='incident-info'),
            html.Div([
                html.Div(dcc.Graph(id='pie-chart_gare'), style={'width': '48%', 'display': 'inline-block'}),
                html.Div(dcc.Graph(id='incident-graph_details_gare'), style={'width': '48%', 'display': 'inline-block'})
            ]),

        ])
        
        

    """
    elif tab == 'details_par_gare':
        return html.Div([
            html.H1("Détails des incidents par gare", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='gare-dropdown',
                options=[{'label': gare, 'value': gare} for gare in df_f['gare_source'].dropna().unique()],
                multi=True,
                value=['Poissy'],
                placeholder="Sélectionnez une ou plusieurs gares",
                style={'width': '90%', 'margin': 'auto'}
            ),
            
            dcc.Graph(id='details_gare_graph'),
            dcc.Slider(
                    id='year-slider',
                    min=years.min(),
                    max=years.max(),
                    value=years.max(),
                    marks={str(year): str(year) for year in years},
                    step=None,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            dcc.RangeSlider(
                    id='month-slider',
                    min=months.min(),
                    max=months.max(),
                    value=[months.min(), months.max()],
                    marks={str(month): month_dict[month] for month in months},
                    step=None
                ),
            html.Div(style={'height': '5px', 'backgroundColor': 'red', 'marginTop':'20px', 'marginBottom': '20px', 'width':'80%', 'marginLeft': 'auto', 'marginRight': 'auto', 'borderRadius': '25px'}), 
            
            html.H1("Typologie des problèmes", style={'textAlign': 'center'}),

            html.Div([
            html.Label("Sélectionnez le type de valeur à afficher :", style={'display': 'block', 'textAlign': 'center', 'marginBottom': '10px'}),
            dcc.RadioItems(
                        id='val_type',
                        options=[
                            {'label': 'Toutes les typologies', 'value': 'all_val'},
                            {'label': 'Typologies non vides', 'value': 'non_empty_val'}
                        ],
                        value='all_val',
                        labelStyle={'display': 'inline-block', 'marginRight': '20px'}  # Espacer les boutons radio
                    ),
            html.Div(style={'height': '2px', 'backgroundColor': 'grey', 'marginTop':'10px', 'marginBottom': '10px', 'width':'30%', 'marginLeft': 'auto', 'marginRight': 'auto', 'borderRadius': '25px'}), 
            html.Label("Sélectionnez le type de tri :", style={'display': 'block', 'textAlign': 'center', 'marginBottom': '10px'}),
            dcc.RadioItems(
                        id='sort_type',
                        options=[
                            {'label': 'Non triés', 'value': 'no_sort'},
                            {'label': 'Croissant', 'value': 'asc_sort'},
                            {'label': 'Décroissant', 'value': 'desc_sort'},

                        ],
                        value='no_sort',
                        labelStyle={'display': 'inline-block', 'marginRight': '20px'}  # Espacer les boutons radio
                    ),
            ], style={'margin-left':'auto', 'margin-right':'auto', 'border': '1px solid #ccc', 'padding': '10px', 'borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '20px', 'width': '60%'}),
            dcc.Graph(id='details_problem_gare_graph'),
        ])
        """
        

@app.callback(
    [Output('incident-graph', 'figure'),
    Output('incident-bar', 'figure'),],

    [Input('year-slider', 'value'),
     Input('month-slider', 'value'),
     Input('problem-dropdown', 'value'),
        Input('sort_type1', 'value')]
     
)
def update_figure(selected_year, selected_month, selected_problems, sort_type):

    if selected_problems == ['all']:
        selected_problems = all_types_split_unique

    # Filtrer les données en fonction de l'année sélectionnée
    filtered_df = df_f[(df_f['year'] == selected_year) 
                       & (df_f['month'] >= selected_month[0]) 
                       & (df_f['month'] <= selected_month[1])
                       & (df_f['label'].str.contains('|'.join(selected_problems)))
                       ]

    filtered_df2 = filtered_df[(filtered_df['tweet_type'] == 'Normal') & (filtered_df['len_label'] > 0)]


    # Agréger les données pour obtenir le nombre d'incidents par gare
    agg_data = filtered_df2.groupby('gare_source').size().reset_index(name='count')

    # Agréger les données pour obtenir le nombre d'incidents par gare
    full_data = pd.DataFrame(gares)
    full_data[['x', 'y']] = pd.DataFrame(full_data['location'].tolist(), index=full_data.index)

    full_data = full_data.merge(agg_data, left_on='name', right_on='gare_source', how='left', )
    full_data['count'] = full_data['count'].fillna(0)
    full_data['year'] = selected_year  # Ajouter l'année sélectionnée au DataFrame
    full_data['month_begin'] = selected_month[0]  # Ajouter l'année sélectionnée au DataFrame
    full_data['month_end'] = selected_month[1]  # Ajouter l'année sélectionnée au DataFrame
    full_data['min_date'] = filtered_df['date'].min().strftime('%Y-%m-%d')
    full_data['max_date'] = filtered_df['date'].max().strftime('%Y-%m-%d')

    scatter_fig = px.scatter(
        full_data, 
        x='x', 
        y='y', 
        size='count', 
        color='count', 
        color_continuous_scale="matter", 
        opacity=1, 
        size_max=13,       
        hover_name='name',
        custom_data=['name', 'count', 'year', 'month_begin', 'month_end', 'min_date', 'max_date']
        )
    
    scatter_fig.update_layout(
        hovermode='closest',
        margin=dict(l=0, r=0, b=0, t=0), # Ajuster les marges pour réduire les bordures
        paper_bgcolor='white',  # Fond du papier en blanc
        plot_bgcolor='white',
        hoverlabel= dict(
            font=dict(
                family="ParisineBold",
                size=12,
                color="#284897",
            ),
            bgcolor="white",


        ),)
    scatter_fig.update_traces(
        #hovertemplate="<i>Date</i>: %{customdata[2]}/%{customdata[3]} au %{customdata[2]}/%{customdata[4]} <br>"+"<i>Gare</i>: %{customdata[0]}<br>"+"<i>Nombre d'incidents</i>: %{customdata[1]}",
        hovertemplate="<i>Date</i>: %{customdata[5]} au %{customdata[6]} <br>"+"<i>Gare</i>: %{customdata[0]}<br>"+"<i>Nombre d'incidents</i>: %{customdata[1]}",

    )

    scatter_fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=img_height,
            sizex=img_width,
            sizey=img_height,
            sizing="stretch",
            opacity=1,
            layer="below"
        )
    )


    
    # Ajuster les limites de l'axe pour correspondre à l'image
    scatter_fig.update_xaxes(visible=False, )
    scatter_fig.update_yaxes(visible=False, scaleanchor="x")

    scatter_fig.update_layout(
        coloraxis_colorbar=dict(
            title="Nombre d'incidents",
            thicknessmode="pixels",
            lenmode="pixels", 
            len=200,
            yanchor="top", 
            y=0.8,
            ticks="outside", 
            )
        )


    # Grouper par gare pour obtenir le nombre d'incidents par gare
    bar_data = filtered_df2.groupby(['gare_source']).size().reset_index(name='count')

    # Trier les données en fonction de l'option sélectionnée
    if sort_type == 'asc_sort':
        bar_data = bar_data.sort_values(by='count', ascending=True)
    elif sort_type == 'desc_sort':
        bar_data = bar_data.sort_values(by='count', ascending=False)
    

        # Créer la figure du bar chart
    bar_fig = px.bar(
        bar_data,
        x='gare_source',
        y='count',
        color='count',
        color_continuous_scale="matter", 
        opacity=1, 
        hover_name='gare_source',
        custom_data=['gare_source', 'count']

    )

    bar_fig.update_traces(
        hovertemplate="<i>Gare</i>: %{customdata[0]}<br>"+"<i>Nombre d'incidents</i>: %{customdata[1]}",
    )

    bar_fig.update_layout(
        xaxis=dict(title=''),
        margin=dict(l=0, r=0, b=20), # Ajuster les marges pour réduire les bordures
        
        barmode='stack',
        #xaxis={
        #    'categoryorder': 'total descending',
        #    'title': 'Gares concernés',
        #    'tickfont': {
        #        'family': 'ParisineBold',
        #        'size': 12,
        #        'color': '#284897'
        #    }
        #},
        
        bargap=0.2,
        yaxis_title='',
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='closest',
        hoverlabel= dict(
            font=dict(
                family="ParisineBold",
                size=12,
                color="#284897",
            ),
            bgcolor="white",


        ),
        coloraxis_colorbar=dict(
            title="Nombre d'incidents",
            thicknessmode="pixels",
            lenmode="pixels", 
            len=200,
            yanchor="top", 
            y=0.95,
            ticks="outside", 
            ),
    )



    return scatter_fig, bar_fig


from datetime import datetime

@app.callback(
    Output('average-response-time', 'children'),
    [Input('incident-type-dropdown', 'value')]
)
def update_figure(selected_incident_type):

    if selected_incident_type == 'all':
        selected_incident_type = all_types_split_unique

    pb_resolve_df_filtered = pb_resolve_df[pb_resolve_df['label'].str.contains('|'.join(selected_incident_type))]

    average_duration = pb_resolve_df_filtered['duration'].mean()  

    average_day = average_duration.days
    average_hour = average_duration.seconds//3600
    average_minute = (average_duration.seconds//60)%60

    current_time = datetime.now().strftime("%H:%M")

    incident_divs = []
    for incident in selected_incident_type:
        incident_df = pb_resolve_df_filtered[pb_resolve_df_filtered['label'].str.contains(incident)]
        incident_average_duration = incident_df['duration'].mean()
        incident_average_day = incident_average_duration.days
        incident_average_hour = incident_average_duration.seconds // 3600
        incident_average_minute = (incident_average_duration.seconds // 60) % 60

        incident_divs.append(                    
            html.Div(style={'height': '3px', 'backgroundColor': '#BCBCBC', 'width': '100%'}),
        )
        incident_divs.append(

            html.Div([
                    html.H3(f"• Temps moyen ({incident})", style={'textAlign': 'left', 'padding':'1%', 'marginLeft':'5%'}),
                    html.Div([
                        html.H3(f"{incident_average_day} jours, {incident_average_hour} heures, {incident_average_minute} minutes", style={'color': 'yellow', 'textAlign': 'center', 'marginLeft': 'auto'})
                    ], style={'backgroundColor': '#4D4D4D', 'padding': '10px', 'marginLeft': 'auto', 'width': '40%', 'display': 'flex', 'alignItems': 'center'})
                ], style={'display': 'flex', 'width': '100%', 'textAlign': 'center', 'justifyContent': 'center'}),
        )

    return html.Div([
            html.Div([
                html.Div([
                    html.Img(src='/assets/IDF_RER_A_logo.svg', style={'width': '15%', 'float': 'left'}),
                    html.H1("Temps de réponses à incidents", style={'marginLeft': '20px', 'marginTop': '0px'}),
                    html.Div(current_time, style={'backgroundColor': 'black', 'color': 'yellow', 'fontSize':'2em','padding': '5px 10px', 'marginLeft': 'auto', 'marginRight':'5%', 'display': 'inline-block'})

                ], style={'display': 'flex', 'alignItems': 'center', 'width': '100%'})
            ], style={'overflow': 'hidden'}),
            html.Div(style={'height': '5px', 'backgroundColor': 'red', 'marginTop': '10px', 'width':'100%'}),
            html.Div([
                html.Div([
                    html.H3(f"Temps moyen (total)", style={'textAlign': 'left', 'marginLeft':'1%', 'padding':'1%'}),
                    html.Div([
                        html.H3(f"{average_day} jours, {average_hour} heures, {average_minute} minutes", style={'color': 'yellow', 'textAlign': 'center', 'marginLeft': 'auto'})
                    ], style={'backgroundColor': '#4D4D4D', 'padding': '10px', 'marginLeft': 'auto', 'width': '40%', 'display': 'flex', 'alignItems': 'center'})
                ], style={'display': 'flex', 'width': '100%'}),
                *incident_divs
            ], style={'height':'300px', 'overflow': 'auto'}),


            ], style={"marginTop":'50px'},)

@app.callback(
    Output('incidents_occurences', 'figure'),
    [Input('year-slider_time_occurences', 'value'),
    Input('month-slider_time_occurences', 'value')]
)
def update_graph(selected_year, selected_months):
    begin_date_selected = "{:04d}-{:02d}-01".format(selected_year, selected_months[0])
    end_date_selected = "{:04d}-{:02d}-{}".format(selected_year, selected_months[1], max_day_per_month[selected_months[1]])

    filtered_df = pb_resolve_df[(pb_resolve_df['begin_date'] >= begin_date_selected) & (pb_resolve_df['begin_date'] <= end_date_selected)]

    filtered_df['month'] = filtered_df.begin_date.dt.month
    filtered_df['year'] = filtered_df.begin_date.dt.year

    problem_counts = filtered_df.groupby('label').size().reset_index(name='count')
    problem_counts = problem_counts.sort_values(by='count', ascending=False)
    problem_counts['percentage'] = (problem_counts['count'] / problem_counts['count'].sum()) * 100
    
    incidents_occurences = px.bar(
    problem_counts,
    x='label', 
    y='percentage', 
    labels={'label': 'Type d\'incident', 'percentage': 'Pourcentage'},
    )
    incidents_occurences.update_traces(texttemplate='%{y:.2f}%', textposition='inside')

    incidents_occurences.update_layout(
    plot_bgcolor='white',  # Fond blanc
    showlegend=False,  # Retirer la légende
    margin=dict(t=0, l=0, r=0),
    )

    return incidents_occurences



@app.callback(
    Output('time_solve_graph', 'figure'),
    [Input('month-slider_time', 'value'),
    Input('year-slider_time', 'value'),
    Input('graph-type', 'value')]

)
def update_graph(selected_months, selected_year, graph_type):

    begin_date_selected = "{:04d}-{:02d}-01".format(selected_year, selected_months[0])
    end_date_selected = "{:04d}-{:02d}-{}".format(selected_year, selected_months[1], max_day_per_month[selected_months[1]])

    filtered_df = pb_resolve_df[(pb_resolve_df['begin_date'] >= begin_date_selected) & (pb_resolve_df['begin_date'] <= end_date_selected)]

    filtered_df['month'] = filtered_df.begin_date.dt.month
    filtered_df['year'] = filtered_df.begin_date.dt.year

    problem_counts = filtered_df.groupby('month').size().reset_index(name='count')
    avg_resolution_time = filtered_df.groupby('month')['duration'].mean().reset_index(name='avg_duration')
    avg_resolution_time['avg_duration_hours'] = avg_resolution_time['avg_duration'].dt.total_seconds() // 3600
    avg_resolution_time['avg_duration_minutes'] = (avg_resolution_time['avg_duration'].dt.total_seconds() % 3600) // 60
    avg_resolution_time['avg_duration_str'] = avg_resolution_time.apply(lambda row: f"{int(row['avg_duration_hours'])}h {int(row['avg_duration_minutes'])}m", axis=1)


    fig = go.Figure()

    if graph_type == 'bar':
        # Ajouter le nombre de problèmes par mois
        fig.add_trace(go.Bar(
            x=problem_counts['month'], 
            y=problem_counts['count'], 
            name='Nombre de problèmes', 
            yaxis='y1',
            marker_color='#284897',
            hovertemplate='Mois: %{x}<br>Nombre de problèmes: %{y}<extra></extra>'
            ))
        
            # Ajouter le temps de résolution moyen par mois
        fig.add_trace(go.Scatter(
            x=avg_resolution_time['month'], 
            y=avg_resolution_time['avg_duration'].dt.total_seconds() / 3600, 
            yaxis='y2', 
            mode='lines+markers', 
            text=avg_resolution_time['avg_duration_str'], 
            line=dict(color='red', width=4),
            marker=dict(size=10),
            hovertemplate='Mois: %{x}<br>Temps de résolution moyen: %{text}<extra></extra>'
            ))
    
        # Mettre à jour la mise en page pour avoir deux axes y
        fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=months, ticktext=[month_dict[month] for month in months], tickfont=dict(size=14, family='ParisineBold', color='#284897')),
            yaxis=dict(title='Nombre de problèmes', side='left', color='#284897',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='#284897')),
            yaxis2=dict(title='Temps de résolution moyen (jours)', overlaying='y', side='right', color='red',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='red')),
            plot_bgcolor='white',  # Fond blanc
            showlegend=False,  # Retirer la légende
            margin=dict(t=0),
        )
    elif graph_type == 'box':
        # Ajouter les boxplots pour le nombre de problèmes par mois
        fig.add_trace(go.Box(
            x=filtered_df['month'], 
            y=filtered_df['duration'].dt.total_seconds() / 3600, 
            name='Temps de résolution (heures)', 
            yaxis='y1',
            marker_color='#284897',
            hovertemplate='Mois: %{x}<br>Temps de résolution: %{y:.2f} heures<extra></extra>'
        ))

        fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=months, ticktext=[month_dict[month] for month in months],  tickfont=dict(size=14, family='ParisineBold', color='#284897')),
            yaxis=dict(title='Temps de résolution des problèmes', side='left', color='#284897',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='#284897')),
            yaxis2=dict(title='Temps de résolution moyen (jours)', overlaying='y', side='right', color='red',  ticks='outside'),
            plot_bgcolor='white',  # Fond blanc
            showlegend=False,
            margin=dict(t=0),
        )
    
    
    
    return fig


@app.callback(
    Output('incidents_details', 'figure'),
    [Input('typology-dropdown-1', 'value'),
    Input('month-slider_time_incidents_details', 'value'),
    Input('year-slider_time_incidents_details', 'value')]
)
def update_graph(typo1, selected_months, selected_year):
    begin_date_selected = "{:04d}-{:02d}-01".format(selected_year, selected_months[0])
    end_date_selected = "{:04d}-{:02d}-{}".format(selected_year, selected_months[1], max_day_per_month[selected_months[1]])

    filtered_df = pb_resolve_df[
        (pb_resolve_df['begin_date'] >= begin_date_selected) & 
        (pb_resolve_df['begin_date'] <= end_date_selected) & 
        (pb_resolve_df['label'].str.contains(typo1))
    ]

    filtered_df['month'] = filtered_df.begin_date.dt.month
    filtered_df['year'] = filtered_df.begin_date.dt.year

    # Grouper par typologie et par mois pour obtenir le nombre de problèmes et le temps de réponse moyen
    grouped_df = filtered_df.groupby(['label', 'month']).agg({
        'label': 'count',
        'duration': 'mean'
    }).rename(columns={'label': 'count', 'duration': 'response_time'}).reset_index()

    fig = go.Figure()

        

    # Ajouter les barres pour le nombre de problèmes par typologie et par mois
    df_typology = grouped_df[grouped_df['label'] == typo1]
    fig.add_trace(go.Bar(
        x=df_typology['month'],
        y=df_typology['count'],
        name=f'Nombre de problèmes ({typo1})',
        marker_color='#284897',
        yaxis='y1',
        hovertemplate='Mois: %{x}<br>Nombre de problèmes: %{y}<extra></extra>'
    ))


    # Ajouter les lignes pour le temps de réponse moyen par typologie et par mois
    fig.add_trace(go.Scatter(
        x=df_typology['month'],
        y=df_typology['response_time'].dt.total_seconds() / 60,
        name=f'Temps de réponse moyen ({typo1})',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='red', width=4),  # Ajouter une largeur de ligne plus grande pour inclure le contour
        marker=dict(size=10),
        hovertemplate='Mois: %{x}<br>Temps de réponse moyen: %{y:.2f} minutes<extra></extra>'
    ))

    # Mettre à jour la mise en page pour ajouter un axe y secondaire
    fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=months, ticktext=[month_dict[month] for month in months], tickfont=dict(size=14, family='ParisineBold', color='#284897')),
            yaxis=dict(title='Nombre de problèmes', side='left', color='#284897',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='#284897')),
            yaxis2=dict(title='Temps de résolution moyen (jours)', overlaying='y', side='right', color='red',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='red')),
            plot_bgcolor='white',  # Fond blanc
            showlegend=False,  # Retirer la légende
            margin=dict(t=0),
    )

    return fig


"""
@app.callback(
    [Output('details_gare_graph', 'figure'),
     Output('details_problem_gare_graph', 'figure') 
     ],
    [Input('gare-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-slider', 'value'),
     Input('val_type', 'value'),
     Input('sort_type', 'value')
     ]
)
def update_graphs(selected_gares, selected_year, selected_month, val_type, sort_type):

    begin_date_selected = "{:04d}-{:02d}-01".format(selected_year, selected_month[0])
    end_date_selected = "{:04d}-{:02d}-{}".format(selected_year, selected_month[1], max_day_per_month[selected_month[1]])

    if selected_gares is None:
        selected_gares = df_f['gare_source'].dropna().unique().tolist()

    filtered_df = df_f[(df_f['year'] == selected_year) 
                       & (df_f['month'] >= selected_month[0]) 
                       & (df_f['month'] <= selected_month[1])
                       & (df_f['gare_source'].str.contains('|'.join(selected_gares)))
                       & (df_f['label'].str.contains('|'.join(all_types_split_unique)))
                       ]

    filtered_df2 = filtered_df[(filtered_df['tweet_type'] == 'Normal') & (filtered_df['len_label'] > 0)]

    if selected_gares:
        filtered_df = filtered_df[filtered_df['gare_source'].isin(selected_gares)]

    # Grouper par gare et mois pour obtenir le nombre d'incidents par mois pour chaque gare
    count_problem_by_gare_month = filtered_df.groupby(['gare_source', 'month']).size().reset_index(name='count')
    count_problem_by_gare_month['month_name'] = count_problem_by_gare_month['month'].apply(lambda x: month_dict[x])

    # Créer un graphique en barres empilées
    bar_fig = px.bar(
        count_problem_by_gare_month, 
        x='month_name', 
        y='count', 
        color='gare_source', 
        barmode='group',  # Utiliser 'overlay' pour superposer les barres
        labels={'month_name': 'Mois', 'count': "Nombre d'incidents", 'gare_source': 'Gare'}
    )

    for trace in bar_fig.data:
        trace.update(opacity=1)

    bar_fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    first_gare = selected_gares[0]
    filtered_df_first_gare = filtered_df[filtered_df['gare_source'] == first_gare]

    data_splitted = {}
    for incident in all_types_split_unique:
        incident_occured = filtered_df_first_gare[filtered_df_first_gare['label'].str.contains(incident)]

        if val_type == 'non_empty_val' and incident_occured.shape[0] == 0:
            continue
        data_splitted[incident] = incident_occured.shape[0]

    data_splitted_df = pd.DataFrame(data_splitted.items(), columns=['label', 'count'])


    if sort_type == 'asc_sort':
        data_splitted_df = data_splitted_df.sort_values(by='count', ascending=True)
    elif sort_type == 'desc_sort':
        data_splitted_df = data_splitted_df.sort_values(by='count', ascending=False)
    
    data_splitted_df['label'] = data_splitted_df['label'].apply(lambda x: x.capitalize())
    # Créer un graphique en barres pour afficher les problèmes selon leur label
    label_fig = px.bar(
        data_splitted_df, 
        x='label', 
        y='count', 
        color='count',
        color_continuous_scale="matter", 
        title=f"Gare : {first_gare} (entre le {begin_date_selected} et {end_date_selected})",
        labels={'label': "Type d'indicent", 'count': "Nombre d'incidents"}
    )
    
    # Définir les marges à zéro et le fond blanc
    label_fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False,
    )



    
    return [bar_fig, label_fig]
"""

@app.callback(
    [Output('incident-info', 'children'),
     Output('pie-chart_gare', 'figure'),
     Output('incident-graph_details_gare', 'figure')],
    [Input('gare-dropdown_details_gare', 'value'),
     Input('year-dropdown_gare', 'value'),
     Input('month-dropdown_gare', 'value')]
)
def update_incident_info(selected_gare, selected_year, selected_months):

    begin_date_selected = "{:04d}-{:02d}-01".format(selected_year, selected_months[0])
    end_date_selected = "{:04d}-{:02d}-{}".format(selected_year, selected_months[1], max_day_per_month[selected_months[1]])

    filtered_df = pb_resolve_df[
        (pb_resolve_df['begin_date'] >= begin_date_selected) & 
        (pb_resolve_df['begin_date'] <= end_date_selected)
    ]
    filtered_df['month'] = filtered_df.begin_date.dt.month
    filtered_df['year'] = filtered_df.begin_date.dt.year

    # Filtrer les données pour la gare sélectionnée
    selected_gare_data = filtered_df[filtered_df['gare_source'] == selected_gare]
    num_incidents = selected_gare_data.shape[0]

    # Calculer le classement de la gare
    df_sorted = filtered_df.groupby('gare_source').size().reset_index(name='count').sort_values(by='count', ascending=False).reset_index(drop=True)
    rank = df_sorted[df_sorted['gare_source'] == selected_gare].index[0] + 1

    # Grouper les données par année et mois pour la gare sélectionnée
    time_grouped = selected_gare_data.groupby(['year', 'month']).size().reset_index(name='count')

    # Créer le texte d'information
    info_text = f"La gare {selected_gare} a {num_incidents} incidents et est classée {rank}ème parmi les {df_sorted.shape[0]}gares, ayant eu des incidents sur la période allant de {begin_date_selected} à {end_date_selected}."

    pie_data = selected_gare_data.groupby('label').size().reset_index(name='incidents')
    # Créer un graphique en lignes pour afficher le nombre d'incidents chronologiquement
    fig = px.line(time_grouped, 
                x=pd.to_datetime(time_grouped[['year', 'month']].assign(day=1)), 
                y='count', 
                title=f"Nombre d'incidents chronologiquement pour la gare {selected_gare}",
                labels={'x': 'Date', 'count': "Nombre d'incidents"})
    fig.update_layout(plot_bgcolor='white')

    pie_fig = px.pie(
        pie_data, 
        names='label',
        values='incidents', title=f"Proportion des problèmes pour la gare {selected_gare}")
    
    pie_fig.update_traces(textinfo='label+percent', textposition='inside')
    pie_fig.update_layout(showlegend=False)

    return info_text, fig, pie_fig

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True, host='127.0.0.1', port=5000)





