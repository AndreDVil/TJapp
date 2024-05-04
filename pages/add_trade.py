from dash import Dash, html, dcc, Input, Output, State, callback
import datetime
from database.db import add_trade_sample
import dash

dash.register_page(__name__, name='Add Trade', path = '/add_trade')


layout = html.Div([
    html.H1("Trade Planning"),
    dcc.Dropdown(id='td_type', options=[
        {'label': 'Spot', 'value': 'spot'},
        {'label': 'Future', 'value': 'future'}
    ], placeholder='Select Trade Type', value='spot', style={'width': '50%'}),
    dcc.Dropdown(id='direction', options=[
        {'label': 'Long', 'value': 'long'},
        {'label': 'Short', 'value': 'short'}
    ], placeholder='Select Direction', value='long', style={'width': '50%'}),
    dcc.Dropdown(id='account', options=[
        {'label': 'T Wealth', 'value': 't_wealth'},
        {'label': 'CT', 'value': 'ct'},
        {'label': 'Swing', 'value': 'swing'}
    ], placeholder='Select Account', value='t_wealth', style={'width': '50%'}),
    dcc.Input(id='strategy', type='text', placeholder='Strategy', required=True),
    dcc.Input(id='asset', type='text', placeholder='Asset', required=True),
    dcc.DatePickerSingle(id='open_date', date=datetime.date.today(), style={'width': '50%'}),
    dcc.Input(id='entry_tgt', type='number', placeholder='Entry Target', required=True, step=0.01),
    dcc.Input(id='stop_tgt', type='number', placeholder='Stop Target', required=True, step=0.01),
    dcc.Input(id='rpt_tgt', type='number', placeholder='Risk per Trade', required=True, step=0.01),
    dcc.Input(id='pos_size_tgt_qt', type='number', placeholder='Position size quantity', readOnly= True),
    html.Div(id='pos_size_tgt_qt_output'),  # Display calculated value here
    html.Button('Submit', id='submit-btn', n_clicks=0),
    html.Div(id='output-container')
])

@callback(
        Output('pos_size_tgt_qt_output', 'children'),
        Output('pos_size_tgt_qt', 'value'),
        Input('entry_tgt', 'value'),
        Input('stop_tgt', 'value'),
        Input('rpt_tgt', 'value')
        )
def calculate_pos_size_tgt_qt(entry_tgt, stop_tgt, rpt_tgt):
    if entry_tgt is not None and stop_tgt is not None and rpt_tgt is not None and rpt_tgt != 0:
        pos_size_tgt_qt = (entry_tgt - stop_tgt) / rpt_tgt
        return f'Position Size Target Quantity: {pos_size_tgt_qt}', pos_size_tgt_qt
    return 'Enter all values to see Position Size Target Quantity', 0




@callback(
    Output('output-container', 'children'),
    [Input('submit-btn', 'n_clicks')],
    [State('td_type', 'value'),
     State('direction', 'value'),
     State('account', 'value'),
     State('strategy', 'value'),
     State('asset', 'value'),
     State('open_date', 'date'),
     State('entry_tgt', 'value'),
     State('stop_tgt', 'value'),
     State('rpt_tgt', 'value'),
     State('pos_size_tgt_qt', 'value')]
)
def handle_form_submission(n_clicks, td_type, direction, account, strategy, asset, open_date, entry_tgt, stop_tgt, rpt_tgt, pos_size_tgt_qt):
    if n_clicks > 0:
        trade_data = {
            'td_st': 'open',  # default status
            'open_date': open_date,
            'account': account,
            'strategy': strategy,
            'td_type': td_type,
            'asset': asset,
            'direction': direction,
            'entry_tgt': entry_tgt,
            'stop_tgt': stop_tgt,
            'rpt_tgt': rpt_tgt,
            'pos_size_tgt_qt': pos_size_tgt_qt
        }
        response = add_trade_sample(trade_data)  # Call the function to insert data into the database
        return response['message']
    return 'Enter trade details and click submit.'


