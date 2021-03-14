
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

con = create_engine("postgres://ptivzjrbexcqrd:7c1a0c9ea6b72bafb091664f01a7b26ddadd3b2e35e7e0d14a28a7536e7b9ff8@ec2-54-155-35-88.eu-west-1.compute.amazonaws.com:5432/de9ca2ec3ia53s")

qg = "select date,value,parameter,year,station from geo_tbl ;"
qm = "select date,value,parameter,year,station from mag_tbl ;"
qr = "select date,value,parameter,year,station from rad_tbl ;"
qw = "select date,value,parameter,year,station from wat_tbl ;"

dg = pd.read_sql(qg, con)
dg['date'] = pd.to_datetime(dg['date'],format='%m/%d/%y')

dg['value'] = dg['value'].astype('float')
dg['year'] = dg['year'].astype('int')
dg['parameter'] = dg['parameter'].astype('string')
dg.head()

dg['Month'] = dg['date'].dt.month
dg['Days'] = dg['date'].dt.day

d = {1:'Jan' ,2:'Feb' ,3:'Mar' ,4:'Apr' ,5:'May' ,6:'Jun' ,7:'Jul' ,8:'Aug' ,9:'Sep' ,10:'Oct' ,11:'Nov' ,12:'Dec'}
dg['Month'] = dg['Month'].map(d)

dg['Days']=dg['Days'].astype(str)
dg['Month'] = dg['Month'].astype('string')
dg['station']=dg['station'].astype('string')

dg['period'] = dg['Month'] + dg['Days']
dg.head()

dm = pd.read_sql(qm, con)
dm['date'] = pd.to_datetime(dm['date'],format='%m/%d/%y')

dm['value'] = dm['value'].astype('float')
dm['year'] = dm['year'].astype('int')
dm['parameter'] = dm['parameter'].astype('string')
dm.head()

dm['Month'] = dm['date'].dt.month
dm['Days'] = dm['date'].dt.day
dm['Month'] = dm['Month'].map(d)

dm['Days']=dm['Days'].astype(str)
dm['Month'] = dm['Month'].astype('string')
dm['station']=dm['station'].astype('string')

dm['period'] = dm['Month'] + dm['Days']
dm.head()

dr = pd.read_sql(qr, con)
dr['date'] = pd.to_datetime(dr['date'],format='%m/%d/%y')

dr['value'] = dr['value'].astype('float')
dr['year'] = dr['year'].astype('int')
dr['parameter'] = dr['parameter'].astype('string')
dr.head()

dr['Month'] = dr['date'].dt.month
dr['Days'] = dr['date'].dt.day
dr['Month'] = dr['Month'].map(d)

dr['Days']=dr['Days'].astype(str)
dr['Month'] = dr['Month'].astype('string')
dr['station']=dr['station'].astype('string')

dr['period'] = dr['Month'] + dr['Days']
dr.head()

dw = pd.read_sql(qw, con)
dw['date'] = pd.to_datetime(dw['date'],format='%m/%d/%y')

dw['value'] = dw['value'].astype('float')
dw['year'] = dw['year'].astype('int')
dw['parameter'] = dw['parameter'].astype('string')
dw.head()

dw['Month'] = dw['date'].dt.month
dw['Days'] = dw['date'].dt.day
dw['Month'] = dw['Month'].map(d)

dw['Days']=dw['Days'].astype(str)
dw['Month'] = dw['Month'].astype('string')
dw['station']=dw['station'].astype('string')

dw['period'] = dw['Month'] + dw['Days']
dw.head()

mov_avg = [2,3,4,5,6,7,8,9,10]
grph_mode = ['Continuous' , 'By year']

app = dash.Dash(__name__ , external_stylesheets = [dbc.themes.FLATLY])
server = app.server

#auth = dash_auth.BasicAuth(
#app,
#   {'G11':'Gowtham11'})

