#
# Python Module for 
# Vectorized Backtesting
# of SMA-based strategies
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import numpy as np
import os
import pandas as pd
from scipy.optimize import brute

class SMABacktester(object):
    """ Class for the vectorized backtesting of SMA-based trading strategies.

    Attributes
    ==========
    symbol: str
        RIC symbol with which to work with
    SMA1: int
        time window in days for shorter SMA
    SMA2: int
        time window in days for longer SMA
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval

    Methods
    =======
    get_data:
        retrieves and prepares the base data set
    set_parameters:
        sets one or two new SMA parameters
    run_strategy:
        runs the backtest for the SMA-based strategy
    plot_results:
        plots the performance of the strategy compared to the symbol
    update_and_run:
        updates SMA parameters and returns the (negative) absolute performance
    optimize_parameters:
        implements a brute force optimizeation for the two SMA parameters
    """

    def __init__(self, symbol, SMA1, SMA2, start, end):
        self.symbol = symbol
        self.SMA1 = SMA1
        self.SMA2 = SMA2
        self.start = start
        self.end = end
        self.results = None
        self.get_data()

    def get_data(self):
        """Retrieves and prepares the data.
        """
        dirpath = os.path.dirname(__file__)
        filepath = os.path.join(dirpath, '../data/pyalgo_eikon_eod_data.csv')
        raw = pd.read_csv(filepath, index_col=0, parse_dates=True).dropna()        
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start:self.end]
        raw.rename(columns={self.symbol: 'price'}, inplace=True)
        raw['return'] = np.log(raw / raw.shift(1))
        raw['SMA1'] = raw['price'].rolling(self.SMA1).mean()
        raw['SMA2'] = raw['price'].rolling(self.SMA2).mean()
        self.data = raw

    def set_parameters(self, SMA1=None, SMA2=None):
        """Updates SMA parameters and respective time series.
        """
        if SMA1 is not None:
            self.SMA1 = SMA1
            self.data['SMA1'] = self.data['price'].rolling(self.SMA1).mean()
        if SMA2 is not None:
            self.SMA2 = SMA2
            self.data['SMA2'] = self.data['price'].rolling(self.SMA2).mean()

    def run_strategy(self):
        """Backtests the trading strategy
        
        :return strategy gross return, out-/under-performance of the strategy
        """
        data = self.data.copy().dropna()
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['return']
        data.dropna(inplace=True)
        data['cum_returns'] = data['return'].cumsum().apply(np.exp)
        data['cum_strategy'] = data['strategy'].cumsum().apply(np.exp)
        self.results = data
        # gross performance of strategy
        gross_perf = data['cum_strategy'].iloc[-1]
        # diff in return = strategy - naive
        diff = gross_perf - data['cum_returns'].iloc[-1]
        return round(gross_perf, 2), round(diff, 2)

    def plot_results(self):
        """Plots the cumulative performace of the trading strategy compared to the naive one.
        """
        if self.results is None:
            print('No results to plot yet. Run a strategy.')
        title = '%s | SMA1=%d, SMA2=%d' % (self.symbol,
                                           self.SMA1,
                                           self.SMA2)
        self.results[['cum_returns', 'cum_strategy']].plot(title=title,
                                                           figsize=(10, 6))

    def update_and_run(self, SMA):
        """Updates SMA parameters and run
        
        :return negative gross return of the updated strategy (negative for minimazation algorithm)
        :param SMA: tuple(SMA1, SMA2)
        """
        self.set_parameters(int(SMA[0]), int(SMA[1]))
        return -self.run_strategy()[0]

    def optimize_parameters(self, SMA1_range, SMA2_range):
        """Finds global maximum given the SMA ranges.
        
        :return optimization object
        :param SMA1_range: tuple(start, end, step size)
        :param SMA2_range: tuple(start, end, step size)
        """
        opt = brute(self.update_and_run, (SMA1_range, SMA2_range), finish=None)
        return opt, -self.update_and_run(opt)

if __name__ == '__main__':
    smabt = SMAVectorBacktester('EUR=', 43, 252,
                                '2010-1-1', '2020-12-31')
    print(smabt.run_strategy())
    smabt.set_parameters(SMA1=20, SMA2=100)
    print(smabt.run_strategy())
    print(smabt.optimize_parameters((30, 56, 4), (200, 300, 4)))
    