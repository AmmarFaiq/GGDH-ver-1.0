

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

with open("https://raw.githubusercontent.com/AmmarFaiq/GGDH-ver-1.0/main/wijkgeo_all_file.json") as f:
  geo_df_fff = json.load(f)
  
df = pd.read_csv(path + 'Pilot_Wijkindicatoren_RoyH_Final_Aangepast - Copy.csv')


radio_themes = dbc.RadioItems(
        id='ani_themes', 
        className='radio',
        options=[dict(label='Overall', value=0), dict(label='Chronic Care', value=1), dict(label='CVD', value=2), dict(label='Youth', value=3), dict(label='Pallative', value=4)],
        value=0, 
        inline=True
    )

options_overall = geo_df.columns[9:25]

options_chronic = geo_df.columns[9:25]

options_CVD = geo_df.columns[9:25]

drop_var = dcc.Dropdown(
        options_overall,
        'Totale bevolking',
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
        value='Roaz', 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )
# ["'s-Gravenhage", "Haaglanden", "Leiden", "Roaz", "Wassenaar"]

slider_map = daq.Slider(
        id = 'slider_map',
        handleLabel={"showCurrentValue": True,"label": "Year"},
        marks = {str(i):str(i) for i in [2015,2016,2017,2018,2019,2019,2020,2021]},
        min = 2015,
        max = 2021,
        size=80, 
        color='#ADD8E6'
    )