controls1 = dbc.Card(
    [
        #dbc.CardHeader(" "),
        
        dbc.FormGroup(
            [
                dbc.Label("Timeline of the Graph:"),
                dcc.DatePickerRange(id = 'date-picker1',
                                    start_date_placeholder_text = "Start Date",
                                    end_date_placeholder_text = "End Date",
                                    start_date = dg['date'].iloc[0],
                                    end_date = dg['date'].iloc[-1],
                                    clearable=True,
                                    initial_visible_month= dg['date'].iloc[0],
                                   ),
            ]
        ),
        
        
        dbc.FormGroup(
            [
                dbc.Label("Select Station:"),
                dcc.Dropdown(id = 'select_station1',
                                    multi = False,
                                    clearable=True,
                                    disabled = False,
                                    style = {'display': True},
                                    placeholder = 'Select station',
                                    options = [{'label': i, 'value': i} for i in dg['station'].unique()]
                                   ),
            ]
        ),
        
        
        dbc.FormGroup(
            [
                dbc.Label("Select Parameter:"),
                dcc.Dropdown(id = 'select_parameter1',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select parameter',
                             options = [{'label': i, 'value': i} for i in dg['parameter'].unique()]
                            ),
            ]
        ),
        
         dbc.FormGroup(
            [
                dbc.Label("Select Graph Mode:"),
                dcc.Dropdown(id = 'select_mode1',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select mode',
                             options = [{'label': i, 'value': i} for i in grph_mode]
                            ),
            ]
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Moving Average:"),
                dcc.Dropdown(id = 'avg_value1',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select No of days',
                             options = [{'label': i, 'value': i} for i in mov_avg]
                            ),
            ]
        ),
    ],
    color="light",outline=True,style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"},
    body=True
)

controls2 = dbc.Card(
    [
        #dbc.CardHeader(" "),
        
        dbc.FormGroup(
            [
                dbc.Label("Timeline of the Graph:"),
                dcc.DatePickerRange(id = 'date-picker2',
                                    start_date_placeholder_text = "Start Date",
                                    end_date_placeholder_text = "End Date",
                                    start_date = dm['date'].iloc[0],
                                    end_date = dm['date'].iloc[-1],
                                    clearable=True,
                                    initial_visible_month= dm['date'].iloc[0],
                                   ),
            ]
        ),
        
        
        dbc.FormGroup(
            [
                dbc.Label("Select Station:"),
                dcc.Dropdown(id = 'select_station2',
                                    multi = False,
                                    clearable=True,
                                    disabled = False,
                                    style = {'display': True},
                                    placeholder = 'Select station',
                                    options = [{'label': i, 'value': i} for i in dm['station'].unique()]
                                   ),
            ]
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Select Parameter:"),
                dcc.Dropdown(id = 'select_parameter2',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select parameter',
                             options = [{'label': i, 'value': i} for i in dm['parameter'].unique()]
                            ),
            ]
        ),
        
        
        
         dbc.FormGroup(
            [
                dbc.Label("Select Graph Mode:"),
                dcc.Dropdown(id = 'select_mode2',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select mode',
                             options = [{'label': i, 'value': i} for i in grph_mode]
                            ),
            ]
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Moving Average:"),
                dcc.Dropdown(id = 'avg_value2',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select No of days',
                             options = [{'label': i, 'value': i} for i in mov_avg]
                            ),
            ]
        ),
    ],
    color="light",outline=True,style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"},
    body=True
)

controls3 = dbc.Card(
    [
        #dbc.CardHeader(" "),
        
        dbc.FormGroup(
            [
                dbc.Label("Timeline of the Graph:"),
                dcc.DatePickerRange(id = 'date-picker3',
                                    start_date_placeholder_text = "Start Date",
                                    end_date_placeholder_text = "End Date",
                                    start_date = dr['date'].iloc[0],
                                    end_date = dr['date'].iloc[-1],
                                    clearable=True,
                                    initial_visible_month= dr['date'].iloc[0],
                                   ),
            ]
        ),
        
        
        dbc.FormGroup(
            [
                dbc.Label("Select Station:"),
                dcc.Dropdown(id = 'select_station3',
                                    multi = False,
                                    clearable=True,
                                    disabled = False,
                                    style = {'display': True},
                                    placeholder = 'Select station',
                                    options = [{'label': i, 'value': i} for i in dr['station'].unique()]
                                   ),
            ]
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Select Parameter:"),
                dcc.Dropdown(id = 'select_parameter3',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select parameter',
                             options = [{'label': i, 'value': i} for i in dr['parameter'].unique()]
                            ),
            ]
        ),
        
        
         dbc.FormGroup(
            [
                dbc.Label("Select Graph Mode:"),
                dcc.Dropdown(id = 'select_mode3',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select mode',
                             options = [{'label': i, 'value': i} for i in grph_mode]
                            ),
            ]
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Moving Average:"),
                dcc.Dropdown(id = 'avg_value3',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select No of days',
                             options = [{'label': i, 'value': i} for i in mov_avg]
                            ),
            ]
        ),
    ],
    color="light",outline=True,style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"},
    body=True
)

