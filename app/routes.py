from app import app
from flask import render_template
from app.forms import LoginForm, UploadForm
from werkzeug.utils import secure_filename
import pandas as pd
import pandas as pd
import pandas_datareader.data as pdr
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv
import yfinance as yf

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    user = {'username': 'Miguel'}

    form = UploadForm()
    
    if form.validate_on_submit():

        filename = secure_filename(form.file.data.filename)
        filestream =  form.file.data 
        filestream.seek(0)

        ticker_list = pd.read_csv( filestream  )

        ticker_list = ticker_list.reset_index()

        print(ticker_list['Ticker'])

        
        ticker_frame = pd.DataFrame(columns=['Close', 'EMA50', 'SMA50', 'EMA100', 'SMA100', 'EMA200', 'SMA200'], index=ticker_list['Ticker'])
        df = pd.DataFrame(columns=['EMA50 < Price', 'SMA50 < Price', 'EMA100 < Price', 'SMA100 < Price', 'EMA200 < Price', 'SMA200 < Price'], index=ticker_list['Ticker'])

        for index, row in ticker_list.iterrows():
            ticker = row['Ticker']

            setTicker = yf.Ticker(ticker)
            data= setTicker.history(period="1y")

            #Test 1: 
            ema50=data['Close'].ewm(span=50,adjust=False).mean()
            ema100=data['Close'].ewm(span=100,adjust=False).mean()
            ema200=data['Close'].ewm(span=200,adjust=False).mean()
            sma50 = data['Close'].rolling(50).mean()
            sma100 = data['Close'].rolling(100).mean()
            sma200 = data['Close'].rolling(200).mean()

            ticker_frame.loc[ticker]['Close'] = data['Close'][-1]
            ticker_frame.loc[ticker]['EMA50'] = ema50[-1]
            ticker_frame.loc[ticker]['SMA50'] = sma50[-1]
            ticker_frame.loc[ticker]['EMA100'] = ema100[-1]
            ticker_frame.loc[ticker]['SMA100'] = sma100[-1]
            ticker_frame.loc[ticker]['EMA200'] = ema200[-1]
            ticker_frame.loc[ticker]['SMA200'] = sma200[-1]



            if ema50[-1] < data['Close'][-1]:
                df.loc[ticker]['EMA50 < Price'] = 'BUY'
            else:
                df.loc[ticker]['EMA50 < Price'] = 'SELL'

            if sma50[-1] < data['Close'][-1]:
                df.loc[ticker]['SMA50 < Price'] = 'BUY'
            else:
                df.loc[ticker]['SMA50 < Price'] = 'SELL'

            if ema100[-1] < data['Close'][-1]:
                df.loc[ticker]['EMA100 < Price'] = 'BUY'
            else:
                df.loc[ticker]['EMA100 < Price'] = 'SELL'

            if sma100[-1] < data['Close'][-1]:
                df.loc[ticker]['SMA100 < Price'] = 'BUY'
            else:
                df.loc[ticker]['SMA100 < Price'] = 'SELL'

            if ema200[-1] < data['Close'][-1]:
                df.loc[ticker]['EMA200 < Price'] = 'BUY'
            else:
                df.loc[ticker]['EMA200 < Price'] = 'SELL'

            if sma200[-1] < data['Close'][-1]:
                df.loc[ticker]['SMA200 < Price'] = 'BUY'
            else:
                df.loc[ticker]['SMA200 < Price'] = 'SELL'

        print (df)
        return render_template('output.html', tables=[df.to_html(classes='data', header="true")], titles=df.columns.values, tickers=[ticker_frame.to_html(classes='data', header="true")], ticker_titles=ticker_frame.columns.values)

    return render_template('upload.html', form=form)
