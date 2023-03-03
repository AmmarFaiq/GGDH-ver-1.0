

import dash
from dash import dcc as dcc
# import dash_html_components as html
from dash import html as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import geopandas as gpd
import requests
import json

# https://raw.githubusercontent.com/AmmarFaiq/GGDH-ver-1.0/main/data/wijkgeo_all_file.json
# https://raw.githubusercontent.com/AmmarFaiq/GGDH-ver-1.0/main/data/WijkEenzaamheid2016.csv
# https://raw.githubusercontent.com/AmmarFaiq/GGDH-ver-1.0/main/data/Pilot_Wijkindicatoren_RoyH_Final_Aangepast%20-%20Copy.CSV
# https://github.com/AmmarFaiq/GGDH-ver-1.0/raw/main/data/wijk_2016_6.geojson
        
path = 'https://raw.githubusercontent.com/AmmarFaiq/GGDH-ver-1.0/main/data/'

geojsondata = gpd.read_file("https://github.com/AmmarFaiq/GGDH-ver-1.0/raw/main/data/wijk_2016_6.geojson")

geojsondata = geojsondata.to_crs(epsg=4326)
geojsondata = geojsondata.explode(index_parts=False)

df_info = pd.read_csv(path + 'WijkEenzaamheid2016.csv')

geo_df = geojsondata.merge(df_info, left_on="WKC", right_on= "wijkcode")

values_region= ["'s-Gravenhage", "Haaglanden", "Leiden", "Roaz", "Wassenar"]

values_haaglanden=["'s-Gravenhage",
        "Delft","Leidschendam-Voorburg",
        "Midden-Delfland", 
        "Pijnacker-Nootdorp","Rijswijk",
        "Wassenaar","Westland","Zoetermeer"]

values_roaz=["'s-Gravenhage", "Alphen aan den Rijn", "Bodegraven-Reeuwijk",
        "Delft","Gouda","Hillegom", "Kaag en Braassem","Katwijk",
        "Krimpenerwaard","Leiden","Leiderdorp", "Leidschendam-Voorburg",
        "Lisse","Midden-Delfland","Nieuwkoop","Noordwijk","Oegstgeest",
        "Pijnacker-Nootdorp","Rijswijk","Teylingen","Voorschoten", "Waddinxveen",
        "Wassenaar","Westland","Zoetermeer","Zoeterwoude","Zuidplas"]

values_all_regions = values_haaglanden + values_roaz

geo_df = geo_df.query("gemnaam in @values_all_regions")

df = pd.read_csv(path + "Pilot_Wijkindicatoren_RoyH_Final_Aangepast%20-%20Copy.CSV")
df_predicted = pd.read_csv(path + "Pilot_Wijkindicatoren_RoyH_Final_Aangepast%20-%20predicted.csv")

resp_json_all = requests.get("https://raw.githubusercontent.com/AmmarFaiq/GGDH-ver-1.0/main/data/wijkgeo_all_file.json")
# The .json() method automatically parses the response into JSON.
geo_df_fff = resp_json_all.json()

# with open("https://raw.githubusercontent.com/AmmarFaiq/GGDH-ver-1.0/main/data/wijkgeo_all_file.json", 'r') as f:
#   geo_df_fff = json.load(f)


radio_themes = dbc.RadioItems(
        id='ani_themes', 
        className='radio',
        options=[dict(label='Overall', value=0), dict(label='Chronic Care', value=1), dict(label='CVD', value=2), dict(label='Youth', value=3), dict(label='Pallative', value=4)],
        value=0, 
        inline=True
    )

options_overall = geo_df.columns[9:25]

# options_chronic = geo_df.columns[9:25]

# options_CVD = geo_df.columns[9:25]

options_overall = df.columns[6:25]

# drop_var = dcc.Dropdown(
#         options_overall,
#         'Totale bevolking',
#         id = 'drop_var_id',
#         clearable=False,
#         searchable=False, 
#         style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
#     )

drop_var = dcc.Dropdown(
        options_overall,
        'Gem GGZ Kosten',
        id = 'drop_var_id',
        clearable=False,
        searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )

drop_wijk = dcc.Dropdown(
        id = 'drop_wijk',
        clearable=False, 
        searchable=False, 
        options=[{'label': 'Roaz', 'value': 'Roaz'},
                {'label': "Haaglanden", 'value': 'Haaglanden'},
                {'label': "'s-gravenhage", 'value': "'s-gravenhage"},
                {'label': 'Leiden', 'value': 'Leiden'},
                {'label': 'Wassenaar', 'value': 'Wassenaar'},
                {'label': 'Delft', 'value': 'Delft'}],
        value="'s-gravenhage", 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )
# ["'s-Gravenhage", "Haaglanden", "Leiden", "Roaz", "Wassenaar"]

slider_map = daq.Slider(
        id = 'slider_map',
        handleLabel={"showCurrentValue": True,"label": "Year"},
        # marks = {str(i):str(i) for i in [2015,2016,2017,2018,2019,2019,2020,2021]},
        # min = 2015,
        # max = 2021,
        marks = {str(i):str(i) for i in [2010,2011,2012,2013,2014,2015,2016]},
        min = 2010,
        max = 2016,
        size=400, 
        color='#ADD8E6'
    )

#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    
        html.Div([
                    html.H1(children='The Hague Neighbourhood Dashboard (Ver 1.0)', style={
                                                                'display': 'inline-block',    
                                                                'width' : '150px',
                                                                'height' : '50px',
                                                                'margin-right': '150px',
                                                                'margin-left': '10px',
                                                                    'font-size': '20px',
                                                                }),
                    html.A([html.Img(src=app.get_asset_url('hc-dh-logo.png'), style={'display': 'inline-block',
                                                                             'margin-top': '10px',
                                                                'width' : '180px',
                                                                'height' : '180px'
                                                                })], href='https://healthcampusdenhaag.nl/nl/'),
                    html.Div([
                        html.Img(src=app.get_asset_url('lumc-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                     'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('uni_leiden-500x500.jpg'), style={'display': 'inline-block',
                                                                                     'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('hhs-500x500.jpg'), style={'display': 'inline-block',
                                                                              'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),                                                   
                    html.Img(src=app.get_asset_url('hmc-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),  
                    html.Img(src=app.get_asset_url('haga_ziekenhuis-500x500.jpg'), style={'display': 'inline-block',
                                                                                          'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('hadoks-1-500x500.jpg'), style={'display': 'inline-block',
                                                                                   'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('parnassia-500x500.jpg'), style={'display': 'inline-block',
                                                                                    'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('rienier_de_graaf-500x500.jpg'), style={'display': 'inline-block',
                                                                                           'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    html.Img(src=app.get_asset_url('gemeente_dh-500x500.jpg'), style={'display': 'inline-block',
                                                                                      'margin-top': '10px',
                                                                'width' : '100px',
                                                                'height' : '100px'
                                                                }),
                    ], style={'display': 'inline-block','margin-left': '300px'}),
            
            
        ], style={ 
                                   'background-image': 'url("/assets/Line.png")',
                                  'background-size': '100%',
                                  'height': '168px',
                                  'width': '101%',
                                  'margin-top': '-10px',
                                  'margin-left': '-10px',
                                  'display':'flex'
                                   }),

    html.Div([
        



        html.Div([
            

            html.Div([
                html.Div([
                    
                    html.Div([
                        
                    html.Label('1. Choose a variable to plot from the Overall Themes:', id='choose_variable'#, style= {'margin': '5px'}
                               ),
                    drop_var,
                    
                    ], className='box'),

                    html.Div([
                        

                        html.Div([ 
                            html.Div([
                                
                                html.Div([
                                    
                                    html.Label(id='title_map', style={'font-size':'medium','padding-bottom': '10%'}), 
                                    html.Br(),
                                    html.Label('Click on a tile to see the trendline!', style={'font-size':'9px','color' : 'black'}),
                                    
                                ], style={'width': '70%'}),
                                
                                html.Div([
                                    drop_wijk, 
                             
                                ], style={'width': '30%'}),
                            ], className='row'),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                slider_map
                            ], style={'margin-left': '15%', 'position':'relative', 'top':'-10px'}),

                            dcc.Graph(id='map', style={'position':'relative',  'height':'300px', 'top':'10px'
                                                       }), 

                            
                            
                        ], className='box', style={}), 
                        html.Div([
                            html.Label(id='wijk_trend_label', style={'font-size': 'medium'}),
                            html.Br(),
                            html.Label('Click the button and legends to know more!', style={'font-size':'9px'}),
                            
                            dcc.Graph(id='wijk_trend_fig', style={'height':'400px'}),
                        ], className='box', style={
                                                    'position':'relative', 
                                                }), 
                        
                    ]),

                    
                ], style={'width': '60%', 'float': 'left', 'box-sizing': 'border-box'}),

                
            
                html.Div([

                    html.Div([   
                        html.Label(id='title_bar'),           
                        dcc.Graph(id='bar_fig', style={'height':'979px'}), 
                        # html.Br(),
                    ], className='box'),
                    
                ], style={'width': '40%','display': 'inline-block'}),


                           
            
            ], style={'display': 'block'}),
    
                html.Div([
                html.Label("Check Out the Other Themes:"), 
                html.Br(),
                radio_themes
            ], className='box', style={ }),
            
            
            

            

            
        ], className='main'),
        html.Div([
                html.Div([
                    html.P(['Health Campus Den Haag', html.Br(),'Turfmarkt 99, 3e etage, 2511 DP, Den Haag'], style={'color':'white', 'font-size':'12px'}),
                ], style={'width':'60%'}), 
                html.Div([
                    html.P(['Sources ', html.Br(), html.A('GGDH-ELAN', href='https://ourworldindata.org/', target='_blank'), ', ', html.A('Microdata CBS', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'color':'white', 'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
    ]),
])


#------------------------------------------------------ Callbacks ------------------------------------------------------

@app.callback(
    [ 
        Output('slider_map', 'max'),
        Output('slider_map', 'value'),
    ],
    [
        Input('drop_var_id', 'value')
    ]
)

def update_slider(product):
    
    year = df['Jaar'].max()
    return year, year

@app.callback(
    Output('map', 'figure'),
    Output('title_map', 'children'),
    Input('slider_map', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value')
    )
def update_graph_map(year_value, xaxis_column_name, wijk_name
                 ):
    dff = df[df['Jaar'] == year_value]
    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF",
                    # "#7FFCFF",
                    # "#95FFF5",
                    # "#ABFFE8",
                    # "#C2FFE3",
                    # "#DAFFE6"
                  ]


    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   

    bigger_region = "Totale bevolking"

    if wijk_name == "Roaz":
        geo_df2 = geo_df.query("gemnaam in @values_roaz")
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=bigger_region,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.1601, "lon": 4.4970}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=9, hover_name="wijknaam")
    
    elif wijk_name == 'Haaglanden':    
        geo_df2 = geo_df.query("gemnaam in @values_haaglanden")
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=bigger_region,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=9, hover_name="wijknaam")

    elif wijk_name == "Leiden":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Leiden"]
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=bigger_region,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.1601, "lon": 4.4970}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")    

    elif wijk_name == "Wassenaar":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Wassenaar"]
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=bigger_region,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.1429, "lon": 4.4012}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")

    elif wijk_name == "Delft":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Delft"]
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=bigger_region,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.0116, "lon": 4.3571}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")
                
    else:
        # geo_df2 = geo_df[geo_df['gemnaam'] == "'s-Gravenhage"]
        # fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=bigger_region,
        #                     locations="WKC", featureidkey="properties.WKC", opacity = 0.3,
        #                     center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale,
        #                     mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")
        # geo_df2 = geo_df[geo_df['gemnaam'] == "'s-Gravenhage"]

        fig = px.choropleth_mapbox(dff, geojson=geo_df_fff, color=xaxis_column_name,
                            locations="Wijkcode", featureidkey="properties.WKC", opacity = 0.3,
                            center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="Wijknaam")

    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":50},
                                  paper_bgcolor='white'
                                  )
    
    return fig, title

# create a new column that put each row into a group of 4 numbers based on the value of a column quartile


@app.callback(
    Output('title_bar', 'children'),
    Output('bar_fig', 'figure'),
    Input('slider_map', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value')
    )
def update_graph_bar(year_value, xaxis_column_name, wijk_name
                    ):
    
    dff = df[df['Jaar'] == year_value]
    bigger_region = "Totale bevolking"
    if wijk_name == "Roaz":
        geo_df2 = geo_df.query("gemnaam in @values_roaz")
        fig = px.bar(x=geo_df2[bigger_region],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        fig.update_traces(customdata=geo_df2['wijknaam'])

    elif wijk_name == 'Haaglanden':    
        geo_df2 = geo_df.query("gemnaam in @values_haaglanden")
        fig = px.bar(x=geo_df2[bigger_region],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        fig.update_traces(customdata=geo_df2['wijknaam'])
    
    elif wijk_name == "Leiden":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Leiden"]
        fig = px.bar(x=geo_df2[bigger_region],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        fig.update_traces(customdata=geo_df2['wijknaam'])

    elif wijk_name == "Wassenaar":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Wassenaar"]
        fig = px.bar(x=geo_df2[bigger_region],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        fig.update_traces(customdata=geo_df2['wijknaam'])

    elif wijk_name == "Delft":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Delft"]
        fig = px.bar(x=geo_df2[bigger_region],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        fig.update_traces(customdata=geo_df2['wijknaam'])

    else:
        # geo_df2 = geo_df[geo_df['gemnaam'] == "'s-Gravenhage"]
        # fig = px.bar(x=geo_df2[bigger_region],
        #         y=geo_df2['wijknaam'],
        #         hover_name=geo_df2['wijknaam']
        #         )
        # fig.update_traces(customdata=geo_df2['wijknaam'])
        # geo_df2 = geo_df[geo_df['gemnaam'] == "'s-Gravenhage"]
        dff['group'] = pd.qcut(dff[xaxis_column_name], 4, labels=['Category 1', 'Category 2', 'Category 3', 'Category 4'])
        colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF",
                    # "#7FFCFF",
                    # "#95FFF5",
                    # "#ABFFE8",
                    # "#C2FFE3",
                    # "#DAFFE6"
                  ]
        fig = px.bar(x=dff[xaxis_column_name],
                y=dff['Wijknaam'],
                color=dff['group'],
                hover_name=dff['Wijknaam'],
                color_discrete_sequence=colorscale
                )
        fig.update_traces(customdata=dff['Wijknaam'])

    title = '2. {} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   
    fig.update_yaxes(title=xaxis_column_name)
    fig.update_xaxes(title=wijk_name)
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  paper_bgcolor='white', 
                                  yaxis={'categoryorder':'total descending'}
                                  )

    return title, fig

# create a dictionary for every unique values in the column 'Wijknaam' with ordered numbers

@app.callback(
    Output('wijk_trend_label', 'children'),
    Output('wijk_trend_fig', 'figure'),
    Input('map', 'clickData'),
    Input('drop_var_id', 'value'),
    State('map', 'figure'),
    prevent_initial_call=False)
def update_graph(clickData, 
                 xaxis_column_name, 
                 f):
    
    wijk_dict = {}
    for i in range(len(df['Wijknaam'].unique())):
        wijk_dict[df['Wijknaam'].unique()[i]] = i
    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF",
                    "#7FFCFF",
                    "#95FFF5",
                    "#ABFFE8",
                    "#C2FFE3",
                    "#DAFFE6"
                  ]
    # df['group'] = pd.qcut(df[xaxis_column_name], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    fig = px.line(df, x='Jaar', y= xaxis_column_name, color='Wijknaam', color_discrete_sequence=colorscale)
    # fig.add_trace(go.Scatter(x=df_predicted['Jaar'], y=df_predicted[xaxis_column_name], mode='lines', line={'dash': 'dash', 'color': 'blue'}))
    
    
    fig.update_layout(
            xaxis=dict(
                rangeselector=
                dict(
                    # buttons=list([
                    #     dict(count=3,
                    #         label="3y",
                    #         step="year",
                    #         stepmode="backward"),
                    #     dict(count=10,
                    #         label="10y",
                    #         step="year",
                    #         stepmode="todate"),
                    #     dict(step="all")
                    # ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                # type="linear"
                type="date"
            ),
            
        )
    fig.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                
                                dict(
                                    args=["visible", True],
                                    # args=[{'visible':False}, [37] ],
                                    label="Select All",
                                    method="restyle"
                                ),
                                 dict(
                                    # args=["visible", True],
                                    args=[{'visible':False}, [37] ],
                                    label="Remove Prediction",
                                    method="restyle"
                                ),
                            ]),
                            pad={"r": 0, "t": -20},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))
    if clickData is None:
        title = '3. {} - {}'.format(xaxis_column_name, "Centrum")
        
        fig.update_traces(visible="legendonly") 

        fig.data[wijk_dict["Centrum"]].visible=True 

        fig.add_trace(go.Scatter(x=df_predicted[df_predicted['Wijknaam'] == "Centrum"]['Jaar'], 
                                 y=df_predicted[df_predicted['Wijknaam'] == "Centrum"][xaxis_column_name], 
                                 mode='lines', line={'dash': 'dash', 'color': 'blue'}, name='Predicted trend'))
    

        return title, fig
    

    else:
        i = clickData['points'][0]['pointNumber']
        city = f['data'][0]['hovertext'][i]
        title = '3.{} - {}'.format(xaxis_column_name, city)

        fig.update_traces(visible="legendonly") 

        fig.add_trace(go.Scatter(x=df_predicted[df_predicted['Wijknaam'] == city]['Jaar'], 
                                 y=df_predicted[df_predicted['Wijknaam'] == city][xaxis_column_name], 
                                 mode='lines', line={'dash': 'dash', 'color': 'blue'}, name='Predicted trend'))
    

        fig.data[wijk_dict[city]].visible=True 

        return title, fig
    

    return title, dash.no_update

# take the first row of the dataframe and create a copy of it for n times



if __name__ == '__main__':
    app.run_server(debug=True)



