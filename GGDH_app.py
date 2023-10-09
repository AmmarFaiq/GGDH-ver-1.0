

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

values_region= ["'s-Gravenhage", "Haaglanden", "Leiden", "Roaz", "Wassenaar"]

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

values_hadoks= ["'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar"]

values_all_regions = values_haaglanden + values_roaz

geo_df = geo_df.query("gemnaam in @values_all_regions")


df_numeric = pd.read_csv(path + 'df_numeric_ver_2.csv', sep = ',')
df_count = pd.read_csv(path + 'df_count_ver_2.csv', sep = ',')
df = df_count.merge(df_numeric, on=['WKC','Wijknaam','GMN','YEAR'])

radio_themes = dbc.RadioItems(
        id='ani_themes', 
        className='radio',
        options=[dict(label='Home', value=0), dict(label='Adv Analytics', value=1), dict(label='Diabetes', value=2), dict(label='Chronic Care', value=3), dict(label='Report', value=4)],
        value=0, 
        inline=True,   
    )


# options_chronic = geo_df.columns[9:25]

# options_CVD = geo_df.columns[9:25]

# options_overall = df.columns[4:25]

NUMERIC_COLUMN_NAME = ['AGE','Person_in_Household','Income','Moving_Count','Lifeevents_Count','UniqueMed_Count',
                       'ZVWKOSTENTOTAAL','ZVWKFARMACIE','ZVWKHUISARTS','ZVWKHUISARTS_NO_REG','ZVWKZIEKENHUIS','ZVWKFARMACIE','ZVWKOSTENPSYCHO']

CATEGORICAL_COLUMN_NAME = ['Total_Population', 
                           '%_Gender_Vrouwen', '%_0to20', '%_21to40', '%_41to60', '%_61to80', '%_Above80',
                           '%_MajorEthnicity_Native Dutch', '%_MajorEthnicity_Western','%_MajorEthnicity_Non-Western', 
                           '%_MinorEthnicity_Marokko', '%_MinorEthnicity_Suriname', '%_MinorEthnicity_Turkije', '%_MinorEthnicity_Voormalige Nederlandse Antillen en Aruba',
                           '%_Multiperson_Household', '%_HouseholdType_Institutional',
                           '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user',
                           '%_Other_social_benefit_user', '%_Sickness_benefit_user','%_Pension_benefit_user', 
                           '%_Moving_count_above_1','%_Lifeevents_count_above_2', 
                           '%_Low_Income', '%_Debt_Mortgage', '%_Debt_Poor', '%_Wanbet',
                           '%_WMO_user','%_WLZ_user'
                           ,'%_ZVWKHUISARTS_user', '%_ZVWKFARMACIE_user', '%_ZVWKZIEKENHUIS_user', '%_ZVWKOSTENPSYCHO_user', 
                           '%_HVZ_Medication_user','%_DIAB_Medication_user','%_BLOEDDRUKV_Medication_user', '%_CHOL_Medication_user',
                           '%_UniqueMed_Count_>=5', '%_UniqueMed_Count_>=10', 
                           '%_Hypertensie_patients', '%_COPD_patients', '%_Diabetes_I_patients','%_Diabetes_II_patients', '%_Chronic_Hartfalen_patients', '%_Morbus_Parkinson_patients', '%_Heupfractuur_patients','%_BMIUP45_patients'
                           ]
COSTS_COLUMN_NAME = ['ZVWKOSTENTOTAAL_MEAN', 'ZVWKHUISARTS_MEAN', 'ZVWKHUISARTS_NO_REG_MEAN', 
                     'ZVWKZIEKENHUIS_MEAN','ZVWKFARMACIE_MEAN', 'ZVWKFARMACIE_MEAN', 'ZVWKOSTENPSYCHO_MEAN',
                     '%_ZVWKHUISARTS_user', '%_ZVWKFARMACIE_user', '%_ZVWKZIEKENHUIS_user', '%_ZVWKOSTENPSYCHO_user'
                     ]

