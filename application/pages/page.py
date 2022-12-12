import dash
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table
from datetime import date

#For model
import pandas as pd
import numpy as np
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
from sklearn.svm import SVC
from sklearn.svm import SVR

import json
# with urlopen('https://raw.githubusercontent.com/wmgeolab/geoBoundaries/3cef88c3d9fd8edbde3ff8a6d9b03eb0f43dff63/releaseData/gbOpen/MYS/ADM1/geoBoundaries-MYS-ADM1_simplified.geojson') as response:
#     counties = json.load(response)

# with open(r'C:\Users\User\PycharmProjects\groceryTrack\assets\map.geojson') as data_file:
#     data = json.load(data_file)

dash.register_page(__name__, path='/', name='Home')

#Read Data
df = pd.read_csv(r'C:\Users\User\Desktop\Grocery Track\full.csv')

#Model stuff
def rmse(predictions, targets):
    return ((predictions - targets) ** 2).mean()

#For train data
data = pd.read_csv(r'C:\Users\User\Desktop\Grocery Track\trainer2.csv', parse_dates=True)
data['date'] = pd.to_datetime(data['date'])
data = data.groupby(['item', 'state', 'date']).sum('price')
data.reset_index(inplace=True)

data_list = []

for i in data['item'].unique():
    for n in data['state']. unique():
        data_list.append(data[(data['item'] == i) & (data['state'] == n)])

for i in range(len(data_list)):
    data_list[i]['Last_1_month_price'] = data_list[i]['price'].shift(1)
    data_list[i]['Last_2_month_price'] = data_list[i]['price'].shift(2)
    data_list[i]['Last_3_month_price'] = data_list[i]['price'].shift(3)

data = pd.DataFrame()

for i in range(len(data_list)):
    data = pd.concat([data, data_list[i]])
    print(data)

data.dropna(inplace=True)

le1 = preprocessing.LabelEncoder()
data['item']= le1.fit_transform(data['item'])

le2 = preprocessing.LabelEncoder()
data['state']= le2.fit_transform(data['state'])

Xtraindata = data.drop(['price','date'],axis=1)
ytraindata = data['price']

#For test data
testdata = pd.read_csv(r'C:\Users\User\Desktop\Grocery Track\tester2.csv', parse_dates=True)
testdata.head()

testdata['date'] = pd.to_datetime(testdata['date'])
testdata = testdata.groupby(['item', 'state', 'date']).sum('price')

testdata.reset_index(inplace=True)

testdata_list = []

for i in testdata['item'].unique():
    for n in testdata['state']. unique():
        testdata_list.append(testdata[(testdata['item'] == i) & (testdata['state'] == n)])

for i in range(len(testdata_list)):
    testdata_list[i]['Last_1_month_price'] = testdata_list[i]['price'].shift(1)
    testdata_list[i]['Last_2_month_price'] = testdata_list[i]['price'].shift(2)
    testdata_list[i]['Last_3_month_price'] = testdata_list[i]['price'].shift(3)

testdata = pd.DataFrame()

for i in range(len(testdata_list)):
    testdata = pd.concat([testdata, testdata_list[i]])
    print(testdata)

testdata.dropna(inplace=True)

testdata['item']= le1.fit_transform(testdata['item'])
testdata['state']= le2.fit_transform(testdata['state'])

Xtestdata = testdata.drop(['price','date'],axis=1)
ytestdata = testdata['price']

#SVM model
regressor = SVR(kernel = 'rbf')
svmtrainpredict = regressor.fit(Xtraindata, ytraindata)

y_pred = regressor.predict(Xtestdata)

def get_mean2years(df,state, item, year1, year2):
    dfy1 = df[(df['date'].dt.year == year1)]
    dfy2 = df[(df['date'].dt.year == year2)]
    date1 = max(dfy1['date'])
    date2 = min(dfy2['date'])
    dfmean = df[(df['date'] > date2) & (df['date'] <= date1)]
    dfmean = dfmean[(dfmean['item'] == item) & (dfmean['state'] == state)]
    mean = dfmean["price"].mean()
    return mean

