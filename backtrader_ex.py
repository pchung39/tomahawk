from datetime from datetime 
import backtrader as bt 

class SmaCross(bt.SignalStrategy):

    def __init__(self):
        sma = by.ind.SMA(period=50)
        price = self.data
        crossover = bt.ind.CrossOver(price,sma)
        self.signal_add(bt.SIGNAL_LONG, crossover)
