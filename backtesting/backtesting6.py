from backtesting import Backtest,Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover,resample_apply
import talib

# print(GOOG)

class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.rsi = self.I(talib.RSI,self.data.Close,self.rsi_window)

    def next(self):
        if crossover(self.rsi,self.upper_bound):
            if self.position.is_long:
                self.position.close()
                self.sell()

        elif crossover(self.rsi,self.lower_bound):
            if self.position.is_short or not self.position:
                self.position.close()
                self.buy()

bt = Backtest(GOOG, RsiOscillator, cash = 10_000,
            commission=.002,
            exclusive_orders=True,
            finalize_trades=True)

stats = bt.run()

print(stats)

# bt.plot(filename="html/Backtesting5")