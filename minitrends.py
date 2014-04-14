def minitrends(x, window, fromdate='1900-01-01', todate=None, charts=True,
               log_scale=False, directory=None):
    """
    Creates local maxima and minima trendlines based on a given window period.

    x - ticker symbol or data set
    window - float definining how long the trendlines should be. If window <
             1, then it will be taken as a percentage of the size of the data
    fromate - start date for the stock data
    todate - end date for the stock data
    charts - boolean value saying whether to print chart to screen
    log_scale - converts data to logarithmic scale
    directory - directory in which data may be found to save on import speed
    """
    # import packages
    import pandas.io.data as pd
    import numpy as np
    from matplotlib.pyplot import plot, show, title, grid

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

    if log_scale is True:  # convert to log scale
        y = np.log(y)
    if window < 1:  # if window is given as fraction of data length
        window = float(window)
        window = int(window * len(y))
    x = np.arange(0, len(y))
    dy = y[window:] - y[:-window]
    crit = dy[:-1] * dy[1:] < 0

    # Find whether max's or min's
    max = (y[x[crit]] - y[x[crit] + window] > 0) & \
          (y[x[crit]] - y[x[crit] - window] > 0) * 1
    min = (y[x[crit]] - y[x[crit] + window] < 0) & \
          (y[x[crit]] - y[x[crit] - window] < 0) * 1
    max = max.astype(float)
    min = min.astype(float)
    max[max == 0] = np.nan
    min[min == 0] = np.nan
    xmax = x[crit] * max
    xmax = xmax[~np.isnan(xmax)]
    xmax = xmax.astype(int)
    xmin = x[crit] * min
    xmin = xmin[~np.isnan(xmin)]
    xmin = xmin.astype(int)

    # See if better max or min in region
    yMax = np.array([])
    xMax = np.array([])
    for i in xmax:
        indx = np.where(xmax == i)[0][0] + 1
        try:
            Y = y[i:xmax[indx]]
            yMax = np.append(yMax, Y.max())
            xMax = np.append(xMax, np.where(y == yMax[-1])[0][0])
        except:
            pass
    yMin = np.array([])
    xMin = np.array([])
    for i in xmax:
        indx = np.where(xmax == i)[0][0] + 1
        try:
            Y = y[i:xmax[indx]]
            yMin = np.append(yMin, Y.min())
            xMin = np.append(xMin, np.where(y == yMin[-1])[0][0])
        except:
            pass
    if y[-1] > yMax[-1]:
        yMax = np.append(yMax, y[-1])
        xMax = np.append(xMax, x[-1])
    if y[0] not in yMax:
        yMax = np.insert(yMax, 0, y[0])
        xMax = np.insert(xMax, 0, x[0])
    if y[-1] < yMin[-1]:
        yMin = np.append(yMin, y[-1])
        xMin = np.append(xMin, x[-1])
    if y[0] not in yMin:
        yMin = np.insert(yMin, 0, y[0])
        xMin = np.insert(xMin, 0, x[0])

    # Plot results if desired
    if charts is True:
        plot(x, y)
        plot(xMax, yMax, '-o')
        plot(xMin, yMin, '-o')
        grid(True)
        show()
    # Return arrays of critical points
    return xMax, yMax, xMin, yMin

# print minitrends(x='goog', window=60, charts=True)