controls4 = dbc.Card(
    [
        #dbc.CardHeader(" "),
        
        dbc.FormGroup(
            [
                dbc.Label("Timeline of the Graph:"),
                dcc.DatePickerRange(id = 'date-picker4',
                                    start_date_placeholder_text = "Start Date",
                                    end_date_placeholder_text = "End Date",
                                    start_date = dw['date'].iloc[0],
                                    end_date = dw['date'].iloc[-1],
                                    clearable=True,
                                    initial_visible_month= dw['date'].iloc[0],
                                   ),
            ]
        ),
        
        
        dbc.FormGroup(
            [
                dbc.Label("Select Station:"),
                dcc.Dropdown(id = 'select_station4',
                                    multi = False,
                                    clearable=True,
                                    disabled = False,
                                    style = {'display': True},
                                    placeholder = 'Select station',
                                    options = [{'label': i, 'value': i} for i in dw['station'].unique()]
                                   ),
            ]
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Select Parameter:"),
                dcc.Dropdown(id = 'select_parameter4',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select parameter',
                             options = [{'label': i, 'value': i} for i in dw['parameter'].unique()]
                            ),
            ]
        ),
              
         dbc.FormGroup(
            [
                dbc.Label("Select Graph Mode:"),
                dcc.Dropdown(id = 'select_mode4',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select mode',
                             options = [{'label': i, 'value': i} for i in grph_mode]
                            ),
            ]
        ),
        
        dbc.FormGroup(
            [
                dbc.Label("Moving Average:"),
                dcc.Dropdown(id = 'avg_value4',
                             multi = False,
                             clearable = True,
                             disabled = False,
                             style = {'display': True},
                             placeholder = 'Select No of days',
                             options = [{'label': i, 'value': i} for i in mov_avg]
                            ),
            ]
        ),
    ],
    color="light",outline=True,style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"},
    body=True
)

app.layout = dbc.Container(
    [
        html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"}
                ),
        
              
        html.Div(" ",style={'padding': 15}),
        
        html.H2("Seismic Activity-GEO"),
        
        html.Hr(),
        
        html.Div(" ",style={'padding': 20}),
        
        dbc.Row(
            [
                dbc.Col(controls1, md=3),
                dbc.Col(dbc.Card(dcc.Graph(id = 'l1'),
                                 color="light",
                                 outline=True,
                                 style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"}
                        ),
                ),
            ],
            align="center",
        ),
        
        html.Div(" ",style={'padding': 15}),
        
        html.Hr(),
        
        html.Div(" ",style={'padding': 25}),
        
        html.H2("Seismic Activity-MAG"),
        
        html.Hr(),
        
        html.Div(" ",style={'padding': 20}),
        
        dbc.Row(
            [
                dbc.Col(controls2, md=3),
                dbc.Col(dbc.Card(dcc.Graph(id = 'l2'),
                                 color="light",
                                 outline=True,
                                 style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"}
                        ),
                ),
            ],
            align="center",
        ),
        
        html.Div(" ",style={'padding': 15}),
        
        html.Hr(),
        
        html.Div(" ",style={'padding': 25}),
        
        html.H2("Seismic Activity-RAD"),
        
        html.Hr(),
        
        html.Div(" ",style={'padding': 20}),
        
        dbc.Row(
            [
                dbc.Col(controls3, md=3),
                dbc.Col(dbc.Card(dcc.Graph(id = 'l3'),
                                 color="light",
                                 outline=True,
                                 style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"}
                        ),
                ),
            ],
            align="center",
        ),
        
        html.Div(" ",style={'padding': 15}),
        
        html.Hr(),
        
        html.Div(" ",style={'padding': 25}),
        
        html.H2("Seismic Activity-WAT"),
        
        html.Hr(),
        
        html.Div(" ",style={'padding': 20}),
        
        dbc.Row(
            [
                dbc.Col(controls4, md=3),
                dbc.Col(dbc.Card(dcc.Graph(id = 'l4'),
                                 color="light",
                                 outline=True,
                                 style={"box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)"}
                        ),
                ),
            ],
            align="center",
        ),
        
        html.Div(" ",style={'padding': 35}),
       
    ],
    fluid=True,
)

