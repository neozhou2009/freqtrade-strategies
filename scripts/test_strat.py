import sys
sys.path.append("/home/neozh/freqtrade-strategies/user_data")
sys.path.append("/home/neozh/freqtrade-strategies")
from freqtrade.resolvers import StrategyResolver
from freqtrade.configuration import Configuration
try:
    from user_data.strategies.BBMod1 import BBMod1
    print("BBMod1 timeframe:", BBMod1.timeframe)
except Exception as e:
    print(e)
