def iterlines(x, window, fromdate='1900-01-01', todate=None, charts=True,
              log_scale=False, directory=None):
    """
    Turn minitrends to iterative process more easily adaptable to
    implementation in simple trading systems; allows backtesting functionality.

    x - ticker symbol or data set
    window - float defining how far back the algorithm checks for critical
             values
    fromate - start date for the stock data
    todate - end date for the stock data
    charts - boolean value saying whether to print chart to screen
    log_scale - converts imported data to logarithmic scale
    directory - directory in which data may be found to save on import speed
    """
    # Import packages
    import pandas.io.data as pd
    import numpy as np
    from matplotlib.pyplot import subplot, plot, show, title, grid

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

    # Turn to log scale if desired
    if log_scale is True:
        y = np.log(y)

    # Change to log scale if desired
    if log_scale is True:
        y = np.log(y)
    if window < 1:
        window = int(window * len(y))
    x = np.arange(0, len(y))
    xmax = np.array(x[0])
    xmin = np.array(x[0])
    ymax = np.array(y[0])
    ymin = np.array(y[0])

    for i in x[window:]:
        if y[i] > max(y[i-window:i]):
            ymax = np.append(ymax, y[i])
            xmax = np.append(xmax, x[i])
        if y[i] < min(y[i-window:i]):
            ymin = np.append(ymin, y[i])
            xmin = np.append(xmin, x[i])

    # Plot results if desired
    if charts is True:
        plot(x, y)
        plot(xmax, ymax, 'o')
        plot(xmin, ymin, 'o')
        grid(True)
        show()

    return R[-1]

# iterlines('goog', 30, charts=True, log_scale=False, backtest=True)
