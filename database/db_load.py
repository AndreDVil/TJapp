from dependencies import *
import sqlite3

# Connect to SQLite - this will create the db file if it does not exist
conn = sqlite3.connect('trading_journal.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS trades")

# Create a table
cursor.execute('''
CREATE TABLE trades (
td_id INTEGER PRIMARY KEY AUTOINCREMENT,
td_st TEXT,
open_date INTEGER,
account TEXT,
strategy TEXT,
cexdex TEXT,
td_type TEXT,
asset TEXT,
direction TEXT,
entry_tgt REAL,
stop_tgt REAL,
rpt_tgt REAL,
pos_size_tgt_qt REAL,
pos_size_tgt REAL,
t1_price REAL,
t1_share REAL,
t1_qt REAL,
t2_price REAL,
t2_share REAL,
t2_qt REAL,
t3_price REAL,
t3_share REAL,
t3_qt REAL,
target_avg REAL,
risk REAL,
return REAL,
rr REAL,
fee_pct REAL,
fin_fee_24h REAL,
td_duration_est REAL,
fin_total_rate REAL,
total_rate REAL,
entry REAL,
pos_size_qt REAL,
pos_size REAL,
tp1_hit REAL,
tp2_hit REAL,
tp3_hit REAL,
man_close_share REAL,
man_close_price REAL,
stopped_share REAL,
stopped_price REAL,
avg_close_price REAL,
close_date INTEGER,
td_open_fee_rate REAL,
td_close_fee_rate REAL,
td_open_fee REAL,
td_close_fee REAL,
financing_fee REAL,
total_fee REAL,
trade_result_gross REAL,
trade_result_net REAL,
rpt REAL,
r_return REAL,
tags TEXT,
exec_st TEXT
)
''')
conn.commit()
conn.close()

# import trade data to trades table

# Load data from CSV file
tdlog_file = "tradelog.csv"

def load_data(filepath):
    """Load data from a CSV file."""
    try:
        df=pd.read_csv(filepath, delimiter=",")
        print(f"Data loaded successfully from {filepath}")
        return df
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return None

def clean_data(df):

    """Perform data cleansing on a DataFrame."""
    if df is not None:
        # Cleansing steps:
        df.dropna(how = 'all', inplace = True) # Remove rows with all missing values
        df.columns = [col.lower() for col in df.columns]  # Convert column names to lowercase
        df=df[df['td_id']>0]
        print("Data cleansing complete.")
        return df
    else:
        print("No data to cleanse.")
        return None

# Load and clean data on module import for main file
data = clean_data(load_data(tdlog_file))

# Connect to the SQLite database
conn = sqlite3.connect('trading_journal.db')

# Write the data to a sqlite table
data.to_sql('trades', conn, if_exists='append', index=False)

conn.close()