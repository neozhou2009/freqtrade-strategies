# pragma pylint: disable=missing-module-docstring, invalid-name

from freqtrade.strategy import IStrategy
from freqtrade.persistence import Trade
from pandas import DataFrame
import pandas as pd
import numpy as np
import talib.abstract as ta
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AlexNexusForgeV4(IStrategy):
    """
    AlexNexusForge V4
    STRUCTURE-FIXED FUTURES STRATEGY
    """

    # ==============================
    # === BASIC CONFIG ============
    # ==============================
    timeframe = "1h"
    startup_candle_count = 200
    process_only_new_candles = True
    can_short = True

    # ==============================
    # === RISK CORE (FIXED) ========
    # ==============================

    # 🔒 HARD STOPLOSS (NO MORE SUICIDE)
    stoploss = -0.04  # -4%

    # ✅ REALISTIC TRAILING
    trailing_stop = True
    trailing_stop_positive = 0.003      # 0.3%
    trailing_stop_positive_offset = 0.01  # start at 1%
    trailing_only_offset_is_reached = True

    # ✅ ROI – 1H REALITY BASED
    minimal_roi = {
        "0": 0.015,
        "60": 0.010,
        "180": 0.008,
        "360": 0.005,
    }

    # Exit behavior
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # ==============================
    # === PROTECTIONS (MANDATORY) ==
    # ==============================
    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 3
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 24,
                "trade_limit": 2,
                "stop_duration_candles": 12,
                "only_per_pair": False
            },
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": 72,
                "trade_limit": 1,
                "max_allowed_drawdown": 0.20
            },
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 48,
                "trade_limit": 2,
                "required_profit": 0.01
            }
        ]

    # ==============================
    # === INDICATORS ===============
    # ==============================
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema50"] = ta.EMA(dataframe["close"], timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe["close"], timeperiod=200)
        dataframe["rsi"] = ta.RSI(dataframe["close"], timeperiod=14)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)

        # Trend state
        dataframe["trend_up"] = (
            (dataframe["close"] > dataframe["ema200"]) &
            (dataframe["ema50"] > dataframe["ema200"])
        )

        dataframe["trend_down"] = (
            (dataframe["close"] < dataframe["ema200"]) &
            (dataframe["ema50"] < dataframe["ema200"])
        )

        return dataframe

    # ==============================
    # === ENTRY ====================
    # ==============================
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["enter_long"] = 0
        dataframe["enter_short"] = 0

        # ✅ LONG – trend continuation only
        dataframe.loc[
            (
                dataframe["trend_up"] &
                (dataframe["rsi"] > 40) &
                (dataframe["rsi"] < 65) &
                (dataframe["close"] > dataframe["ema50"])
            ),
            "enter_long"
        ] = 1

        # ✅ SHORT – only real downtrend
        dataframe.loc[
            (
                dataframe["trend_down"] &
                (dataframe["rsi"] < 60) &
                (dataframe["rsi"] > 35) &
                (dataframe["close"] < dataframe["ema50"])
            ),
            "enter_short"
        ] = 1

        return dataframe

    # ==============================
    # === EXIT (STRUCTURAL) ========
    # ==============================
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["exit_long"] = 0
        dataframe["exit_short"] = 0

        # ❗ EXIT LONG only when trend breaks
        dataframe.loc[
            (
                (dataframe["close"] < dataframe["ema50"]) |
                (dataframe["rsi"] < 35)
            ),
            "exit_long"
        ] = 1

        # ❗ EXIT SHORT only when trend breaks
        dataframe.loc[
            (
                (dataframe["close"] > dataframe["ema50"]) |
                (dataframe["rsi"] > 65)
            ),
            "exit_short"
        ] = 1

        return dataframe

    # ==============================
    # === LEVERAGE CONTROL =========
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
        # 🔒 HARD CAP – STOP OVERCONFIDENCE
        return min(3.0, max_leverage)
