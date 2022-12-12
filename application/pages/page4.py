import dash
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import math

dash.register_page(__name__, name='Fruits')

df = pd.read_csv(r'C:\Users\User\Desktop\Grocery Track\full.csv')

def get_month(month):
    mon = ''
    if month == 1:
        mon = "Jan"
    elif month == 2:
        mon = "Feb"
    elif month == 3:
        mon = "Mar"
    elif month == 4:
        mon = "Apr"
    elif month == 5:
        mon = "May"
    elif month == 6:
        mon = "Jun"
    elif month == 7:
        mon = "Jul"
    elif month == 8:
        mon = "Aug"
    elif month == 9:
        mon = "Sep"
    elif month == 10:
        mon = "Oct"
    elif month == 11:
        mon = "Nov"
    elif month == 12:
        mon = "Dec"

    return mon

def get_mean(df,state, item, year):
    dfmean = df[(df['item'] == item) & (df['state'] == state) & (df['date'].dt.year == year)]
    dfmean = dfmean["price"].mean()
    return dfmean

def get_median(df,state, item, year):
    dfmedian = df[(df['item'] == item) & (df['state'] == state) & (df['date'].dt.year == year)]
    dfmedian = dfmedian["price"].median()
    return dfmedian

def get_var(df,state, item, year):
    dfvar = df[(df['item'] == item) & (df['state'] == state) & (df['date'].dt.year == year)]
    numb = len(dfvar['price'])
    # m will have the mean value
    m = sum(dfvar['price']) / numb
    # Square deviations
    devi = [(x - m) ** 2 for x in dfvar['price']]
    # Variance
    variance = sum(devi) / numb
    return variance

def get_std(df,state, item, year):
    var = get_var(df,state, item, year)
    std = math.sqrt(var)
    return std

#fruit list
fruitlist = {'apple fuji','pineapple','watermelon','green apple','red apple','papaya','banana'}
statelist = df['state'].unique()
df['date'] = pd.to_datetime(df['date'])
yearlist = df['date'].dt.year.unique()
monthlistall = df['date'].dt.month.unique()

