# Frequency Strategy Test Report

**Total Strategies:** 465
**Passed:** 238
**Failed:** 227

## Failed Strategies
### BBMod1
- File: `BBMod1.py`
- Duration: 5.38s
- Error Log:
```
...)
  File "/freqtrade/user_data/strategies/BBMod1.py", line 464, in informative_1h_indicators
    informative_1h['rsi'] = ta.RSI(informative_1h['close'], timeperiod=14)
    ~~~~~~~~~~~~~~^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4322, in __setitem__
    self._set_item(key, value)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4535, in _set_item
    value, refs = self._sanitize_column(value)
                  ~~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 5288, in _sanitize_column
    com.require_length_match(value, self.index)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/common.py", line 573, in require_length_match
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Length of values (0) does not match length of index (576)

```
### BBRSITV
- File: `BBRSITV.py`
- Duration: 5.36s
- Error Log:
```
...2026-02-18 06:38:57,533 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:38:57,534 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:38:57,534 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:38:57,553 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:38:57,567 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:38:59,215 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:38:59,239 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BBRSITV from '/freqtrade/user_data/strategies/BBRSITV.py'...
2026-02-18 06:38:59,240 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:38:59,241 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BBRSIv2
- File: `BBRSIv2.py`
- Duration: 5.29s
- Error Log:
```
...2026-02-18 06:39:02,903 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:39:02,903 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:39:02,904 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:39:02,914 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:39:02,926 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:39:04,502 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:39:04,546 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BBRSIv2 from '/freqtrade/user_data/strategies/BBRSIv2.py'...
2026-02-18 06:39:04,547 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:39:04,547 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BB_RPB_TSL
- File: `BB_RPB_TSL.py`
- Duration: 5.29s
- Error Log:
```
..., line 779, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL.py", line 408, in informative_1h_indicators
    mom = momdiv(informative_1h)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL.py", line 1158, in momdiv
    mom: Series = ta.MOM(dataframe, timeperiod=mom_length)
                  ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "talib/_abstract.pxi", line 474, in talib._ta_lib.Function.__call__
  File "talib/_abstract.pxi", line 384, in talib._ta_lib.Function.outputs
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/series.py", line 578, in __init__
    com.require_length_match(data, index)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/common.py", line 573, in require_length_match
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Length of values (0) does not match length of index (576)

```
### BB_RPB_TSL_2
- File: `BB_RPB_TSL_2.py`
- Duration: 3.26s
- Error Log:
```
...` to download the data
2026-02-18 06:39:13,184 - freqtrade.data.history.datahandlers.idatahandler - WARNING - ETH/USDT:USDT, futures, 5m, data ends at 2026-01-21 23:55:00
2026-02-18 06:39:13,196 - freqtrade.optimize.backtesting - INFO - Loading data from 2026-01-20 00:00:00 up to 2026-01-21 23:55:00 (1 days).
2026-02-18 06:39:13,198 - freqtrade.data.history.datahandlers.idatahandler - WARNING - No history for BTC/USDT:USDT, funding_rate, 1h found. Use `freqtrade download-data` to download the data
2026-02-18 06:39:13,210 - freqtrade.data.history.datahandlers.idatahandler - WARNING - No history for BTC/USDT:USDT, mark, 1h found. Use `freqtrade download-data` to download the data
2026-02-18 06:39:13,240 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2026-02-18 06:39:13,241 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy BB_RPB_TSL_2
2026-02-18 06:39:13,242 - freqtrade - ERROR - Cannot determine parameter space for max_slip.

```
### BB_RPB_TSL_BI
- File: `BB_RPB_TSL_BI.py`
- Duration: 5.35s
- Error Log:
```
... to download the data
2026-02-18 06:39:18,557 - freqtrade.data.history.datahandlers.idatahandler - WARNING - ETH/USDT:USDT, futures, 5m, data ends at 2026-01-21 23:55:00
2026-02-18 06:39:18,569 - freqtrade.optimize.backtesting - INFO - Loading data from 2026-01-20 00:00:00 up to 2026-01-21 23:55:00 (1 days).
2026-02-18 06:39:18,570 - freqtrade.data.history.datahandlers.idatahandler - WARNING - No history for BTC/USDT:USDT, funding_rate, 1h found. Use `freqtrade download-data` to download the data
2026-02-18 06:39:18,580 - freqtrade.data.history.datahandlers.idatahandler - WARNING - No history for BTC/USDT:USDT, mark, 1h found. Use `freqtrade download-data` to download the data
2026-02-18 06:39:18,608 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2026-02-18 06:39:18,609 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy BB_RPB_TSL_BI
2026-02-18 06:39:18,610 - freqtrade - ERROR - Cannot determine parameter space for max_slip.

```
### BB_RPB_TSL_BIV1
- File: `BB_RPB_TSL_BIV1.py`
- Duration: 5.44s
- Error Log:
```
...o download the data
2026-02-18 06:39:24,034 - freqtrade.data.history.datahandlers.idatahandler - WARNING - ETH/USDT:USDT, futures, 5m, data ends at 2026-01-21 23:55:00
2026-02-18 06:39:24,045 - freqtrade.optimize.backtesting - INFO - Loading data from 2026-01-20 00:00:00 up to 2026-01-21 23:55:00 (1 days).
2026-02-18 06:39:24,047 - freqtrade.data.history.datahandlers.idatahandler - WARNING - No history for BTC/USDT:USDT, funding_rate, 1h found. Use `freqtrade download-data` to download the data
2026-02-18 06:39:24,055 - freqtrade.data.history.datahandlers.idatahandler - WARNING - No history for BTC/USDT:USDT, mark, 1h found. Use `freqtrade download-data` to download the data
2026-02-18 06:39:24,084 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2026-02-18 06:39:24,086 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy BB_RPB_TSL_BIV1
2026-02-18 06:39:24,087 - freqtrade - ERROR - Cannot determine parameter space for max_slip.

