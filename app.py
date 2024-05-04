from flask import Flask
from index import app as dash_app  # Importing the Dash app setup from index.py
from server import server as app
from database.db import get_all_trades, add_trade, update_trade, delete_trade, add_trade_sample

# Define Flask-specific routes if necessary
@app.route('/hello')
def hello():
    return 'Hello, this is a custom Flask route outside of Dash!'

@app.route('/api/trades', methods=['GET'])
def api_get_trades():
    trades = get_all_trades()
    return jsonify(trades)

@app.route('/api/trades', methods=['POST'])
def api_add_trade():
    data = request.get_json()
    result = add_trade(data)
    return jsonify(result)

@app.route('/api/trades', methods=['POST'])
def api_add_trade_sample():
    data = request.get_json()
    result = add_trade_sample(data)
    return jsonify(result)

@app.route('/api/trades/<int:trade_id>', methods=['PUT'])
def api_update_trade(trade_id):
    data = request.get_json()
    result = update_trade(trade_id, data)
    return jsonify(result)

@app.route('/api/trades/<int:trade_id>', methods=['DELETE'])
def api_delete_trade(trade_id):
    result = delete_trade(trade_id)
    return jsonify(result)

# Run the server only if app.py is the script being executed
if __name__ == '__main__':
    dash_app.run_server(debug=True)