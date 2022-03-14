import numpy

def ATR(data, atr_const):
    data = data.head(atr_const+1)
    box = []
    for a in range(atr_const):
        TR1 = data['high_price'].iloc[a] - data['low_price'].iloc[a]
        TR2 = data['high_price'].iloc[a] - data['trade_price'].iloc[a+1]
        TR3 = data['low_price'].iloc[a] - data['trade_price'].iloc[a+1]
        True_range = max(TR1,TR2,TR3)
        box.append(True_range)
    ATR = round(numpy.mean(box),2)
    return ATR