"""
DOCSTRING
"""
import matplotlib
import numpy

def back_testing():
    """
    DOCSTRING
    """
    dates, prices, volumes = [], [], []
    try:
        source_code = open('btceUSD.csv', 'r').read()
        split_source = source_code.split('\n')
        for line in split_source[-50000:]:
            split_line = line.split(',')
            dates.append(float(split_line[0]))
            prices.append(float(split_line[1]))
            volumes.append(float(split_line[2]))
    except Exception as exception:
        print('Failed:Back Testing:' + str(exception))
    ema_price = exponential_moving_average(prices, 50)
    rsi_line = relative_strength_index(prices, n_variable=1500)
    stance, last_purchase_price, net_profit = 'none', 0, 0
    print(
        'Starting Time:' + str(
            datetime.datetime.fromtimestamp(float(dates[0])).strftime('%Y-%m-%d %H:%M:%S')
            )
        )
    for count, element in enumerate(rsi_line):
        if stance == 'none':
            if element < 40:
                stance = 'holding'
                print('Bought Bitcoin @ ' + prices[count])
                last_purchase_price = prices[count]
        elif stance == 'holding':
            if element > 60:
                stance = 'none'
                print('Sold Bitcoin @ ' + prices[count])
                fees = 0.002*(prices[count]+last_purchase_price)
                print('Transaction Fees:' + fees)
                trade_profit = (prices[count]-last_purchase_price)-fees
                print('Trade Profit:' + trade_profit)
                net_profit += trade_profit
    print('Net Profit:' + net_profit)

def exponential_moving_average(values, window):
    """
    Calculate exponential moving average.
    """
    weights = numpy.exp(numpy.linspace(-1.0, 0.0, window))
    weights /= weights.sum()
    average = numpy.convolve(values, weights, mode='full')[:len(values)]
    average[:window] = average[window]
    return average

def relative_strength_index(prices, n_variable=14):
    """
    Calculate relative strength index.
    """
    deltas = numpy.diff(prices)
    seed = deltas[:n_variable+1]
    up_value = seed[seed >= 0].sum()/n_variable
    down_value = -seed[seed < 0].sum()/n_variable
    relative_strength = up_value/down_value
    relative_strength_index = numpy.zeros_like(prices)
    relative_strength_index[:n_variable] = 100.0-100.0/(1.0+relative_strength)
    for i in range(n_variable, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.0
        else:
            upval = 0.0
            downval = -delta
        up_value = (up_value*(n_variable-1) + upval)/n_variable
        down_value = (down_value*(n_variable-1) + downval)/n_variable
        relative_strength = up_value/down_value
        relative_strength_index[i] = 100.0-100.0/(1.0+relative_strength)
    return relative_strength_index

def testing_data():
    """
    DOCSTRING
    """
    dates, prices, volumes = [], [], []
    try:
        source_code = open('btceUSD.csv', 'r').read()
        split_source = source_code.split('\n')
        for line in split_source[-50000:]:
            split_line = line.split(',')
            dates.append(float(split_line[0]))
            prices.append(float(split_line[1]))
            volumes.append(float(split_line[2]))
    except Exception as exception:
        print('Failed:Raw Data:' + str(exception))
    axis_1 = matplotlib.pyplot.subplot2grid((6, 4), (2, 0), rowspan=4, colspan=4)
    axis_1.plot(dates, prices)
    axis_1.grid(True)
    rsi_line = relative_strength_index(prices, n_variable=700)
    axis_2 = matplotlib.pyplot.subplot2grid((6, 4), (0, 0), sharex=axis_1, rowspan=2, colspan=4)
    axis_2.plot(dates, rsi_line)
    axis_2.axhline(40, color='g')
    axis_2.axhline(60, color='r')
    axis_2.set_yticks([40, 60])
    axis_2.grid(True)
    matplotlib.pyplot.show()

if __name__ == '__main__':
    testing_data()