layout = html.Div(
    [
        dbc.Row([
            dbc.Row([
                dbc.Col(
                    [
                        html.H3("Price Performance for selected item")
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(id='fruitDropdown',
                                     options=[{'label': x, 'value': x} for x in fruitlist],
                                     value="apple fuji", persistence = True, persistence_type = 'memory'),]),
                        dbc.Col([
                            dcc.Dropdown(id='stateDropdownfruit', multi=True,
                                         options=[{'label': x, 'value': x} for x in statelist],
                                         value=["malaysia", "johor", "selangor", "sabah", "perak", "sarawak"], persistence = True, persistence_type = 'memory')]),
                    ]),
                    ]
                )
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='overall-fruit')
                ], width=12)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id='stateDropdown2fruit',
                                 options=[{'label': x, 'value': x} for x in statelist],
                                 value="malaysia", persistence = True, persistence_type = 'memory'),
                ]),
                dbc.Col([
                    dcc.Dropdown(id='yearDropdownfruit',
                                 options=[{'label': x, 'value': x} for x in yearlist],
                                 value=2021, persistence = True, persistence_type = 'memory'),
                ])
            ]),
                dbc.Row([
                    dcc.Graph(id='bar-fig-fruit')
                ]),
                dbc.Row([
                    html.Br(),
                    html.Div(id="calnum5", children='', style={}),
                    html.Div(id="calnum6", children='', style={}),
                    html.Div(id="calnum7", children='', style={}),
                    html.Div(id="calnum8", children='', style={}),
html.Br(),
html.Br(),
                ])

                ], width=7
            ),
            dbc.Col([
dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options = [{'label': x, 'value': x} for x in monthlistall], id='monthdropdownfruit', value = 1, persistence = True, persistence_type = 'memory'),
                    html.Br(),
                    html.Br(),
                ])
    ]),
                dbc.Row([dbc.Row([
                html.Div(id = 'fruittitleline',children='',style = {'fontsize':'25px', 'textAlign':'center'}),
html.Br(),
html.Br()
            ]),
            dbc.Row([
               dbc.Col([
                   html.Div(id = 'top1fruit',children = '')
               ]),
                dbc.Col([
                   html.Div(id = 'top1fruitprice',children = '')
               ]),
                html.Br()
            ]),
            dbc.Row([
                dbc.Col([
                   html.Div(id = 'top2fruit',children = '')
               ]),
                dbc.Col([
                   html.Div(id = 'top2fruitprice',children = '')
               ]),
                html.Br()
            ]),
            dbc.Row([
                dbc.Col([
                   html.Div(id = 'top3fruit',children = '')
               ]),
                dbc.Col([
                   html.Div(id = 'top3fruitprice',children = '')
               ]),
                html.Br()
            ]),
            dbc.Row([
                dbc.Col([
                   html.Div(id = 'top4fruit',children = '')
               ]),
                dbc.Col([
                   html.Div(id = 'top4fruitprice',children = '')
               ]),
                html.Br()
            ]),
            dbc.Row([
                dbc.Col([
                   html.Div(id = 'top5fruit',children = '')
               ]),
                dbc.Col([
                   html.Div(id = 'top5fruitprice',children = '')
               ]),])
                    ]),
                dbc.Row([html.Hr(style={'borderWidth': "0.3vh", "width": "100%", "color": "#FEC700"}),]),
                dbc.Row([
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.H4("Growth Rate of Selected Item", className="card-title"),
                                    html.P("The price and result are only for reference.",
                                           style={'textAlign': 'right'}),
                                    dcc.Dropdown(id='fruitDropdown2',
                                     options=[{'label': x, 'value': x} for x in fruitlist],
                                     value="apple fuji", persistence = True, persistence_type = 'memory'),
                                    dcc.Dropdown(id='stateDropdown3fruit',
                                     options=[{'label': x, 'value': x} for x in statelist],
                                     value="malaysia", persistence = True, persistence_type = 'memory'),
                                    html.Br(),
                                    html.Div(id="fruitsentence1", children='', style={}),
                                    html.Div(id="fruitsentence2", children='', style={}),
                                    html.Div(id="fruitsentence3", children='', style={}),
                                    html.Div(id="fruitsentence4", children='', style={}),
                                ]
                            ),
                        ],
                        style={"height": "22rem"},
                    )
                ]
            ),
                ], width=4)
            ]),
        ])

