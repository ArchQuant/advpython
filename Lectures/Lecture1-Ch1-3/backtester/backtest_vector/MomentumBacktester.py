#
# Momentum strategies backtesting
# (c) Yves J, Hilpisch
#
import numpy as np
import os
import pandas as pd

class MomentumBacktester(object):
    """Momentum strategy backtester
    """
    def __init__(self, symbol, start, end, amount, tran_cost):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.amount = amount
        self.tc = tran_cost # propotional transaction costs, e.g. 0.5% per trade
        self.result = None
        self.get_data()

    def get_data(self):
        dirpath = os.path.dirname(__file__)
        filepath = os.path.join(dirpath, '../data/pyalgo_eikon_eod_data.csv')
        raw = pd.read_csv(filepath, index_col=0, parse_dates=True).dropna()        
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start:self.end]
        raw.rename(columns={self.symbol: 'price'}, inplace=True)
        raw['returns'] = np.log(raw / raw.shift(1))
        self.data = raw

    def run_strategy(self, momentum=1):
        self.momentum = momentum
        data = self.data.copy().dropna()
        data['position'] = np.sign(data['returns'].rolling(momentum).mean())
        data['strategy'] = data['position'].shift(1) * data['returns']
        # determine when a trade occurs
        data.dropna(inplace=True)
        trades = data['position'].diff().fillna(0) != 0
        # substract transaction costs
        data['strategy'][trades] -= self.tc
        data['cum_returns'] = self.amount * data['returns'].cumsum().apply(np.exp)
        data['cum_strategy'] = self.amount * data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # overall performance of the strategy
        total_perf = self.results['cum_strategy'].iloc[-1]
        diff = total_perf - self.results['cum_returns'].iloc[-1]
        return round(total_perf, 2), round(diff, 2)

    def plot_results(self):
        if self.results is None:
            print('No results yet.')
        else:
            title = '%s | tran_cost = %.4f' % (self.symbol, self.tc)
            self.results[['cum_returns', 'cum_strategy']].plot(title=title, figsize=(10, 6))

if __name__ == '__main__':
    mombt = MomentumBacktester('XAU=', '2010-1-1', '2020-12-31', 10000, 0.0)
    print(mombt.run_strategy())
    print(mombt.run_strategy(momentum=3))
    mombt = MomentumBacktester('XAU=', '2010-1-1', '2020-12-31', 10000, 0.001)
    print(mombt.run_strategy(momentum=3))