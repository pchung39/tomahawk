import talib
import yfinance as yf

data = yf.download("SPY", start="2020-01-01", end="2020-08-01")

morning_star = talib.CDLMORNINGSTAR(open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"])

engulfing = talib.CDLENGULFING(open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"])

data["morning_star"] = morning_star
data["engulfing"] = engulfing

engulfing_days = data[data["engulfing"] != 0]
print(engulfing_days)