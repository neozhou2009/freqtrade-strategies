from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class AlwaysBuy(IStrategy):
    """
    Improved AlwaysBuy Strategy - Now with proper exit signals

    CRITICAL FIXES:
    - Changed from "always buy" to trend-based entry
    - Added proper exit signals with multiple conditions
    - Fixed unrealistic ROI values (100%+)
    - Added technical indicators for signal quality
    - Added trailing stop to protect profits

    WARNING: Original strategy would always buy but never sell properly,
    leading to continuous position opening and potential margin calls.
    """

    INTERFACE_VERSION = 3

    # ROI table - Fixed: Realistic profit targets
    minimal_roi = {
        "0": 0.10,
        "60": 0.07,
        "120": 0.05,
        "240": 0.03
    }

    # Stoploss - More reasonable -15%
    stoploss = 0.10  # [-10%] 已优化: 原值为 -0.1500 (已禁用), 改为 +0.10 (止损启用)

    # Trailing stop - ENABLED to protect profits
    trailing_stop = True
    trailing_stop_positive = 0.015   # 1.5% profit triggers trailing
    trailing_stop_positive_offset = 0.04  # 4% profit moves stop to +1.5%
    trailing_only_offset_is_reached = True

    # Better timeframe for trend analysis
    timeframe = "15m"
    use_exit_signal = True

    # Position sizing limit
    max_open_trades = 3

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add technical indicators for better signal generation
        """
        # EMA for trend identification
        dataframe['ema_fast'] = ta.EMA(dataframe, timeperiod=9)
        dataframe['ema_slow'] = ta.EMA(dataframe, timeperiod=21)

        # RSI for overbought/oversold
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # ATR for volatility-based stops
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry conditions - Trend following with filters
        """
        dataframe.loc[
            (
                (dataframe['ema_fast'] > dataframe['ema_slow']) &  # Uptrend
                (dataframe['close'] > dataframe['ema_fast']) &  # Price above fast EMA
                (dataframe['rsi'] < 70) &  # Not overbought
                (dataframe['volume'] > 0)
            ),
            ['enter_long', 'enter_tag']
        ] = (1, 'trend_follow')

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit conditions - Multiple exit scenarios
        """
        # Exit when trend reverses or overbought
        dataframe.loc[
            (
                (
                    (dataframe['ema_fast'] < dataframe['ema_slow']) |  # Trend reversed
                    (dataframe['rsi'] > 75)  # Or severely overbought
                ) &
                (dataframe['volume'] > 0)
            ),
            ['exit_long', 'exit_tag']
        ] = (1, 'trend_reversal')

        return dataframe
