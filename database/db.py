from dependencies import pd
import sqlite3
from flask import current_app, g


def get_db():
    if 'db' not in g:
        # Establish a connection to the SQLite database
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # This makes the rows behave like dicts

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def add_trade(trade_data):
    db = get_db()
    sql = ''' INSERT INTO trades(td_st, open_date, account, strategy, cexdex, td_type, asset, 
            direction, entry_tgt, stop_tgt, rpt_tgt, pos_size_tgt_qt, pos_size_tgt, t1_price, 
            t1_share, t1_qt, t2_price, t2_share, t2_qt, t3_price, t3_share, t3_qt, target_avg, 
            risk, return, rr, fee_pct, fin_fee_24h, td_duration_est, fin_total_rate, total_rate, 
            entry, pos_size_qt, pos_size, tp1_hit, tp2_hit, tp3_hit, man_close_share, 
            man_close_price, stopped_share, stopped_price, avg_close_price, close_date, 
            td_open_fee_rate, td_close_fee_rate, td_open_fee, td_close_fee, financing_fee, 
            total_fee, trade_result_gross, trade_result_net, rpt, r_return, tags, exec_st)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    params = (
        trade_data['td_st'], trade_data['open_date'], trade_data['account'], trade_data['strategy'],
        trade_data['cexdex'], trade_data['td_type'], trade_data['asset'], trade_data['direction'],
        trade_data['entry_tgt'], trade_data['stop_tgt'], trade_data['rpt_tgt'], trade_data['pos_size_tgt_qt'],
        trade_data['pos_size_tgt'], trade_data['t1_price'], trade_data['t1_share'], trade_data['t1_qt'],
        trade_data['t2_price'], trade_data['t2_share'], trade_data['t2_qt'], trade_data['t3_price'],
        trade_data['t3_share'], trade_data['t3_qt'], trade_data['target_avg'], trade_data['risk'],
        trade_data['return'], trade_data['rr'], trade_data['fee_pct'], trade_data['fin_fee_24h'],
        trade_data['td_duration_est'], trade_data['fin_total_rate'], trade_data['total_rate'],
        trade_data['entry'], trade_data['pos_size_qt'], trade_data['pos_size'], trade_data['tp1_hit'],
        trade_data['tp2_hit'], trade_data['tp3_hit'], trade_data['man_close_share'], trade_data['man_close_price'],
        trade_data['stopped_share'], trade_data['stopped_price'], trade_data['avg_close_price'],
        trade_data['close_date'], trade_data['td_open_fee_rate'], trade_data['td_close_fee_rate'],
        trade_data['td_open_fee'], trade_data['td_close_fee'], trade_data['financing_fee'],
        trade_data['total_fee'], trade_data['trade_result_gross'], trade_data['trade_result_net'],
        trade_data['rpt'], trade_data['r_return'], trade_data['tags'], trade_data['exec_st']
    )
    db.execute(sql, params)
    db.commit()
    return {'status': 'success', 'message': 'Trade successfully added'}



def get_all_trades():
    with current_app.app_context():
        db = get_db()
        return pd.read_sql_query('SELECT * FROM trades where is_deleted = False', con=db)



def update_trade(trade_id, data):
    db = get_db()
    db.execute('UPDATE trades SET symbol=?, quantity=?, price=? WHERE id=?',
               (data['symbol'], data['quantity'], data['price'], trade_id))
    db.commit()
    return {'status': 'success', 'message': 'Trade updated'}

def delete_trade(trade_id):
    db = get_db()
    db.execute('DELETE FROM trades WHERE id=?', (trade_id,))
    db.commit()
    return {'status': 'success', 'message': 'Trade deleted'}


def add_trade_sample(trade_data):
    db = get_db()
    sql = ''' INSERT INTO trades (td_st, open_date, account, strategy, cexdex, td_type, asset,
                                  direction, entry_tgt, stop_tgt, rpt_tgt, pos_size_tgt_qt,
                                  t1_price, t2_price, t3_price, pos_size_tgt, t1_share, t1_qt, t2_share, t2_qt,
                                  t3_share, t3_qt, target_avg, risk, return, rr, fee_pct, fin_fee_24h,
                                  td_duration_est, fin_total_rate, total_rate, entry, pos_size_qt, pos_size,
                                  tp1_hit, tp2_hit, tp3_hit, man_close_share, man_close_price, stopped_share,
                                  stopped_price, avg_close_price, close_date, td_open_fee_rate, td_close_fee_rate,
                                  td_open_fee, td_close_fee, financing_fee, total_fee, trade_result_gross, 
                                  trade_result_net, rpt, r_return, tags, exec_st)
              VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                      NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 
                      NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 
                      NULL, NULL, NULL, NULL, NULL) '''
    params = (
        trade_data['td_st'], trade_data['open_date'], trade_data['account'], trade_data['strategy'],
        trade_data['td_type'], trade_data['asset'], trade_data['direction'],
        trade_data['entry_tgt'], trade_data['stop_tgt'], trade_data['rpt_tgt'], trade_data['pos_size_tgt_qt']
    )
    db.execute(sql, params)
    db.commit()
    return {'status': 'success', 'message': 'Trade successfully added'}    