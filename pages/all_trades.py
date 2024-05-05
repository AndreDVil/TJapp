from dependencies import *
from database.db import *
from server import server

dash.register_page(__name__, name='All Trades', path = '/alltrades')

# Fetch data from the database
with server.app_context():
    df_trades = get_all_trades()

# build the layout for trades table
layout = html.Div([
    dash_table.DataTable(
        id='trades-table',
        columns=[{"name": i, "id": i} for i in df_trades.columns],
        data=df_trades.to_dict('records'),
        style_table={'height': '500px', 'overflowY': 'auto'},
        row_selectable='single'
    ),
    html.Button('Delete Trade', id='delete-button', n_clicks=0),
    html.Div(id='delete-output')
])

@callback(
    Output('delete-output', 'children'),
    Input('delete-button', 'n_clicks'),
    State('trades-table', 'selected_rows'),
    State('trades-table', 'data')
)
def delete_trade(n_clicks, selected_rows, rows):
    if n_clicks > 0 and selected_rows is not None:
        selected_id = rows[selected_rows[0]]['td_id']
        db = get_db()
        db.execute('UPDATE trades SET is_deleted = TRUE WHERE td_id = ?', (selected_id,))
        db.commit()
        return 'Trade marked as deleted.'
    return ''


  