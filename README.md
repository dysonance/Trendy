trendy
======

Numerical trendline Python algorithms for technical analysis of financial securities.

Installation
------------
1. Clone or download the ZIP file and unpack.
2. Go to the unpacked directory and copy to your Python path. Alternatively, you can place the trendy.py file in an easily reachable directory and import into your current working Python environment with
```python
execfile('/path/to/trendy.py')
```
or
```python
import trendy
```

I am still working on getting this project hosted on the Python Package Index, but for now this at least enables you to start using and gaining familiarity with the algorithms.

Examples
--------
Once the files have been imported, you can implement them with simple function calls. Here are some examples.
```python
# Download Apple price history and save adjusted close prices to numpy array
import pandas.io.data as pd
x = pd.DataReader("AAPL", "yahoo")['Adj Close']

# Make some trendlines
import trendy

# Generate general support/resistance trendlines and show the chart
# winow < 1 is considered a fraction of the length of the data set
trendy.gentrends(x, window = 1.0/3, charts = True)

# Generate a series of support/resistance lines by segmenting the price history
trendy.segtrends(x, segments = 2, charts = True)  # equivalent to gentrends with window of 1/2
trendy.segtrends(x, segments = 5, charts = True)  # plots several S/R lines

# Generate smaller support/resistance trendlines to frame price over smaller periods
trendy.minitrends(x, window = 30, charts = True)

# Iteratively generate trading signals based on maxima/minima in given window
trendy.iterlines(x, window = 30, charts = True)  # buy at green dots, sell at red dots
```
