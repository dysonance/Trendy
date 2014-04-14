def segtrend(x, segments=2.0, charts=True, fromdate='1900-01-01', todate=None,
             log_scale=False, directory=None):
    """
    Trendline algorithm that segments data into pieces and finds trendlines
    using those subsets.

    x - ticker symbol or data set
    threshold - ratio from 0 to 1 giving the desired extrema barrier window
    charts - boolean, whether or not to print charts to screen
    fromdate - when to start pulling stock data (defaults to all data)
    todate - when to stop pulling stock data (if none, defaults to most recent)
    log_scale - converts data to logarithmic scale
    directory - directory in which data may be found to save on import speed
    """
    # IMPORT PACKAGES
    import pandas.io.data as pd
    from matplotlib.pyplot import plot, grid, show, title
    import numpy as np

    # Check inputs and get data
    if type(x) == str:
        if directory is None:
            if todate is None:
                y = pd.DataReader(x, 'yahoo', fromdate)
                y = np.array(y['Adj Close'])
            else:
                y = pd.DataReader(x, 'yahoo', fromdate, todate)
                y = np.array(y['Adj Close'])
        else:
            y = pd.read_csv(directory + x + '.csv')
            if (fromdate == '1900-01-01') & (todate is None):
                y = np.array(y['Adj Close'])
            elif (fromdate == '1900-01-01') & (todate is not None):
                todate = np.where(y.Date == str(todate)[0:10])[0][0]
                y = np.array(y['Adj Close'])[0:todate]
            elif (fromdate != '1900-01-01') & (todate is None):
                fromdate = np.where(y.Date == str(fromdate)[0:10])[0][0]
                y = y['Adj Close'][fromdate:]
            elif (fromdate != '1900-01-01') & (todate is not None):
                fromdate = np.where(y.Date == str(fromdate)[0:10])[0][0]
                todate = np.where(y.Date == str(todate)[0:10])[0][0]
                y = y['Adj Close'][fromdate:todate]
    else:
        y = x
    if log_scale:
        y = np.log(y)  # change to log scale if desired
    # Implement trendlines

    segments = int(segments)
    maxima = np.ones(segments)
    minima = np.ones(segments)
    segsize = int(len(y)/(segments))
    for i in range(1, segments+1):
        ind2 = i*segsize
        ind1 = ind2 - segsize
        maxima[i-1] = max(y[ind1:ind2])
        minima[i-1] = min(y[ind1:ind2])
    
    # Find the indexes of these maxima in the data
    x_maxima = np.ones(segments)
    x_minima = np.ones(segments)
    for i in range(0, segments):
        x_maxima[i] = np.where(y == maxima[i])[0][0]
        x_minima[i] = np.where(y == minima[i])[0][0]
    
    # Return some output
    if charts:
        plot(y)
    for i in range(0, segments-1):
        maxslope = (maxima[i+1] - maxima[i]) / (x_maxima[i+1] - x_maxima[i])
        a_max = maxima[i] - (maxslope * x_maxima[i])
        b_max = maxima[i] + (maxslope * (len(y) - x_maxima[i]))
        maxline = np.linspace(a_max, b_max, len(y))

        minslope = (minima[i+1] - minima[i]) / (x_minima[i+1] - x_minima[i])
        a_min = minima[i] - (minslope * x_minima[i])
        b_min = minima[i] + (minslope * (len(y) - x_minima[i]))
        minline = np.linspace(a_min, b_min, len(y)) 

        if charts:
            plot(maxline, 'g')
            plot(minline, 'r')

    # OUTPUT
    grid(True)
    show()
    return x_maxima, maxima, x_minima, minima

# Run it
# segtrend(x='goog',
         segments=5,
         charts=True,
         fromdate='1900-01-01',
         todate=None,
         directory='/Users/JAmos/Dropbox/Research/Trading/Data Dump/')