@callback(
    [Output(component_id='overall-fruit', component_property='figure')],
    [Input(component_id='fruitDropdown', component_property='value'), Input(component_id='stateDropdownfruit', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph(item_chosen, state_chosen):
    if len(state_chosen) == 0:
        return dash.no_update
    elif type(state_chosen)==str:
        dffiltered = df[(df['item'] == item_chosen) & (df['state']==state_chosen)]
        fig = px.line(dffiltered, x="date", y="price", color='state')
        return [fig]
    else:
        dffiltered = df[(df['item'] == item_chosen) &(df['state'].isin(state_chosen))]
        fig = px.line(dffiltered, x="date", y="price", color='state')
        # fig.update_layout(title={'text':'vegetables price trend'})
        return [fig]

@callback(
    [Output(component_id='bar-fig-fruit', component_property='figure')],
    [Input(component_id='stateDropdown2fruit', component_property='value'), Input(component_id='yearDropdownfruit', component_property='value')
     , Input(component_id='fruitDropdown', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph(state_chosen, year_chosen, item_chosen):
    if len(state_chosen) == 0 | len(item_chosen) == 0:
        return dash.no_update
    else:
        dffiltered = df[(df['item'] == item_chosen) & (df['state']==state_chosen) & (df['date'].dt.year == year_chosen)]
        fig = px.line(dffiltered, x="date", y="price")
        fig.update_layout(title={'text':'monthly price trend'})
        y = get_mean(dffiltered, state_chosen, item_chosen, year_chosen)
        fig.add_hline(y=y, line_dash="dash", line_color="green", annotation_text=round(y,2))
        return [fig]

@callback(
    [Output('fruitsentence1', 'children'), Output('fruitsentence2', 'children'), Output('fruitsentence3', 'children'), Output('fruitsentence4', 'children')],
    [Input('fruitDropdown2', 'value'), Input('stateDropdown3fruit', 'value')],
    prevent_initial_call=False
)
def update_my_words(item_chosen, state_chosen):
    if len(item_chosen) == 0 | len(state_chosen) == 0:
        return dash.no_update

    resultlist = []
    meanlist=[]

    for i in yearlist:
        mean = get_mean(df, state_chosen, item_chosen, i)
        meanlist.append(mean)
        i+1

    for i in yearlist:
        y1 = get_mean(df, state_chosen, item_chosen, i)
        if i !=2022:
            y2 = get_mean(df, state_chosen, item_chosen, i+1)
            rate = ((y2/y1)-1)*100
            resultlist.append(round(rate,2))
            i + 1

    y1 = get_mean(df, state_chosen, item_chosen, min(yearlist))
    y2 = get_mean(df, state_chosen, item_chosen, max(yearlist))
    res = round(((y2/y1)-1)*100,2)

    return '2020 growth rate based on 2019 : {} %'.format(resultlist[0]), '2021 growth rate based on 2020 : {} %'.format(resultlist[1]), '2021 growth rate based on 2022 : {} %'.format(resultlist[2]), 'Overall : 2022 growth rate based on 2019 : {} %'.format(res)

@callback(
    [Output('calnum5', 'children'), Output('calnum6', 'children'), Output('calnum7', 'children'), Output('calnum8', 'children')],
    [Input(component_id='stateDropdown2fruit', component_property='value'), Input(component_id='yearDropdownfruit', component_property='value')
     , Input(component_id='fruitDropdown', component_property='value')],
    prevent_initial_call=False
)
def update_my_stats(state_chosen, year_chosen, item_chosen):
    if len(state_chosen) == 0 | len(item_chosen) == 0:
        return dash.no_update
    else:
        dffiltered = df[(df['item'] == item_chosen) & (df['state']==state_chosen) & (df['date'].dt.year == year_chosen)]
        y = get_mean(dffiltered, state_chosen, item_chosen, year_chosen)
        var = get_var(dffiltered, state_chosen, item_chosen, year_chosen)
        std = get_std(dffiltered, state_chosen, item_chosen, year_chosen)

        return 'The mean(average) price for the year is {}'.format(round(y,4)), 'The median price for the year is {}'.format(round(get_median(dffiltered, state_chosen, item_chosen, year_chosen),4)), 'The variance price for the year is {}'.format(round(var,4)), 'The standard deviation price for the year is {}'.format(round(std,4))

@callback(
    [Output('fruittitleline', 'children'), Output('top1fruit', 'children'), Output('top1fruitprice', 'children'),
     Output('top2fruit', 'children'), Output('top2fruitprice', 'children'), Output('top3fruit', 'children'),
     Output('top3fruitprice', 'children'), Output('top4fruit', 'children'), Output('top4fruitprice', 'children'),
     Output('top5fruit', 'children'), Output('top5fruitprice', 'children')],
    [Input('stateDropdown2fruit', 'value'), Input('yearDropdownfruit', 'value'),Input('monthdropdownfruit', 'value')],
    prevent_initial_call=False
)
def update_topvegelist(state_chosen, year_chosen, month_chosen):
    dffiltered = df[(df['state'] == state_chosen)]
    dffiltered = dffiltered[(dffiltered['date'].dt.year == year_chosen)]
    dffiltered = dffiltered[(dffiltered['date'].dt.month == month_chosen)]
    dffiltered = dffiltered[dffiltered['item'].isin(fruitlist)]

    dffiltered = dffiltered.sort_values("price")
    mon=get_month(month_chosen)

    return 'The Top 5 fruit in {} {}'.format(mon, year_chosen), dffiltered['item'].iloc[0], dffiltered['price'].iloc[0], dffiltered['item'].iloc[1], dffiltered['price'].iloc[1], dffiltered['item'].iloc[2], dffiltered['price'].iloc[2], dffiltered['item'].iloc[3], dffiltered['price'].iloc[3], dffiltered['item'].iloc[4], dffiltered['price'].iloc[4]