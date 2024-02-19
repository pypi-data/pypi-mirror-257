import numpy as np
import pandas_ta as ta
from collections import deque

class SMA:
    def __init__(self, period):
        self.period = period
        self.points = []
        self.value = None
    def compute(self, point):
        return np.mean(self.points + [float(point)])
    def update(self, point):
        self.points.append(float(point))
        self.points = self.points[-self.period:]
        if(len(self.points) == self.period):
            self.value = np.mean(self.points)
        return self.value
    
class EMA:
    def __init__(self, period, smoothing_factor=2):
        self.period = period
        self.smoothing_factor = smoothing_factor
        self.mult = self.smoothing_factor / (1+self.period)
        self.points = []
        self.value = None
    def update(self, point):
        self.points.append(point)
        self.points = self.points[-(self.period+1):]
        if(len(self.points) == self.period):
            self.value = np.mean(self.points) # Simple SMA
        elif(len(self.points) > self.period):
            self.value = (point * self.mult) + (self.value * (1-self.mult))
        return self.value

class WMA:
    def __init__(self, period):
        self.period = period
        self.points = deque(maxlen=period)
        self._den = (period*(period+1))//2
        self._weights = np.arange(1,period+1)
        self.value = None
    def update(self, point):
        self.points.append(point)
        if(len(self.points) == self.period):
            self.value = sum(self._weights*self.points)/self._den
        return self.value

class SMMA:
    '''Smoothed Moving Average'''
    def __init__(self, period):
        assert period > 1, "Period needs to be greater than 1."
        self.period = period
        self.ema_period = self.period*2-1
        # https://stackoverflow.com/a/72533211/6430403
        self.ema = EMA(self.ema_period)
    def update(self, point):
        self.value = self.ema.update(point)
        return self.value
    
class RSI:
    def __init__(self, period):
        self.period = period
        self.points = []
        self.losses = []
        self.gains = []
        self.avg_gain = None
        self.avg_loss = None
        self.rsi = None
        self.value = None
    # def compute(self, point):
    #     points = self.points + [float(point)]
        
    def update(self, point):
        self.points.append(float(point))
        if(len(self.points) > 1):
            diff = self.points[-1] - self.points[-2]
            if(diff >= 0):
                self.gains.append(diff)
                self.losses.append(0)
            else:
                self.gains.append(0)
                self.losses.append(-diff)
        self.points = self.points[-(self.period+1):]
        self.gains = self.gains[-(self.period):]
        self.losses = self.losses[-(self.period):]

        if(len(self.points) == self.period+1):
            if(self.avg_gain is None):
                self.avg_gain = np.mean(self.gains)
                self.avg_loss = np.mean(self.losses)
            else:
                self.avg_gain = ((self.avg_gain*(self.period-1)) + self.gains[-1])/self.period
                self.avg_loss = ((self.avg_loss*(self.period-1)) + self.losses[-1])/self.period
            rs = self.avg_gain / self.avg_loss
            self.rsi = 100 - (100/(1+rs))
            self.value = self.rsi
        return self.value

class TRANGE:
    '''True Range'''
    def __init__(self):
        self.prev_close = None
        self.value = None
    def compute(self, candle):
        if(self.prev_close is None):
            return candle['high'] - candle['low']
        else:
            return max(
                candle['high'] - candle['low'],
                abs(candle['high'] - self.prev_close),
                abs(candle['low'] - self.prev_close)
            )
    def update(self, candle):
        self.value = self.compute(candle)
        self.prev_close = candle['close']
        return self.value

class ATR:
    '''Average True Range'''
    def __init__(self, period, candles=None):
        self.period = period
        self.period_1 = period-1
        self.TR = TRANGE()
        if(candles is None):
            self.atr = 0
            self.value = None
            self.count = 0
        else:
            ta_ATR = ta.atr(candles['high'], candles['low'], candles['close'], length=period)
            self.atr = ta_ATR.iloc[-1]
            self.value = self.atr
            self.count = len(ta_ATR)
            self.TR.update(candles.iloc[-1])
    def compute(self, candle):
        tr = self.TR.compute(candle)
        if(self.count < self.period):
            return None
        elif(self.count == self.period):
            return (self.atr + tr)/self.period
        else:
            return (self.atr*self.period_1 + tr)/self.period

    def update(self, candle):
        self.count += 1
        tr = self.TR.update(candle)
        if(self.count < self.period):
            self.atr += tr
            return None
        if(self.count == self.period):
            self.atr += tr
            self.atr /= self.period
        else:
            self.atr = (self.atr*self.period_1 + tr)/self.period
        self.value = self.atr
        return self.value

