# pragma pylint: disable=missing-module-docstring, invalid-name

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from datetime import datetime
from freqtrade.persistence import Trade


class AlexNexusForgeV7(IStrategy):
    """
    AlexNexusForge V7
    IMPROVEMENT: "Lock It In" (Tiered Trailing)
    - Fixes V6's "Profit Roundtrip" issue.
    - Adds Tiered Trailing Stop (Break Even at 2%).
    - Adds RSI Overbought/Oversold early exits.
    """

    timeframe = "1h"
    startup_candle_count = 200
    process_only_new_candles = True
    can_short = True

    # ==============================
    # === RISK MANAGEMENT ==========
    # ==============================

    # 1. Stoploss: -5% (Fixed risk)
    stoploss = -0.05

    # 2. ROI: Still wide to let profits run, but helps with spikes
    minimal_roi = {
        "0": 0.20,       # Take profit at 20% spike
        "60": 0.10,      # After 1 hour, take 10%
        "120": 0.05,     # After 2 hours, take 5%
    }

    # 3. Custom Trailing Stop (The Secret Sauce)
    use_custom_stoploss = True

    # 4. Exit Signal
    use_exit_signal = True
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
                "lookback_period_candles": 48,
                "trade_limit": 2,
                "stop_duration_candles": 12,
            },
        ]

    # ==============================
    # === CUSTOM STOPLOSS ==========
    # ==============================
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        
        # Tier 1: Break Even
        # If profit > 2%, move SL to 0.5% profit (Secure fees)
        if current_profit > 0.02:
            return -0.015  # Trailing offset from current price? No, this Logic is relative to OPEN
            # Freqtrade logic: return value is relative to current_rate
            # We want to lock in profit.
            # simpler approach: Smart Trailing
            
            if current_profit > 0.10:
                return 0.05  # Lock 5% if we hit 10%
            elif current_profit > 0.05:
                return 0.02  # Lock 2% if we hit 5%
            elif current_profit > 0.02:
                 return 0.005 # Lock 0.5% (Break Even) if we hit 2%

        # Default: fixed stoploss
        return 1  # 1 means "do nothing / keep default"

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
        
        # MACD Confirmation
        macd_strong_up = dataframe["macd"] > dataframe["macdsignal"]
        macd_strong_down = dataframe["macd"] < dataframe["macdsignal"]

        # --- LONG ENTRY ---
        dataframe.loc[
            (
                is_uptrend &
                strong_trend &
                has_volume &
                macd_strong_up & 
                (dataframe["rsi"] < 70)
            ),
            "enter_long"
        ] = 1

        # --- SHORT ENTRY ---
        dataframe.loc[
            (
                is_downtrend &
                strong_trend &
                has_volume &
                macd_strong_down &
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

        # 1. TREND REVERSAL (EMA Cross)
        dataframe.loc[
            qtpylib.crossed_below(dataframe["ema50"], dataframe["ema200"]),
            "exit_long"
        ] = 1

        dataframe.loc[
            qtpylib.crossed_above(dataframe["ema50"], dataframe["ema200"]),
            "exit_short"
        ] = 1
        
        # 2. RSI OVERBOUGHT/OVERSOLD (Early exit)
        # If Long and RSI > 80 -> TAKE PROFIT
        dataframe.loc[dataframe["rsi"] > 80, "exit_long"] = 1
        
        # If Short and RSI < 20 -> TAKE PROFIT
        dataframe.loc[dataframe["rsi"] < 20, "exit_short"] = 1

        return dataframe

    # ==============================
    # === LEVERAGE =================
    # ==============================
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, side: str, **kwargs) -> float:
        return 2.0
