#
# Python Script
# with Online Trading Algorithm
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import zmq
import datetime
import numpy as np
import pandas as pd

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://127.0.0.1:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

df = pd.DataFrame()
mom = 3
min_length = mom + 1

while True:
    data = socket.recv_string()
    t = datetime.datetime.now()
    sym, value = data.split()
    # pd.append is deprecated. Use pd.concat
    df = pd.concat((df, pd.DataFrame({sym: float(value)}, index=[t])))
    # only process the most recent 1-5s, since all the previous periods are settled.
    dr = df.resample('5s', label='right').last()
    print('\nLength of dr is:' + len(dr) + '\n')
    print(dr)
    dr['returns'] = np.log(dr / dr.shift(1))
    if len(dr) > min_length:
        min_length += 1
        dr['momentum'] = np.sign(dr['returns'].rolling(mom).mean())
        print('\n' + '=' * 51)
        print('NEW SIGNAL | {}'.format(datetime.datetime.now()))
        print('=' * 51)
        print(dr.iloc[:-1].tail())
        if dr['momentum'].iloc[-1] == 1.0:
            print('\nLong market position.')
            # take some action (e.g. place buy order)
        elif dr['momentum'].iloc[-1]] == -1.0:
            print('\nShort market position.')
            # take some action (e.g. place sell order)
