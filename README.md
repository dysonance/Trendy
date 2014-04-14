trendy
======

Numerical trendline Python algorithms for technical analysis of financial securities.

Installation
------------
1. Clone or download the ZIP file.
2. Unpack the zip file.
3. Find the unpacked directory and copy the files to your Python path. Otherwise, you can place them in an easily reachable directory and import any of the files individually into your current working Python environment with


        execfile('/path/to/trendy-master/file.py')

I am working on getting this project hosted on the Python Package Index, but for now this at least enables you to start using and gaining familiarity with the algorithms.

Examples
--------
Once the files have been imported, you can implement them with simple function calls. Here are some examples.

This example places general trendlines framing the entire price history of Facebook (ticker: FB).

    gentrends(x = 'fb')

You can change the window period to alter the sensitivity and flexibility of the general trendline function. This example applies the function to LinkedIn (ticker: LNKD) with a window period of 1/2 (half of the length of the price history). Keep in mind that if using a version before Python 3, you will need to specify that the window period is a float with decimals.

    gentrends(x = 'lnkd', window = 1.0/2.0)

You can also specify window periods of integer values. For example, if LinkedIn has been on the market for 730 trading days, the above example is equivalent to:

    gentrends(x = 'lnkd', window = 365)

If you want trendlines that provide a description of the price movement over smaller timeframes, it may be more useful to use the 'minitrends' function, where smaller window periods may prove more useful.

    minitrends(x = 'lnkd', window = 30)

It is also possible to feed it raw data as a NumPy array instead of a ticker symbol.

    import numpy as np
    import pandas.io.data as pd
    lnkd = np.array(pd.DataReader('lnkd', 'yahoo')['Adj Close'])
    minitrends(x = lnkd, window = 30)