@app.callback(Output('l1', 'figure'),
             [Input('date-picker1' , 'start_date'),
              Input('date-picker1' , 'end_date'),
              Input('select_station1','value'),
              Input('select_parameter1', 'value'),
              Input('select_mode1', 'value'),
              Input('avg_value1', 'value')])

def update_graph1(start_date , end_date , select_station , select_parameter , select_mode , avg_value):
    
    
    data1 = dg[((dg['date'] > start_date) & (dg['date'] < end_date)) & (dg['station'] == select_station)]
    
    data2 = data1[data1['parameter']==select_parameter]

    figure = None
    
    if select_mode == 'Continuous' :
        
        trace_1 = go.Scatter(x = data2['date'] , y = data2['value'] , line_color = "#461B7E",showlegend=True,name='Values')
    
        data2['rolling_mean'] = data2['value'].rolling(window=avg_value).mean()
    
        trace_2 = go.Scatter(x = data2['date'] , y = data2['rolling_mean'] , line_color = "#00CED1",showlegend=True,
                         name='Average')
    
        figure = go.Figure(data = [trace_1,trace_2])
                       
        figure.update_xaxes(ticklabelmode = "period", rangeslider_visible = True , autorange = True)
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_parameter)
    
           
    elif select_mode == 'By year' :
        
        year = data2['year'].unique()

        t=[]
        
        for y in year :
            
            dfy = data2[data2.year == y].copy()
    
            dfy['avg'] = dfy['value'].mean()
    
            traces = go.Scatter(
                                x = dfy.period,
                                y = dfy.value,
                                mode = "lines",
                                name=str(y),
                                showlegend=True
                     )
    
            trg = go.Scatter(
                             x = dfy.period,
                             y = dfy.avg,
                             mode = "lines",
                             name=str(y)+'avg',
                             showlegend= True,
                             line={'dash': 'dash'}
                  )
    
            t.append(traces)
    
            t.append(trg)
        
        figure = go.Figure(data = t)
        
        figure.update_xaxes(rangeslider_visible = True )
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_parameter)
    
    return figure

@app.callback(Output('l2', 'figure'),
             [Input('date-picker2' , 'start_date'),
              Input('date-picker2' , 'end_date'),
              Input('select_station2', 'value'),
              Input('select_parameter2','value'),
              Input('select_mode2', 'value'),
              Input('avg_value2', 'value')])

def update_graph2(start_date , end_date , select_station2 ,select_parameter2 , select_mode , avg_value):
    
    
    data1 = dm[((dm['date'] > start_date) & (dm['date'] < end_date)) & (dm['station'] == select_station2)]
    
    data2 = data1[data1['parameter']==select_parameter2]
    
    if select_mode == 'Continuous' :
        
        trace_1 = go.Scatter(x = data2['date'] , y = data2['value'] , line_color = "#461B7E",showlegend=True,name='Values')
    
        data2['rolling_mean'] = data2['value'].rolling(window=avg_value).mean()
    
        trace_2 = go.Scatter(x = data2['date'] , y = data2['rolling_mean'] , line_color = "#00CED1",showlegend=True,
                         name='Average')
    
        figure = go.Figure(data = [trace_1,trace_2])
                       
        figure.update_xaxes(ticklabelmode = "period", rangeslider_visible = True , autorange = True)
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_station2)
    

    
    elif select_mode == 'By year' :
        
        year = data2['year'].unique()

        t=[]
        
        for y in year :
            
            dfy = data2[data2.year == y].copy()
    
            dfy['avg'] = dfy['value'].mean()
    
            traces = go.Scatter(
                                x = dfy.period,
                                y = dfy.value,
                                mode = "lines",
                                name=str(y),
                                showlegend=True
                     )
    
            trg = go.Scatter(
                             x = dfy.period,
                             y = dfy.avg,
                             mode = "lines",
                             name=str(y)+'avg',
                             showlegend= True,
                             line={'dash': 'dash'}
                  )
    
            t.append(traces)
    
            t.append(trg)
        
        figure = go.Figure(data = t)
        
        figure.update_xaxes(rangeslider_visible = True )
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_station2)
    
    return figure