```
### BB_RPB_TSL_SMA_Tranz
- File: `BB_RPB_TSL_SMA_Tranz.py`
- Duration: 5.56s
- Error Log:
```
...running with dry_run enabled
2026-02-18 06:39:27,564 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:39:27,564 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:39:27,576 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:39:27,588 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:39:29,351 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:39:29,481 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/BB_RPB_TSL_SMA_Tranz.py due to 'The `scipy` install you are using seems to be 
broken, (extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:39:29,488 - freqtrade - ERROR - Impossible to load Strategy 'BB_RPB_TSL_SMA_Tranz'. This class does not exist or contains Python code errors.

```
### BB_RPB_TSL_SMA_Tranz_TB_1_1_1
- File: `BB_RPB_TSL_SMA_Tranz_TB_1_1_1.py`
- Duration: 5.56s
- Error Log:
```
...informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL_SMA_Tranz_TB_1_1_1.py", line 1116, in informative_1h_indicators
    mom = momdiv(informative_1h)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL_SMA_Tranz_TB_1_1_1.py", line 3123, in momdiv
    mom: Series = ta.MOM(dataframe, timeperiod=mom_length)
                  ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "talib/_abstract.pxi", line 474, in talib._ta_lib.Function.__call__
  File "talib/_abstract.pxi", line 384, in talib._ta_lib.Function.outputs
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/series.py", line 578, in __init__
    com.require_length_match(data, index)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/common.py", line 573, in require_length_match
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Length of values (0) does not match length of index (576)

```
### BB_RPB_TSL_SMA_Tranz_TB_MOD
- File: `BB_RPB_TSL_SMA_Tranz_TB_MOD.py`
- Duration: 3.57s
- Error Log:
```
...
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL_SMA_Tranz_TB_MOD.py", line 1479, in informative_1h_indicators
    mom = momdiv(informative_1h)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL_SMA_Tranz_TB_MOD.py", line 310, in momdiv
    mom: Series = ta.MOM(dataframe, timeperiod=mom_length)
                  ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "talib/_abstract.pxi", line 474, in talib._ta_lib.Function.__call__
  File "talib/_abstract.pxi", line 384, in talib._ta_lib.Function.outputs
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/series.py", line 578, in __init__
    com.require_length_match(data, index)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/common.py", line 573, in require_length_match
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Length of values (0) does not match length of index (576)

```
### BB_RPB_TSL_Tranz
- File: `BB_RPB_TSL_Tranz.py`
- Duration: 5.33s
- Error Log:
```
...in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL_Tranz.py", line 459, in informative_1h_indicators
    mom = momdiv(informative_1h)
  File "/freqtrade/user_data/strategies/BB_RPB_TSL_Tranz.py", line 1943, in momdiv
    mom: Series = ta.MOM(dataframe, timeperiod=mom_length)
                  ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "talib/_abstract.pxi", line 474, in talib._ta_lib.Function.__call__
  File "talib/_abstract.pxi", line 384, in talib._ta_lib.Function.outputs
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/series.py", line 578, in __init__
    com.require_length_match(data, index)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/common.py", line 573, in require_length_match
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Length of values (0) does not match length of index (576)

```
### BB_RPB_TSLmeneguzzo
- File: `BB_RPB_TSLmeneguzzo.py`
- Duration: 6.50s
- Error Log:
```
...ulate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/BB_RPB_TSLmeneguzzo.py", line 378, in informative_1h_indicators
    mom = momdiv(informative_1h)
  File "/freqtrade/user_data/strategies/BB_RPB_TSLmeneguzzo.py", line 1058, in momdiv
    mom: Series = ta.MOM(dataframe, timeperiod=mom_length)
                  ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "talib/_abstract.pxi", line 474, in talib._ta_lib.Function.__call__
  File "talib/_abstract.pxi", line 384, in talib._ta_lib.Function.outputs
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/series.py", line 578, in __init__
    com.require_length_match(data, index)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/common.py", line 573, in require_length_match
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Length of values (0) does not match length of index (576)

```
### BbRoi
- File: `BbRoi.py`
- Duration: 5.73s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:39:56,211 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:39:56,212 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:39:56,212 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:39:56,212 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:39:56,213 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:39:56,213 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:39:56,214 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### BcmbigzDevelop
- File: `BcmbigzDevelop.py`
- Duration: 5.69s
- Error Log:
```
...40:00,147 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:00,148 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:00,148 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:00,160 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:00,173 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:01,796 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:01,841 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BcmbigzDevelop from '/freqtrade/user_data/strategies/BcmbigzDevelop.py'...
2026-02-18 06:40:01,842 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:01,843 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BcmbigzV1
- File: `BcmbigzV1.py`
- Duration: 3.72s
- Error Log:
```
...-02-18 06:40:05,947 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:05,948 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:05,948 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:05,959 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:05,971 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:05,631 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:05,683 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BcmbigzV1 from '/freqtrade/user_data/strategies/BcmbigzV1.py'...
2026-02-18 06:40:05,684 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:05,684 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigPete
- File: `BigPete.py`
- Duration: 5.90s
- Error Log:
```
...2026-02-18 06:40:09,669 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:09,670 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:09,671 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:09,699 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:09,724 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:11,537 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:11,569 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigPete from '/freqtrade/user_data/strategies/BigPete.py'...
2026-02-18 06:40:11,570 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:11,571 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ03
- File: `BigZ03.py`
- Duration: 6.56s
- Error Log:
```
...e
2026-02-18 06:40:16,244 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:16,244 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:16,244 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:16,259 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:16,272 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:18,182 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:18,236 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ03 from '/freqtrade/user_data/strategies/BigZ03.py'...
2026-02-18 06:40:18,237 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:18,238 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ0307HO
- File: `BigZ0307HO.py`
- Duration: 5.67s
- Error Log:
```
...2-18 06:40:22,117 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:22,117 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:22,118 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:22,128 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:22,141 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:23,745 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:23,793 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ0307HO from '/freqtrade/user_data/strategies/BigZ0307HO.py'...
2026-02-18 06:40:23,794 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:23,795 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ03HO
- File: `BigZ03HO.py`
- Duration: 5.72s
- Error Log:
```
...26-02-18 06:40:28,047 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:28,048 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:28,048 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:28,058 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:28,070 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:29,658 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:29,683 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ03HO from '/freqtrade/user_data/strategies/BigZ03HO.py'...
2026-02-18 06:40:29,683 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:29,684 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ04
- File: `BigZ04.py`
- Duration: 3.23s
- Error Log:
```
...e
2026-02-18 06:40:33,286 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:33,287 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:33,287 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:33,298 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:33,310 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:34,988 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:35,052 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ04 from '/freqtrade/user_data/strategies/BigZ04.py'...
2026-02-18 06:40:35,052 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:35,053 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ0407
- File: `BigZ0407.py`
- Duration: 5.38s
- Error Log:
```
...26-02-18 06:40:41,922 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:41,922 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:41,923 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:41,934 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:41,948 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:43,623 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:43,696 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ0407 from '/freqtrade/user_data/strategies/BigZ0407.py'...
2026-02-18 06:40:43,696 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:43,697 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ0407HO
- File: `BigZ0407HO.py`
- Duration: 5.38s
- Error Log:
```
...2-18 06:40:47,324 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:47,324 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:47,325 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:47,336 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:47,347 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:48,914 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:48,972 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ0407HO from '/freqtrade/user_data/strategies/BigZ0407HO.py'...
2026-02-18 06:40:48,972 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:48,973 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ04HO
- File: `BigZ04HO.py`
- Duration: 5.25s
- Error Log:
```
...26-02-18 06:40:52,714 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:52,715 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:52,715 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:52,726 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:52,738 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:54,336 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:54,359 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ04HO from '/freqtrade/user_data/strategies/BigZ04HO.py'...
2026-02-18 06:40:54,360 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:54,361 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ04HO2
- File: `BigZ04HO2.py`
- Duration: 5.38s
- Error Log:
```
...-02-18 06:40:57,943 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:40:57,944 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:40:57,944 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:57,955 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:40:57,967 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:40:59,646 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:40:59,687 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ04HO2 from '/freqtrade/user_data/strategies/BigZ04HO2.py'...
2026-02-18 06:40:59,687 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:40:59,688 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ04_TSL3
- File: `BigZ04_TSL3.py`
- Duration: 3.53s
- Error Log:
```
...18 06:41:01,290 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:01,290 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:01,291 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:01,303 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:01,319 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:03,284 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:03,319 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ04_TSL3 from '/freqtrade/user_data/strategies/BigZ04_TSL3.py'...
2026-02-18 06:41:03,320 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:03,321 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ04_TSL4
- File: `BigZ04_TSL4.py`
- Duration: 5.54s
- Error Log:
```
...18 06:41:06,922 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:06,922 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:06,923 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:06,933 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:06,946 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:08,623 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:08,688 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ04_TSL4 from '/freqtrade/user_data/strategies/BigZ04_TSL4.py'...
2026-02-18 06:41:08,689 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:08,689 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ06
- File: `BigZ06.py`
- Duration: 5.50s
- Error Log:
```
...e
2026-02-18 06:41:12,769 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:12,769 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:12,770 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:12,780 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:12,792 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:14,307 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:14,338 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ06 from '/freqtrade/user_data/strategies/BigZ06.py'...
2026-02-18 06:41:14,338 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:14,339 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ07
- File: `BigZ07.py`
- Duration: 5.33s
- Error Log:
```
...e
2026-02-18 06:41:18,009 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:18,009 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:18,010 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:18,020 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:18,033 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:19,645 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:19,702 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ07 from '/freqtrade/user_data/strategies/BigZ07.py'...
2026-02-18 06:41:19,702 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:19,703 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ07Next
- File: `BigZ07Next.py`
- Duration: 5.27s
- Error Log:
```
...2-18 06:41:23,352 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:23,352 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:23,353 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:23,363 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:23,375 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:24,967 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:25,029 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ07Next from '/freqtrade/user_data/strategies/BigZ07Next.py'...
2026-02-18 06:41:25,029 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:25,030 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BigZ07Next2
- File: `BigZ07Next2.py`
- Duration: 3.73s
- Error Log:
```
...18 06:41:28,601 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:28,602 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:28,602 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:28,612 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:28,629 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:30,596 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:30,678 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BigZ07Next2 from '/freqtrade/user_data/strategies/BigZ07Next2.py'...
2026-02-18 06:41:30,679 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:30,680 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BinClucMad
- File: `BinClucMad.py`
- Duration: 5.44s
- Error Log:
```
...2-18 06:41:32,481 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:32,481 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:32,482 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:32,495 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:32,509 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:34,140 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:34,181 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BinClucMad from '/freqtrade/user_data/strategies/BinClucMad.py'...
2026-02-18 06:41:34,181 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:34,182 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BinClucMadDevelop
- File: `BinClucMadDevelop.py`
- Duration: 5.88s
- Error Log:
```
...254 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:38,255 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:38,255 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:38,267 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:38,280 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:39,927 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:39,969 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BinClucMadDevelop from '/freqtrade/user_data/strategies/BinClucMadDevelop.py'...
2026-02-18 06:41:39,970 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:39,970 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BinClucMadSMADevelop
- File: `BinClucMadSMADevelop.py`
- Duration: 5.60s
- Error Log:
```
...freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:44,052 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:44,053 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:44,063 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:44,075 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:45,719 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:45,751 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BinClucMadSMADevelop from '/freqtrade/user_data/strategies/BinClucMadSMADevelop.py'...
2026-02-18 06:41:45,752 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:45,753 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### BinClucMadV1
- File: `BinClucMadV1.py`
- Duration: 5.51s
- Error Log:
```
... 06:41:49,387 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:49,387 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:49,388 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:49,399 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:49,410 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:51,172 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:51,220 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy BinClucMadV1 from '/freqtrade/user_data/strategies/BinClucMadV1.py'...
2026-02-18 06:41:51,220 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:51,221 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CBPete9
- File: `CBPete9.py`
- Duration: 5.17s
- Error Log:
```
...2026-02-18 06:41:54,863 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:54,863 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:54,864 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:54,874 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:54,886 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:56,398 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:56,421 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CBPete9 from '/freqtrade/user_data/strategies/CBPete9.py'...
2026-02-18 06:41:56,421 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:56,422 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Cluc4werk
- File: `Cluc4werk.py`
- Duration: 3.12s
- Error Log:
```
...-02-18 06:41:58,040 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:41:58,041 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:41:58,041 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:58,051 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:41:58,065 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:41:59,585 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:41:59,619 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Cluc4werk from '/freqtrade/user_data/strategies/Cluc4werk.py'...
2026-02-18 06:41:59,619 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:41:59,620 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Cluc5werk
- File: `Cluc5werk.py`
- Duration: 5.45s
- Error Log:
```
...-02-18 06:42:03,296 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:42:03,296 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:42:03,297 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:03,307 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:03,319 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:42:04,993 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:42:05,032 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Cluc5werk from '/freqtrade/user_data/strategies/Cluc5werk.py'...
2026-02-18 06:42:05,032 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:42:05,033 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Cluc7werk
- File: `Cluc7werk.py`
- Duration: 5.40s
- Error Log:
```
...-02-18 06:42:08,695 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:42:08,695 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:42:08,696 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:08,707 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:08,719 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:42:10,457 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:42:10,488 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Cluc7werk from '/freqtrade/user_data/strategies/Cluc7werk.py'...
2026-02-18 06:42:10,489 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:42:10,489 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ClucFiatROI
- File: `ClucFiatROI.py`
- Duration: 5.35s
- Error Log:
```
...18 06:42:14,201 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:42:14,201 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:42:14,201 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:14,211 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:14,224 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:42:15,763 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:42:15,785 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ClucFiatROI from '/freqtrade/user_data/strategies/ClucFiatROI.py'...
2026-02-18 06:42:15,786 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:42:15,787 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ClucFiatSlow
- File: `ClucFiatSlow.py`
- Duration: 5.67s
- Error Log:
```
... 06:42:19,723 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:42:19,723 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:42:19,724 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:19,735 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:19,753 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:42:21,471 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:42:21,499 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ClucFiatSlow from '/freqtrade/user_data/strategies/ClucFiatSlow.py'...
2026-02-18 06:42:21,500 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:42:21,500 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ClucHAnix
- File: `ClucHAnix.py`
- Duration: 5.50s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:42:30,304 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:42:30,305 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:42:30,305 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:42:30,305 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:42:30,306 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:42:30,306 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:42:30,307 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### ClucHAnix5m
- File: `ClucHAnix5m.py`
- Duration: 5.52s
- Error Log:
```
...NFO - Instance is running with dry_run enabled
2026-02-18 06:42:34,058 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:42:34,059 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:34,070 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:34,083 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:42:35,713 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:42:35,775 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/ClucHAnix5m.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:42:35,815 - freqtrade - ERROR - Impossible to load Strategy 'ClucHAnix5m'. This class does not exist or contains Python code errors.

```
### ClucHAnix_5m
- File: `ClucHAnix_5m.py`
- Duration: 5.40s
- Error Log:
```
...ne 180, in populate_indicators
    inf_heikinashi = qtpylib.heikinashi(informative)
  File "/freqtrade/freqtrade/vendor/qtpylib/indicators.py", line 107, in heikinashi
    bars.at[0, "ha_open"] = (bars.at[0, "open"] + bars.at[0, "close"]) / 2
                             ~~~~~~~^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2576, in __getitem__
    return super().__getitem__(key)
           ~~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2528, in __getitem__
    return self.obj._get_value(*key, takeable=self._takeable)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4232, in _get_value
    row = self.index.get_loc(index)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexes/range.py", line 415, in get_loc
    raise KeyError(key) from err
KeyError: 0

```
### ClucHAnix_5m1
- File: `ClucHAnix_5m1.py`
- Duration: 5.95s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:42:47,198 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:42:47,198 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:42:47,198 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:42:47,199 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:42:47,199 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:42:47,199 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:42:47,200 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### ClucHAnix_BB_RPB_MOD
- File: `ClucHAnix_BB_RPB_MOD.py`
- Duration: 5.88s
- Error Log:
```
...running with dry_run enabled
2026-02-18 06:42:50,999 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:42:50,999 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:51,010 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:51,024 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:42:52,891 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:42:52,993 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/ClucHAnix_BB_RPB_MOD.py due to 'The `scipy` install you are using seems to be 
broken, (extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:42:53,008 - freqtrade - ERROR - Impossible to load Strategy 'ClucHAnix_BB_RPB_MOD'. This class does not exist or contains Python code errors.

```
### ClucHAnix_BB_RPB_MOD2_ROI
- File: `ClucHAnix_BB_RPB_MOD2_ROI.py`
- Duration: 3.43s
- Error Log:
```
...th dry_run enabled
2026-02-18 06:42:54,808 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:42:54,808 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:54,820 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:42:54,834 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:42:56,436 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:42:56,507 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/ClucHAnix_BB_RPB_MOD2_ROI.py due to 'The `scipy` install you are using seems to be 
broken, (extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:42:56,541 - freqtrade - ERROR - Impossible to load Strategy 'ClucHAnix_BB_RPB_MOD2_ROI'. This class does not exist or contains Python code errors.

```
### ClucHAnix_BB_RPB_MOD_CTT
- File: `ClucHAnix_BB_RPB_MOD_CTT.py`
- Duration: 5.62s
- Error Log:
```
...with dry_run enabled
2026-02-18 06:43:00,342 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:00,342 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:00,353 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:00,365 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:02,051 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:02,140 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/ClucHAnix_BB_RPB_MOD_CTT.py due to 'The `scipy` install you are using seems to be 
broken, (extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:43:02,152 - freqtrade - ERROR - Impossible to load Strategy 'ClucHAnix_BB_RPB_MOD_CTT'. This class does not exist or contains Python code errors.

```
### ClucHAnix_BB_RPB_MOD_E0V1E_ROI
- File: `ClucHAnix_BB_RPB_MOD_E0V1E_ROI.py`
- Duration: 5.56s
- Error Log:
```
... enabled
2026-02-18 06:43:05,953 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:05,954 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:05,966 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:05,980 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:07,677 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:07,752 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/ClucHAnix_BB_RPB_MOD_E0V1E_ROI.py due to 'The `scipy` install you are using seems 
to be broken, (extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:43:07,786 - freqtrade - ERROR - Impossible to load Strategy 'ClucHAnix_BB_RPB_MOD_E0V1E_ROI'. This class does not exist or contains Python code errors.

```
### ClucHAnix_hhll
- File: `ClucHAnix_hhll.py`
- Duration: 5.72s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:43:13,419 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:43:13,419 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:43:13,420 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:43:13,420 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:43:13,421 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:43:13,421 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:43:13,422 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### ClucHAwerk
- File: `ClucHAwerk.py`
- Duration: 5.74s
- Error Log:
```
...2-18 06:43:17,337 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:43:17,337 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:17,338 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:17,348 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:17,361 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:19,169 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:19,221 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ClucHAwerk from '/freqtrade/user_data/strategies/ClucHAwerk.py'...
2026-02-18 06:43:19,221 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:43:19,222 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV2
- File: `CombinedBinHAndClucV2.py`
- Duration: 3.30s
- Error Log:
```
...dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/CombinedBinHAndClucV2.py", line 106, in populate_indicators
    informative = self.get_informative_indicators(informative.copy(), metadata)
  File "/freqtrade/user_data/strategies/CombinedBinHAndClucV2.py", line 79, in get_informative_indicators
    ssl_down, ssl_up = SSLChannels(dataframe, 25)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/CombinedBinHAndClucV2.py", line 26, in SSLChannels
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, np.where(df['close'] < df['smaLow'], -1, np.NAN))
                                                                                                  ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### CombinedBinHAndClucV3
