import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import util.translate as tr

app = dash.Dash(__name__, use_pages= True)

server = app.server
        
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.A(html.Img(src= app.get_asset_url('hc-dh-logo.png')), href= 'https://healthcampusdenhaag.nl/nl/')),
                    dbc.Col([html.H1("ELAN Neighbourhood Dashboard"), html.P('Last updated January 2024', id="last_update")], id= 'headersub'),
                ],
                align="center",
                className="g-0",
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [dcc.Link('Neighbourhood', href= '/'),
                    dcc.Link('Supply and Demand', href='/supplydemand'),
                    dcc.Link("Diabetes", href="/diabetes"),
                    dcc.Link("Palliative care", href="/palliative"),
                    dcc.Link("Pedriatric care", href="/young")],
                    className="ms-auto",
                    id= "navmenu"
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
            html.Div(html.Img(src=app.get_asset_url('flag-NL.svg'), alt=tr.Language.NL.value,  id='select_language'), id='lang_select_parent')
        ], id ="headercontent"
    ),
    id= 'header',
    className="mb-5"
)

footer = html.Div([
                html.Div([
                    html.P([
                        html.H1('Health Campus Den Haag'),'Turfmarkt 99', html.Br(), '3rd floor', html.Br(), '2511 DP, Den Haag'], id="footerleft")
                ], className= 'footerelement'), 
                html.Div([
                    html.Ul([html.Li(dcc.Link('About', href= '/about')), html.Li(dcc.Link('changelog', href= '/changelog')), html.Li("link to Elan?")])
                ], className= 'footerelement'),
                html.Div([
                    html.H1('Partners'),
                    html.A([html.Img(src=app.get_asset_url('lumc-1-500x500.jpg'))], href='https://www.lumc.nl/en/'),
                    html.A([html.Img(src=app.get_asset_url('uni_leiden-500x500.jpg'))], href='https://www.universiteitleiden.nl/en'),
                    html.A([html.Img(src=app.get_asset_url('hhs-500x500.jpg'))], href='https://www.dehaagsehogeschool.nl/'),                                                   
                    html.A([html.Img(src=app.get_asset_url('hmc-1-500x500.jpg'))], href='https://www.haaglandenmc.nl/'),  
                    html.A([html.Img(src=app.get_asset_url('haga_ziekenhuis-500x500.jpg'))], href='https://www.hagaziekenhuis.nl/home/'),
                    html.A([html.Img(src=app.get_asset_url('hadoks-1-500x500.jpg'))], href='https://www.hadoks.nl/'),
                    html.A([html.Img(src=app.get_asset_url('parnassia-500x500.jpg'))], href='https://www.parnassia.nl/'),
                    html.A([html.Img(src=app.get_asset_url('rienier_de_graaf-500x500.jpg'))], href='https://reinierdegraaf.nl/'),
                    html.A([html.Img(src=app.get_asset_url('gemeente_dh-500x500.jpg'))], href='https://www.denhaag.nl/nl.htm'),
                    ], id = 'partners', className = 'footerelement'),
            ], id = 'footer')


app.layout = html.Div([dcc.Store(id='session', storage_type='session'), navbar,    
    html.Div(html.Div(html.Div(dash.page_container, id='main', className= 'toggle'))),
    footer
])


#------------------------------------------------------ Callbacks ------------------------------------------------------

# navigation
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# language
@app.callback(
    Output('select_language', 'alt'),
    Output('select_language', 'src'),
    Output('session', 'data'),
    Input('select_language', 'alt'),
    Input('lang_select_parent', 'n_clicks'),
    prevent_initial_call=False
)
def update_language(value, clicks):

    if value == tr.Language.EN.value:
        value = tr.Language.NL.value
        flag = app.get_asset_url('flag-EN.svg')
    else:
        value = tr.Language.EN.value
        flag = app.get_asset_url('flag-NL.svg')
            
    tr.change_language(value)
    return value, flag, (value)

# localisation (chained)
@app.callback(
    Output('last_update', 'children'),
    Output('navmenu', 'children'),
    Output('footerleft', 'children'),
    Input('session', 'data')
)
def localise(language):
    last_update = (tr.translate("last update") + tr.translate_date(2024, 1, 1))
    nav =  [dcc.Link(tr.translate('Neighbourhood'), href= '/'),
            dcc.Link(tr.translate('Supply and Demand'), href='/supplydemand'),
            dcc.Link(tr.translate("Diabetes"), href="/diabetes"),
            dcc.Link(tr.translate("Palliative care"), href="/palliative"),
            dcc.Link(tr.translate("Pedriatric care"), href="/young")]
    footer = html.P([html.H1('Health Campus Den Haag'),'Turfmarkt 99', html.Br(),
                     tr.translate('3rd floor'), html.Br(), '2511 DP, Den Haag'])
    return last_update, nav, footer


if __name__ == '__main__':
    app.run_server(debug=True,  dev_tools_hot_reload=False)