class SuperTrend:
    def __init__(self, atr_length, factor, candles=None):
        self.factor = factor
        if(candles is None):
            self.ATR = ATR(atr_length)
            self.lower_band = None
            self.upper_band = None
            self.super_trend = 1
            self.final_band = None
            self.value = (None, None) # direction, value
        else:
            self.ATR = ATR(atr_length, candles=candles)
            ta_ST = ta.supertrend(candles['high'], candles['low'], candles['close'], length=atr_length, multiplier=self.factor, offset=0)
            ta_ST.columns = ta_ST.columns.str.replace('_.*','',regex=True)
            ta_ST_last = ta_ST.iloc[-1]
            self.lower_band = ta_ST_last['SUPERTl']
            self.upper_band = ta_ST_last['SUPERTs']
            self.super_trend = int(ta_ST_last['SUPERTd'])
            self.final_band = ta_ST_last['SUPERT']
            self.value = (self.super_trend, self.final_band) # direction, value
                        
    def compute(self, candle):
        median = round((candle['high']+candle['low'])/2, 4)
        atr = self.ATR.compute(candle)
        if(atr is None):
            return None, None
        basic_upper_band = round(median + self.factor * atr, 4)
        basic_lower_band = round(median - self.factor * atr, 4)
        super_trend = self.super_trend
        if self.super_trend == 1:
            upper_band = basic_upper_band
            lower_band = max(basic_lower_band, self.lower_band) if self.lower_band is not None else basic_lower_band
            if candle['close'] <= self.lower_band: super_trend = -1
        else:
            lower_band = basic_lower_band
            upper_band = min(basic_upper_band, self.upper_band) if self.upper_band is not None else basic_upper_band
            if candle['close'] >= self.upper_band: super_trend = 1
        if(super_trend == 1):
            final_band = lower_band
        else:
            final_band = upper_band
        return (super_trend, final_band)
    def update(self, candle):
        median = round((candle['high']+candle['low'])/2, 4)
        atr = self.ATR.update(candle)
        if(atr is None):
            return None, None
        basic_upper_band = round(median + self.factor * atr, 4)
        basic_lower_band = round(median - self.factor * atr, 4)
        if self.super_trend == 1:
            self.upper_band = basic_upper_band
            self.lower_band = max(basic_lower_band, self.lower_band) if self.lower_band is not None else basic_lower_band
            if candle['close'] <= self.lower_band:
                self.super_trend = -1
        else:
            self.lower_band = basic_lower_band
            self.upper_band = min(basic_upper_band, self.upper_band) if self.upper_band is not None else basic_upper_band
            if candle['close'] >= self.upper_band:
                self.super_trend = 1

        if(self.super_trend == 1):
            self.final_band = self.lower_band
        else:
            self.final_band = self.upper_band
        self.value = (self.super_trend, self.final_band)
        return self.value

class HeikinAshi:
    def __init__(self):
        self.value = None

    def compute(self, candle):
        ha = {}
        ha['close'] = round((candle.open+candle.high+candle.low+candle.close)/4,4)
        if(self.value is None):
            # no previous candle
            ha['open'] = candle.open
        else:
            ha['open'] = round((self.value['open']+self.value['close'])/2,4)
        ha['high'] = max(candle.high, ha['open'], ha['close'])
        ha['low'] = min(candle.low, ha['open'], ha['close'])
        return ha

    def update(self, candle):
        self.value = self.compute(candle)
        return self.value

class Renko:
    def __init__(self, start_price=None):
        self.bricks = []
        self.current_direction = 0
        self.brick_end_price = start_price
        self.pwick = 0   # positive wick
        self.nwick = 0   # negative wick
        self.brick_num = 0
        self.value = None
        
    def _create_brick(self, direction, brick_size, price):
        self.brick_end_price = round(self.brick_end_price + direction*brick_size,2)
        brick = {
            'direction': direction,
            'brick_num': self.brick_num,
            'wick_size': self.nwick if direction==1 else self.pwick,
            'brick_size': brick_size,
            'brick_end_price': self.brick_end_price,
            'price': price
        }
        self.bricks.append(brick)
        self.brick_num += 1
        self.current_direction = direction
        self.pwick = 0
        self.nwick = 0
        return brick        
        
    def update(self, price, brick_size):
        if(self.brick_end_price is None):
            self.brick_end_price = price
            #print("renko brick start price:", price)
            return None
        if(brick_size is None): return None
        bricks = None
        change = round(price - self.brick_end_price, 2)
        self.pwick = max(change, self.pwick)
        self.nwick = min(-change, self.nwick)
        if(self.current_direction == 0):
            direction = 0
            if(change >= brick_size): direction = 1
            elif(-change >= brick_size): direction = -1
            if(direction != 0):
                #print("firect brick direction:", str(direction))
                num_bricks = int(abs(change)//brick_size)
                bricks = [self._create_brick(direction, brick_size, price) for i in range(num_bricks)]
                
        elif(self.current_direction == 1):
            if(change >= brick_size):
                # more bricks in +1 direction
                num_bricks = int(abs(change)//brick_size)
                bricks = [self._create_brick(1, brick_size, price) for i in range(num_bricks)]
                
            elif(-change >= 2*brick_size):
                # reverse direction to -1
                num_bricks = int(abs(change)//brick_size)
                bricks = [self._create_brick(-1, brick_size, price) for i in range(num_bricks-1)]
                
        elif(self.current_direction == -1):
            if(-change >= brick_size):
                # more bricks in -1 direction
                num_bricks = int(abs(change)//brick_size)
                bricks = [self._create_brick(-1, brick_size, price) for i in range(num_bricks)]
                
            elif(change >= 2*brick_size):
                # reverse direction to +1
                num_bricks = int(abs(change)//brick_size)
                bricks = [self._create_brick(1, brick_size, price) for i in range(num_bricks-1)]

        self.value = bricks
        return bricks

import operator
COMPARATORS = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq    
}
class IsOrder:
    ''' Checks if a given list of elements is in an order. eg. all increasing '''
    ''' all_increasing = IsOrder('>', len) '''
    ''' all_decreasing = IsOrder('<=', len) '''
    ''' doubling = IsOrder(lambda a,b: a == 2*b, len) '''
    def __init__(self, comparator, length):
        self.comparator = COMPARATORS.get(comparator, comparator)
        self.length = length
        self.q = deque(length*[None], maxlen=length)
        self.fresh = True
        self.order_idx = 1
        self.is_ordered = False
        self.value = False

    def update(self, element):
        self.q.append(element)
        if(self.fresh): 
            self.fresh = False
            return False
        # comparator (new element, old element)
        if(self.comparator(element, self.q[-2])):
            self.order_idx += 1
        else:
            self.order_idx = 1
        self.is_ordered = self.order_idx >= self.length
        self.value = self.is_ordered
        return self.value