- File: `CombinedBinHAndClucV3.py`
- Duration: 5.51s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:43:26,356 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:26,357 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:26,367 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:26,381 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:27,978 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:27,999 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV3 from '/freqtrade/user_data/strategies/CombinedBinHAndClucV3.py'...
2026-02-18 06:43:28,000 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:43:28,000 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV4
- File: `CombinedBinHAndClucV4.py`
- Duration: 5.67s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:43:31,987 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:31,988 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:32,000 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:32,015 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:33,696 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:33,740 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV4 from '/freqtrade/user_data/strategies/CombinedBinHAndClucV4.py'...
2026-02-18 06:43:33,740 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:43:33,741 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV5
- File: `CombinedBinHAndClucV5.py`
- Duration: 5.52s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:43:37,562 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:37,563 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:37,573 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:37,587 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:39,319 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:39,364 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV5 from '/freqtrade/user_data/strategies/CombinedBinHAndClucV5.py'...
2026-02-18 06:43:39,365 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:43:39,365 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV5Hyperoptable
- File: `CombinedBinHAndClucV5Hyperoptable.py`
- Duration: 5.62s
- Error Log:
```
...ed
2026-02-18 06:43:43,195 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:43,195 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:43,208 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:43,223 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:44,856 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:44,889 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CombinedBinHAndClucV5Hyperoptable.py due to 'The `scipy` install you are using 
seems to be broken, (extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:43:44,921 - freqtrade - ERROR - Impossible to load Strategy 'CombinedBinHAndClucV5Hyperoptable'. This class does not exist or contains Python code errors.

```
### CombinedBinHAndClucV6
- File: `CombinedBinHAndClucV6.py`
- Duration: 3.65s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:43:48,893 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:48,893 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:48,904 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:48,917 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:50,524 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:50,587 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV6 from '/freqtrade/user_data/strategies/CombinedBinHAndClucV6.py'...
2026-02-18 06:43:50,587 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:43:50,588 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV6H
- File: `CombinedBinHAndClucV6H.py`
- Duration: 5.40s
- Error Log:
```
...trade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:43:52,401 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:52,401 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:52,412 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:52,424 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:54,034 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:54,069 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV6H from '/freqtrade/user_data/strategies/CombinedBinHAndClucV6H.py'...
2026-02-18 06:43:54,069 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:43:54,070 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV7
- File: `CombinedBinHAndClucV7.py`
- Duration: 5.90s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:43:57,889 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:43:57,889 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:57,901 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:43:57,915 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:43:59,717 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:43:59,760 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV7 from '/freqtrade/user_data/strategies/CombinedBinHAndClucV7.py'...
2026-02-18 06:43:59,761 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:43:59,761 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV8
- File: `CombinedBinHAndClucV8.py`
- Duration: 5.76s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:04,016 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:04,016 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:04,027 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:04,041 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:05,715 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:05,755 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV8 from '/freqtrade/user_data/strategies/CombinedBinHAndClucV8.py'...
2026-02-18 06:44:05,756 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:05,757 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV8Hyper
- File: `CombinedBinHAndClucV8Hyper.py`
- Duration: 5.67s
- Error Log:
```
...change.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:09,675 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:09,675 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:09,686 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:09,699 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:11,398 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:11,434 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV8Hyper from '/freqtrade/user_data/strategies/CombinedBinHAndClucV8Hyper.py'...
2026-02-18 06:44:11,435 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:11,435 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV8XH
- File: `CombinedBinHAndClucV8XH.py`
- Duration: 3.68s
- Error Log:
```
...ade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:18,752 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:18,752 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:18,769 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:18,787 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:20,400 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:20,436 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV8XH from '/freqtrade/user_data/strategies/CombinedBinHAndClucV8XH.py'...
2026-02-18 06:44:20,437 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:20,437 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHAndClucV8XHO
- File: `CombinedBinHAndClucV8XHO.py`
- Duration: 5.96s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:24,285 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:24,286 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:24,296 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:24,309 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:26,311 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:26,338 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHAndClucV8XHO from '/freqtrade/user_data/strategies/CombinedBinHAndClucV8XHO.py'...
2026-02-18 06:44:26,339 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:26,340 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHClucAndMADV3
- File: `CombinedBinHClucAndMADV3.py`
- Duration: 6.22s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:31,059 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:31,059 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:31,070 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:31,082 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:32,708 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:32,750 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHClucAndMADV3 from '/freqtrade/user_data/strategies/CombinedBinHClucAndMADV3.py'...
2026-02-18 06:44:32,750 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:32,751 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHClucAndMADV5
- File: `CombinedBinHClucAndMADV5.py`
- Duration: 5.37s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:36,459 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:36,460 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:36,470 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:36,483 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:38,159 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:38,181 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHClucAndMADV5 from '/freqtrade/user_data/strategies/CombinedBinHClucAndMADV5.py'...
2026-02-18 06:44:38,182 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:38,182 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHClucAndMADV6
- File: `CombinedBinHClucAndMADV6.py`
- Duration: 5.39s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:41,873 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:41,873 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:41,884 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:41,899 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:43,577 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:43,604 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHClucAndMADV6 from '/freqtrade/user_data/strategies/CombinedBinHClucAndMADV6.py'...
2026-02-18 06:44:43,605 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:43,606 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CombinedBinHClucAndMADV9
- File: `CombinedBinHClucAndMADV9.py`
- Duration: 3.27s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:45,179 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:45,179 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:45,190 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:45,202 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:46,850 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:46,876 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CombinedBinHClucAndMADV9 from '/freqtrade/user_data/strategies/CombinedBinHClucAndMADV9.py'...
2026-02-18 06:44:46,876 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:46,877 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CoreStrategy
- File: `CoreStrategy.py`
- Duration: 5.72s
- Error Log:
```
... 06:44:50,918 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:44:50,918 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:50,919 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:50,929 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:50,942 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:52,601 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:52,625 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy CoreStrategy from '/freqtrade/user_data/strategies/CoreStrategy.py'...
2026-02-18 06:44:52,626 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:44:52,626 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### CryptoFrog
- File: `CryptoFrog.py`
- Duration: 5.40s
- Error Log:
```
... INFO - Instance is running with dry_run enabled
2026-02-18 06:44:56,248 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:44:56,249 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:56,260 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:44:56,274 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:44:57,919 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:44:57,994 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrog.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:44:58,007 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrog'. This class does not exist or contains Python code errors.

```
### CryptoFrogHO
- File: `CryptoFrogHO.py`
- Duration: 5.41s
- Error Log:
```
...O - Instance is running with dry_run enabled
2026-02-18 06:45:01,747 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:01,748 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:01,758 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:01,771 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:03,402 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:03,457 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogHO.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:03,487 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogHO'. This class does not exist or contains Python code errors.

```
### CryptoFrogHO2
- File: `CryptoFrogHO2.py`
- Duration: 5.27s
- Error Log:
```
...- Instance is running with dry_run enabled
2026-02-18 06:45:07,057 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:07,058 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:07,068 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:07,080 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:08,675 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:08,742 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogHO2.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:08,753 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogHO2'. This class does not exist or contains Python code errors.

```
### CryptoFrogHO2A
- File: `CryptoFrogHO2A.py`
- Duration: 3.48s
- Error Log:
```
...Instance is running with dry_run enabled
2026-02-18 06:45:12,530 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:12,530 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:12,541 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:12,553 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:14,276 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:14,342 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogHO2A.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:14,359 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogHO2A'. This class does not exist or contains Python code errors.

```
### CryptoFrogHO3A1
- File: `CryptoFrogHO3A1.py`
- Duration: 5.40s
- Error Log:
```
...stance is running with dry_run enabled
2026-02-18 06:45:15,896 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:15,896 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:15,907 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:15,920 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:17,604 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:17,676 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogHO3A1.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:17,694 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogHO3A1'. This class does not exist or contains Python code errors.

```
### CryptoFrogHO3A2
- File: `CryptoFrogHO3A2.py`
- Duration: 6.06s
- Error Log:
```
...stance is running with dry_run enabled
2026-02-18 06:45:21,436 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:21,436 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:21,446 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:21,465 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:23,348 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:23,441 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogHO3A2.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:23,451 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogHO3A2'. This class does not exist or contains Python code errors.

```
### CryptoFrogHO3A3
- File: `CryptoFrogHO3A3.py`
- Duration: 5.64s
- Error Log:
```
...stance is running with dry_run enabled
2026-02-18 06:45:27,558 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:27,558 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:27,570 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:27,585 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:29,324 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:29,400 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogHO3A3.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:29,419 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogHO3A3'. This class does not exist or contains Python code errors.

```
### CryptoFrogHO3A4
- File: `CryptoFrogHO3A4.py`
- Duration: 5.65s
- Error Log:
```
...stance is running with dry_run enabled
2026-02-18 06:45:33,201 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:33,201 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:33,212 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:33,224 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:34,878 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:34,944 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogHO3A4.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:34,967 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogHO3A4'. This class does not exist or contains Python code errors.

```
### CryptoFrogNFI
- File: `CryptoFrogNFI.py`
- Duration: 5.91s
- Error Log:
```
...- Instance is running with dry_run enabled
2026-02-18 06:45:39,009 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:39,009 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:39,020 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:39,032 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:40,722 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:40,827 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogNFI.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:40,838 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogNFI'. This class does not exist or contains Python code errors.

```
### CryptoFrogNFIHO1A
- File: `CryptoFrogNFIHO1A.py`
- Duration: 3.88s
- Error Log:
```
...ce is running with dry_run enabled
2026-02-18 06:45:42,857 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:42,857 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:42,869 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:42,883 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:44,549 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:44,627 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogNFIHO1A.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:44,662 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogNFIHO1A'. This class does not exist or contains Python code errors.

```
### CryptoFrogOffset
- File: `CryptoFrogOffset.py`
- Duration: 5.68s
- Error Log:
```
...ance is running with dry_run enabled
2026-02-18 06:45:48,805 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:48,806 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:48,826 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:48,846 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:50,499 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:50,606 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/CryptoFrogOffset.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:45:50,622 - freqtrade - ERROR - Impossible to load Strategy 'CryptoFrogOffset'. This class does not exist or contains Python code errors.

```
### DCBBBounce
- File: `DCBBBounce.py`
- Duration: 5.73s
- Error Log:
```
...ge - INFO - Instance is running with dry_run enabled
2026-02-18 06:45:54,553 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:45:54,554 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:54,565 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:45:54,577 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:45:56,248 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:45:56,268 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/DCBBBounce.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:45:56,308 - freqtrade - ERROR - Impossible to load Strategy 'DCBBBounce'. This class does not exist or contains Python code errors.

```
### DIV_v1
- File: `DIV_v1.py`
- Duration: 5.53s
- Error Log:
```
...754, in backtest_one_strategy
    preprocessed = self.strategy.advise_all_indicators(data)
  File "/freqtrade/freqtrade/strategy/interface.py", line 1749, in advise_all_indicators
    res[pair] = self.advise_indicators(pair_data.copy(), {"pair": pair}).copy()
                ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1811, in advise_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/DIV_v1.py", line 78, in populate_indicators
    dataframe = divergence(dataframe, "rsi")
  File "/freqtrade/user_data/strategies/DIV_v1.py", line 101, in divergence
    dataframe['ohlc_bottom'] = np.NaN
                               ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 781, in __getattr__
    raise AttributeError(
    ...<3 lines>...
    )
AttributeError: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

```
### DevilStra
- File: `DevilStra.py`
- Duration: 3.24s
- Error Log:
```
...ange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:09,059 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:09,059 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:09,070 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:09,082 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:10,664 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:10,688 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/DevilStra.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:46:10,725 - freqtrade - ERROR - Impossible to load Strategy 'DevilStra'. This class does not exist or contains Python code errors.

```
### Diamond
- File: `Diamond.py`
- Duration: 5.50s
- Error Log:
```
...exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:14,403 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:14,403 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:14,414 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:14,426 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:16,034 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:16,039 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Diamond.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:46:16,082 - freqtrade - ERROR - Impossible to load Strategy 'Diamond'. This class does not exist or contains Python code errors.

```
### Dyna_opti
- File: `Dyna_opti.py`
- Duration: 5.68s
- Error Log:
```
...O - Starting freqtrade in Backtesting mode
2026-02-18 06:46:20,050 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:20,051 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:20,051 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:20,065 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:20,079 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:21,763 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:21,825 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Dyna_opti.py due to 'No module named 'arrow''
2026-02-18 06:46:21,830 - freqtrade - ERROR - Impossible to load Strategy 'Dyna_opti'. This class does not exist or contains Python code errors.

```
### EI3v2_tag_cofi_green
- File: `EI3v2_tag_cofi_green.py`
- Duration: 5.40s
- Error Log:
```
...freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:25,633 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:25,634 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:25,644 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:25,657 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:27,230 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:27,286 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy EI3v2_tag_cofi_green from '/freqtrade/user_data/strategies/EI3v2_tag_cofi_green.py'...
2026-02-18 06:46:27,287 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:46:27,287 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### EMA50
- File: `EMA50.py`
- Duration: 5.41s
- Error Log:
```
...nge.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:31,074 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:31,074 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:31,085 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:31,098 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:32,718 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:32,738 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/EMA50.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:46:32,763 - freqtrade - ERROR - Impossible to load Strategy 'EMA50'. This class does not exist or contains Python code errors.

```
### EMA520015_V17
- File: `EMA520015_V17.py`
- Duration: 3.69s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:46:36,387 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:46:36,387 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:46:36,388 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:46:36,388 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:46:36,388 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:46:36,389 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:46:36,389 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### EMABreakout
- File: `EMABreakout.py`
- Duration: 5.40s
- Error Log:
```
... - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:40,111 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:40,111 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:40,123 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:40,136 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:41,862 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:41,876 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/EMABreakout.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:46:41,904 - freqtrade - ERROR - Impossible to load Strategy 'EMABreakout'. This class does not exist or contains Python code errors.

```
### ElliotV2
- File: `ElliotV2.py`
- Duration: 5.20s
- Error Log:
```
...26-02-18 06:46:45,419 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:45,419 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:45,420 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:45,430 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:45,442 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:47,060 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:47,108 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV2 from '/freqtrade/user_data/strategies/ElliotV2.py'...
2026-02-18 06:46:47,108 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:46:47,109 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV4
- File: `ElliotV4.py`
- Duration: 5.50s
- Error Log:
```
...26-02-18 06:46:50,849 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:50,849 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:50,850 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:50,860 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:50,872 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:52,434 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:52,476 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV4 from '/freqtrade/user_data/strategies/ElliotV4.py'...
2026-02-18 06:46:52,476 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:46:52,477 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV531
- File: `ElliotV531.py`
- Duration: 5.55s
- Error Log:
```
...2-18 06:46:56,364 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:46:56,365 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:46:56,365 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:56,376 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:46:56,389 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:46:58,017 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:46:58,108 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV531 from '/freqtrade/user_data/strategies/ElliotV531.py'...
2026-02-18 06:46:58,109 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:46:58,110 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV5HO
- File: `ElliotV5HO.py`
- Duration: 5.51s
- Error Log:
```
...2-18 06:47:01,957 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:01,958 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:01,958 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:01,971 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:01,985 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:03,631 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:03,672 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV5HO from '/freqtrade/user_data/strategies/ElliotV5HO.py'...
2026-02-18 06:47:03,673 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:03,673 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV5HOMod2
- File: `ElliotV5HOMod2.py`
- Duration: 3.20s
- Error Log:
```
...47:05,227 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:05,227 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:05,227 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:05,238 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:05,251 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:06,880 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:06,908 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV5HOMod2 from '/freqtrade/user_data/strategies/ElliotV5HOMod2.py'...
2026-02-18 06:47:06,909 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:06,909 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV5HOMod3
- File: `ElliotV5HOMod3.py`
- Duration: 5.30s
- Error Log:
```
...47:10,697 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:10,697 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:10,698 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:10,709 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:10,721 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:12,213 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:12,242 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV5HOMod3 from '/freqtrade/user_data/strategies/ElliotV5HOMod3.py'...
2026-02-18 06:47:12,242 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:12,243 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV7
- File: `ElliotV7.py`
- Duration: 5.44s
- Error Log:
```
...26-02-18 06:47:15,868 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:15,868 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:15,868 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:15,879 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:15,892 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:17,642 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:17,691 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV7 from '/freqtrade/user_data/strategies/ElliotV7.py'...
2026-02-18 06:47:17,692 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:17,692 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV8HO
- File: `ElliotV8HO.py`
- Duration: 5.46s
- Error Log:
```
...2-18 06:47:21,316 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:21,316 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:21,317 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:21,327 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:21,339 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:23,090 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:23,126 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV8HO from '/freqtrade/user_data/strategies/ElliotV8HO.py'...
2026-02-18 06:47:23,126 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:23,127 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV8_original
- File: `ElliotV8_original.py`
- Duration: 5.21s
- Error Log:
```
...810 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:26,811 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:26,811 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:26,822 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:26,835 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:28,373 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:28,423 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV8_original from '/freqtrade/user_data/strategies/ElliotV8_original.py'...
2026-02-18 06:47:28,423 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:28,424 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV8_original_ichiv2
- File: `ElliotV8_original_ichiv2.py`
- Duration: 3.52s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:32,042 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:32,042 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:32,053 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:32,065 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:33,104 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:33,143 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV8_original_ichiv2 from '/freqtrade/user_data/strategies/ElliotV8_original_ichiv2.py'...
2026-02-18 06:47:33,144 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:33,145 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### ElliotV8_original_ichiv3
- File: `ElliotV8_original_ichiv3.py`
- Duration: 5.26s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:35,561 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:35,561 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:35,572 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:35,585 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:37,184 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:37,239 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy ElliotV8_original_ichiv3 from '/freqtrade/user_data/strategies/ElliotV8_original_ichiv3.py'...
2026-02-18 06:47:37,240 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:37,241 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Elliotv8
- File: `Elliotv8.py`
- Duration: 5.44s
- Error Log:
```
...26-02-18 06:47:40,830 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:40,830 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:40,831 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:40,841 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:40,854 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:42,585 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:42,610 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Elliotv8 from '/freqtrade/user_data/strategies/Elliotv8.py'...
2026-02-18 06:47:42,611 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:42,611 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Fakebuy
- File: `Fakebuy.py`
- Duration: 5.46s
- Error Log:
```
...47:46,329 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:46,330 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:46,331 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:46,351 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:46,365 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:48,078 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:48,155 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Fakebuy from '/freqtrade/user_data/strategies/Fakebuy.py'...
2026-02-18 06:47:48,156 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:47:48,157 - freqtrade - ERROR - Please migrate your implementation of `check_buy_timeout` to `check_entry_timeout`.