itemlistall = df['item'].unique()
statelistall = df['state'].unique()
catlistall = ['vegetables', 'fruits','meats & seafoods']
df['date'] = pd.to_datetime(df['date'])
yearlistall = df['date'].dt.year.unique()
all_options = {
    'vegetables': ['spinach','ladies fingers','tomatoes','red chilli (kulai)','long beans','french bean','round cabbage','cauliflower','carrot','cucumber'],
    'fruits': ['apple fuji','pineapple','watermelon','green apple','red apple','papaya','banana'],
    'meats & seafoods': ['chicken','beef','siakap fish','prawn','cuttlefish','crab','black pomfret (fish)','hardtail scad (fish)','indian mackerel (fish)','threadfin bream (fish)','red snapper (fish)','spanish mackerel, batang (fish)','longtail tuna, black (fish)','selayang (fish)'],
}
encode_options_item = {
    'spinach':'27',
    'ladies fingers':'14',
    'tomatoes':'29',
    'red chilli (kulai)':'21',
    'long beans':'15',
    'french bean':'10',
    'round cabbage':'23',
    'cauliflower':'5',
    'carrot':'4',
    'cucumber':'8',
    'apple fuji':'0',
    'pineapple':'18',
    'watermelon':'30',
    'green apple':'11',
    'red apple':'20',
    'papaya':'17',
    'banana':'1',
    'chicken':'6',
    'beef':'2',
    'siakap fish':'25',
    'prawn':'19',
    'cuttlefish':'9',
    'crab':'7',
    'black pomfret (fish)':'3',
    'hardtail scad (fish)':'12',
    'indian mackerel (fish)':'13',
    'threadfin bream (fish)':'28',
    'red snapper (fish)':'22',
    'spanish mackerel, batang (fish)':'26',
    'longtail tuna, black (fish)':'16',
    'selayang (fish)':'24',
}

encode_options_state = {
    'johor':'0',
    'malaysia':'1',
    'perak':'2',
    'sabah':'3',
    'sarawak':'4',
    'selangor':'5',
}

layout = html.Div(
    [
        dbc.Row([
                dbc.Col([
                        html.H3("Overall Dashboard")
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
            dbc.Col([
                dcc.Dropdown(id='itemDropdownall',
                             options=[{'label': x, 'value': x} for x in itemlistall],
                             value="spinach", persistence=True, persistence_type='memory'),
                    ])
            ]
        ),
        dbc.Row([
            dbc.Col([dash_table.DataTable(id='tableall',fill_width=False,style_table={'overflowX': 'auto','overflowY': 'auto'}),]),
                dbc.Col([
                    dcc.Graph(id='themap')
                    ], width=8
                ),
            html.Br(),html.Br(),html.Br()
            ]
        ),
        dbc.Row(
            [
                dbc.Row(
            [
                # Price calculator
                dbc.Col(
                    dbc.Card([
                            dbc.CardBody(
                                [
                                    html.H4("Price Calculator", className="card-title"),
                                    html.P("The price and result are only for reference.",
                                           style={'textAlign': 'right'}),
                                    html.P(
                                        "Item Category : ",
                                        className="card-text",
                                    ),
                                    dcc.Dropdown(id='itemDropdowncat',
                                                 options=[{'label': x, 'value': x} for x in catlistall],
                                                 value="spinach", persistence=True, persistence_type='memory'),
                                    html.Br(),
                                    html.P(
                                        "Type of Item : ",
                                        className="card-text",
                                    ),
                                    dcc.Dropdown(id='itemDropdownall0',
                                                 options=[{'label': x, 'value': x} for x in itemlistall],
                                                 value="", persistence=True, persistence_type='memory',disabled = True),
                                    html.Br(),
                                    html.P(
                                        "Item Price : ",
                                        className="card-text",
                                    ),
                                    dcc.Input(id="inputcal", type="number", debounce = False),
                                    html.Br(),
                                    html.Br(),
                                    dbc.Button("Calculate", color="primary", id="calbut"),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.Br(),
                                    html.P(
                                        "Average Price : ",
                                        className="price-text1",
                                    ),
                                    html.Div(id="allsentence1", children='', style={}),
                                    html.Br(),
                                    html.P(
                                        "Received Price : ",
                                        className="price-text2",
                                    ),
                                    html.Div(id="allsentence2", children='', style={}),
                                    html.Br(),
                                    html.Div(id="allsentence3", children='', style={'textAlign': 'center', 'color': 'blue', 'fontSize': '30px'})
                                ]
                            ),
                        ],
                        style={"width": "35rem", "height": "45rem"},
                    )
                ),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(id='preDropdown',
                                         options=[{'label': x, 'value': x} for x in itemlistall],
                                         value="spinach", persistence=True, persistence_type='memory'),
                        ]),
                        dbc.Col([
                            dcc.Dropdown(id='stateDropdownpre',
                                         options=[{'label': x, 'value': x} for x in statelistall],
                                         value="malaysia",
                                         persistence=True, persistence_type='memory')
                        ])
                    ]),
                    dbc.Row([
                        dcc.Graph(id='predict')]),
                    dbc.Row([
                        html.H4(id = 'msevalue', children=("MSE Value : 2.6787803450847707"),style={'textAlign': 'center', 'color': 'blue', 'fontSize': '18px'}),
                    ]),
]),
            ]
        )
    ]
)
        ]
)

