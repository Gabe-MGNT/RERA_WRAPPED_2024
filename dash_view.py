import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
from constant import month_dict, max_day_per_month, gares, gare_list
from data_preparation import df_f, pb_resolve_df, all_types_split_unique
from load_img import img, img_height, img_width

# Créer l'application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Obtenir les années uniques pour le slider
years = df_f['year'].unique()
years.sort()
months = df_f['month'].unique()
months.sort()

app.layout = html.Div([
    html.Div([
        html.Img(id='logo_rera', src='assets/IDF_RER_A_logo.svg'),
        html.H1('Dashboard du RER A')
    ], className="title_div"),   
    html.Div(className='separator'),
    dcc.Tabs(id="multiple_tabs", value="accueil", children=[
        dcc.Tab(label="Vue générale", 
                value='ligne_rer_a',
                 className='tab', selected_className='tab--selected' ),
        dcc.Tab(label="Temps réponse à incident", 
                value='temps_reponse_incidents',
                 className='tab', selected_className='tab--selected' ),
        dcc.Tab(label="Détails par gare", 
                value='details_par_gare', 
                className='tab', selected_className='tab--selected'),
    ], ),
    html.Div(className='separator'),
    html.Div(id='tabs-content-example-graph', className="main_content")
])


@callback(Output('tabs-content-example-graph', 'children'),Input('multiple_tabs', 'value'))
def render_content(tab):
    if tab == 'ligne_rer_a':
        return html.Div([
            html.H1("Nombre d'incidents par gare"),
            html.Div([
            html.Label("Sélectionnez le type de problème :"),
            dcc.Dropdown(
                id='problem-dropdown',
                options=[{'label': 'Tous les problèmes', 'value': 'all'}] +[{'label': problem.capitalize(), 'value': problem} for problem in all_types_split_unique],
                value=['all'], 
                multi=True,),
            ]
            , className="modifiers"
            , style={'width': '95%'}),            
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
            html.H1("Nombre d'incidents par typologie sélectionnées"),
            html.H5(id='incidents_selected'),
            html.Div([ 
            html.Label("Sélectionnez le type de tri :", className='label'),
            dcc.RadioItems(
                        id='sort_type1',
                        options=[
                            {'label': 'Non triés', 'value': 'no_sort'},
                            {'label': 'Croissant', 'value': 'asc_sort'},
                            {'label': 'Décroissant', 'value': 'desc_sort'},
                        ],
                        value='no_sort',
                        labelStyle={'display': 'inline-block', 'marginRight': '20px'}
                    ),
            ]
            , className="modifiers"
            , style={'width': '60%'}),
            dcc.Graph(id='incident-bar', config={"displayModeBar": False})
            ])
        ])
    elif tab == 'temps_reponse_incidents':
        return html.Div([
            html.H1("Temps de réponse aux incidents"),

            html.Div([
            html.Label("Sélectionnez le type d'incident :", className='label'),
            dcc.Dropdown(
                id='incident-type-dropdown',
                options=[{'label': 'Tous les problèmes', 'value': 'all'}] +[{'label': problem.capitalize(), 'value': problem} for problem in all_types_split_unique],
                value=['all'],  # Sélectionner tous les types par défaut
                multi=True,
                optionHeight=50,
                placeholder="Sélectionnez un type d'incident",
                searchable=True,
            ),
            ]
            , className="modifiers"
            , style={'width': '95%'}),
            html.Div([
            html.Div(id='average-response-time'),
                ], className="average_response_time_display"),
            html.Div(className='separator'),
            html.H1("Vue complète"),

                html.Div([
                    html.Label("Sélectionnez le type de graphique :", className='label'),
                    dcc.RadioItems(
                        id='graph-type',
                        options=[
                            {'label': 'Simplifié', 'value': 'bar'},
                            {'label': 'Détaillé', 'value': 'box'}
                        ],
                        value='bar',
                        labelStyle={'display': 'inline-block', 'marginRight': '20px'}
                    )
                ]
                , className="modifiers"
                , style={'width': '50%'}),                
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
                html.H1("Problèmes les plus courants"),
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
                html.H1("Par typologie spécifique"),

                html.Div([
                    html.Label("Sélectionnez la typologie d'incidents", className='label'),
                    dcc.Dropdown(
                    id='typology-dropdown-1',
                    options=[{'label': typology.upper(), 'value': typology} for typology in all_types_split_unique],
                    value=all_types_split_unique[0],
                    style={'width': '100%', 'display': 'inline-block', 'marginRight': '4%'}
                    ),
                ] 
                , className="modifiers"
                , style={'width': '80%'}                
                ),


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
                step=None,
                className='custom-slider'
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
            html.Div(className='separator'),
            html.Div(className='red_full_line'),
            html.Div([
                    html.Div([
                        html.Div([
                        html.H3(id='incident-classement'),
                        html.H1(id='selected_gare'),
                    ], id="classement_gare"),
                        html.H3(id='incident-info'),
                    ], id='gare_and_period'),
                    html.Div([
                        html.H3(id='incident-numbers'),
                        html.H5("incidents")
                    ], id='gare_and_incident_number')
                ], style={'display': 'flex', 'width': '100%', 'height':'10%'}),
            html.Div(className='red_full_line'),
            html.Div([
                html.Div(dcc.Graph(id='pie-chart_gare', config={"displayModeBar": False}), style={'width': '48%'}, ),
                html.Div(className="grey_vertical_separator"),  # Séparateur vertical
                html.Div(dcc.Graph(id='incident-graph_details_gare', config={"displayModeBar": False}), style={'width': '48%'})
            ], style={"display": 'flex', 'width': '100%', 'alignItems': 'center', 'justifyContent': 'center'}),
            html.Div(className='separator'),
            html.H3("Classement de la gare sur la période sélectionnée"),
            dcc.Graph(id='classement_general', config={"displayModeBar": False}),

        ])      

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

    filtered_df = df_f[(df_f['year'] == selected_year) 
                       & (df_f['month'] >= selected_month[0]) 
                       & (df_f['month'] <= selected_month[1])
                       & (df_f['label'].str.contains('|'.join(selected_problems)))
                       ]

    filtered_df2 = filtered_df[(filtered_df['tweet_type'] == 'Normal') & (filtered_df['len_label'] > 0)]


    agg_data = filtered_df2.groupby('gare_source').size().reset_index(name='count')

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
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='white', 
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

    bar_data = filtered_df2.groupby(['gare_source']).size().reset_index(name='count')

    if sort_type == 'asc_sort':
        bar_data = bar_data.sort_values(by='count', ascending=True)
    elif sort_type == 'desc_sort':
        bar_data = bar_data.sort_values(by='count', ascending=False)
    
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
        margin=dict(l=0, r=0, b=20), 
        
        barmode='stack',    
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
        Output('incidents_selected', 'children'),
        Input('problem-dropdown', 'value')
)
def update_h5(selected_incident_type):
    return "(" + ", ".join(selected_incident_type) + ")"

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
    plot_bgcolor='white',
    showlegend=False,
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
        fig.add_trace(go.Bar(
            x=problem_counts['month'], 
            y=problem_counts['count'], 
            name='Nombre de problèmes', 
            yaxis='y1',
            marker_color='#284897',
            hovertemplate='Mois: %{x}<br>Nombre de problèmes: %{y}<extra></extra>'
            ))
        
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
    
        fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=months, ticktext=[month_dict[month] for month in months], tickfont=dict(size=14, family='ParisineBold', color='#284897')),
            yaxis=dict(title='Nombre de problèmes', side='left', color='#284897',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='#284897')),
            yaxis2=dict(title='Temps de résolution moyen (jours)', overlaying='y', side='right', color='red',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='red')),
            plot_bgcolor='white',  # Fond blanc
            showlegend=False,  # Retirer la légende
            margin=dict(t=0),
        )
    elif graph_type == 'box':
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

    grouped_df = filtered_df.groupby(['label', 'month']).agg({
        'label': 'count',
        'duration': 'mean'
    }).rename(columns={'label': 'count', 'duration': 'response_time'}).reset_index()

    fig = go.Figure()

    df_typology = grouped_df[grouped_df['label'] == typo1]
    fig.add_trace(go.Bar(
        x=df_typology['month'],
        y=df_typology['count'],
        name=f'Nombre de problèmes ({typo1})',
        marker_color='#284897',
        yaxis='y1',
        hovertemplate='Mois: %{x}<br>Nombre de problèmes: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=df_typology['month'],
        y=df_typology['response_time'].dt.total_seconds() / 60,
        name=f'Temps de réponse moyen ({typo1})',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='red', width=4), 
        marker=dict(size=10),
        hovertemplate='Mois: %{x}<br>Temps de réponse moyen: %{y:.2f} minutes<extra></extra>'
    ))

    fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=months, ticktext=[month_dict[month] for month in months], tickfont=dict(size=14, family='ParisineBold', color='#284897')),
            yaxis=dict(title='Nombre de problèmes', side='left', color='#284897',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='#284897')),
            yaxis2=dict(title='Temps de résolution moyen (jours)', overlaying='y', side='right', color='red',  ticks='outside', title_font=dict(size=18, family='ParisineBold', color='red')),
            plot_bgcolor='white', 
            showlegend=False,
            margin=dict(t=0),
    )

    return fig


