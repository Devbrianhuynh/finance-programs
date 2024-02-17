from options_terminal import Options_Chain as OC
from flask import Flask, render_template
import psycopg2
import pandas as pd

class Options_Application:
    def __init__(self, ticker = None, expiration_date = None):
        self.ticker = ticker
        self.exp_date = expiration_date

    
    def input_options_to_dataset(self):
        options_chain = OC(self.ticker, self.exp_date)
        options_chain.front_month_call_options()
        options_chain.front_month_put_options()


    # Pull out the data from the options_research database
    def extract_options_from_dataset(self):
        conn = psycopg2.connect(
            dbname = 'options_research',
            user = 'postgres',
            password = 'postgressoftware',
            host = 'localhost',
            port = '5432'
        )

        cur = conn.cursor()

        cur.execute('SELECT * FROM call_options_chain') # Connect this with put_options_chain, connected by the strike price

        rows = cur.fetchall()

        columns = ('id', 'symbol', 'contract_name', 'bid', 'ask', 'mid', 'premium', 'change', 'volume', 
                   'open_interest', 'implied_volatility', 'expiry_date', 'strike', 'added_time')

        options_table = []

        for row in rows:
            column_row = dict(zip(columns, row))
            options_table.append(column_row)

        options_table = pd.DataFrame(options_table)

        return options_table


options_application = Options_Application() # Input the ticker and exp_date through the main dashboard
input_options = options_application.input_options_to_dataset()
extra_options = options_application.extract_options_from_dataset()

# Connect your application with HTML/CSS via Flask
app = Flask(__name__)

@app.route('/generate_table')
def generate_table():
    # Transfer the options_table from extract_options_from_dataset to here
    options_table = extra_options

    return render_template('options_dashboard.html', options_table = options_table)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)