```
### FastSupertrend
- File: `FastSupertrend.py`
- Duration: 5.53s
- Error Log:
```
...ge - INFO - Instance is running with dry_run enabled
2026-02-18 06:47:57,321 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:47:57,322 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:57,340 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:47:57,357 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:47:59,069 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:47:59,100 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/FastSupertrend.py due to 'cannot import name 'IntParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:47:59,115 - freqtrade - ERROR - Impossible to load Strategy 'FastSupertrend'. This class does not exist or contains Python code errors.

```
### FastSupertrendOpt
- File: `FastSupertrendOpt.py`
- Duration: 3.24s
- Error Log:
```
...NFO - Instance is running with dry_run enabled
2026-02-18 06:48:00,727 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:00,727 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:00,738 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:00,750 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:02,446 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:02,472 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/FastSupertrendOpt.py due to 'cannot import name 'IntParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:48:02,492 - freqtrade - ERROR - Impossible to load Strategy 'FastSupertrendOpt'. This class does not exist or contains Python code errors.

```
### FiveMinCrossAbove
- File: `FiveMinCrossAbove.py`
- Duration: 5.34s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:48:07,829 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:48:07,830 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:48:07,830 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:48:07,831 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:48:07,831 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:48:07,831 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:48:07,832 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### FrostAuraRandomStrategy
- File: `FrostAuraRandomStrategy.py`
- Duration: 5.39s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:48:13,151 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:48:13,151 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:48:13,152 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:48:13,152 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:48:13,153 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:48:13,153 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:48:13,153 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### GodStraNew
- File: `GodStraNew.py`
- Duration: 5.39s
- Error Log:
```
...ge - INFO - Instance is running with dry_run enabled
2026-02-18 06:48:16,874 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:16,875 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:16,892 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:16,914 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:18,595 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:18,633 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/GodStraNew.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:48:18,641 - freqtrade - ERROR - Impossible to load Strategy 'GodStraNew'. This class does not exist or contains Python code errors.

```
### GodStraNew40
- File: `GodStraNew40.py`
- Duration: 5.37s
- Error Log:
```
... INFO - Instance is running with dry_run enabled
2026-02-18 06:48:22,245 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:22,245 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:22,255 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:22,268 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:23,888 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:23,907 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/GodStraNew40.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:48:23,933 - freqtrade - ERROR - Impossible to load Strategy 'GodStraNew40'. This class does not exist or contains Python code errors.

```
### GodStraNew_SMAonly
- File: `GodStraNew_SMAonly.py`
- Duration: 2.97s
- Error Log:
```
...ance is running with dry_run enabled
2026-02-18 06:48:27,560 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:27,561 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:27,572 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:27,584 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:29,100 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:29,130 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/GodStraNew_SMAonly.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:48:29,147 - freqtrade - ERROR - Impossible to load Strategy 'GodStraNew_SMAonly'. This class does not exist or contains Python code errors.

```
### Guacamole
- File: `Guacamole.py`
- Duration: 5.34s
- Error Log:
```
...0,623 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:48:30,623 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:30,624 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:30,634 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:30,646 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:32,271 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:32,298 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Guacamole from '/freqtrade/user_data/strategies/Guacamole.py'...
2026-02-18 06:48:32,299 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:48:32,299 - freqtrade - ERROR - Please migrate your implementation of `check_buy_timeout` to `check_entry_timeout`.

```
### Hacklemore2
- File: `Hacklemore2.py`
- Duration: 5.12s
- Error Log:
```
...9 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:48:35,880 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:35,880 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:35,890 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:35,902 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:37,442 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:37,494 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Hacklemore2 from '/freqtrade/user_data/strategies/Hacklemore2.py'...
2026-02-18 06:48:37,495 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:48:37,495 - freqtrade - ERROR - Please migrate your implementation of `check_buy_timeout` to `check_entry_timeout`.

```
### Hacklemore3
- File: `Hacklemore3.py`
- Duration: 5.25s
- Error Log:
```
...18 06:48:41,103 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:48:41,103 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:41,104 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:41,118 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:41,132 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:42,705 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:42,748 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Hacklemore3 from '/freqtrade/user_data/strategies/Hacklemore3.py'...
2026-02-18 06:48:42,749 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:48:42,749 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### HarmonicDivergence
- File: `HarmonicDivergence.py`
- Duration: 5.36s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:48:48,042 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:48:48,042 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:48:48,042 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:48:48,043 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:48:48,043 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:48:48,044 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:48:48,044 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### HyperStra_GSN_SMAOnly
- File: `HyperStra_GSN_SMAOnly.py`
- Duration: 5.50s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:48:51,879 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:51,880 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:51,892 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:51,905 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:53,617 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:53,642 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy HyperStra_GSN_SMAOnly from '/freqtrade/user_data/strategies/HyperStra_GSN_SMAOnly.py'...
2026-02-18 06:48:53,643 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:48:53,644 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### HyperStra_SMAOnly
- File: `HyperStra_SMAOnly.py`
- Duration: 3.10s
- Error Log:
```
...253 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:48:57,253 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:48:57,254 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:57,264 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:48:57,278 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:48:56,768 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:48:56,801 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy HyperStra_SMAOnly from '/freqtrade/user_data/strategies/HyperStra_SMAOnly.py'...
2026-02-18 06:48:56,801 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:48:56,802 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Ichimoku_SenkouSpanCross
- File: `Ichimoku_SenkouSpanCross.py`
- Duration: 5.35s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:49:02,117 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:49:02,118 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:49:02,119 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:49:02,119 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:49:02,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:49:02,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:49:02,121 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### Ichimoku_v31
- File: `Ichimoku_v31.py`
- Duration: 5.21s
- Error Log:
```
...acktesting mode
2026-02-18 06:49:05,730 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:49:05,730 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:05,731 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:05,743 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:05,755 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:07,374 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:07,379 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Ichimoku_v31.py due to 'unexpected indent (Ichimoku_v31.py, line 24)'
2026-02-18 06:49:07,412 - freqtrade - ERROR - Impossible to load Strategy 'Ichimoku_v31'. This class does not exist or contains Python code errors.

```
### Ichimoku_v37
- File: `Ichimoku_v37.py`
- Duration: 5.40s
- Error Log:
```
...acktesting mode
2026-02-18 06:49:11,122 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:49:11,123 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:11,123 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:11,133 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:11,146 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:12,740 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:12,772 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Ichimoku_v37.py due to 'unexpected indent (Ichimoku_v37.py, line 24)'
2026-02-18 06:49:12,789 - freqtrade - ERROR - Impossible to load Strategy 'Ichimoku_v37'. This class does not exist or contains Python code errors.

```
### Inverse
- File: `Inverse.py`
- Duration: 5.43s
- Error Log:
```
... line 1811, in advise_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/Inverse.py", line 203, in populate_indicators
    informative_p = self.informative_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/Inverse.py", line 142, in informative_indicators
    ssl_down, ssl_up = self.SSLChannels(informative_p, 20)
                       ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/Inverse.py", line 257, in SSLChannels
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, np.where(df['close'] < df['smaLow'], -1, np.NAN))
                                                                                                  ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### InverseV2
- File: `InverseV2.py`
- Duration: 5.36s
- Error Log:
```
...1811, in advise_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/InverseV2.py", line 211, in populate_indicators
    informative_p = self.informative_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/InverseV2.py", line 141, in informative_indicators
    ssl_down, ssl_up = self.SSLChannels(informative_p, 20)
                       ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/InverseV2.py", line 279, in SSLChannels
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, np.where(df['close'] < df['smaLow'], -1, np.NAN))
                                                                                                  ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### KAMACCIRSI
- File: `KAMACCIRSI.py`
- Duration: 3.20s
- Error Log:
```
...2-18 06:49:25,095 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:49:25,095 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:25,096 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:25,107 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:25,119 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:26,802 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:26,822 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy KAMACCIRSI from '/freqtrade/user_data/strategies/KAMACCIRSI.py'...
2026-02-18 06:49:26,823 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:49:26,824 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Kamaflage
- File: `Kamaflage.py`
- Duration: 5.39s
- Error Log:
```
...0,503 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:49:30,504 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:30,504 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:30,514 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:30,528 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:32,178 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:32,217 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Kamaflage from '/freqtrade/user_data/strategies/Kamaflage.py'...
2026-02-18 06:49:32,217 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:49:32,218 - freqtrade - ERROR - Please migrate your implementation of `check_buy_timeout` to `check_entry_timeout`.

```
### LookaheadStrategy
- File: `LookaheadStrategy.py`
- Duration: 5.56s
- Error Log:
```
...freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:49:41,576 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:41,577 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:41,587 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:41,600 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:43,248 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:43,290 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/LookaheadStrategy.py due to 'invalid syntax. Perhaps you forgot a comma? 
(LookaheadStrategy.py, line 56)'
2026-02-18 06:49:43,292 - freqtrade - ERROR - Impossible to load Strategy 'LookaheadStrategy'. This class does not exist or contains Python code errors.

```
### MacheteV8b
- File: `MacheteV8b.py`
- Duration: 5.49s
- Error Log:
```
... INFO - Instance is running with dry_run enabled
2026-02-18 06:49:47,031 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:47,032 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:47,042 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:47,055 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:48,742 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:48,811 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/MacheteV8b.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:49:48,829 - freqtrade - ERROR - Impossible to load Strategy 'MacheteV8b'. This class does not exist or contains Python code errors.

```
### MacheteV8bRallimod2
- File: `MacheteV8bRallimod2.py`
- Duration: 3.55s
- Error Log:
```
...s running with dry_run enabled
2026-02-18 06:49:52,695 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:52,695 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:52,706 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:52,719 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:52,243 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:52,316 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/MacheteV8bRallimod2.py due to 'The `scipy` install you are using seems to be 
broken, (extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:49:52,355 - freqtrade - ERROR - Impossible to load Strategy 'MacheteV8bRallimod2'. This class does not exist or contains Python code errors.

```
### MarketChyperHyperStrategy
- File: `MarketChyperHyperStrategy.py`
- Duration: 5.52s
- Error Log:
```
...ng with dry_run enabled
2026-02-18 06:49:56,067 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:49:56,067 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:56,078 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:49:56,091 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:49:57,718 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:49:57,742 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/MarketChyperHyperStrategy.py due to 'cannot import name 'CategoricalParameter' from
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:49:57,769 - freqtrade - ERROR - Impossible to load Strategy 'MarketChyperHyperStrategy'. This class does not exist or contains Python code errors.

```
### MiniLambo
- File: `MiniLambo.py`
- Duration: 7.08s
- Error Log:
```
... - INFO - Instance is running with dry_run enabled
2026-02-18 06:50:01,932 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:50:01,933 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:01,952 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:01,975 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:50:04,925 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:50:04,965 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/MiniLambo.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:50:04,984 - freqtrade - ERROR - Impossible to load Strategy 'MiniLambo'. This class does not exist or contains Python code errors.

```
### MomStrategy
- File: `MomStrategy.py`
- Duration: 5.33s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:50:10,267 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:50:10,268 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:50:10,268 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:50:10,268 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:50:10,269 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:50:10,269 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:50:10,269 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### MostOfAll
- File: `MostOfAll.py`
- Duration: 5.20s
- Error Log:
```
...exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:50:13,983 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:50:13,984 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:13,995 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:14,008 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:50:15,492 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:50:15,526 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/MostOfAll.py due to 'cannot import name 'DecimalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:50:15,551 - freqtrade - ERROR - Impossible to load Strategy 'MostOfAll'. This class does not exist or contains Python code errors.

```
### MultiMA_TSL
- File: `MultiMA_TSL.py`
- Duration: 3.17s
- Error Log:
```
...xing.py", line 908, in __setitem__
    indexer = self._get_setitem_indexer(key)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 751, in _get_setitem_indexer
    self._ensure_listlike_indexer(key)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 875, in _ensure_listlike_indexer
    new_mgr = self.obj._mgr.reindex_indexer(
        keys, indexer=indexer, axis=0, only_slice=True, use_na_proxy=True
    )
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/internals/managers.py", line 693, in reindex_indexer
    self.axes[axis]._validate_can_reindex(indexer)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexes/base.py", line 4328, in _validate_can_reindex
    raise ValueError("cannot reindex on an axis with duplicate labels")
ValueError: cannot reindex on an axis with duplicate labels

```
### MultiMA_TSL3
- File: `MultiMA_TSL3.py`
- Duration: 5.36s
- Error Log:
```
...~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1811, in advise_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/MultiMA_TSL3.py", line 322, in populate_indicators
    dataframe['pm'], dataframe['pmx'] = pmax(heikinashi, MAtype=1, length=9, multiplier=27, period=10, src=3)
                                        ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/MultiMA_TSL3.py", line 870, in pmax
    pmx = np.where((pm_arr > 0.00), np.where((mavalue < pm_arr), 'down', 'up'), np.NaN)
                                                                                ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 781, in __getattr__
    raise AttributeError(
    ...<3 lines>...
    )
AttributeError: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

```
### MultiMA_TSL3_Mod
- File: `MultiMA_TSL3_Mod.py`
- Duration: 5.34s
- Error Log:
```
...~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1811, in advise_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/MultiMA_TSL3_Mod.py", line 313, in populate_indicators
    dataframe['pm'], dataframe['pmx'] = pmax(heikinashi, MAtype=1, length=9, multiplier=27, period=10, src=3)
                                        ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/MultiMA_TSL3_Mod.py", line 637, in pmax
    pmx = np.where((pm_arr > 0.00), np.where((mavalue < pm_arr), 'down',  'up'), np.NaN)
                                                                                 ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 781, in __getattr__
    raise AttributeError(
    ...<3 lines>...
    )
AttributeError: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

```
### MultiMa
- File: `MultiMa.py`
- Duration: 5.30s
- Error Log:
```
...xchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:50:33,097 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:50:33,098 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:33,110 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:33,122 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:50:34,790 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:50:34,817 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/MultiMa.py due to 'cannot import name 'IntParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:50:34,836 - freqtrade - ERROR - Impossible to load Strategy 'MultiMa'. This class does not exist or contains Python code errors.

```
### MultiOffsetLamboV0
- File: `MultiOffsetLamboV0.py`
- Duration: 5.21s
- Error Log:
```
...5 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:50:38,456 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:50:38,456 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:38,467 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:38,480 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:50:40,051 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:50:40,084 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy MultiOffsetLamboV0 from '/freqtrade/user_data/strategies/MultiOffsetLamboV0.py'...
2026-02-18 06:50:40,085 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:50:40,086 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NASOSRv6_private_Reinuvader_20211121
- File: `NASOSRv6_private_Reinuvader_20211121.py`
- Duration: 5.19s
- Error Log:
```
..., in informative_1h_indicators
    inf_heikinashi = qtpylib.heikinashi(informative)
  File "/freqtrade/freqtrade/vendor/qtpylib/indicators.py", line 107, in heikinashi
    bars.at[0, "ha_open"] = (bars.at[0, "open"] + bars.at[0, "close"]) / 2
                             ~~~~~~~^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2576, in __getitem__
    return super().__getitem__(key)
           ~~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2528, in __getitem__
    return self.obj._get_value(*key, takeable=self._takeable)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4232, in _get_value
    row = self.index.get_loc(index)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexes/range.py", line 415, in get_loc
    raise KeyError(key) from err
