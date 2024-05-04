from dependencies import *
from database.db import *
from server import server

dash.register_page(__name__, name='All Trades', path = '/alltrades')

# Fetch data from the database
with server.app_context():
    df_trades = get_all_trades()

layout = html.Div([
    html.H1("Trades Table"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df_trades.columns],
        data=df_trades.to_dict('records'),
        style_table={'height': '300px', 'overflowY': 'auto'}
    )
])


  