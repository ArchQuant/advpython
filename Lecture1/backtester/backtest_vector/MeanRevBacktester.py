#
# Mean reversion strategies backtesting
# (c) Yves J, Hilpisch
#
import numpy as np
import os
import pandas as pd
from backtest_vector.MomentumBacktester import *

# MeanRevBacktester uses MomentumBacktester as the base class
class MeanRevBacktester(MomentumBacktester):
    """Mean reversion strategy backtester
    """
    def run_strategy(self, SMA, threshold):
        data = self.data.copy().dropna()
        data['SMA'] = data['price'].rolling(SMA).mean()
        data['distance'] = data['price'] - data['SMA']
        data.dropna(inplace=True)
        # sell signals
        data['position'] = np.where(data['distance'] > threshold, -1, np.nan)
        # buy signals
        data['position'] = np.where(data['distance'] < -threshold, 1, data['position'])
        # set position to zero when the price crosses the SMA
        data['position'] = np.where(data['distance'] * data['distance'].shift(1) < 0, 0, data['position'])
        data['position'] = data['position'].ffill().fillna(0)
        data['strategy'] = data['position'].shift(1) * data['returns']
        # determine when a trade occurs for transaction cost
        trades = data['position'].diff().fillna(0) != 0
        data['strategy'][trades] -= self.tc
        data['cum_returns'] = self.amount * data['returns'].cumsum().apply(np.exp)
        data['cum_strategy'] = self.amount * data['strategy'].cumsum().apply(np.exp)
        self.results = data
        total_perf = self.results['cum_strategy'].iloc[-1]
        diff = total_perf - self.results['cum_returns'].iloc[-1]
        return round(total_perf, 2), round(diff, 2)

if __name__ == '__main__':
    mrbt = MeanRevBacktester('GDX', '2010-1-1', '2020-12-31', 10000, 0.0)
    print(mrbt.run_strategy(SMA=25, threshold=5))
    mrbt = MeanRevBacktester('GDX', '2010-1-1', '2020-12-31', 10000, 0.001)
    print(mrbt.run_strategy(SMA=25, threshold=5))
    mrbt = MeanRevBacktester('GLD', '2010-1-1', '2020-12-31', 10000, 0.001)
    print(mrbt.run_strategy(SMA=42, threshold=7.5))