KeyError: 0

```
### NASOSv4
- File: `NASOSv4.py`
- Duration: 5.22s
- Error Log:
```
...2026-02-18 06:50:48,902 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:50:48,902 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:50:48,903 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:48,913 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:48,926 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:50:50,476 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:50:50,535 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NASOSv4 from '/freqtrade/user_data/strategies/NASOSv4.py'...
2026-02-18 06:50:50,535 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:50:50,536 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NASOSv5
- File: `NASOSv5.py`
- Duration: 5.67s
- Error Log:
```
...2026-02-18 06:50:54,241 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:50:54,241 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:50:54,242 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:54,257 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:50:54,275 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:50:56,061 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:50:56,105 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NASOSv5 from '/freqtrade/user_data/strategies/NASOSv5.py'...
2026-02-18 06:50:56,106 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:50:56,107 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NASOSv5_mod1
- File: `NASOSv5_mod1.py`
- Duration: 5.86s
- Error Log:
```
... 06:51:00,072 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:51:00,073 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:51:00,073 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:00,084 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:00,097 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:51:01,978 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:51:02,033 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NASOSv5_mod1 from '/freqtrade/user_data/strategies/NASOSv5_mod1.py'...
2026-02-18 06:51:02,034 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:51:02,034 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NASOSv5_mod1_DanMod
- File: `NASOSv5_mod1_DanMod.py`
- Duration: 5.52s
- Error Log:
```
...- freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:51:05,947 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:51:05,947 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:05,958 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:05,970 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:51:07,576 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:51:07,605 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NASOSv5_mod1_DanMod from '/freqtrade/user_data/strategies/NASOSv5_mod1_DanMod.py'...
2026-02-18 06:51:07,605 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:51:07,606 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NASOSv5_mod2
- File: `NASOSv5_mod2.py`
- Duration: 5.52s
- Error Log:
```
... 06:51:11,477 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:51:11,477 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:51:11,478 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:11,489 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:11,502 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:51:13,088 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:51:13,134 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NASOSv5_mod2 from '/freqtrade/user_data/strategies/NASOSv5_mod2.py'...
2026-02-18 06:51:13,135 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:51:13,136 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NASOSv5_mod3
- File: `NASOSv5_mod3.py`
- Duration: 3.63s
- Error Log:
```
... 06:51:15,196 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:51:15,196 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:51:15,197 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:15,208 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:15,224 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:51:16,766 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:51:16,813 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NASOSv5_mod3 from '/freqtrade/user_data/strategies/NASOSv5_mod3.py'...
2026-02-18 06:51:16,813 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:51:16,814 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NFI46
- File: `NFI46.py`
- Duration: 5.70s
- Error Log:
```
....strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: True
2026-02-18 06:51:22,559 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:51:22,560 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:51:22,560 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:51:22,560 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:51:22,561 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:51:22,561 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:51:22,561 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### NFI46Frog
- File: `NFI46Frog.py`
- Duration: 5.77s
- Error Log:
```
... - INFO - Instance is running with dry_run enabled
2026-02-18 06:51:31,929 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:51:31,929 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:31,941 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:31,954 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:51:33,673 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:51:33,752 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/NFI46Frog.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:51:33,766 - freqtrade - ERROR - Impossible to load Strategy 'NFI46Frog'. This class does not exist or contains Python code errors.

```
### NFI46FrogZ
- File: `NFI46FrogZ.py`
- Duration: 5.83s
- Error Log:
```
... INFO - Instance is running with dry_run enabled
2026-02-18 06:51:37,718 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:51:37,718 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:37,737 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:37,751 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:51:39,601 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:51:39,688 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/NFI46FrogZ.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:51:39,699 - freqtrade - ERROR - Impossible to load Strategy 'NFI46FrogZ'. This class does not exist or contains Python code errors.

```
### NFI46Offset
- File: `NFI46Offset.py`
- Duration: 3.28s
- Error Log:
```
....strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: True
2026-02-18 06:51:44,200 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:51:44,201 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:51:44,201 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:51:44,202 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:51:44,203 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:51:44,203 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:51:44,205 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### NFI46OffsetHOA1
- File: `NFI46OffsetHOA1.py`
- Duration: 5.41s
- Error Log:
```
....strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: True
2026-02-18 06:51:48,361 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:51:48,362 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:51:48,362 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:51:48,363 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:51:48,363 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:51:48,363 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:51:48,364 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### NFI46Z
- File: `NFI46Z.py`
- Duration: 5.27s
- Error Log:
```
...e
2026-02-18 06:51:52,070 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:51:52,070 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:51:52,070 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:52,082 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:51:52,095 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:51:53,722 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:51:53,759 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NFI46Z from '/freqtrade/user_data/strategies/NFI46Z.py'...
2026-02-18 06:51:53,760 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:51:53,761 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NFI47V2
- File: `NFI47V2.py`
- Duration: 5.33s
- Error Log:
```
....strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: True
2026-02-18 06:51:59,110 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:51:59,110 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:51:59,111 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:51:59,111 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:51:59,111 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:51:59,112 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:51:59,112 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### NFI4Frog
- File: `NFI4Frog.py`
- Duration: 5.96s
- Error Log:
```
...ge - INFO - Instance is running with dry_run enabled
2026-02-18 06:52:02,735 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:52:02,735 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:52:02,745 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:52:02,757 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:52:04,997 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:52:05,078 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/NFI4Frog.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:52:05,089 - freqtrade - ERROR - Impossible to load Strategy 'NFI4Frog'. This class does not exist or contains Python code errors.

```
### NFI5MOHO
- File: `NFI5MOHO.py`
- Duration: 5.77s
- Error Log:
```
...rs.strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: True
2026-02-18 06:52:10,641 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:52:10,642 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:52:10,642 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:52:10,642 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:52:10,643 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:52:10,643 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:52:10,644 - freqtrade - ERROR - Configuration error: Market exit orders require exit_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### NFI731_BUSD
- File: `NFI731_BUSD.py`
- Duration: 3.91s
- Error Log:
```
....populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NFI731_BUSD.py", line 3493, in populate_indicators
    dataframe = self.normal_tf_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NFI731_BUSD.py", line 3362, in normal_tf_indicators
    dataframe['pm'], dataframe['pmx'] = pmax(heikinashi, MAtype=1, length=9, multiplier=27, period=10, src=3)
                                        ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NFI731_BUSD.py", line 4579, in pmax
    pmx = np.where((pm_arr > 0.00), np.where((mavalue < pm_arr), 'down',  'up'), np.NaN)
                                                                                 ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 781, in __getattr__
    raise AttributeError(
    ...<3 lines>...
    )
AttributeError: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

