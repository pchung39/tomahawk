import pandas as pd

class Tickers(object):

    def __init__(self, nyse, nasdaq):
        self.csvs = [nyse, nasdaq]
        self.ticker_list = []

        self.convert_to_dataframe()
    
    def convert_to_dataframe(self):


        for c in self.csvs:

            converted = pd.read_csv(c)
            ticker_list = converted["Symbol"].to_list()

            scrubbed_list = self.scrub_tickers(ticker_list)
            self.ticker_list += scrubbed_list

    def scrub_tickers(self, tickers):

        new_tickers_list = []
        for index, t in enumerate(tickers):
            if "^" in t:
                continue
            
            stripped = t.strip()
            
            new_tickers_list.append(stripped)
        return new_tickers_list
    
    def print_list(self):

        print(self.ticker_list)

t = Tickers("../tickers/nyse_072021.csv", "../tickers/nasdaq_072021.csv")
t.print_list()