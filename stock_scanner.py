# code for finding breakout candidates with Python and Pandas 
import os
import pandas

#TODO figure out how to stream this from alpaca

def is_consolidating(df, percentage=2):

    # closing within a couple percentage range 

    recent_candlesticks = df[-15:]
    print(recent_candlesticks)

    max_close = recent_candlesticks["Close"].max()
    min_close = recent_candlesticks["Close"].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):
        return True

    return False

def is_breaking_out(df, percentage=2.5):

    last_close = df[-1:]["Close"].values[0]

    if is_consolidating(df[:-1], percentage=percentage):
        # is the last candle greater than max of previous candlestick
        recent_closes = df[-16:-1]

        if last_close > recent_closes["Close"].max():
            return True
    
    return False


for filename in os.listdir('datasets/daily'):
    df = pandas.read_csv('datasets/daily/{}'.format(filename))
    
    if is_consolidating(df, percentage=2.5):
        print("{} is consolidating".format(filename))

    if is_breaking_out(df):
        print("{} is breaking out".format(filename))
    