```
### NFIX_BB_RPB
- File: `NFIX_BB_RPB.py`
- Duration: 5.51s
- Error Log:
```
...esult = _merger(left, right)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 405, in _merger
    op = _OrderedMerge(
        x,
    ...<6 lines>...
        how=how,
    )
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 1912, in __init__
    _MergeOperation.__init__(
    ~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<9 lines>...
        sort=True,  # factorize sorts
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 807, in __init__
    self._maybe_coerce_merge_keys()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 1513, in _maybe_coerce_merge_keys
    raise ValueError(msg)
ValueError: You are trying to merge on datetime64[ns, UTC] and object columns for key 'date'. If you wish to proceed you should use pd.concat

```
### NFIX_BB_RPB_c7c477d_20211030
- File: `NFIX_BB_RPB_c7c477d_20211030.py`
- Duration: 5.49s
- Error Log:
```
...trade/user_data/strategies/NFIX_BB_RPB_c7c477d_20211030.py", line 3724, in informative_1h_indicators
    informative_1h['res_level'] = Series(np.where(res_series, np.where(informative_1h['close'] > informative_1h['open'], informative_1h['close'], informative_1h['open']), float('NaN'))).ffill()
                                                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/ops/common.py", line 76, in new_method
    return method(self, other)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/arraylike.py", line 56, in __gt__
    return self._cmp_method(other, operator.gt)
           ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/series.py", line 6133, in _cmp_method
    raise ValueError("Can only compare identically-labeled Series objects")
ValueError: Can only compare identically-labeled Series objects

```
### NfiNextModded
- File: `NfiNextModded.py`
- Duration: 5.84s
- Error Log:
```
...ators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NfiNextModded.py", line 4856, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NfiNextModded.py", line 4479, in informative_1h_indicators
    ssl_down, ssl_up = SSLChannels(informative_1h, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NfiNextModded.py", line 5258, in SSLChannels
    hlv = Series(np.where(dataframe['close'] > smaHigh, 1, np.where(dataframe['close'] < smaLow, -1, np.NAN)))
                                                                                                     ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### NormalizerStrategy
- File: `NormalizerStrategy.py`
- Duration: 5.56s
- Error Log:
```
...2 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:52:35,522 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:52:35,523 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:52:35,535 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:52:35,547 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:52:37,232 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:52:37,260 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NormalizerStrategy from '/freqtrade/user_data/strategies/NormalizerStrategy.py'...
2026-02-18 06:52:37,261 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:52:37,261 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NormalizerStrategyHO2
- File: `NormalizerStrategyHO2.py`
- Duration: 3.32s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:52:40,101 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:52:40,101 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:52:38,835 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:52:38,848 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:52:40,564 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:52:40,611 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NormalizerStrategyHO2 from '/freqtrade/user_data/strategies/NormalizerStrategyHO2.py'...
2026-02-18 06:52:40,612 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:52:40,612 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NostalgiaForInfinityNext
- File: `NostalgiaForInfinityNext.py`
- Duration: 6.18s
- Error Log:
```
...a)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext.py", line 3493, in populate_indicators
    dataframe = self.normal_tf_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext.py", line 3362, in normal_tf_indicators
    dataframe['pm'], dataframe['pmx'] = pmax(heikinashi, MAtype=1, length=9, multiplier=27, period=10, src=3)
                                        ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext.py", line 4579, in pmax
    pmx = np.where((pm_arr > 0.00), np.where((mavalue < pm_arr), 'down',  'up'), np.NaN)
                                                                                 ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 781, in __getattr__
    raise AttributeError(
    ...<3 lines>...
    )
AttributeError: `np.NaN` was removed in the NumPy 2.0 release. Use `np.nan` instead.

```
### NostalgiaForInfinityNextV7155
- File: `NostalgiaForInfinityNextV7155.py`
- Duration: 5.56s
- Error Log:
```
...ataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNextV7155.py", line 4658, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNextV7155.py", line 4321, in informative_1h_indicators
    ssl_down, ssl_up = SSLChannels(informative_1h, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNextV7155.py", line 5738, in SSLChannels
    hlv = Series(np.where(dataframe['close'] > smaHigh, 1, np.where(dataframe['close'] < smaLow, -1, np.NAN)))
                                                                                                     ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### NostalgiaForInfinityNext_ChangeToTower_V5_2
- File: `NostalgiaForInfinityNext_ChangeToTower_V5_2.py`
- Duration: 5.76s
- Error Log:
```
...r_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_2.py", line 2944, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_2.py", line 2631, in informative_1h_indicators
    ssl_down, ssl_up = SSLChannels(informative_1h, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_2.py", line 3762, in SSLChannels
    hlv = Series(np.where(dataframe['close'] > smaHigh, 1, np.where(dataframe['close'] < smaLow, -1, np.NAN)))
                                                                                                     ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### NostalgiaForInfinityNext_ChangeToTower_V5_3
- File: `NostalgiaForInfinityNext_ChangeToTower_V5_3.py`
- Duration: 5.78s
- Error Log:
```
...r_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_3.py", line 2946, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_3.py", line 2633, in informative_1h_indicators
    ssl_down, ssl_up = SSLChannels(informative_1h, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V5_3.py", line 3764, in SSLChannels
    hlv = Series(np.where(dataframe['close'] > smaHigh, 1, np.where(dataframe['close'] < smaLow, -1, np.NAN)))
                                                                                                     ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### NostalgiaForInfinityNext_ChangeToTower_V6
- File: `NostalgiaForInfinityNext_ChangeToTower_V6.py`
- Duration: 3.92s
- Error Log:
```
...de/user_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V6.py", line 2981, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V6.py", line 2631, in informative_1h_indicators
    ssl_down, ssl_up = SSLChannels(informative_1h, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_ChangeToTower_V6.py", line 3801, in SSLChannels
    hlv = Series(np.where(dataframe['close'] > smaHigh, 1, np.where(dataframe['close'] < smaLow, -1, np.NAN)))
                                                                                                     ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### NostalgiaForInfinityNext_maximizer
- File: `NostalgiaForInfinityNext_maximizer.py`
- Duration: 6.01s
- Error Log:
```
...ata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_maximizer.py", line 3034, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_maximizer.py", line 2706, in informative_1h_indicators
    ssl_down, ssl_up = SSLChannels(informative_1h, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityNext_maximizer.py", line 3934, in SSLChannels
    hlv = Series(np.where(dataframe['close'] > smaHigh, 1, np.where(dataframe['close'] < smaLow, -1, np.NAN)))
                                                                                                     ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### NostalgiaForInfinityV1
- File: `NostalgiaForInfinityV1.py`
- Duration: 5.37s
- Error Log:
```
...trade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:53:22,688 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:53:22,689 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:22,699 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:22,713 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:53:24,395 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:53:24,428 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NostalgiaForInfinityV1 from '/freqtrade/user_data/strategies/NostalgiaForInfinityV1.py'...
2026-02-18 06:53:24,429 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:53:24,430 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NostalgiaForInfinityV2
- File: `NostalgiaForInfinityV2.py`
- Duration: 5.40s
- Error Log:
```
...trade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:53:28,065 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:53:28,065 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:28,076 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:28,088 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:53:29,740 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:53:29,764 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NostalgiaForInfinityV2 from '/freqtrade/user_data/strategies/NostalgiaForInfinityV2.py'...
2026-02-18 06:53:29,764 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:53:29,765 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NostalgiaForInfinityV3
- File: `NostalgiaForInfinityV3.py`
- Duration: 5.40s
- Error Log:
```
...trade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:53:33,437 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:53:33,437 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:33,447 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:33,459 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:53:35,101 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:53:35,152 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NostalgiaForInfinityV3 from '/freqtrade/user_data/strategies/NostalgiaForInfinityV3.py'...
2026-02-18 06:53:35,152 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:53:35,153 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NostalgiaForInfinityV7_7_2
- File: `NostalgiaForInfinityV7_7_2.py`
- Duration: 3.25s
- Error Log:
```
...icators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityV7_7_2.py", line 2992, in populate_indicators
    informative_1h = self.informative_1h_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityV7_7_2.py", line 2699, in informative_1h_indicators
    ssl_down, ssl_up = SSLChannels(informative_1h, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/NostalgiaForInfinityV7_7_2.py", line 3881, in SSLChannels
    hlv = Series(np.where(dataframe['close'] > smaHigh, 1, np.where(dataframe['close'] < smaLow, -1, np.NAN)))
                                                                                                     ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### NostalgiaForInfinityX
- File: `NostalgiaForInfinityX.py`
- Duration: 5.40s
- Error Log:
```
...esult = _merger(left, right)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 405, in _merger
    op = _OrderedMerge(
        x,
    ...<6 lines>...
        how=how,
    )
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 1912, in __init__
    _MergeOperation.__init__(
    ~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<9 lines>...
        sort=True,  # factorize sorts
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 807, in __init__
    self._maybe_coerce_merge_keys()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/reshape/merge.py", line 1513, in _maybe_coerce_merge_keys
    raise ValueError(msg)
ValueError: You are trying to merge on datetime64[ns, UTC] and object columns for key 'date'. If you wish to proceed you should use pd.concat

```
### NostalgiaForInfinityXw
- File: `NostalgiaForInfinityXw.py`
- Duration: 5.99s
- Error Log:
```
...n informative_1h_indicators
    inf_heikinashi = qtpylib.heikinashi(informative_1h)
  File "/freqtrade/freqtrade/vendor/qtpylib/indicators.py", line 107, in heikinashi
    bars.at[0, "ha_open"] = (bars.at[0, "open"] + bars.at[0, "close"]) / 2
                             ~~~~~~~^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2576, in __getitem__
    return super().__getitem__(key)
           ~~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2528, in __getitem__
    return self.obj._get_value(*key, takeable=self._takeable)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4232, in _get_value
    row = self.index.get_loc(index)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexes/range.py", line 415, in get_loc
    raise KeyError(key) from err
KeyError: 0

```
### NotAnotherSMAOffSetStrategy_V2
- File: `NotAnotherSMAOffSetStrategy_V2.py`
- Duration: 5.68s
- Error Log:
```
...xchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:53:53,716 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:53:53,717 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:53,727 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:53,742 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:53:55,562 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:53:55,601 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffSetStrategy_V2 from '/freqtrade/user_data/strategies/NotAnotherSMAOffSetStrategy_V2.py'...
2026-02-18 06:53:55,602 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:53:55,603 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategy
- File: `NotAnotherSMAOffsetStrategy.py`
- Duration: 5.37s
- Error Log:
```
...ange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:53:59,258 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:53:59,258 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:59,269 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:53:59,282 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:01,016 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:01,042 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategy from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategy.py'...
2026-02-18 06:54:01,043 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:01,044 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategyHO
- File: `NotAnotherSMAOffsetStrategyHO.py`
- Duration: 3.39s
- Error Log:
```
....exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:54:03,800 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:03,800 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:03,812 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:02,570 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:04,348 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:04,367 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategyHO from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategyHO.py'...
2026-02-18 06:54:04,367 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:04,368 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategyHOv3
- File: `NotAnotherSMAOffsetStrategyHOv3.py`
- Duration: 5.49s
- Error Log:
```
...hange - INFO - Instance is running with dry_run enabled
2026-02-18 06:54:08,096 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:08,097 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:08,109 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:08,124 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:09,830 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:09,876 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategyHOv3 from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategyHOv3.py'...
2026-02-18 06:54:09,877 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:09,878 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategyLite
- File: `NotAnotherSMAOffsetStrategyLite.py`
- Duration: 5.65s
- Error Log:
```
...hange - INFO - Instance is running with dry_run enabled
2026-02-18 06:54:13,742 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:13,743 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:13,753 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:13,766 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:15,572 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:15,615 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategyLite from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategyLite.py'...
2026-02-18 06:54:15,616 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:15,617 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategyModHO
- File: `NotAnotherSMAOffsetStrategyModHO.py`
- Duration: 5.47s
- Error Log:
```
...nge - INFO - Instance is running with dry_run enabled
2026-02-18 06:54:19,311 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:19,311 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:19,322 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:19,336 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:21,023 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:21,058 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategyModHO from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategyModHO.py'...
2026-02-18 06:54:21,059 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:21,060 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901
- File: `NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901.py`
- Duration: 5.41s
- Error Log:
```
... dry_run enabled
2026-02-18 06:54:24,748 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:24,748 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:24,759 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:24,772 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:26,411 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:26,459 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901 from 
'/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901.py'...
2026-02-18 06:54:26,460 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:26,461 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategyX1
- File: `NotAnotherSMAOffsetStrategyX1.py`
- Duration: 3.40s
- Error Log:
```
....exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:54:30,296 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:30,297 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:30,308 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:30,321 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:31,856 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:31,928 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategyX1 from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategyX1.py'...
2026-02-18 06:54:31,929 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:31,929 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategy_uzi
- File: `NotAnotherSMAOffsetStrategy_uzi.py`
- Duration: 5.65s
- Error Log:
```
...hange - INFO - Instance is running with dry_run enabled
2026-02-18 06:54:33,774 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:33,775 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:33,785 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:33,799 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:35,497 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:35,536 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategy_uzi from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategy_uzi.py'...
2026-02-18 06:54:35,537 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:35,538 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### SuperTrendPure
- File: `SuperTrendPure.py`
- Duration: 5.30s
- Error Log:
```
...ge - INFO - Instance is running with dry_run enabled
2026-02-18 06:58:00,050 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:58:00,050 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:00,061 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:00,076 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:58:01,803 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:58:01,810 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/SuperTrendPure.py due to 'cannot import name 'IntParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:58:01,846 - freqtrade - ERROR - Impossible to load Strategy 'SuperTrendPure'. This class does not exist or contains Python code errors.

```
### Schism4
- File: `Schism4.py`
- Duration: 3.21s
- Error Log:
```
... INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:57:19,511 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:19,512 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:19,512 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:19,523 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:19,535 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:19,070 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:19,114 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Schism4.py due to 'No module named 'arrow''
2026-02-18 06:57:19,133 - freqtrade - ERROR - Impossible to load Strategy 'Schism4'. This class does not exist or contains Python code errors.

```
### ichiV1_Marius
- File: `ichiV1_Marius.py`
- Duration: 12.44s
- Error Log:
```
...- Instance is running with dry_run enabled
2026-02-18 06:59:09,151 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:59:09,152 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:59:09,165 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:59:09,184 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:59:16,453 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:59:16,559 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/ichiV1_Marius.py due to 'The `scipy` install you are using seems to be broken, 
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:59:16,564 - freqtrade - ERROR - Impossible to load Strategy 'ichiV1_Marius'. This class does not exist or contains Python code errors.

```
### SMAOffsetProtectOptV1Mod2
- File: `SMAOffsetProtectOptV1Mod2.py`
- Duration: 5.09s
- Error Log:
```
...exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:33,844 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:33,845 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:33,856 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:33,869 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:35,399 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:35,423 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMAOffsetProtectOptV1Mod2 from '/freqtrade/user_data/strategies/SMAOffsetProtectOptV1Mod2.py'...
2026-02-18 06:56:35,424 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:35,424 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### mark_strat_opt
- File: `mark_strat_opt.py`
- Duration: 5.25s
- Error Log:
```
...:20,321 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2026-02-18 06:59:20,323 - freqtrade.commands.optimize_commands - INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:59:20,324 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:59:20,324 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:59:20,325 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:59:20,335 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:59:20,347 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:59:21,808 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:59:21,847 - freqtrade - ERROR - Impossible to load Strategy 'mark_strat_opt'. This class does not exist or contains Python code errors.

```
### SampleStrategyV2
- File: `SampleStrategyV2.py`
- Duration: 3.37s
- Error Log:
```
...8 06:56:51,540 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): buy_trend_length = 288
2026-02-18 06:56:51,540 - freqtrade.strategy.hyper - INFO - No params for sell found, using default values.
2026-02-18 06:56:51,540 - freqtrade.strategy.hyper - INFO - Strategy Parameter(default): sell_rsi = 70
2026-02-18 06:56:51,541 - freqtrade.data.dataprovider - INFO - Loading data for ETH/USDT:USDT 1h from 2025-12-09 08:00:00 to 2026-01-22 00:00:00
2026-02-18 06:56:51,543 - freqtrade.data.history.datahandlers.idatahandler - WARNING - No history for ETH/USDT:USDT, futures, 1h found. Use `freqtrade download-data` to download the data
2026-02-18 06:56:51,544 - freqtrade.data.dataprovider - WARNING - No data found for (ETH/USDT:USDT, 1h, ).
2026-02-18 06:56:51,608 - freqtrade.data.converter.converter - WARNING - ETH/USDT:USDT has no data left after adjusting for startup candles, skipping.
2026-02-18 06:56:51,609 - freqtrade - ERROR - No data left after adjusting for startup candles.

```
### SMAOffsetProtectOptV1_kkeue_20210619
- File: `SMAOffsetProtectOptV1_kkeue_20210619.py`
- Duration: 5.33s
- Error Log:
```
...O - Instance is running with dry_run enabled
2026-02-18 06:56:39,012 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:39,012 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:39,023 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:39,034 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:40,802 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:40,861 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMAOffsetProtectOptV1_kkeue_20210619 from 
'/freqtrade/user_data/strategies/SMAOffsetProtectOptV1_kkeue_20210619.py'...
2026-02-18 06:56:40,862 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:40,863 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### strato
- File: `strato.py`
- Duration: 5.83s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:59:33,891 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:59:33,892 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:59:33,892 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:59:33,892 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:59:33,893 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:59:33,893 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:59:33,894 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### Schism2
- File: `Schism2.py`
- Duration: 5.20s
- Error Log:
```
... INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:57:03,466 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:03,466 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:03,466 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:03,476 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:03,489 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:05,093 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:05,145 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Schism2.py due to 'No module named 'arrow''
2026-02-18 06:57:05,154 - freqtrade - ERROR - Impossible to load Strategy 'Schism2'. This class does not exist or contains Python code errors.

```
### Obelisk_Ichimoku_Slow_v1_3
- File: `Obelisk_Ichimoku_Slow_v1_3.py`
- Duration: 5.98s
- Error Log:
```
...icators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/Obelisk_Ichimoku_Slow_v1_3.py", line 220, in populate_indicators
    informative = self.slow_tf_indicators(informative.copy(), metadata)
  File "/freqtrade/user_data/strategies/Obelisk_Ichimoku_Slow_v1_3.py", line 168, in slow_tf_indicators
    ssl_down, ssl_up = ssl_atr(dataframe, 10)
                       ~~~~~~~^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/Obelisk_Ichimoku_Slow_v1_3.py", line 64, in ssl_atr
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, np.where(df['close'] < df['smaLow'], -1, np.NAN))
                                                                                                  ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### true_lambo
- File: `true_lambo.py`
- Duration: 4.78s
- Error Log:
```
...ne 513, in populate_indicators
    inf_heikinashi = qtpylib.heikinashi(informative)
  File "/freqtrade/freqtrade/vendor/qtpylib/indicators.py", line 107, in heikinashi
    bars.at[0, "ha_open"] = (bars.at[0, "open"] + bars.at[0, "close"]) / 2
                             ~~~~~~~^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2576, in __getitem__
    return super().__getitem__(key)
           ~~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2528, in __getitem__
    return self.obj._get_value(*key, takeable=self._takeable)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4232, in _get_value
    row = self.index.get_loc(index)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexes/range.py", line 415, in get_loc
    raise KeyError(key) from err
KeyError: 0

```
### Schism2MM
- File: `Schism2MM.py`
- Duration: 5.53s
- Error Log:
```
...O - Starting freqtrade in Backtesting mode
2026-02-18 06:57:08,808 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:08,809 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:08,809 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:08,820 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:08,832 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:10,585 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:10,605 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Schism2MM.py due to 'No module named 'arrow''
2026-02-18 06:57:10,647 - freqtrade - ERROR - Impossible to load Strategy 'Schism2MM'. This class does not exist or contains Python code errors.

```
### TenderEnter
- File: `TenderEnter.py`
- Duration: 5.52s
- Error Log:
```
....strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: True
2026-02-18 06:58:07,292 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:58:07,293 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:58:07,293 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:58:07,293 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:58:07,294 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:58:07,294 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:58:07,294 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### Supertrend
- File: `SuperTrend.py`
- Duration: 5.39s
- Error Log:
```
...e.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:54,673 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:54,674 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:54,684 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:54,696 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:56,450 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:56,460 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/SuperTrend.py due to 'cannot import name 'IntParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:57:56,496 - freqtrade - ERROR - Impossible to load Strategy 'Supertrend'. This class does not exist or contains Python code errors.

```
### bbema
- File: `bbema.py`
- Duration: 3.25s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:58:16,155 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:58:16,156 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:58:16,156 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:58:16,156 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:58:16,157 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:58:16,157 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:58:16,157 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### custom_sell
- File: `custom_sell.py`
- Duration: 5.23s
- Error Log:
```
...Starting freqtrade in Backtesting mode
2026-02-18 06:58:49,321 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:58:49,321 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:58:49,322 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:49,333 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:49,346 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:58:50,847 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:58:50,904 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/custom_sell.py due to 'No module named 'arrow''
2026-02-18 06:58:50,906 - freqtrade - ERROR - Impossible to load Strategy 'custom_sell'. This class does not exist or contains Python code errors.

```
### SMAOffset
- File: `SMAOffset.py`
- Duration: 5.56s
- Error Log:
```
... 06:56:08,773 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:08,774 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:08,774 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:08,784 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:08,798 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:10,676 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:10,717 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/SMAOffset.py due to 'unindent does not match any outer indentation level 
(SMAOffset.py, line 27)'
2026-02-18 06:56:10,722 - freqtrade - ERROR - Impossible to load Strategy 'SMAOffset'. This class does not exist or contains Python code errors.

```
### SMAOffsetProtectOptV1
- File: `SMAOffsetProtectOptV1.py`
- Duration: 5.57s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:19,985 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:19,986 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:19,997 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:20,010 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:21,745 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:21,766 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMAOffsetProtectOptV1 from '/freqtrade/user_data/strategies/SMAOffsetProtectOptV1.py'...
2026-02-18 06:56:21,766 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:21,767 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### StochRSITEMA
- File: `StochRSITEMA.py`
- Duration: 3.78s
- Error Log:
```
... 06:57:45,424 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:45,425 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:45,425 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:45,436 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:45,450 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:47,455 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:47,488 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy StochRSITEMA from '/freqtrade/user_data/strategies/StochRSITEMA.py'...
2026-02-18 06:57:47,488 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:57:47,489 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### SMA_BBRSI
- File: `SMA_BBRSI.py`
- Duration: 5.17s
- Error Log:
```
...-02-18 06:56:44,360 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:44,361 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:44,362 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:44,372 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:44,384 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:45,911 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:45,978 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMA_BBRSI from '/freqtrade/user_data/strategies/SMA_BBRSI.py'...
2026-02-18 06:56:45,978 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:45,979 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### cryptohassle
- File: `cryptohassle.py`
- Duration: 5.07s
- Error Log:
```
...strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: False
2026-02-18 06:58:37,176 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:58:37,177 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:58:37,177 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:58:37,178 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:58:37,178 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:58:37,179 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:58:37,179 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### Obelisk_TradePro_Ichi_v2_1
- File: `Obelisk_TradePro_Ichi_v2_1.py`
- Duration: 5.20s
- Error Log:
```
...pair}).copy()
                ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1811, in advise_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/Obelisk_TradePro_Ichi_v2_1.py", line 172, in populate_indicators
    ssl_down, ssl_up = SSLChannels(dataframe, 10)
                       ~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/Obelisk_TradePro_Ichi_v2_1.py", line 58, in SSLChannels
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, np.where(df['close'] < df['smaLow'], -1, np.NAN))
                                                                                                  ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### Renko
- File: `Renko.py`
- Duration: 5.29s
- Error Log:
```
...ode
2026-02-18 06:55:58,104 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:55:58,104 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:55:58,105 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:58,116 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:58,129 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:55:59,848 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:55:59,872 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy Renko from '/freqtrade/user_data/strategies/Renko.py'...
2026-02-18 06:55:59,873 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:55:59,873 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### SMAOPv1_TTF
- File: `SMAOPv1_TTF.py`
- Duration: 5.34s
- Error Log:
```
...18 06:56:03,280 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:03,281 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:03,281 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:03,291 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:03,303 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:05,177 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:05,206 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMAOPv1_TTF from '/freqtrade/user_data/strategies/SMAOPv1_TTF.py'...
2026-02-18 06:56:05,206 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:05,207 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Schism5
- File: `Schism5.py`
- Duration: 5.55s
- Error Log:
```
... INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:57:23,033 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:23,033 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:23,033 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:23,045 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:23,058 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:24,630 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:24,690 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Schism5.py due to 'No module named 'arrow''
2026-02-18 06:57:24,692 - freqtrade - ERROR - Impossible to load Strategy 'Schism5'. This class does not exist or contains Python code errors.

```
### SlowPotato
- File: `SlowPotato.py`
- Duration: 5.46s
- Error Log:
```
....strategy_resolver - INFO - Strategy using ignore_roi_if_entry_signal: True
2026-02-18 06:57:35,895 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using exit_profit_offset: 0.0
2026-02-18 06:57:35,895 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2026-02-18 06:57:35,896 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2026-02-18 06:57:35,896 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using position_adjustment_enable: False
2026-02-18 06:57:35,896 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_entry_position_adjustment: -1
2026-02-18 06:57:35,897 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using max_open_trades: 3
2026-02-18 06:57:35,897 - freqtrade - ERROR - Configuration error: Market entry orders require entry_pricing.price_side = "other".
Please make sure to review the documentation at https://www.freqtrade.io/en/stable.

```
### custom
- File: `custom.py`
- Duration: 3.13s
- Error Log:
```
...e
2026-02-18 06:58:43,961 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:58:43,962 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:58:43,962 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:43,973 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:43,985 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:58:45,641 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:58:45,681 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy custom from '/freqtrade/user_data/strategies/custom.py'...
2026-02-18 06:58:45,682 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:58:45,683 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### fahmibah
- File: `fahmibah.py`
- Duration: 6.87s
- Error Log:
```
...ne 200, in populate_indicators
    inf_heikinashi = qtpylib.heikinashi(informative)
  File "/freqtrade/freqtrade/vendor/qtpylib/indicators.py", line 107, in heikinashi
    bars.at[0, "ha_open"] = (bars.at[0, "open"] + bars.at[0, "close"]) / 2
                             ~~~~~~~^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2576, in __getitem__
    return super().__getitem__(key)
           ~~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 2528, in __getitem__
    return self.obj._get_value(*key, takeable=self._takeable)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4232, in _get_value
    row = self.index.get_loc(index)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexes/range.py", line 415, in get_loc
    raise KeyError(key) from err
KeyError: 0

```
### NowoIchimoku1hV1
- File: `NowoIchimoku1hV1.py`
- Duration: 6.07s
- Error Log:
```
...e_entry(dataframe, metadata)
  File "/freqtrade/freqtrade/strategy/interface.py", line 1832, in advise_entry
    df = self.populate_entry_trend(dataframe, metadata)
  File "/freqtrade/user_data/strategies/NowoIchimoku1hV1.py", line 200, in populate_entry_trend
    if df.loc[i - 1, 'buy']:
       ~~~~~~^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 1184, in __getitem__
    return self.obj._get_value(*key, takeable=self._takeable)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4225, in _get_value
    series = self._get_item_cache(col)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/frame.py", line 4649, in _get_item_cache
    loc = self.columns.get_loc(item)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexes/base.py", line 3819, in get_loc
    raise KeyError(key) from err
KeyError: 'buy'

```
### Obelisk_3EMA_StochRSI_ATR
- File: `Obelisk_3EMA_StochRSI_ATR.py`
- Duration: 5.84s
- Error Log:
```
...cators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/Obelisk_3EMA_StochRSI_ATR.py", line 133, in populate_indicators
    informative = self.do_indicators(informative.copy(), metadata)
  File "/freqtrade/user_data/strategies/Obelisk_3EMA_StochRSI_ATR.py", line 92, in do_indicators
    dataframe.loc[
    ~~~~~~~~~~~~~^
        (dataframe['ema8'] > dataframe['ema14']) &
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
    ,
    ^
    'go_long'] = 1
    ^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 912, in __setitem__
    iloc._setitem_with_indexer(indexer, value, self.name)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/indexing.py", line 1848, in _setitem_with_indexer
    raise ValueError(
    ...<2 lines>...
    )
ValueError: cannot set a frame with no defined index and a scalar

```
### Schism6
- File: `Schism6.py`
- Duration: 5.64s
- Error Log:
```
... INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:57:28,677 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:28,678 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:28,678 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:28,690 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:28,704 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:30,337 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:30,355 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Schism6.py due to 'No module named 'arrow''
2026-02-18 06:57:30,394 - freqtrade - ERROR - Impossible to load Strategy 'Schism6'. This class does not exist or contains Python code errors.

```
### SuperHV27
- File: `SuperHV27.py`
- Duration: 5.57s
- Error Log:
```
...O - Starting freqtrade in Backtesting mode
2026-02-18 06:57:49,295 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:49,296 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:49,297 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:49,308 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:49,322 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:51,018 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:51,064 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/SuperHV27.py due to 'No module named 'arrow''
2026-02-18 06:57:51,089 - freqtrade - ERROR - Impossible to load Strategy 'SuperHV27'. This class does not exist or contains Python code errors.

```
### bbrsi1_strategy
- File: `bbrsi1_strategy.py`
- Duration: 5.43s
- Error Log:
```
...19,753 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2026-02-18 06:58:19,755 - freqtrade.commands.optimize_commands - INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:58:19,756 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:58:19,756 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:58:19,757 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:19,767 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:19,779 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:58:21,514 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:58:21,565 - freqtrade - ERROR - Impossible to load Strategy 'bbrsi1_strategy'. This class does not exist or contains Python code errors.

```
### Schism3
- File: `Schism3.py`
- Duration: 5.27s
- Error Log:
```
... INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:57:14,251 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:14,251 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:14,252 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:14,263 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:14,274 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:15,976 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:16,014 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Schism3.py due to 'No module named 'arrow''
2026-02-18 06:57:16,037 - freqtrade - ERROR - Impossible to load Strategy 'Schism3'. This class does not exist or contains Python code errors.

```
### SMAOffsetProtectOptV0
- File: `SMAOffsetProtectOptV0.py`
- Duration: 5.41s
- Error Log:
```
...eqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:14,305 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:14,306 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:14,316 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:14,329 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:16,103 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:16,161 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMAOffsetProtectOptV0 from '/freqtrade/user_data/strategies/SMAOffsetProtectOptV0.py'...
2026-02-18 06:56:16,162 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:16,162 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NotAnotherSMAOffsetStrategy_uzi3
- File: `NotAnotherSMAOffsetStrategy_uzi3.py`
- Duration: 5.53s
- Error Log:
```
...nge - INFO - Instance is running with dry_run enabled
2026-02-18 06:54:39,358 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:54:39,359 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:39,370 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:54:39,384 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:54:41,014 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:54:41,036 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy NotAnotherSMAOffsetStrategy_uzi3 from '/freqtrade/user_data/strategies/NotAnotherSMAOffsetStrategy_uzi3.py'...
2026-02-18 06:54:41,037 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:54:41,038 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### NowoIchimoku5mV2
- File: `NowoIchimoku5mV2.py`
- Duration: 3.60s
- Error Log:
```
...~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/ops/common.py", line 76, in new_method
    return method(self, other)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/arraylike.py", line 194, in __sub__
    return self._arith_method(other, operator.sub)
           ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/series.py", line 6154, in _arith_method
    return base.IndexOpsMixin._arith_method(self, other, op)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/base.py", line 1391, in _arith_method
    result = ops.arithmetic_op(lvalues, rvalues, op)
  File "/home/ftuser/.local/lib/python3.13/site-packages/pandas/core/ops/array_ops.py", line 273, in arithmetic_op
    res_values = op(left, right)
TypeError: unsupported operand type(s) for -: 'numpy.ndarray' and 'Timedelta'

```
### TrixV23Strategy
- File: `TrixV23Strategy.py`
- Duration: 5.53s
- Error Log:
```
...date = self.backtest_one_strategy(strat, data, timerange)
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/optimize/backtesting.py", line 1754, in backtest_one_strategy
    preprocessed = self.strategy.advise_all_indicators(data)
  File "/freqtrade/freqtrade/strategy/interface.py", line 1749, in advise_all_indicators
    res[pair] = self.advise_indicators(pair_data.copy(), {"pair": pair}).copy()
                ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1806, in advise_indicators
    dataframe = _create_and_merge_informative_pair(
        self, dataframe, metadata, inf_data, populate_fn
    )
  File "/freqtrade/freqtrade/strategy/informative_decorator.py", line 140, in _create_and_merge_informative_pair
    raise ValueError(
    ...<2 lines>...
    )
ValueError: Informative dataframe for (BTC/USDT, 1h, futures) is empty. Can't populate informative indicators.

```
### RalliV1
- File: `RalliV1.py`
- Duration: 5.20s
- Error Log:
```
...2026-02-18 06:55:44,269 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:55:44,270 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:55:44,270 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:44,282 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:44,294 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:55:45,790 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:55:45,827 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy RalliV1 from '/freqtrade/user_data/strategies/RalliV1.py'...
2026-02-18 06:55:45,827 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:55:45,828 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### SMAOffsetProtectOptV1Mod
- File: `SMAOffsetProtectOptV1Mod.py`
- Duration: 5.30s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:28,608 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:28,609 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:28,620 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:28,632 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:30,377 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:30,423 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMAOffsetProtectOptV1Mod from '/freqtrade/user_data/strategies/SMAOffsetProtectOptV1Mod.py'...
2026-02-18 06:56:30,424 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:30,425 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Stinkfist
- File: `Stinkfist.py`
- Duration: 5.76s
- Error Log:
```
...O - Starting freqtrade in Backtesting mode
2026-02-18 06:57:39,797 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:57:39,798 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:57:39,798 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:39,813 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:57:39,836 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:57:41,556 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:57:41,593 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Stinkfist.py due to 'No module named 'arrow''
2026-02-18 06:57:41,629 - freqtrade - ERROR - Impossible to load Strategy 'Stinkfist'. This class does not exist or contains Python code errors.

```
### RalliV1_disable56
- File: `RalliV1_disable56.py`
- Duration: 5.48s
- Error Log:
```
...615 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:55:49,616 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:55:49,616 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:49,627 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:49,640 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:55:51,483 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:55:51,520 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy RalliV1_disable56 from '/freqtrade/user_data/strategies/RalliV1_disable56.py'...
2026-02-18 06:55:51,520 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:55:51,521 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### Schism
- File: `Schism.py`
- Duration: 5.19s
- Error Log:
```
... - INFO - Starting freqtrade in Backtesting mode
2026-02-18 06:56:58,219 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:58,219 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:58,219 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:58,229 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:58,241 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:59,900 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:59,919 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Schism.py due to 'No module named 'arrow''
2026-02-18 06:56:59,966 - freqtrade - ERROR - Impossible to load Strategy 'Schism'. This class does not exist or contains Python code errors.

```
### RSIv2
- File: `RSIv2.py`
- Duration: 5.16s
- Error Log:
```
... self.backtest_one_strategy(strat, data, timerange)
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/optimize/backtesting.py", line 1754, in backtest_one_strategy
    preprocessed = self.strategy.advise_all_indicators(data)
  File "/freqtrade/freqtrade/strategy/interface.py", line 1749, in advise_all_indicators
    res[pair] = self.advise_indicators(pair_data.copy(), {"pair": pair}).copy()
                ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1806, in advise_indicators
    dataframe = _create_and_merge_informative_pair(
        self, dataframe, metadata, inf_data, populate_fn
    )
  File "/freqtrade/freqtrade/strategy/informative_decorator.py", line 140, in _create_and_merge_informative_pair
    raise ValueError(
    ...<2 lines>...
    )
ValueError: Informative dataframe for (ETH/USDT:USDT, 30m, futures) is empty. Can't populate informative indicators.

```
### epretrace
- File: `epretrace.py`
- Duration: 6.27s
- Error Log:
```
...ange - INFO - Instance is running with dry_run enabled
2026-02-18 06:58:54,984 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:58:54,985 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:54,998 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:55,012 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:58:56,741 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:58:56,763 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/epretrace.py due to 'cannot import name 'CategoricalParameter' from 
'freqtrade.strategy.hyper' (/freqtrade/freqtrade/strategy/hyper.py)'
2026-02-18 06:58:56,799 - freqtrade - ERROR - Impossible to load Strategy 'epretrace'. This class does not exist or contains Python code errors.

```
### Obelisk_Ichimoku_ZEMA_v1
- File: `Obelisk_Ichimoku_ZEMA_v1.py`
- Duration: 5.80s
- Error Log:
```
...se_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/Obelisk_Ichimoku_ZEMA_v1.py", line 215, in populate_indicators
    informative = self.slow_tf_indicators(informative.copy(), metadata)
  File "/freqtrade/user_data/strategies/Obelisk_Ichimoku_ZEMA_v1.py", line 133, in slow_tf_indicators
    ssl_down, ssl_up = ssl_atr(dataframe, 10)
                       ~~~~~~~^^^^^^^^^^^^^^^
  File "/freqtrade/user_data/strategies/Obelisk_Ichimoku_ZEMA_v1.py", line 29, in ssl_atr
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, np.where(df['close'] < df['smaLow'], -1, np.NAN))
                                                                                                  ^^^^^^
  File "/home/ftuser/.local/lib/python3.13/site-packages/numpy/__init__.py", line 795, in __getattr__
    raise AttributeError(f"module {__name__!r} has no attribute {attr!r}")
AttributeError: module 'numpy' has no attribute 'NAN'. Did you mean: 'nan'?

```
### RaposaDivergenceV1
- File: `RaposaDivergenceV1.py`
- Duration: 3.00s
- Error Log:
```
...e is running with dry_run enabled
2026-02-18 06:55:54,981 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:55:54,981 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:54,992 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:55,003 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:55:54,500 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:55:54,548 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/RaposaDivergenceV1.py due to 'The `scipy` install you are using seems to be broken,
(extension modules cannot be imported), please try reinstalling.'
2026-02-18 06:55:54,557 - freqtrade - ERROR - Impossible to load Strategy 'RaposaDivergenceV1'. This class does not exist or contains Python code errors.

```
### Persia
- File: `Persia.py`
- Duration: 3.30s
- Error Log:
```
... freqtrade in Backtesting mode
2026-02-18 06:55:28,568 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:55:28,569 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:55:28,569 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:28,580 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:55:28,593 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:55:30,174 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:55:30,214 - freqtrade.resolvers.iresolver - WARNING - Could not import /freqtrade/user_data/strategies/Persia.py due to 'No module named 'numpy.lib.function_base''
2026-02-18 06:55:30,249 - freqtrade - ERROR - Impossible to load Strategy 'Persia'. This class does not exist or contains Python code errors.

```
### SMAOffsetProtectOptV1HO1
- File: `SMAOffsetProtectOptV1HO1.py`
- Duration: 3.24s
- Error Log:
```
...e.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:56:23,250 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:56:23,250 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:23,261 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:56:23,273 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:56:25,024 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:56:25,061 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy SMAOffsetProtectOptV1HO1 from '/freqtrade/user_data/strategies/SMAOffsetProtectOptV1HO1.py'...
2026-02-18 06:56:25,062 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:56:25,063 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### conny
- File: `conny.py`
- Duration: 5.33s
- Error Log:
```
...t()
    ~~~~~~~~~~~~~~~~~^^
  File "/freqtrade/freqtrade/optimize/backtesting.py", line 1844, in start
    min_date, max_date = self.backtest_one_strategy(strat, data, timerange)
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/optimize/backtesting.py", line 1754, in backtest_one_strategy
    preprocessed = self.strategy.advise_all_indicators(data)
  File "/freqtrade/freqtrade/strategy/interface.py", line 1749, in advise_all_indicators
    res[pair] = self.advise_indicators(pair_data.copy(), {"pair": pair}).copy()
                ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1811, in advise_indicators
    dataframe = self.populate_indicators(dataframe, metadata)
  File "/freqtrade/user_data/strategies/conny.py", line 66, in populate_indicators
    dataframe['consensus_sell'] = c.score()['exit']
                                  ~~~~~~~~~^^^^^^^^
KeyError: 'exit'

```
### bestV2
- File: `bestV2.py`
- Duration: 5.12s
- Error Log:
```
...e
2026-02-18 06:58:25,212 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2026-02-18 06:58:25,212 - freqtrade.exchange.exchange - INFO - Using CCXT 4.5.29
2026-02-18 06:58:25,213 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:25,224 - freqtrade.exchange.exchange - INFO - Applying additional ccxt config: {'options': {'defaultType': 'swap'}}
2026-02-18 06:58:25,237 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2026-02-18 06:58:26,703 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2026-02-18 06:58:26,761 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy bestV2 from '/freqtrade/user_data/strategies/bestV2.py'...
2026-02-18 06:58:26,761 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2026-02-18 06:58:26,762 - freqtrade - ERROR - DEPRECATED: Using 'sell_profit_offset' moved to 'exit_profit_offset'.

```
### RSI
- File: `RSI.py`
- Duration: 5.32s
- Error Log:
```
... self.backtest_one_strategy(strat, data, timerange)
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/optimize/backtesting.py", line 1754, in backtest_one_strategy
    preprocessed = self.strategy.advise_all_indicators(data)
  File "/freqtrade/freqtrade/strategy/interface.py", line 1749, in advise_all_indicators
    res[pair] = self.advise_indicators(pair_data.copy(), {"pair": pair}).copy()
                ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/freqtrade/freqtrade/strategy/interface.py", line 1806, in advise_indicators
    dataframe = _create_and_merge_informative_pair(
        self, dataframe, metadata, inf_data, populate_fn
    )
  File "/freqtrade/freqtrade/strategy/informative_decorator.py", line 140, in _create_and_merge_informative_pair
    raise ValueError(
    ...<2 lines>...
    )
ValueError: Informative dataframe for (ETH/USDT:USDT, 30m, futures) is empty. Can't populate informative indicators.

```

## Passed Strategies
- ADXMomentum (7.99s)
- ADX_15M_USDT (5.75s)
- ADX_15M_USDT2 (6.52s)
- ASDTSRockwellTrading (8.34s)
- ActionZone (7.83s)
- AdxSmas (6.26s)
- AlligatorStrat (6.41s)
- AlligatorStrategy (7.83s)
- AlwaysBuy (5.50s)
- Apollo11 (3.90s)
- AverageStrategy (5.83s)
- AwesomeMacd (7.59s)
- bbrsi (7.98s)
- BBRSI2 (4.50s)
- BBRSI21 (7.46s)
- BBRSI3366 (5.31s)
- BBRSI4cust (6.25s)
- BBRSINaiveStrategy (7.80s)
- BBRSIOptim2020Strategy (6.93s)
- BBRSIOptimStrategy (6.68s)
- BBRSIOptimizedStrategy (6.60s)
- BBRSIS (7.68s)
- BBRSIStrategy (5.47s)
- BBRSIoriginal (8.87s)
- BB_RPB_TSL_RNG (6.24s)
- BB_RPB_TSL_RNG_2 (6.03s)
- BB_RPB_TSL_RNG_TBS (8.92s)
- BB_RPB_TSL_RNG_TBS_GOLD (7.27s)
- BB_RPB_TSL_RNG_VWAP (6.09s)
- BB_RPB_TSL_c7c477d_20211030 (5.90s)
- BB_RSI (5.85s)
- BB_Strategy04 (8.56s)
- BBands (8.10s)
- BBandsRSI (5.80s)
- BBlower (7.27s)
- Babico_SMA5xBBmid (6.10s)
- Bandtastic (7.24s)
- BbandRsi (8.15s)
- BbandRsiRolling (5.13s)
- BinHV27 (6.57s)
- BinHV45 (5.53s)
- BinHV45HO (6.47s)
- BreakEven (5.23s)
- BuyAllSellAllStrategy (8.61s)
- BuyOnly (7.65s)
- CCIStrategy (5.71s)
- CMCWinner (6.49s)
- Cci (7.82s)
- Chandem (6.43s)
- Chandemtwo (8.80s)
- Chispei (6.80s)
- Cluc4 (7.72s)
- ClucMay72018 (7.85s)
- CofiBitStrategy (8.60s)
- CombinedBinHAndCluc (3.93s)
- CombinedBinHAndCluc2021 (3.95s)
- CombinedBinHAndCluc2021Bull (7.14s)
- CombinedBinHAndClucHyperV0 (7.24s)
- CombinedBinHAndClucHyperV3 (7.29s)
- Combined_Indicators (7.70s)
- Combined_NFIv6_SMA (4.42s)
- Combined_NFIv7_SMA (7.05s)
- Combined_NFIv7_SMA_Rallipanos_20210707 (6.94s)
- Combined_NFIv7_SMA_bAdBoY_20211204 (8.05s)
- CrossEMAStrategy (8.38s)
- CustomStoplossWithPSAR (9.06s)
- DD (8.33s)
- Divergences (8.39s)
- Dracula (6.04s)
- EMABBRSI (7.75s)
- EMASkipPump (8.46s)
- EMAVolume (8.02s)
- EMA_CROSSOVER_STRATEGY (7.66s)
- EXPERIMENTAL_STRATEGY (7.70s)
- FRAYSTRAT (8.05s)
- FixedRiskRewardLoss (7.08s)
- ForexSignal (8.22s)
- FrostAuraM115mStrategy (7.53s)
- FrostAuraM11hStrategy (5.95s)
- FrostAuraM21hStrategy (7.77s)
- FrostAuraM315mStrategy (7.61s)
- FrostAuraM31hStrategy (7.83s)
- GodCard (7.32s)
- Gumbo1 (8.25s)
- HansenSmaOffsetV1 (7.56s)
- Heracles (8.37s)
- HourBasedStrategy (5.84s)
- INSIDEUP (6.42s)
- Ichess (8.02s)
- Ichi (8.36s)
- Ichimoku (8.15s)
- Ichimoku_v12 (8.50s)
- Ichimoku_v30 (9.53s)
- Ichimoku_v32 (6.89s)
- Ichimoku_v33 (7.76s)
- InformativeSample (7.25s)
- JustROCR (7.34s)
- JustROCR3 (9.52s)
- JustROCR5 (10.00s)
- JustROCR6 (7.03s)
- KC_BB (8.65s)
- Leveraged (7.58s)
- Low_BB (6.57s)
- LuxOSC (11.09s)
- MAC (10.86s)
- MACDCCI (6.33s)
- MACDRSI200 (7.67s)
- MACDStrategy (8.39s)
- MACDStrategy_crossed (8.07s)
- MACD_EMA (5.64s)
- MACD_TRIPLE_MA (7.46s)
- MACD_TRI_EMA (8.21s)
- MADisplaceV3 (7.39s)
- MFI (5.53s)
- Macd (7.97s)
- Maro4hMacdSd (7.66s)
- Martin (7.77s)
- Minmax (9.11s)
- Momentumv2 (6.24s)
- MontrealStrategy (7.63s)
- MultiRSI (6.53s)
- NFI5MOHO2 (7.49s)
- NFI5MOHO_WIP (7.62s)
- NFI5MOHO_WIP_1 (8.56s)
- NFI5MOHO_WIP_2 (5.46s)
- NFI7MOHO (7.08s)
- NFINextMOHO (7.15s)
- NFINextMOHO2 (4.98s)
- NFINextMultiOffsetAndHO (8.00s)
- NFINextMultiOffsetAndHO2 (7.63s)
- Nostalgia (7.56s)
- NostalgiaForInfinityNextGen (6.93s)
- NostalgiaForInfinityNextGen_TSL (5.68s)
- NostalgiaForInfinityV4 (7.04s)
- NostalgiaForInfinityV4HO (7.31s)
- NostalgiaForInfinityV5 (7.50s)
- NostalgiaForInfinityV5MultiOffsetAndHO (5.85s)
- NostalgiaForInfinityV5MultiOffsetAndHO2 (8.48s)
- NostalgiaForInfinityV6 (9.54s)
- NostalgiaForInfinityV6HO (6.36s)
- NostalgiaForInfinityV7 (7.77s)
- NostalgiaForInfinityV7_SMA (7.85s)
- NostalgiaForInfinityV7_SMAv2 (6.26s)
- NostalgiaForInfinityV7_SMAv2_1 (7.99s)
- NostalgiaForInfinityX2 (5.11s)
- Saturn5 (7.25s)
- adx_opt_strat (7.77s)
- stratfib (6.98s)
- YOLO (7.29s)
- ema (7.55s)
- Roth01 (7.71s)
- ONUR (7.54s)
- Seb (7.79s)
- ReinforcedQuickie (7.62s)
- PRICEFOLLOWINGX (7.59s)
- Strategy005 (7.26s)
- TechnicalExampleStrategy (6.22s)
- RSIBB02 (7.56s)
- WaveTrendStra (7.67s)
- SwingHigh (6.99s)
- bbrsi4Freq (7.81s)
- SMAOG (5.12s)
- TemaPureNeat (7.56s)
- bb_rsi_opt_new (7.11s)
- NowoIchimoku1hV2 (7.00s)
- UziChan (5.38s)
- Uptrend (7.88s)
- Roth03 (5.52s)
- SMAIP3 (7.10s)
- PRICEFOLLOWING2 (7.37s)
- PrawnstarOBV (8.77s)
- Stavix2 (8.91s)
- ichiV1 (8.76s)
- PumpDetector (8.50s)
- TDSequentialStrategy (9.46s)
- TrixStrategy (8.75s)
- XebTradeStrat (9.36s)
- Quickie (8.70s)
- SampleStrategy (8.86s)
- Trend_Strength_Directional (9.75s)
- RobotradingBody (5.90s)
- STRATEGY_RSI_BB_CROSS (8.04s)
- SmoothOperator (6.11s)
- SwingHighToSky (7.65s)
- TrixV21Strategy (6.01s)
- TheForce (8.02s)
- SRsi (7.94s)
- SMAIP3v2 (7.29s)
- VWAP (8.38s)
- Scalp (6.76s)
- UziChan2 (7.59s)
- keltnerchannel (7.43s)
- Slowbro (6.32s)
- adxbbrsi2 (4.40s)
- TemaPureTwo (6.62s)
- adaptive (6.32s)
- SMAOffsetV2 (6.39s)
- StrategyScalpingFast (4.53s)
- MabStra (6.78s)
- TrailingBuyStrat2 (6.89s)
- ReinforcedAverageStrategy (6.80s)
- TEMA (4.95s)
- TemaMaster (7.02s)
- botbaby (3.58s)
- SmoothScalp (5.82s)
- Simple (6.15s)
- Obelisk_TradePro_Ichi_v1_1 (6.01s)
- flawless_lambo (7.46s)
- ObeliskIM_v1_1 (6.11s)
- TheRealPullbackV2 (6.69s)
- XtraThicc (6.39s)
- STRATEGY_RSI_BB_BOUNDS_CROSS (6.28s)
- Strategy001_custom_sell (4.47s)
- PRICEFOLLOWING (5.42s)
- wtc (6.40s)
- Strategy002 (5.36s)
- TrixV15Strategy (5.62s)
- macd_recovery (5.41s)
- heikin (6.85s)
- quantumfirst (6.64s)
- stoploss (4.58s)
- Strategy003 (4.35s)
- redditMA (6.15s)
- e6v34 (6.27s)
- SMAOffsetProtectOpt (6.20s)
- TemaMaster3 (6.24s)
- hlhb (6.60s)
- SupertrendStrategy (6.68s)
- mark_strat (6.34s)
- ObeliskRSI_v6_1 (6.67s)
- StrategyScalpingFast2 (4.13s)
- UltimateMomentumIndicator (6.75s)
- Sar (3.69s)
- Strategy004 (3.39s)
- Strategy001 (5.66s)
- hansencandlepatternV1 (3.74s)
- TemaPure (5.80s)
- ReinforcedSmoothScalp (5.53s)
