from datetime import datetime
import backtrader as bt
import yfinance as yf
import math

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=50,  # period for the fast moving average
        pslow=200   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


class GoldenCross(bt.Strategy):

    params = (
        ('fast', 50),
        ('slow', 200),
        ('order_percentage', 0.95), 
        ('ticker', 'SPY')
    )

    def __init__(self):
        self.fast = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname='50 day moving average'
        )

        self.slow = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname='200 day moving average'
        )

        self.crossover = bt.ind.CrossOver(self.fast, self.slow) 

    def next(self):

        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))

                self.buy(size=self.size)
            
        if self.position.size > 0:
            if self.crossover < 0:
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()

class BuyHold(bt.Strategy):

    def next(self):
        size = int(self.broker.getcash() / self.data)
        self.buy(size=size)

cerebro = bt.Cerebro()
cerebro.broker.setcash(40000.0)
cerebro.addstrategy(BuyHold)
#cerebro.addsizer(bt.sizers.SizerFix, stake=70)

data = bt.feeds.YahooFinanceData(dataname='TSLA', fromdate=datetime(2005, 1, 1), todate=datetime(2015, 12, 31))
cerebro.adddata(data)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()