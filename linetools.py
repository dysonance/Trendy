# File containing functions providing utilities for evaluating lines.

def line_eqn((x0, y0), (x1, y1)):
    """
    Returns the equation of a line in the form of a lambda expression,
    based on two given tuples of x- and y-coordinates.
    """
    m = (y1 - y0)/(x1 - x0)
    b = y1 - m * x1
    y = lambda x: m*x + b
    return y


def line_slope(x, y, chart=False):
    """
    Returns the slope(s) of the line(s) between either two coordinate points
    (given as array-like data) or two arrays of coordinate values.
    """
    import numpy as np
    m = np.diff(y) / np.diff(x)
    m = m[~np.isnan(m)]
    if (chart is True):
        plot(m)
        show()
    return m


def line_intercept(x, y, chart=False):
    """
    Returns the y-intercepts(s) of the line(s) between either two coordinate
    points (given as array-like data) or two arrays of coordinate values.
    """
    import numpy as np
    m = np.diff(y) / np.diff(x)
    m = m[~np.isnan(m)]
    b = y - m*x
    if chart is True:
        plot(b)
        show()
    return b