@app.callback(Output('l3', 'figure'),
             [Input('date-picker3' , 'start_date'),
              Input('date-picker3' , 'end_date'),
              Input('select_station3', 'value'),
              Input('select_parameter3','value'),
              Input('select_mode3', 'value'),
              Input('avg_value3', 'value')])

def update_graph3(start_date , end_date , select_station3 , select_parameter3 , select_mode , avg_value):
    
    
    data1 = dr[((dr['date'] > start_date) & (dr['date'] < end_date)) & (dr['station'] == select_station3)]
    
    data2 = data1[data1['parameter']==select_parameter3]
    
    if select_mode == 'Continuous' :
        
        trace_1 = go.Scatter(x = data2['date'] , y = data2['value'] , line_color = "#461B7E",showlegend=True,name='Values')
    
        data2['rolling_mean'] = data2['value'].rolling(window=avg_value).mean()
    
        trace_2 = go.Scatter(x = data2['date'] , y = data2['rolling_mean'] , line_color = "#00CED1",showlegend=True,
                         name='Average')
    
        figure = go.Figure(data = [trace_1,trace_2])
                       
        figure.update_xaxes(ticklabelmode = "period", rangeslider_visible = True , autorange = True)
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_station3)
    
    elif select_mode == 'By year' :
        
        year = data2['year'].unique()

        t=[]
        
        for y in year :
            
            dfy = data2[data2.year == y].copy()
    
            dfy['avg'] = dfy['value'].mean()
    
            traces = go.Scatter(
                                x = dfy.period,
                                y = dfy.value,
                                mode = "lines",
                                name=str(y),
                                showlegend=True
                     )
    
            trg = go.Scatter(
                             x = dfy.period,
                             y = dfy.avg,
                             mode = "lines",
                             name=str(y)+'avg',
                             showlegend= True,
                             line={'dash': 'dash'}
                  )
    
            t.append(traces)
    
            t.append(trg)
        
        figure = go.Figure(data = t)
        
        figure.update_xaxes(rangeslider_visible = True )
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_station3)
    
    return figure

@app.callback(Output('l4', 'figure'),
             [Input('date-picker4' , 'start_date'),
              Input('date-picker4' , 'end_date'),
              Input('select_station4', 'value'),
              Input('select_parameter4','value'),
              Input('select_mode4', 'value'),
              Input('avg_value4', 'value')])

def update_graph4(start_date , end_date , select_station4 ,select_parameter4 , select_mode , avg_value):
    
    
    data1 = dw[((dw['date'] > start_date) & (dw['date'] < end_date)) & (dw['station'] == select_station4)]
    
    data2 = data1[data1['parameter']==select_parameter4]
    
    if select_mode == 'Continuous' :
        
        trace_1 = go.Scatter(x = data2['date'] , y = data2['value'] , line_color = "#461B7E",showlegend=True,name='Values')
    
        data2['rolling_mean'] = data2['value'].rolling(window=avg_value).mean()
    
        trace_2 = go.Scatter(x = data2['date'] , y = data2['rolling_mean'] , line_color = "#00CED1",showlegend=True,
                         name='Average')
    
        figure = go.Figure(data = [trace_1,trace_2])
                       
        figure.update_xaxes(ticklabelmode = "period", rangeslider_visible = True , autorange = True)
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_station4)
    
    elif select_mode == 'By year' :
        
        year = data2['year'].unique()

        t=[]
        
        for y in year :
            
            dfy = data2[data2.year == y].copy()
    
            dfy['avg'] = dfy['value'].mean()
    
            traces = go.Scatter(
                                x = dfy.period,
                                y = dfy.value,
                                mode = "lines",
                                name=str(y),
                                showlegend=True
                     )
    
            trg = go.Scatter(
                             x = dfy.period,
                             y = dfy.avg,
                             mode = "lines",
                             name=str(y)+'avg',
                             showlegend= True,
                             line={'dash': 'dash'}
                  )
    
            t.append(traces)
    
            t.append(trg)
        
        figure = go.Figure(data = t)
        
        figure.update_xaxes(rangeslider_visible = True )
    
        figure.update_layout(template = 'plotly_white', title="Data of "+select_station4)
    
    return figure

if __name__ == '__main__':
    app.run_server(debug = False)

