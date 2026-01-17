# pragma pylint: disable=missing-module-docstring, invalid-name

from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
from datetime import datetime


class AlexNexusForgeV5(IStrategy):
    """
    AlexNexusForge V5
    EXPECTANCY FIX – EXIT SIGNAL REMOVED + TREND FILTER
    """

    timeframe = "1h"
    startup_candle_count = 200
    process_only_new_candles = True
    can_short = True

    # ==============================
    # === RISK STRUCTURE ===========
    # ==============================

    stoploss = -0.03  # 🔒 smaller loss

    trailing_stop = True
    trailing_stop_positive = 0.006      # 0.6%
    trailing_stop_positive_offset = 0.015  # start at 1.5%
    trailing_only_offset_is_reached = True

    minimal_roi = {
        "0": 0.02,
        "120": 0.015,
        "360": 0.01,
        "720": 0.005,
    }

    # ❌ KILL EXIT SIGNAL
    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # ==============================
    # === PROTECTIONS ==============
    # ==============================
    @property
    def protections(self):
        return [
            {"method": "CooldownPeriod", "stop_duration_candles": 3},
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 24,
                "trade_limit": 2,
                "stop_duration_candles": 12,
            },
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": 72,
                "trade_limit": 1,
                "max_allowed_drawdown": 0.20,
            },
        ]

    # ==============================
    # === INDICATORS ===============
    # ==============================
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema50"] = ta.EMA(dataframe["close"], timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe["close"], timeperiod=200)
        dataframe["rsi"] = ta.RSI(dataframe["close"], timeperiod=14)
        dataframe["adx"] = ta.ADX(dataframe)
        return dataframe

    # ==============================
    # === ENTRY ====================
    # ==============================
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["enter_long"] = 0
        dataframe["enter_short"] = 0

        # 🚫 NO TRADE IN CHOP
        trend_filter = dataframe["adx"] > 25

        dataframe.loc[
            (
                trend_filter &
                (dataframe["close"] > dataframe["ema200"]) &
                (dataframe["ema50"] > dataframe["ema200"]) &
                (dataframe["rsi"] > 45) &
                (dataframe["rsi"] < 70)
            ),
            "enter_long"
        ] = 1

        dataframe.loc[
            (
                trend_filter &
                (dataframe["close"] < dataframe["ema200"]) &
                (dataframe["ema50"] < dataframe["ema200"]) &
                (dataframe["rsi"] < 55) &
                (dataframe["rsi"] > 30)
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
        return dataframe

    # ==============================
    # === LEVERAGE =================
    # ==============================
    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        side: str,
        **kwargs
    ) -> float:
        return min(3.0, max_leverage)