#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.H1(children='The Hague Neighbourhood Dashboard (Ver 1.0)'),
        html.Label('We are interested in investigating the trend of supply and demand of healthcare services in primary care (GPs) in the Hague. Here you can understand different neighbourhood healthcare utilization separated by their type of healthcare service. You can also see the trend of healthcare utilization in the Hague over the years. The data is from 2010 to 2019.', 
                    style={'color':'rgb(33 36 35)'}), 
        html.Img(src=app.get_asset_url('HCDHLUMCHADOKS.png'), style={'position': 'relative', 'width': '180%', 'left': '-83px', 'top': '-20px'}),
    ], className='side_bar'),

    html.Div([
        html.Div([
            html.Div([
                html.Label("Choose a Care Product:"), 
                html.Br(),
                html.Br(),
                radio_themes
            ], className='box', style={'margin': '5px', 'padding-top':'15px', 'padding-bottom':'15px'}),

            html.Div([
                html.Div([

                    html.Div([
                    html.Label('1. Choose a variable to plot from the Overall Themes:', id='choose_variable', style= {'margin': '5px'}),
                    drop_var,
                    
                    ], className='box'),

                    html.Div([
                        html.Div([
                            html.Label('Overall Mean Zorg Kosten (ZVW)', style={'font-size': 'medium'}),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                html.Div([
                                    html.H4('KOSTENTOTAL', style={'font-size': 'small','font-weight':'normal'}),
                                    html.H3(id='mean_total')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('HUISARTS', style={'font-size': 'small','font-weight':'normal'}),
                                    html.H3(id='mean_huisarts')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('SPECIALIST', style={'font-size': 'small','font-weight':'normal'}),
                                    html.H3(id='mean_specialist')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('FARMACIE', style={'font-size': 'small','font-weight':'normal'}),
                                    html.H3(id='mean_farmacie')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('PSYCOLOGIE', style={'font-size': 'small','font-weight':'normal'}),
                                    html.H3(id='mean_psy')
                                ],className='box_emissions'),

                            ], style={'display': 'flex'}),

                        ], className='box', style={'heigth':'10%'}),

                        html.Div([ 
                            html.Div([
                                
                                html.Div([
                                    html.Br(),
                                    html.Label(id='title_map', style={'font-size':'medium','padding-bottom': '10%'}), 
                                    html.Br(),
                                    html.Label('These Number refer to the average healthcare consumption per disctrict from chosen variable (Please click to see the trendline)', style={'font-size':'9px','color' : 'black'}),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                ], style={'width': '70%'}),
                                html.Div([

                                ], style={'width': '5%'}),
                                html.Div([
                                    drop_wijk, 
                                    html.Br(),
                                    html.Br(), 
                                ], style={'width': '25%'}),
                            ], className='row'),
                            
                            dcc.Graph(id='map', style={'position':'relative', 'top':'-50px'}), 

                            html.Div([
                                slider_map
                            ], style={'margin-left': '15%', 'position':'relative', 'top':'-38px'}),
                            
                        ], className='box', style={'padding-bottom': '0px'}), 
                    ]),
                ], style={'width': '60%', 'float': 'left', 'box-sizing': 'border-box'}),

                
            
                html.Div([

                    html.Div([   
                        html.Label(id='title_bar'),           
                        dcc.Graph(id='bar_fig'), 
                        html.Div([              
                            html.P(id='comment')
                        ], className='box_comment'),
                    ], className='box', style={'padding-bottom':'10px'}),

                    # html.Div([
                    #     html.Img(src=app.get_asset_url('Food.png'), style={'width': '100%', 'position':'relative', 'opacity':'80%'}),
                    # ]),

                ], style={'width': '40%', 'float': 'right', 'box-sizing': 'border-box'}),


                           
            
            ]),

            
            
            html.Div([
                html.Div([
                    html.Label(id='wijk_trend_label', style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Click on it to know more!', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(id='wijk_trend_fig')
                ], className='box', style={'width': '45%', 'float': 'left', 'box-sizing': 'border-box'}), 
                html.Div([
                    html.Label(id="all_trend_label", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Click on it to know more!', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(id='all_trend_fig')
                ], className='box', style={'width': '52%', 'float': 'right', 'box-sizing': 'border-box'}), 
                
            ]),
            
            

            

            html.Div([
                html.Div([
                    html.P(['Health Campus Den Haag', html.Br(),'M. Ammar Faiq, Frank Ardesch, Jeroen Sturijs, Marc B.'], style={'color':'white', 'font-size':'12px'}),
                ], style={'width':'60%'}), 
                html.Div([
                    html.P(['Sources ', html.Br(), html.A('GGDH-ELAN', href='https://ourworldindata.org/', target='_blank'), ', ', html.A('Microdata CBS', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'color':'white', 'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
        ], className='main'),
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
    Output('mean_total', 'children'),
    Output('mean_huisarts', 'children'),
    Output('mean_specialist', 'children'),
    Output('mean_farmacie', 'children'),
    Output('mean_psy', 'children'),    
    Input('slider_map', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value')
    )
def update_graph_map(year_value, xaxis_column_name, wijk_name
                 ):
    dff = df[df['Jaar'] == year_value]
    
    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   

    if wijk_name == "Roaz":
        geo_df2 = geo_df.query("gemnaam in @values_roaz")
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=xaxis_column_name,
                            locations="wijknaam", featureidkey="properties.wijknaam", opacity = 0.3,
                            center={"lat": 52.1601, "lon": 4.4970},
                            mapbox_style="carto-positron", zoom=9, hover_name="wijknaam")
        mean_total_str = str(np.round(geo_df2['Totale bevolking'].mean(),2))
        mean_huisarts_str = str(np.round(geo_df2['Bevolking 19 jaar en ouder'].mean(),2))
        mean_specialist_str = str(np.round(geo_df2['Bevolking 65 jaar en ouder'].mean(),2))
        mean_farmacie_str = str(np.round(geo_df2["% eenzaam*"].mean(),2))
        mean_psy_str = str(np.round(geo_df2["% ernstig eenzaam*"].mean(),2))
    
    elif wijk_name == 'Haaglanden':    
        geo_df2 = geo_df.query("gemnaam in @values_haaglanden")
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=xaxis_column_name,
                            locations="wijknaam", featureidkey="properties.wijknaam", opacity = 0.3,
                            center={"lat": 52.0705, "lon": 4.3003},
                            mapbox_style="carto-positron", zoom=9, hover_name="wijknaam")
        mean_total_str = str(np.round(geo_df2['Totale bevolking'].mean(),2))
        mean_huisarts_str = str(np.round(geo_df2['Bevolking 19 jaar en ouder'].mean(),2))
        mean_specialist_str = str(np.round(geo_df2['Bevolking 65 jaar en ouder'].mean(),2))
        mean_farmacie_str = str(np.round(geo_df2["% eenzaam*"].mean(),2))
        mean_psy_str = str(np.round(geo_df2["% ernstig eenzaam*"].mean(),2))

    elif wijk_name == "Leiden":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Leiden"]
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=xaxis_column_name,
                            locations="wijknaam", featureidkey="properties.wijknaam", opacity = 0.3,
                            center={"lat": 52.1601, "lon": 4.4970},
                            mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")    
        mean_total_str = str(np.round(geo_df2['Totale bevolking'].mean(),2))
        mean_huisarts_str = str(np.round(geo_df2['Bevolking 19 jaar en ouder'].mean(),2))
        mean_specialist_str = str(np.round(geo_df2['Bevolking 65 jaar en ouder'].mean(),2))
        mean_farmacie_str = str(np.round(geo_df2["% eenzaam*"].mean(),2))
        mean_psy_str = str(np.round(geo_df2["% ernstig eenzaam*"].mean(),2))

    elif wijk_name == "Wassenaar":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Wassenaar"]
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=xaxis_column_name,
                            locations="wijknaam", featureidkey="properties.wijknaam", opacity = 0.3,
                            center={"lat": 52.1429, "lon": 4.4012},
                            mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")
        mean_total_str = str(np.round(geo_df2['Totale bevolking'].mean(),2))
        mean_huisarts_str = str(np.round(geo_df2['Bevolking 19 jaar en ouder'].mean(),2))
        mean_specialist_str = str(np.round(geo_df2['Bevolking 65 jaar en ouder'].mean(),2))
        mean_farmacie_str = str(np.round(geo_df2["% eenzaam*"].mean(),2))
        mean_psy_str = str(np.round(geo_df2["% ernstig eenzaam*"].mean(),2))

    elif wijk_name == "Delft":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Delft"]
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=xaxis_column_name,
                            locations="wijknaam", featureidkey="properties.wijknaam", opacity = 0.3,
                            center={"lat": 52.0116, "lon": 4.3571},
                            mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")
        mean_total_str = str(np.round(geo_df2['Totale bevolking'].mean(),2))
        mean_huisarts_str = str(np.round(geo_df2['Bevolking 19 jaar en ouder'].mean(),2))
        mean_specialist_str = str(np.round(geo_df2['Bevolking 65 jaar en ouder'].mean(),2))
        mean_farmacie_str = str(np.round(geo_df2["% eenzaam*"].mean(),2))
        mean_psy_str = str(np.round(geo_df2["% ernstig eenzaam*"].mean(),2))
                
    else:
        geo_df2 = geo_df[geo_df['gemnaam'] == "'s-Gravenhage"]
        fig = px.choropleth_mapbox(geo_df2, geojson=geo_df_fff, color=xaxis_column_name,
                            locations="wijknaam", featureidkey="properties.wijknaam", opacity = 0.3,
                            center={"lat": 52.0705, "lon": 4.3003},
                            mapbox_style="carto-positron", zoom=10, hover_name="wijknaam")
        mean_total_str = str(np.round(geo_df2['Totale bevolking'].mean(),2))
        mean_huisarts_str = str(np.round(geo_df2['Bevolking 19 jaar en ouder'].mean(),2))
        mean_specialist_str = str(np.round(geo_df2['Bevolking 65 jaar en ouder'].mean(),2))
        mean_farmacie_str = str(np.round(geo_df2["% eenzaam*"].mean(),2))
        mean_psy_str = str(np.round(geo_df2["% ernstig eenzaam*"].mean(),2))
    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":50},
                                  height=500,
                                  paper_bgcolor='#F9F9F8')
    
    return fig, title, mean_total_str, mean_huisarts_str, mean_specialist_str, mean_farmacie_str, mean_psy_str

@app.callback(
    Output('title_bar', 'children'),
    Output('bar_fig', 'figure'),
    Output('comment', 'children'),
    Input('slider_map', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value')
    )
def update_graph_bar(year_value, xaxis_column_name, wijk_name
                    ):
    if wijk_name == "Roaz":
        geo_df2 = geo_df.query("gemnaam in @values_roaz")
        fig = px.bar(x=geo_df2[xaxis_column_name],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        comment = ["Look at the beef production emissions! Each kilogram of beef produces almost 60 kg of CO2.", html.Br(), html.Br()]
        fig.update_traces(customdata=geo_df2['wijknaam'])

    elif wijk_name == 'Haaglanden':    
        geo_df2 = geo_df.query("gemnaam in @values_haaglanden")
        fig = px.bar(x=geo_df2[xaxis_column_name],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        comment = ["Look at the beef production emissions! Each kilogram of beef produces almost 60 kg of CO2.", html.Br(), html.Br()]
        fig.update_traces(customdata=geo_df2['wijknaam'])
    
    elif wijk_name == "Leiden":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Leiden"]
        fig = px.bar(x=geo_df2[xaxis_column_name],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        comment = ["Look at the beef production emissions! Each kilogram of beef produces almost 60 kg of CO2.", html.Br(), html.Br()]
        fig.update_traces(customdata=geo_df2['wijknaam'])

    elif wijk_name == "Wassenaar":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Wassenaar"]
        fig = px.bar(x=geo_df2[xaxis_column_name],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        comment = ["Look at the beef production emissions! Each kilogram of beef produces almost 60 kg of CO2.", html.Br(), html.Br()]
        fig.update_traces(customdata=geo_df2['wijknaam'])

    elif wijk_name == "Delft":
        geo_df2 = geo_df[geo_df['gemnaam'] == "Delft"]
        fig = px.bar(x=geo_df2[xaxis_column_name],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        comment = ["Look at the beef production emissions! Each kilogram of beef produces almost 60 kg of CO2.", html.Br(), html.Br()]
        fig.update_traces(customdata=geo_df2['wijknaam'])

    else:
        geo_df2 = geo_df[geo_df['gemnaam'] == "'s-Gravenhage"]
        fig = px.bar(x=geo_df2[xaxis_column_name],
                y=geo_df2['wijknaam'],
                hover_name=geo_df2['wijknaam']
                )
        comment = ["Look at the beef production emissions! Each kilogram of beef produces almost 60 kg of CO2.", html.Br()]
        fig.update_traces(customdata=geo_df2['wijknaam'])

    title = '2. {} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   
    fig.update_yaxes(title=xaxis_column_name)
    fig.update_xaxes(title=wijk_name)
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":10},
                                  height=755,
                                  paper_bgcolor='#F9F9F8', 
                                  yaxis={'categoryorder':'total descending'}
                                  )

    return title, fig, comment

@app.callback(
    Output('wijk_trend_label', 'children'),
    Output('wijk_trend_fig', 'figure'),
    Input('map', 'clickData'),
    # Input('drop_var_id', 'value'),
    State('map', 'figure'),
    prevent_initial_call=False)
def update_graph(clickData, 
                #  xaxis_column_name, 
                 f):
    if clickData is None:
        dff = df[df['Wijknaam'] == "Centrum"]
        title = '3. {} - {}'.format('Gem GGZ Kosten', "Centrum")
        fig = px.line(dff, x='Jaar', y='Gem GGZ Kosten')
        return title, fig
    
    else:
        i = clickData['points'][0]['pointNumber']
        city = f['data'][0]['hovertext'][i]
        dff = df[df['Wijknaam'] == city]
        title = '3.{} - {}'.format('Gem GGZ Kosten', city)
        fig = px.line(dff, x='Jaar', y='Gem GGZ Kosten')
        return title, fig
    
    return title, dash.no_update

@app.callback(
    Output('all_trend_label', 'children'),
    Output('all_trend_fig', 'figure'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value')

    )
def update_graph(xaxis_column_name, 
                 wijk_name 
                 ):
    title = '4. Time series clustering {} - {} ( {} - {})'.format('Gem GGZ Kosten', "All",  xaxis_column_name, wijk_name)
    fig = px.line(df, x='Jaar', y='Gem GGZ Kosten', color='Wijknaam')

    return title, fig



if __name__ == '__main__':
    app.run_server(debug=True)



