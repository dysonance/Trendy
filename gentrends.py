def gentrends(x, window=1.0/3.0, charts=True, fromdate='1900-01-01',
              todate=None, log_scale=False, directory=None):
    """
    Engine for generating S/R extrema trendlines based on given price data.

    x - ticker symbol or data set
    window - ratio from 0 to 1 giving the desired extrema barrier window
    charts - boolean, whether or not to print charts to screen
    fromdate - when to start pulling stock data (defaults to all data)
    todate - when to stop pulling stock data (if none, defaults to most recent)
    directory - directory in which data may be found to save on import speed
    """
    # Import packages
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

    if log_scale is True:  # change to log scale
        y = np.log(y)
    # Implement trendlines
    if window < 1:
        window = int(window * len(y))
    max1 = max(y)  # find the absolute max of the adjusted close
    min1 = min(y)  # find the absolute min of the adjusted close
    max1loc = np.where(y == max1)[0][0]  # find the index of the abs max
    min1loc = np.where(y == min1)[0][0]  # find the index of the abs min

    # GET THE SECONDARY EXTREMA AND FIND THEIR LOCATIONS IN THE DATA
    # First the max
    if max1loc + window > len(y):
        max2 = max(y[0:(max1loc - window)])
    else:
        max2 = max(y[(max1loc + window):])

    # Now the min
    if min1loc - window < 0:
        min2 = min(y[(min1loc + window):])
    else:
        min2 = min(y[0:(min1loc - window)])

    # Now find the indices of the secondary extrema
    max2loc = np.where(y == max2)[0][0]  # find the index of the 2nd max
    min2loc = np.where(y == min2)[0][0]  # find the index of the 2nd min

    # CREATE, EXTEND, AND PLOT THE TRENDLINES
    maxslope = (max1 - max2) / (max1loc - max2loc)  # slope between max points
    minslope = (min1 - min2) / (min1loc - min2loc)  # slope between min points
    a_max = max1 - (maxslope * max1loc)  # y-intercept for max trendline
    a_min = min1 - (minslope * min1loc)  # y-intercept for min trendline
    b_max = max1 + (maxslope * (len(y) - max1loc))  # extend to last data pt
    b_min = min1 + (minslope * (len(y) - min1loc))  # extend to last data point
    maxline = np.linspace(a_max, b_max, len(y))  # Y values between max's
    minline = np.linspace(a_min, b_min, len(y))  # Y values between min's

    # OUTPUT
    trends = np.transpose(np.array((y, maxline, minline)))
    trends = pd.DataFrame(trends, index=np.arange(0, len(y)),
                          columns=['price', 'maxline', 'minline'])

    if charts:
        plot(trends)
        if type(x) == str:
            title(x.upper())
        grid()
        show()

    execfile('line_eqn.py')
    return trends, maxslope, minslope

# Run
# gentrends(x='hcbk',
#            window=30,
#            charts=True,
#            # fromdate='2010-06-10',
#            # todate='2009-01-06',
#            directory='/Users/JAmos/Dropbox/Research/Trading/Data Dump/')
