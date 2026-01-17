# pragma pylint: disable=missing-module-docstring, invalid-name

from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from datetime import datetime


class AlexNexusForgeV6(IStrategy):
    """
    AlexNexusForge V6
    PHILOSOPHY: "Let Profits Run" (Trend Following)
    - Wide ROI loop to catch big pumps/dumps.
    - Looser trailing stop to prevent shakeouts.
    - Stricter entry (Volume + MACD confirmation).
    """

    timeframe = "1h"
    startup_candle_count = 200
    process_only_new_candles = True
    can_short = True

    # ==============================
    # === RISK MANAGEMENT (FIXED) ==
    # ==============================

    # 1. Stoploss: -5% (Standard for 1h trend following)
    stoploss = -0.05

    # 2. Trailing Stop: Designed to catch big trends
    trailing_stop = True
    # Trail 2% behind price (Loose trail)
    trailing_stop_positive = 0.02
    # Only activate trailing after we are 6% in profit (Secure the bag late, let early volatility play out)
    trailing_stop_positive_offset = 0.06
    trailing_only_offset_is_reached = True

    # 3. ROI: Minimum manual target needed, mostly rely on trailing stop or trend reversal
    minimal_roi = {
        "0": 100.0,       # Effectively disable ROI for immediate profit, wait for trend
        "720": 0.15,      # After 30 days (720h), accept 15%
        "1440": 0.05,     # After 60 days, accept 5%
    }

    # 4. Exit Signal: ONLY exit on trend reversal
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # ==============================
    # === PROTECTIONS ==============
    # ==============================
    @property
    def protections(self):
        return [
            {"method": "CooldownPeriod", "stop_duration_candles": 5},
            # Lockout pair if it hits stoploss 3 times in a row
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 48,
                "trade_limit": 3,
                "stop_duration_candles": 24,
            },
        ]

    # ==============================
    # === INDICATORS ===============
    # ==============================
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Trend
        dataframe["ema50"] = ta.EMA(dataframe["close"], timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe["close"], timeperiod=200)

        # Momentum
        dataframe["rsi"] = ta.RSI(dataframe["close"], timeperiod=14)
        dataframe["adx"] = ta.ADX(dataframe)
        
        # MACD
        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        # Volume
        dataframe["volume_mean"] = dataframe["volume"].rolling(24).mean()

        return dataframe

    # ==============================
    # === ENTRY ====================
    # ==============================
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["enter_long"] = 0
        dataframe["enter_short"] = 0

        # Conditions
        is_uptrend = (dataframe["close"] > dataframe["ema200"]) & (dataframe["ema50"] > dataframe["ema200"])
        is_downtrend = (dataframe["close"] < dataframe["ema200"]) & (dataframe["ema50"] < dataframe["ema200"])
        
        has_volume = dataframe["volume"] > dataframe["volume_mean"]
        strong_trend = dataframe["adx"] > 25
        
        # Momentum check (Don't buy top / sell bottom)
        rsi_valid_long = dataframe["rsi"] < 70
        rsi_valid_short = dataframe["rsi"] > 30

        # MACD Confirmation
        macd_cross_up = qtpylib.crossed_above(dataframe["macd"], dataframe["macdsignal"])
        macd_strong_up = dataframe["macd"] > dataframe["macdsignal"]
        
        macd_cross_down = qtpylib.crossed_below(dataframe["macd"], dataframe["macdsignal"])
        macd_strong_down = dataframe["macd"] < dataframe["macdsignal"]

        # --- LONG ENTRY ---
        # 1. Trend is UP
        # 2. ADX indicates trend strength
        # 3. Volume is above average
        # 4. MACD is bullish
        dataframe.loc[
            (
                is_uptrend &
                strong_trend &
                has_volume &
                macd_strong_up & 
                rsi_valid_long
            ),
            "enter_long"
        ] = 1

        # --- SHORT ENTRY ---
        # 1. Trend is DOWN
        # 2. ADX indicates trend strength
        # 3. Volume is above average
        # 4. MACD is bearish
        dataframe.loc[
            (
                is_downtrend &
                strong_trend &
                has_volume &
                macd_strong_down &
                rsi_valid_short
            ),
            "enter_short"
        ] = 1

        return dataframe

    # ==============================
    # === EXIT =====================
    # ==============================
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["exit_long"] = 0
        dataframe["exit_short"] = 0

        # EXIT ON TREND REVERSAL
        # If EMA50 crosses below EMA200, the Uptrend is dead -> Exit Long
        dataframe.loc[
            qtpylib.crossed_below(dataframe["ema50"], dataframe["ema200"]),
            "exit_long"
        ] = 1

        # If EMA50 crosses above EMA200, the Downtrend is dead -> Exit Short
        dataframe.loc[
            qtpylib.crossed_above(dataframe["ema50"], dataframe["ema200"]),
            "exit_short"
        ] = 1

        return dataframe

    # ==============================
    # === LEVERAGE =================
    # ==============================
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, side: str, **kwargs) -> float:
        # Conservative leverage for trend following to withstand volatility
        return 2.0