MEDICATION_COLUMN_NAME = ['UniqueMed_Count', '%_HVZ_Medication_user','%_DIAB_Medication_user','%_BLOEDDRUKV_Medication_user', '%_CHOL_Medication_user',
                      '%_UniqueMed_Count_>=5', '%_UniqueMed_Count_>=10', 
                     ]

INCOME_COLUMN_NAME = ['Income_MEAN', '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user',
                      '%_Other_social_benefit_user', '%_Sickness_benefit_user','%_Pension_benefit_user',
                      '%_Low_Income', '%_Debt_Mortgage',
                     ]

df['Income_MEAN'] = df['Income_MEAN'].mask(((df['YEAR'] <2011) | (df['YEAR'] >2021)), np.nan)

df['%_WMO_user'] = df['%_WMO_user'].mask(((df['YEAR'] <2015) ), np.nan)
df['%_WLZ_user'] = df['%_WLZ_user'].mask(((df['YEAR'] <2015) ), np.nan)

df['ZVWKOSTENTOTAAL_MEAN'] = df['ZVWKOSTENTOTAAL_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKFARMACIE_MEAN'] = df['ZVWKFARMACIE_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKHUISARTS_MEAN'] = df['ZVWKHUISARTS_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKHUISARTS_NO_REG_MEAN'] = df['ZVWKHUISARTS_NO_REG_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKZIEKENHUIS_MEAN'] = df['ZVWKZIEKENHUIS_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKFARMACIE_MEAN'] = df['ZVWKFARMACIE_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKOSTENPSYCHO_MEAN'] = df['ZVWKOSTENPSYCHO_MEAN'].mask( (df['YEAR'] >2020), np.nan)

df['%_ZVWKHUISARTS_user'] = df['%_ZVWKHUISARTS_user'].mask( (df['YEAR'] >2020), np.nan)
df['%_ZVWKFARMACIE_user'] = df['%_ZVWKFARMACIE_user'].mask( (df['YEAR'] >2020), np.nan)
df['%_ZVWKZIEKENHUIS_user'] = df['%_ZVWKZIEKENHUIS_user'].mask( (df['YEAR'] >2020), np.nan)
df['%_ZVWKOSTENPSYCHO_user'] = df['%_ZVWKOSTENPSYCHO_user'].mask( (df['YEAR'] >2020), np.nan)



drop_var = dcc.Dropdown(
        CATEGORICAL_COLUMN_NAME + NUMERIC_COLUMN_NAME,
        'Total_Population',
        id = 'drop_var_id',
        clearable=False,
        searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )

drop_wijk = dcc.Dropdown(
        id = 'drop_wijk',
        clearable=False, 
        searchable=False, 
        options=[
            {'label': "Hadoks Area", 'value': "HadoksArea"},
            {'label': "'s-gravenhage", 'value': "'s-gravenhage"},
            {'label': "Rijswijk", 'value': "Rijswijk"},
            {'label': 'Leidschendam-Voorburg', 'value': 'Leidschendam-Voorburg'},
            {'label': 'Wassenaar', 'value': 'Wassenaar'},
            # {'label': 'Roaz', 'value': 'Roaz'},
            # {'label': "Haaglanden", 'value': 'Haaglanden'},
            # {'label': 'Leiden', 'value': 'Leiden'},
            # {'label': 'Delft', 'value': 'Delft'}
            ],
        value="'s-gravenhage", 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )
#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    
        html.Div([
                    html.H1(children='ELAN Neighbourhood Dashboard', style={
                                                                'display': 'inline-block',    
                                                                'width' : '150px',
                                                                'height' : '50px',
                                                                'margin-right': '150px',
                                                                'margin-left': '10px',
                                                                    'font-size': '20px',
                                                                }),
                    html.A([html.Img(src=app.get_asset_url('hc-dh-logo.png'), style={'display': 'inline-block',
                                                                             'margin-top': '10px',
                                                                'width' : '110px',
                                                                'height' : '110px'
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
                    html.Label('Choose a variable to plot :', id='choose_variable'#, style= {'margin': '5px'}
                               ),
                    drop_var], style={'width': '30%','display': 'inline-block'}),

                    html.Div([
                    html.Label('Choose a region to plot:', id='choose_area'#, style= {'margin': '5px'}
                               ),
                                    drop_wijk, 
                             
                                ], style={'width': '15%','display': 'inline-block'}),
                    html.Div([
                    html.Label('Choose neighbourhoods to plot:', id='choose_wijk'#, style= {'margin': '5px'}
                               ),
                                    dcc.Dropdown(
                                            CATEGORICAL_COLUMN_NAME + NUMERIC_COLUMN_NAME,
                                            # 'Total_Population',
                                            id = 'drop_wijk_spec_id',
                                            clearable=True,
                                            searchable=True, 
                                            multi=True,
                                            style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
                                        ), 
                             
                                ], style={'width': '55%','display': 'inline-block'}),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    # html.Br(),
                    # html.Br(),            
                    html.Div([
                                daq.Slider(
                                    id = 'slider_map',
                                    handleLabel={"showCurrentValue": True,"label": "Year"},
                                    # marks = {str(i):str(i) for i in [str(i) for i in range(2009, 2023)]},
                                    # min = 2009,
                                    # max = 2022,
                                    size=1000, 
                                    color='#ADD8E6'
                                )
                            ],  style={  'margin-left' : '15%', 'margin-right' : '15%', 'padding':'1%'}),
                    ], className='box'),
                html.Div([
                    

                    html.Div([
                        

                        html.Div([ 
                            html.Div([
                                
                                html.Div([
                                    
                                    html.Label(id='title_map', style={'font-size':'medium','padding-bottom': '10%'}), 
                                    html.Br(),
                                    html.Label('Click on a tile to see the trendline!', style={'font-size':'9px','color' : 'black'}),
                                    
                                ], style={'width': '70%'}),
                                
                                
                            ], className='row'),
                            
                            
                            
                            

                            dcc.Graph(id='map', style={'position':'relative',  'height':'466px', 'top':'10px'
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

                    
                ], style={'width': '65%', 'float': 'left', 'box-sizing': 'border-box'}),

                
            
                html.Div([

                    html.Div([   
                        html.Label(id='title_bar'),           
                        dcc.Graph(id='bar_fig', style={'height':'964px'}), 
                        # html.Br(),
                    ], className='box'),
                    
                ], style={'width': '35%','display': 'inline-block'}),


                           
            
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
                    html.P(['Sources ', html.Br(), html.A('ELAN', href='https://ourworldindata.org/', target='_blank'), ', ', html.A('Microdata CBS', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'color':'white', 'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
    ]),
])


#------------------------------------------------------ Callbacks ------------------------------------------------------


@app.callback(
    [ 
        Output('drop_wijk_spec_id', 'options'),
        Output('drop_wijk_spec_id', 'value'),
       
    ],
    [
        Input('drop_wijk', 'value')
    ]
)
def update_slider(wijk_name):

    if wijk_name == 'HadoksArea':    
        dff = df.query("GMN in @values_hadoks")
        options = list(dff.Wijknaam.unique())
        
    elif wijk_name == "'s-gravenhage":    

        dff = df[df.GMN == "'s-Gravenhage"]
        options = list(dff.Wijknaam.unique())
        
    elif wijk_name == "Wassenaar":    

        dff = df[df.GMN == "Wassenaar"]
        options = list(dff.Wijknaam.unique())
        
    else:
        dff = df[df.GMN == wijk_name]
        options = list(dff.Wijknaam.unique())
       
    return options, options


@app.callback(
    [ 
        Output('slider_map', 'min'),
        Output('slider_map', 'max'),
        Output('slider_map', 'marks'),
        Output('slider_map', 'value'),
    ],
    [
        Input('drop_var_id', 'value')
    ]
)
def update_slider(xaxis_column_name):

    if xaxis_column_name in NUMERIC_COLUMN_NAME :
        variable_name = xaxis_column_name + "_MEAN"
    else:
        variable_name = xaxis_column_name
    
    if variable_name in INCOME_COLUMN_NAME:
        marks = {str(i):str(i) for i in [str(i) for i in range(2011, 2022)]}
        min = 2011
        max = 2021
    elif (variable_name == '%_WMO_user'):
        marks = {str(i):str(i) for i in [str(i) for i in range(2015, 2023)]}
        min = 2015
        max = 2022
    elif (variable_name == '%_WLZ_user') :
        marks = {str(i):str(i) for i in [str(i) for i in range(2015, 2022)]}
        min = 2015
        max = 2021
    elif (variable_name in MEDICATION_COLUMN_NAME) :
        marks = {str(i):str(i) for i in [str(i) for i in range(2009, 2022)]}
        min = 2009
        max = 2021
    elif (variable_name == '%_Wanbet'):
        marks = {str(i):str(i) for i in [str(i) for i in range(2010, 2021)]}
        min = 2010
        max = 2020
    elif variable_name in COSTS_COLUMN_NAME:
        marks = {str(i):str(i) for i in [str(i) for i in range(2009, 2021)]}
        min = 2009
        max = 2020
    else:
        marks = {str(i):str(i) for i in [str(i) for i in range(2009, 2023)]}
        min = 2009
        max = 2022

    return min, max, marks, max


@app.callback(
    Output('map', 'figure'),
    Output('title_map', 'children'),
    Input('slider_map', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value'),
    Input('drop_wijk_spec_id', 'value')
    )
def update_graph_map(year_value, xaxis_column_name, wijk_name, wijk_spec
                 ):
    dff = df[df['YEAR'] == year_value]
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


    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)

    if xaxis_column_name in NUMERIC_COLUMN_NAME :
        variable_name = xaxis_column_name + "_MEAN"
    else:
        variable_name = xaxis_column_name
        
    dff = dff.query("Wijknaam in @wijk_spec")

    fig = px.choropleth_mapbox(dff, geojson=geo_df_fff, color=variable_name,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.5,
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
    Input('drop_wijk', 'value'),
    Input('drop_wijk_spec_id', 'value')
    )
def update_graph_bar(year_value, xaxis_column_name, wijk_name, wijk_spec
                    ):
    
    dff = df[df['YEAR'] == year_value]
    colorscale = ["#6ADDFF",
                  # "#56B7FF",
                  "#4980DF", 
                  # "#3C50BF",
                    # "#38309F", 
                    "#402580"
                    ]
    if xaxis_column_name in NUMERIC_COLUMN_NAME :
        variable_name = xaxis_column_name + "_MEAN"
    else:
        variable_name = xaxis_column_name
        

    # if wijk_name == "Wassenaar":    

    #     dff = dff.query("Wijknaam in @wijk_spec")
    #     dff = dff.sort_values(by=[variable_name], ascending=False).reset_index()
    #     dff['group'] = pd.qcut(dff[variable_name], 2, labels=['Low','High'])
    # else:

    #     dff = dff.query("Wijknaam in @wijk_spec")
    #     dff = dff.sort_values(by=[variable_name], ascending=False).reset_index()

    
    if len(wijk_spec) == 0 :
        dff = dff[dff['GMN'] == "'s-Gravenhage"][dff['Wijknaam'] ==' Wijk 28 Centrum']
        fig = px.bar(x=dff[variable_name],
                y=dff['Wijknaam'],
                # color=dff['group'],
                hover_name=dff['Wijknaam'],
                color_discrete_sequence=colorscale
                )

    elif (len(wijk_spec) > 0) & (len(wijk_spec) < 3):

        dff = dff.query("Wijknaam in @wijk_spec")
        dff = dff.sort_values(by=[variable_name], ascending=False).reset_index()    
        fig = px.bar(x=dff[variable_name],
                y=dff['Wijknaam'],
                # color=dff['group'],
                hover_name=dff['Wijknaam'],
                color_discrete_sequence=colorscale
                )
    else:
        dff = dff.query("Wijknaam in @wijk_spec")
        dff = dff.sort_values(by=[variable_name], ascending=False).reset_index()   
        dff['group'] = pd.qcut(dff[variable_name], 3, labels=['Low', 'Medium', 'High'])
        
        fig = px.bar(x=dff[variable_name],
                y=dff['Wijknaam'],
                color=dff['group'],
                hover_name=dff['Wijknaam'],
                color_discrete_sequence=colorscale
                )  
     
    
    fig.update_traces(customdata=dff['Wijknaam'])

    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   
    fig.update_yaxes(title=variable_name)
    fig.update_xaxes(title=wijk_name)
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  paper_bgcolor='white', 
                                  yaxis={'categoryorder':'total ascending'}
                                  )

    return title, fig

@app.callback(
    Output('wijk_trend_label', 'children'),
    Output('wijk_trend_fig', 'figure'),
    Input('map', 'clickData'),
    Input('drop_var_id', 'value'),
    Input('drop_wijk', 'value'),
    Input('drop_wijk_spec_id', 'value'),
    State('map', 'figure'),
    prevent_initial_call=False)
def update_graph(clickData, 
                 xaxis_column_name, wijk_name, wijk_spec,
                 f):
    
    # if wijk_name == 'HadoksArea':
    #     dff = df.query("GMN in @values_hadoks")
    # elif wijk_name == "'s-gravenhage":
    #     dff = df[df['GMN'] == "'s-Gravenhage"]
    # else:
    #     dff = df[df['GMN'] == wijk_name]

    

    if xaxis_column_name in NUMERIC_COLUMN_NAME :
        variable_name = xaxis_column_name + "_MEAN"
    else:
        variable_name = xaxis_column_name

    if len(wijk_spec) == 0:
        dff = df[df['GMN'] == "'s-Gravenhage"][df['Wijknaam'] ==' Wijk 28 Centrum']
    else:
        dff = df.query("Wijknaam in @wijk_spec")

    wijk_dict = {}
    for i in range(len(dff['Wijknaam'].unique())):
        wijk_dict[dff['Wijknaam'].unique()[i]] = i
    
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
    
    fig = px.line(dff, x='YEAR', y= variable_name, color='Wijknaam', color_discrete_sequence=colorscale)

    fig.update_layout(
            xaxis=dict(
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
                                    label="Select All",
                                    method="restyle"
                                ),
                                dict(
                                    args=[{'visible':'legendonly'} ],
                                    label="Remove All",
                                    method="restyle"
                                ),
                                #  dict(
                                #     # args=["visible", True],
                                #     args=[{'visible':False}, [37] ],
                                #     label="Remove Prediction",
                                #     method="restyle"
                                # ),
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
# asu
    if clickData is None:
        title = '{} - {}'.format(xaxis_column_name, " Wijk 28 Centrum")
        
        fig.update_traces(visible="legendonly") 
        
        fig.data[wijk_dict[list(wijk_dict.keys())[0]]].visible=True 

        # fig.add_trace(go.Scatter(x=df_predicted[df_predicted['Wijknaam'] == " Wijk 28 Centrum"]['Jaar'], 
        #                          y=df_predicted[df_predicted['Wijknaam'] == " Wijk 28 Centrum"][variable_name], 
        #                          mode='lines', line={'dash': 'dash', 'color': 'blue'}, name='Predicted trend'))
    

        return title, fig
    

    else:
        i = clickData['points'][0]['pointNumber']
        city = f['data'][0]['hovertext'][i]
        title = '3.{} - {}'.format(xaxis_column_name, city)

        fig.update_traces(visible="legendonly") 

        # fig.add_trace(go.Scatter(x=df_predicted[df_predicted['Wijknaam'] == city]['Jaar'], 
        #                          y=df_predicted[df_predicted['Wijknaam'] == city][variable_name], 
        #                          mode='lines', line={'dash': 'dash', 'color': 'blue'}, name='Predicted trend'))
    

        fig.data[wijk_dict[city]].visible=True 

        return title, fig
    

    return title, dash.no_update



if __name__ == '__main__':
    app.run_server(debug=True)