@callback(
    [Output(component_id='themap', component_property='figure')],
    [Input(component_id='itemDropdownall', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph(item_chosen):
    if len(item_chosen) == 0:
        return dash.no_update
    else:
        dffiltered = df[(df['item'] == item_chosen)]
        dfnew = pd.DataFrame(columns=["state", "price"])

        for x in statelistall:
            dfmean = dffiltered[dffiltered['state'] == x]
            dfmean = dfmean["price"].mean()

            addnewlist = [x, dfmean]
            dfnew.loc[len(dfnew)] = addnewlist

        dfnew = dfnew.assign(country='MYS')
        dfnomas = dfnew[dfnew['state'] != 'malaysia']
        # dfnomas['price'] = round(dfnomas['price'],2)

        fig2 = px.scatter_geo(dfnomas, locations="country", size="price")
        return [fig2]

@callback(
    [Output(component_id='itemDropdownall0', component_property='options'),Output(component_id='itemDropdownall0', component_property='disabled')],
    [Input(component_id='itemDropdowncat', component_property='value')],
    prevent_initial_call=True
)
def update_my_dropdown(cat_chosen):
    if len(cat_chosen) == 0:
        return dash.no_update
    else:
        return [{'label': i, 'value': i} for i in all_options[cat_chosen]], False

@callback(
    [Output('allsentence1', 'children'), Output('allsentence2', 'children'), Output('allsentence3', 'children')],
    [Input('calbut', 'n_clicks')],
    [State('inputcal', 'value'), State('itemDropdownall', 'value')],
    prevent_initial_call=True
)
def update_my_dropdown(_, input_price, item_chosen):
    if len(item_chosen) == 0:
        return dash.no_update
    else:
        meannum = get_mean2years(df, "malaysia", item_chosen, max(yearlistall), max(yearlistall) - 1)
        percentage = ((input_price/meannum) - 1) * 100
        return round(meannum,2), round(input_price,2), '{} %'.format(round(percentage, 4))

@callback(
    Output(component_id='tableall', component_property='data'),
    [Input(component_id='itemDropdownall', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph(item_chosen):
    if len(item_chosen) == 0:
        return dash.no_update
    else:
        dffiltered = df[(df['item'] == item_chosen)]
        dfnew = pd.DataFrame(columns=["state", "mean price", "min(price)", "max(price)"])

        for x in statelistall:
            dfmean = dffiltered[dffiltered['state'] == x]
            meanvalue = dfmean["price"].mean()
            dfmin = min(dfmean['price'])
            dfmax = max(dfmean['price'])

            addnewlist = [x, meanvalue, dfmin, dfmax]
            dfnew.loc[len(dfnew)] = addnewlist

        dfnew = dfnew.assign(country='MYS')
        # dfnomas = dfnew[dfnew['state'] != 'malaysia']
        dfnew['mean price'] = round(dfnew['mean price'],2)
        dfnew = dfnew.drop(['country'], axis=1)

        data = dfnew.to_dict('records')

        return data

@callback(
    [Output(component_id='predict', component_property='figure')],
    [Input(component_id='preDropdown', component_property='value'), Input(component_id='stateDropdownpre', component_property='value')],
    prevent_initial_call=False
)
def update_my_predict_graph(item_chosen, state_chosen):
    if len(state_chosen) == 0:
        return dash.no_update
    elif type(state_chosen)==str:
        dffiltered = df[(df['item'] == item_chosen) & (df['state']==state_chosen)]
        dffiltered = dffiltered[(dffiltered['date'].dt.year == 2022)]

        item = encode_options_item[item_chosen]
        state = encode_options_state[state_chosen]

        #For oct prediction (7,8,9)
        mon1 = dffiltered['price'].iloc[6]
        mon2 = dffiltered['price'].iloc[7]
        mon3 = dffiltered['price'].iloc[8]

        pre_oct = regressor.predict(np.array([item, state, mon1, mon2, mon3]).reshape(1, -1))

        # For nov prediction (8,9,10)
        mon1 = mon2.copy()
        mon2 = mon3.copy()
        mon3 = pre_oct[0].copy()

        pre_nov = regressor.predict(np.array([item, state, mon1, mon2, mon3]).reshape(1, -1))

        # For nov prediction (9,10,11)
        mon1 = mon2.copy()
        mon2 = pre_oct[0].copy()
        mon3 = pre_nov[0].copy()

        pre_dec = regressor.predict(np.array([item, state, mon1, mon2, mon3]).reshape(1, -1))

        data = {'item': [item_chosen,item_chosen,item_chosen], 'state': [state_chosen,state_chosen,state_chosen], 'date': ['10/1/2022','11/1/2022','12/1/2022'], 'price': [pre_oct[0],pre_nov[0],pre_dec[0]]}
        dfback = pd.DataFrame(data)
        dfback['date'] = pd.to_datetime(dfback['date'])

        df_merged = pd.concat([dffiltered, dfback])
        print(df_merged)

        fig = px.line(df_merged, x="date", y="price", color='state')

        fig.add_vrect(x0="2022-10-01", x1="2022-12-01",
                      annotation_text="predicted", annotation_position="top left",
                      fillcolor="red", opacity=0.25, line_width=0)

        fig.update_layout(title={'text': 'Predicted Result for selected item in selected state'})
        return [fig]