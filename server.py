from flask import Flask
from database.db import close_db

server = Flask(__name__)
server.config['SECRET_KEY'] = 'your_secret_key'
server.config['DATABASE'] = 'database/trading_journal.db'

@server.teardown_appcontext
def close_connection(exception):
    close_db(exception)