@app.callback(
    [Output('incident-info', 'children'),
     Output("selected_gare", 'children'),
    Output("incident-classement", 'children'),
    Output('incident-numbers', 'children'),
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

    selected_gare_data = filtered_df[filtered_df['gare_source'] == selected_gare]
    num_incidents = selected_gare_data.shape[0]

    df_sorted = filtered_df.groupby('gare_source').size().reset_index(name='count').sort_values(by='count', ascending=False).reset_index(drop=True)
    rank = df_sorted[df_sorted['gare_source'] == selected_gare].index[0] + 1

    time_grouped = selected_gare_data.groupby(['year', 'month']).size().reset_index(name='count')

    info_text = f"Sur la période allant de {begin_date_selected} à {end_date_selected}."
    selected_gare_info = f"{selected_gare}"
    nombre_incidents = f"{num_incidents}"
    classement_incident = f"#{rank}"

    pie_data = selected_gare_data.groupby('label').size().reset_index(name='incidents')

    fig = px.line(time_grouped, 
                x=pd.to_datetime(time_grouped[['year', 'month']].assign(day=1)), 
                y='count', 
                title=f"Nombre d'incidents chronologiquement pour la gare {selected_gare}",
                labels={'x': 'Date', 'count': "Nombre d'incidents"})
    fig.update_traces(
        line=dict(color='#284897', width=4),
    )
    fig.update_layout(plot_bgcolor='white')

    pie_fig = px.pie(
        pie_data, 
        names='label',
        values='incidents', title=f"Proportion des problèmes pour la gare {selected_gare}",
        color_discrete_sequence=px.colors.sequential.matter_r
        )
    
    pie_fig.update_traces(textinfo='label+percent', textposition='inside')
    pie_fig.update_layout(showlegend=False)

    return info_text, selected_gare_info, classement_incident, nombre_incidents, fig, pie_fig


@app.callback(
    Output('classement_general', 'figure'),
    [Input('year-dropdown_gare', 'value'),
    Input('month-dropdown_gare', 'value'),
    Input('gare-dropdown_details_gare', 'value')
    ]
)
def update_classement_general(selected_year, selected_months, selected_gare):
    begin_date_selected = "{:04d}-{:02d}-01".format(selected_year, selected_months[0])
    end_date_selected = "{:04d}-{:02d}-{}".format(selected_year, selected_months[1], max_day_per_month[selected_months[1]])

    filtered_df = pb_resolve_df[
        (pb_resolve_df['begin_date'] >= begin_date_selected) & 
        (pb_resolve_df['begin_date'] <= end_date_selected)
    ]
    filtered_df['month'] = filtered_df.begin_date.dt.month
    filtered_df['year'] = filtered_df.begin_date.dt.year


    all_gares = pd.DataFrame({'gare_source': gare_list})    

    df_sorted = filtered_df.groupby('gare_source').size().reset_index(name='count').sort_values(by='count', ascending=False).reset_index(drop=True)
    df_all_gares = all_gares.merge(df_sorted, on='gare_source', how='left').fillna(0)

    df_all_gares = df_all_gares.sort_values(by='count', ascending=False)

    bar_fig = px.bar(
        df_all_gares, 
        x='gare_source', 
        y='count', 
        color='count',
        color_continuous_scale="matter", 
        title="Nombre d'incidents par gare",
        labels={'gare_source': 'Gare', 'count': "Nombre d'incidents"}
    )
    bar_fig.update_traces(marker=dict(
        color=['green' if gare == selected_gare else px.colors.sequential.matter_r[int(i * len(px.colors.sequential.matter_r) / len(df_all_gares['gare_source']))] for i, gare in enumerate(df_all_gares['gare_source'])],
    ))

    bar_fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=df_all_gares['gare_source'],
        ticktext=[f'<b><span style="color:green">{gare}</span></b>' if gare == selected_gare else gare for gare in df_all_gares['gare_source']]
    ),
    yaxis=dict(title='Nombre d\'incidents'),
    plot_bgcolor='white',
    title='',
    margin=dict(t=0, b=0, l=0, r=0),
    )

    return bar_fig

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True, host='127.0.0.1', port=5000)





