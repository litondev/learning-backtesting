from backtesting import Backtest,Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover
import talib

# print(GOOG)

def optim_func(series):
    if series["# Trades"] < 5:
        # KETIKA HASIKNYA -1 BERARTI YANG PALING KECIL DIA TIDAK AKAN DIPILIH ATAU DITAMPILKAN KAREAN KALAH PERFORMA
        return -1

    return series["Equity Final [$]"] / series["Exposure Time [%]"]

class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.rsi = self.I(talib.RSI,self.data.Close,self.rsi_window)

    def next(self):
        if crossover(self.rsi,self.upper_bound):
            self.position.close()
        elif crossover(self.rsi,self.lower_bound):
            self.buy()

bt = Backtest(GOOG, RsiOscillator, cash = 10_000,
            commission=.002,
            exclusive_orders=True,
            finalize_trades=True)

# stats = bt.optimize(
#     upper_bound = range(50,80),
#     lower_bound = range(10,30),
#     rsi_window = 14,
#     # MAKSIMALKAN SELURUH INPUTAN  YANG PALING MAKSIMAL YANG AKAN DI TAMPILKAN
#     maximize = optim_func,
#     # BATASAN OPTIMIZE 
#     constraint = lambda param: param.upper_bound > param.lower_bound,
    # max_tries=100)

stats = bt.run()

print(stats)

bt.plot(filename="/html")