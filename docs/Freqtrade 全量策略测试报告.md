# Freqtrade 全量策略测试报告

- **总测试策略数:** 465
- **成功运行:** 87
- **失败/无数据:** 378
- **测试周期:** 5分钟 (2025-12-20 ~ 2026-01-14)

## 🏆 Top 20 最佳策略
| 排名 | 策略名称 | 总收益率 | 胜率 | 交易次数 | 夏普比率 | 最大回撤 |
|---|---|---|---|---|---|---|
| 1 | **MACDCCI** | 6.23% | 100.00% | 2 | 4.52 | 0.00% |
| 2 | **BbandRsiRolling** | 6.09% | 65.00% | 20 | 15.30 | 0.07% |
| 3 | **FixedRiskRewardLoss** | 5.75% | 100.00% | 2 | 5.39 | 0.00% |
| 4 | **Quickie** | 5.73% | 100.00% | 20 | 129.26 | 0.00% |
| 5 | **CustomStoplossWithPSAR** | 5.73% | 100.00% | 2 | 5.37 | 0.00% |
| 6 | **Obelisk_3EMA_StochRSI_ATR** | 5.57% | 100.00% | 2 | 5.61 | 0.00% |
| 7 | **SmoothOperator** | 5.55% | 72.73% | 44 | 18.62 | 0.89% |
| 8 | **Ichimoku_v12** | 5.32% | 100.00% | 5 | 7.18 | 0.00% |
| 9 | **BbandRsi** | 4.55% | 76.92% | 52 | 13.03 | 0.93% |
| 10 | **ADX_15M_USDT2** | 4.48% | 45.16% | 31 | 14.66 | 0.08% |
| 11 | **Simple** | 4.40% | 79.31% | 29 | 9.65 | 1.02% |
| 12 | **MACDStrategy** | 4.40% | 100.00% | 15 | 95.81 | 0.00% |
| 13 | **Ichimoku_v30** | 4.39% | 75.00% | 12 | 5.52 | 0.72% |
| 14 | **Roth01** | 4.32% | 45.45% | 44 | 15.43 | 0.07% |
| 15 | **Trend_Strength_Directional** | 4.08% | 52.50% | 40 | 17.56 | 0.10% |
| 16 | **macd_recovery** | 3.99% | 61.54% | 26 | 4.90 | 2.48% |
| 17 | **Stavix2** | 3.94% | 80.00% | 5 | 3.24 | 0.46% |
| 18 | **HourBasedStrategy** | 3.83% | 60.00% | 20 | 11.74 | 0.10% |
| 19 | **ADX_15M_USDT** | 3.68% | 56.67% | 30 | 17.37 | 0.06% |
| 20 | **MACDStrategy_crossed** | 3.40% | 92.86% | 14 | 12.64 | 0.48% |

## 完整列表 (按收益排序)
| 策略名称 | 状态 | 总收益率 | 胜率 | 交易次数 | 说明 |
|---|---|---|---|---|---|
| MACDCCI | ✅ | 6.23% | 100.00% | 2 | 盈利 |
| BbandRsiRolling | ✅ | 6.09% | 65.00% | 20 | 盈利 |
| FixedRiskRewardLoss | ✅ | 5.75% | 100.00% | 2 | 盈利 |
| Quickie | ✅ | 5.73% | 100.00% | 20 | 盈利 |
| CustomStoplossWithPSAR | ✅ | 5.73% | 100.00% | 2 | 盈利 |
| Obelisk_3EMA_StochRSI_ATR | ✅ | 5.57% | 100.00% | 2 | 盈利 |
| SmoothOperator | ✅ | 5.55% | 72.73% | 44 | 盈利 |
| Ichimoku_v12 | ✅ | 5.32% | 100.00% | 5 | 盈利 |
| BbandRsi | ✅ | 4.55% | 76.92% | 52 | 盈利 |
| ADX_15M_USDT2 | ✅ | 4.48% | 45.16% | 31 | 盈利 |
| Simple | ✅ | 4.40% | 79.31% | 29 | 盈利 |
| MACDStrategy | ✅ | 4.40% | 100.00% | 15 | 盈利 |
| Ichimoku_v30 | ✅ | 4.39% | 75.00% | 12 | 盈利 |
| Roth01 | ✅ | 4.32% | 45.45% | 44 | 盈利 |
| Trend_Strength_Directional | ✅ | 4.08% | 52.50% | 40 | 盈利 |
| macd_recovery | ✅ | 3.99% | 61.54% | 26 | 盈利 |
| Stavix2 | ✅ | 3.94% | 80.00% | 5 | 盈利 |
| HourBasedStrategy | ✅ | 3.83% | 60.00% | 20 | 盈利 |
| ADX_15M_USDT | ✅ | 3.68% | 56.67% | 30 | 盈利 |
| MACDStrategy_crossed | ✅ | 3.40% | 92.86% | 14 | 盈利 |
| SwingHighToSky | ✅ | 3.04% | 45.24% | 42 | 盈利 |
| Cci | ✅ | 2.34% | 52.94% | 119 | 盈利 |
| MACDRSI200 | ✅ | 2.07% | 56.52% | 23 | 盈利 |
| Ichimoku_v32 | ✅ | 1.95% | 31.43% | 35 | 盈利 |
| adxbbrsi2 | ✅ | 1.86% | 54.55% | 11 | 盈利 |
| ReinforcedQuickie | ✅ | 1.63% | 73.68% | 57 | 盈利 |
| BBRSI21 | ✅ | 1.60% | 57.14% | 21 | 盈利 |
| LookaheadStrategy | ✅ | 1.55% | 100.00% | 1 | 盈利 |
| MFI | ✅ | 1.45% | 61.90% | 63 | 盈利 |
| Roth03 | ✅ | 1.33% | 52.94% | 17 | 盈利 |
| EMASkipPump | ✅ | 1.32% | 63.98% | 186 | 盈利 |
| DD | ✅ | 1.17% | 56.10% | 164 | 盈利 |
| SmoothScalp | ✅ | 0.93% | 82.35% | 17 | 盈利 |
| BBRSI3366 | ✅ | 0.87% | 45.54% | 101 | 盈利 |
| BinHV27 | ✅ | 0.66% | 61.90% | 21 | 盈利 |
| SwingHigh | ✅ | 0.57% | 55.56% | 9 | 盈利 |
| Bandtastic | ✅ | 0.55% | 66.13% | 248 | 盈利 |
| adx_opt_strat | ✅ | 0.10% | 33.33% | 6 | 盈利 |
| Leveraged | ✅ | 0.05% | 44.83% | 87 | 盈利 |
| adaptive | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| VWAP | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| BinHV45 | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| ClucMay72018 | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| HansenSmaOffsetV1 | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| Combined_Indicators | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| JustROCR6 | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| Low_BB | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| SMAOffsetProtectOpt | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| Macd | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| JustROCR3 | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| JustROCR | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| JustROCR5 | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| BreakEven | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| BinHV45HO | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| KC_BB | ✅ | 0.00% | 0.00% | 0 | 亏损 |
| CCIStrategy | ✅ | -0.10% | 33.33% | 3 | 亏损 |
| ReinforcedSmoothScalp | ✅ | -0.18% | 66.67% | 9 | 亏损 |
| CMCWinner | ✅ | -0.65% | 46.51% | 43 | 亏损 |
| ObeliskRSI_v6_1 | ✅ | -0.77% | 46.77% | 62 | 亏损 |
| MACD_TRIPLE_MA | ✅ | -0.97% | 35.71% | 56 | 亏损 |
| AlwaysBuy | ✅ | -1.27% | 46.22% | 238 | 亏损 |
| Scalp | ✅ | -1.39% | 39.24% | 79 | 亏损 |
| UziChan | ✅ | -1.62% | 38.89% | 126 | 亏损 |
| ObeliskIM_v1_1 | ✅ | -1.85% | 15.79% | 19 | 亏损 |
| MACD_EMA | ✅ | -2.22% | 37.86% | 103 | 亏损 |
| Ichess | ✅ | -2.27% | 31.02% | 187 | 亏损 |
| Obelisk_TradePro_Ichi_v1_1 | ✅ | -2.66% | 24.68% | 158 | 亏损 |
| AwesomeMacd | ✅ | -2.77% | 28.46% | 123 | 亏损 |
| CofiBitStrategy | ✅ | -3.11% | 33.73% | 83 | 亏损 |
| ADXMomentum | ✅ | -3.36% | 37.10% | 124 | 亏损 |
| EMAVolume | ✅ | -4.67% | 20.63% | 126 | 亏损 |
| MultiRSI | ✅ | -5.31% | 45.21% | 73 | 亏损 |
| Chispei | ✅ | -5.69% | 27.19% | 331 | 亏损 |
| XebTradeStrat | ✅ | -6.35% | 76.05% | 309 | 亏损 |
| Ichimoku_v33 | ✅ | -6.43% | 20.24% | 168 | 亏损 |
| e6v34 | ✅ | -6.95% | 25.49% | 204 | 亏损 |
| BBRSI4cust | ✅ | -7.95% | 31.78% | 409 | 亏损 |
| AdxSmas | ✅ | -8.44% | 26.15% | 195 | 亏损 |
| AverageStrategy | ✅ | -12.51% | 17.41% | 402 | 亏损 |
| keltnerchannel | ✅ | -13.56% | 18.97% | 406 | 亏损 |
| MACD_TRI_EMA | ✅ | -13.86% | 24.12% | 485 | 亏损 |
| ASDTSRockwellTrading | ✅ | -15.73% | 19.71% | 487 | 亏损 |
| AlligatorStrat | ✅ | -16.18% | 23.05% | 590 | 亏损 |
| TechnicalExampleStrategy | ✅ | -19.76% | 29.59% | 828 | 亏损 |
| hansencandlepatternV1 | ✅ | -19.81% | 17.63% | 556 | 亏损 |
| heikin | ✅ | -26.31% | 20.74% | 921 | 亏损 |
| WaveTrendStra | ✅ | -28.25% | 20.50% | 1083 | 亏损 |
| RSI | ❌ | - | - | - | Error: Return code non-zero... |
| RSIv2 | ❌ | - | - | - | Error: Return code non-zero... |
| RalliV1 | ❌ | - | - | - | Error: Return code non-zero... |
| RalliV1_disable56 | ❌ | - | - | - | Error: Return code non-zero... |
| RaposaDivergenceV1 | ❌ | - | - | - | Error: Return code non-zero... |
| ReinforcedAverageStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| Renko | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityXw | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffSetStrategy_V2 | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategyHO | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategyHOv3 | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategyLite | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategyModHO | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901 | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategyX1 | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategy_uzi | ❌ | - | - | - | Error: Return code non-zero... |
| NotAnotherSMAOffsetStrategy_uzi3 | ❌ | - | - | - | Error: Return code non-zero... |
| NowoIchimoku1hV1 | ❌ | - | - | - | Error: Return code non-zero... |
| NowoIchimoku1hV2 | ❌ | - | - | - | Error: Return code non-zero... |
| NowoIchimoku5mV2 | ❌ | - | - | - | Error: Return code non-zero... |
| RSIBB02 | ❌ | - | - | - | Error: Return code non-zero... |
| SAR | ❌ | - | - | - | Error: Return code non-zero... |
| SMAIP3 | ❌ | - | - | - | Error: Return code non-zero... |
| SMAIP3v2 | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOG | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOPv1_TTF | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffset | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffsetProtectOptV0 | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffsetProtectOptV1 | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffsetProtectOptV1HO1 | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffsetProtectOptV1Mod | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffsetProtectOptV1Mod2 | ❌ | - | - | - | Error: Return code non-zero... |
| Persia | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffsetV2 | ❌ | - | - | - | Error: Return code non-zero... |
| SMA_BBRSI | ❌ | - | - | - | Error: Return code non-zero... |
| SRsi | ❌ | - | - | - | Error: Return code non-zero... |
| Obelisk_Ichimoku_ZEMA_v1 | ❌ | - | - | - | Error: Return code non-zero... |
| Obelisk_TradePro_Ichi_v2_1 | ❌ | - | - | - | Error: Return code non-zero... |
| PRICEFOLLOWING | ❌ | - | - | - | Error: Return code non-zero... |
| PRICEFOLLOWING2 | ❌ | - | - | - | Error: Return code non-zero... |
| PRICEFOLLOWINGX | ❌ | - | - | - | Error: Return code non-zero... |
| ONUR | ❌ | - | - | - | Error: Return code non-zero... |
| PrawnstarOBV | ❌ | - | - | - | Error: Return code non-zero... |
| PumpDetector | ❌ | - | - | - | Error: Return code non-zero... |
| SMAOffsetProtectOptV1_kkeue_20210619 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNext | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNextGen | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNextGen_TSL | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNextV7155 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNext_ChangeToTower_V5_2 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNext_ChangeToTower_V5_3 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNext_ChangeToTower_V6 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityNext_maximizer | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV1 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI46FrogZ | ❌ | - | - | - | Error: Return code non-zero... |
| NFI46Offset | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV3 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI46Z | ❌ | - | - | - | Error: Return code non-zero... |
| NFI47V2 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI4Frog | ❌ | - | - | - | Error: Return code non-zero... |
| NFI5MOHO | ❌ | - | - | - | Error: Return code non-zero... |
| NFI5MOHO2 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI5MOHO_WIP | ❌ | - | - | - | Error: Return code non-zero... |
| NFI5MOHO_WIP_1 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI5MOHO_WIP_2 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI731_BUSD | ❌ | - | - | - | Error: Return code non-zero... |
| NFI7MOHO | ❌ | - | - | - | Error: Return code non-zero... |
| NFINextMOHO | ❌ | - | - | - | Error: Return code non-zero... |
| NFI46OffsetHOA1 | ❌ | - | - | - | Error: Return code non-zero... |
| Obelisk_Ichimoku_Slow_v1_3 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV2 | ❌ | - | - | - | Error: Return code non-zero... |
| RobotradingBody | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV4 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV4HO | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV5 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV5MultiOffsetAndHO | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV5MultiOffsetAndHO2 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV6 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV6HO | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV7 | ❌ | - | - | - | Error: Return code non-zero... |
| Nostalgia | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV7_SMA | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV7_SMAv2 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV7_SMAv2_1 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityX | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityX2 | ❌ | - | - | - | Error: Return code non-zero... |
| NFINextMultiOffsetAndHO2 | ❌ | - | - | - | Error: Return code non-zero... |
| NFIX_BB_RPB | ❌ | - | - | - | Error: Return code non-zero... |
| NFIX_BB_RPB_c7c477d_20211030 | ❌ | - | - | - | Error: Return code non-zero... |
| NfiNextModded | ❌ | - | - | - | Error: Return code non-zero... |
| NormalizerStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| NormalizerStrategyHO2 | ❌ | - | - | - | Error: Return code non-zero... |
| NostalgiaForInfinityV7_7_2 | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSIoriginal | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSIv2 | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_2 | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_BI | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_BIV1 | ❌ | - | - | - | Error: Return code non-zero... |
| TemaMaster | ❌ | - | - | - | Error: Return code non-zero... |
| TemaMaster3 | ❌ | - | - | - | Error: Return code non-zero... |
| TemaPure | ❌ | - | - | - | Error: Return code non-zero... |
| TemaPureNeat | ❌ | - | - | - | Error: Return code non-zero... |
| BBandsRSI | ❌ | - | - | - | Error: Return code non-zero... |
| TenderEnter | ❌ | - | - | - | Error: Return code non-zero... |
| TheForce | ❌ | - | - | - | Error: Return code non-zero... |
| TheRealPullbackV2 | ❌ | - | - | - | Error: Return code non-zero... |
| TrailingBuyStrat2 | ❌ | - | - | - | Error: Return code non-zero... |
| TrixStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| TrixV15Strategy | ❌ | - | - | - | Error: Return code non-zero... |
| TrixV21Strategy | ❌ | - | - | - | Error: Return code non-zero... |
| TrixV23Strategy | ❌ | - | - | - | Error: Return code non-zero... |
| UltimateMomentumIndicator | ❌ | - | - | - | Error: Return code non-zero... |
| Uptrend | ❌ | - | - | - | Error: Return code non-zero... |
| UziChan2 | ❌ | - | - | - | Error: Return code non-zero... |
| TemaPureTwo | ❌ | - | - | - | Error: Return code non-zero... |
| bb_rsi_opt_new | ❌ | - | - | - | Error: Return code non-zero... |
| bbema | ❌ | - | - | - | Error: Return code non-zero... |
| bbrsi1_strategy | ❌ | - | - | - | Error: Return code non-zero... |
| bbrsi4Freq | ❌ | - | - | - | Error: Return code non-zero... |
| bestV2 | ❌ | - | - | - | Error: Return code non-zero... |
| botbaby | ❌ | - | - | - | Error: Return code non-zero... |
| conny | ❌ | - | - | - | Error: Return code non-zero... |
| cryptohassle | ❌ | - | - | - | Error: Return code non-zero... |
| custom | ❌ | - | - | - | Error: Return code non-zero... |
| custom_sell | ❌ | - | - | - | Error: Return code non-zero... |
| ema | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSITV | ❌ | - | - | - | Error: Return code non-zero... |
| fahmibah | ❌ | - | - | - | Error: Return code non-zero... |
| flawless_lambo | ❌ | - | - | - | Error: Return code non-zero... |
| wtc | ❌ | - | - | - | Error: Return code non-zero... |
| XtraThicc | ❌ | - | - | - | Error: Return code non-zero... |
| YOLO | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSINaiveStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSIOptim2020Strategy | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSIOptimStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSIOptimizedStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSIS | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSIStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| epretrace | ❌ | - | - | - | Error: Return code non-zero... |
| Schism5 | ❌ | - | - | - | Error: Return code non-zero... |
| Schism6 | ❌ | - | - | - | Error: Return code non-zero... |
| Seb | ❌ | - | - | - | Error: Return code non-zero... |
| SlowPotato | ❌ | - | - | - | Error: Return code non-zero... |
| Slowbro | ❌ | - | - | - | Error: Return code non-zero... |
| Stinkfist | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_RNG_2 | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_RNG_TBS | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_RNG_TBS_GOLD | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_RNG_VWAP | ❌ | - | - | - | Error: Return code non-zero... |
| StochRSITEMA | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_SMA_Tranz_TB_1_1_1 | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_SMA_Tranz_TB_MOD | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_Tranz | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_c7c477d_20211030 | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSLmeneguzzo | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RSI | ❌ | - | - | - | Error: Return code non-zero... |
| BB_Strategy04 | ❌ | - | - | - | Error: Return code non-zero... |
| BBands | ❌ | - | - | - | Error: Return code non-zero... |
| NFINextMOHO2 | ❌ | - | - | - | Error: Return code non-zero... |
| BBlower | ❌ | - | - | - | Error: Return code non-zero... |
| Babico_SMA5xBBmid | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_SMA_Tranz | ❌ | - | - | - | Error: Return code non-zero... |
| Strategy001 | ❌ | - | - | - | Error: Return code non-zero... |
| Strategy001_custom_sell | ❌ | - | - | - | Error: Return code non-zero... |
| Strategy002 | ❌ | - | - | - | Error: Return code non-zero... |
| Strategy003 | ❌ | - | - | - | Error: Return code non-zero... |
| Strategy004 | ❌ | - | - | - | Error: Return code non-zero... |
| Strategy005 | ❌ | - | - | - | Error: Return code non-zero... |
| StrategyScalpingFast | ❌ | - | - | - | Error: Return code non-zero... |
| StrategyScalpingFast2 | ❌ | - | - | - | Error: Return code non-zero... |
| SuperHV27 | ❌ | - | - | - | Error: Return code non-zero... |
| SuperTrend | ❌ | - | - | - | Error: Return code non-zero... |
| SuperTrendPure | ❌ | - | - | - | Error: Return code non-zero... |
| Schism4 | ❌ | - | - | - | Error: Return code non-zero... |
| TDSequentialStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| TEMA | ❌ | - | - | - | Error: Return code non-zero... |
| STRATEGY_RSI_BB_BOUNDS_CROSS | ❌ | - | - | - | Error: Return code non-zero... |
| STRATEGY_RSI_BB_CROSS | ❌ | - | - | - | Error: Return code non-zero... |
| SampleStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| SampleStrategyV2 | ❌ | - | - | - | Error: Return code non-zero... |
| Saturn5 | ❌ | - | - | - | Error: Return code non-zero... |
| Schism | ❌ | - | - | - | Error: Return code non-zero... |
| Schism2 | ❌ | - | - | - | Error: Return code non-zero... |
| Schism2MM | ❌ | - | - | - | Error: Return code non-zero... |
| Schism3 | ❌ | - | - | - | Error: Return code non-zero... |
| SupertrendStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogHO2A | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogHO3A1 | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogHO3A2 | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogHO3A3 | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogHO3A4 | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogNFI | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogNFIHO1A | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogOffset | ❌ | - | - | - | Error: Return code non-zero... |
| DCBBBounce | ❌ | - | - | - | Error: Return code non-zero... |
| DIV_v1 | ❌ | - | - | - | Error: Return code non-zero... |
| MontrealStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV5Hyperoptable | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV6 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV6H | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV7 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV8 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV8Hyper | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV8XH | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV8XHO | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHClucAndMADV3 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHClucAndMADV5 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHClucAndMADV6 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV5 | ❌ | - | - | - | Error: Return code non-zero... |
| FrostAuraM115mStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| FrostAuraM11hStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| DevilStra | ❌ | - | - | - | Error: Return code non-zero... |
| Diamond | ❌ | - | - | - | Error: Return code non-zero... |
| Divergences | ❌ | - | - | - | Error: Return code non-zero... |
| Dracula | ❌ | - | - | - | Error: Return code non-zero... |
| Dyna_opti | ❌ | - | - | - | Error: Return code non-zero... |
| EI3v2_tag_cofi_green | ❌ | - | - | - | Error: Return code non-zero... |
| EMA50 | ❌ | - | - | - | Error: Return code non-zero... |
| EMA520015_V17 | ❌ | - | - | - | Error: Return code non-zero... |
| EMABBRSI | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogHO2 | ❌ | - | - | - | Error: Return code non-zero... |
| EMA_CROSSOVER_STRATEGY | ❌ | - | - | - | Error: Return code non-zero... |
| EXPERIMENTAL_STRATEGY | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV2 | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV4 | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV531 | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV5HO | ❌ | - | - | - | Error: Return code non-zero... |
| Combined_NFIv7_SMA_bAdBoY_20211204 | ❌ | - | - | - | Error: Return code non-zero... |
| CoreStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| CrossEMAStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrog | ❌ | - | - | - | Error: Return code non-zero... |
| CryptoFrogHO | ❌ | - | - | - | Error: Return code non-zero... |
| EMABreakout | ❌ | - | - | - | Error: Return code non-zero... |
| true_lambo | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix_BB_RPB_MOD | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix_BB_RPB_MOD2_ROI | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix_BB_RPB_MOD_CTT | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix_BB_RPB_MOD_E0V1E_ROI | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix_hhll | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAwerk | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndCluc | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndCluc2021 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndCluc2021Bull | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucHyperV0 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHClucAndMADV9 | ❌ | - | - | - | Error: Return code non-zero... |
| AlligatorStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| Apollo11 | ❌ | - | - | - | Error: Return code non-zero... |
| BBMod1 | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSI | ❌ | - | - | - | Error: Return code non-zero... |
| BBRSI2 | ❌ | - | - | - | Error: Return code non-zero... |
| hlhb | ❌ | - | - | - | Error: Return code non-zero... |
| ichiV1 | ❌ | - | - | - | Error: Return code non-zero... |
| ichiV1_Marius | ❌ | - | - | - | Error: Return code non-zero... |
| mabStra | ❌ | - | - | - | Error: Return code non-zero... |
| mark_strat | ❌ | - | - | - | Error: Return code non-zero... |
| mark_strat_opt | ❌ | - | - | - | Error: Return code non-zero... |
| ActionZone | ❌ | - | - | - | Error: Return code non-zero... |
| Combined_NFIv6_SMA | ❌ | - | - | - | Error: Return code non-zero... |
| Combined_NFIv7_SMA | ❌ | - | - | - | Error: Return code non-zero... |
| Combined_NFIv7_SMA_Rallipanos_20210707 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucHyperV3 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV2 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV3 | ❌ | - | - | - | Error: Return code non-zero... |
| CombinedBinHAndClucV4 | ❌ | - | - | - | Error: Return code non-zero... |
| Chandem | ❌ | - | - | - | Error: Return code non-zero... |
| Chandemtwo | ❌ | - | - | - | Error: Return code non-zero... |
| Cluc4 | ❌ | - | - | - | Error: Return code non-zero... |
| Cluc4werk | ❌ | - | - | - | Error: Return code non-zero... |
| strato | ❌ | - | - | - | Error: Return code non-zero... |
| Cluc7werk | ❌ | - | - | - | Error: Return code non-zero... |
| ClucFiatROI | ❌ | - | - | - | Error: Return code non-zero... |
| ClucFiatSlow | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix5m | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix_5m | ❌ | - | - | - | Error: Return code non-zero... |
| ClucHAnix_5m1 | ❌ | - | - | - | Error: Return code non-zero... |
| quantumfirst | ❌ | - | - | - | Error: Return code non-zero... |
| redditMA | ❌ | - | - | - | Error: Return code non-zero... |
| stoploss | ❌ | - | - | - | Error: Return code non-zero... |
| stratfib | ❌ | - | - | - | Error: Return code non-zero... |
| Cluc5werk | ❌ | - | - | - | Error: Return code non-zero... |
| MacheteV8b | ❌ | - | - | - | Error: Return code non-zero... |
| MacheteV8bRallimod2 | ❌ | - | - | - | Error: Return code non-zero... |
| MarketChyperHyperStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| Maro4hMacdSd | ❌ | - | - | - | Error: Return code non-zero... |
| Martin | ❌ | - | - | - | Error: Return code non-zero... |
| MiniLambo | ❌ | - | - | - | Error: Return code non-zero... |
| Minmax | ❌ | - | - | - | Error: Return code non-zero... |
| MomStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| Momentumv2 | ❌ | - | - | - | Error: Return code non-zero... |
| CBPete9 | ❌ | - | - | - | Error: Return code non-zero... |
| ForexSignal | ❌ | - | - | - | Error: Return code non-zero... |
| InformativeSample | ❌ | - | - | - | Error: Return code non-zero... |
| Inverse | ❌ | - | - | - | Error: Return code non-zero... |
| InverseV2 | ❌ | - | - | - | Error: Return code non-zero... |
| KAMACCIRSI | ❌ | - | - | - | Error: Return code non-zero... |
| Kamaflage | ❌ | - | - | - | Error: Return code non-zero... |
| BbRoi | ❌ | - | - | - | Error: Return code non-zero... |
| BcmbigzDevelop | ❌ | - | - | - | Error: Return code non-zero... |
| BcmbigzV1 | ❌ | - | - | - | Error: Return code non-zero... |
| BigPete | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ03 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ0307HO | ❌ | - | - | - | Error: Return code non-zero... |
| Ichimoku_v37 | ❌ | - | - | - | Error: Return code non-zero... |
| NFINextMultiOffsetAndHO | ❌ | - | - | - | Error: Return code non-zero... |
| BB_RPB_TSL_RNG | ❌ | - | - | - | Error: Return code non-zero... |
| MostOfAll | ❌ | - | - | - | Error: Return code non-zero... |
| MultiMA_TSL | ❌ | - | - | - | Error: Return code non-zero... |
| MultiMA_TSL3 | ❌ | - | - | - | Error: Return code non-zero... |
| MultiMA_TSL3_Mod | ❌ | - | - | - | Error: Return code non-zero... |
| MultiMa | ❌ | - | - | - | Error: Return code non-zero... |
| MultiOffsetLamboV0 | ❌ | - | - | - | Error: Return code non-zero... |
| NASOSRv6_private_Reinuvader_20211121 | ❌ | - | - | - | Error: Return code non-zero... |
| NASOSv4 | ❌ | - | - | - | Error: Return code non-zero... |
| NASOSv5 | ❌ | - | - | - | Error: Return code non-zero... |
| MADisplaceV3 | ❌ | - | - | - | Error: Return code non-zero... |
| NASOSv5_mod1_DanMod | ❌ | - | - | - | Error: Return code non-zero... |
| NASOSv5_mod2 | ❌ | - | - | - | Error: Return code non-zero... |
| NASOSv5_mod3 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI46 | ❌ | - | - | - | Error: Return code non-zero... |
| NFI46Frog | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ0407HO | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ04HO | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ04HO2 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ04_TSL3 | ❌ | - | - | - | Error: Return code non-zero... |
| LuxOSC | ❌ | - | - | - | Error: Return code non-zero... |
| MAC | ❌ | - | - | - | Error: Return code non-zero... |
| NASOSv5_mod1 | ❌ | - | - | - | Error: Return code non-zero... |
| GodStraNew40 | ❌ | - | - | - | Error: Return code non-zero... |
| GodStraNew_SMAonly | ❌ | - | - | - | Error: Return code non-zero... |
| Guacamole | ❌ | - | - | - | Error: Return code non-zero... |
| Gumbo1 | ❌ | - | - | - | Error: Return code non-zero... |
| Hacklemore2 | ❌ | - | - | - | Error: Return code non-zero... |
| Hacklemore3 | ❌ | - | - | - | Error: Return code non-zero... |
| HarmonicDivergence | ❌ | - | - | - | Error: Return code non-zero... |
| Heracles | ❌ | - | - | - | Error: Return code non-zero... |
| HyperStra_GSN_SMAOnly | ❌ | - | - | - | Error: Return code non-zero... |
| HyperStra_SMAOnly | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV5HOMod2 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ03HO | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV7 | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV8HO | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV8_original | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV8_original_ichiv2 | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV8_original_ichiv3 | ❌ | - | - | - | Error: Return code non-zero... |
| Elliotv8 | ❌ | - | - | - | Error: Return code non-zero... |
| FRAYSTRAT | ❌ | - | - | - | Error: Return code non-zero... |
| Fakebuy | ❌ | - | - | - | Error: Return code non-zero... |
| FastSupertrend | ❌ | - | - | - | Error: Return code non-zero... |
| FastSupertrendOpt | ❌ | - | - | - | Error: Return code non-zero... |
| FiveMinCrossAbove | ❌ | - | - | - | Error: Return code non-zero... |
| ElliotV5HOMod3 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ04 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ0407 | ❌ | - | - | - | Error: Return code non-zero... |
| INSIDEUP | ❌ | - | - | - | Error: Return code non-zero... |
| Ichi | ❌ | - | - | - | Error: Return code non-zero... |
| Ichimoku | ❌ | - | - | - | Error: Return code non-zero... |
| Ichimoku_SenkouSpanCross | ❌ | - | - | - | Error: Return code non-zero... |
| Ichimoku_v31 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ04_TSL4 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ06 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ07 | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ07Next | ❌ | - | - | - | Error: Return code non-zero... |
| GodStraNew | ❌ | - | - | - | Error: Return code non-zero... |
| BinClucMad | ❌ | - | - | - | Error: Return code non-zero... |
| BinClucMadDevelop | ❌ | - | - | - | Error: Return code non-zero... |
| BinClucMadSMADevelop | ❌ | - | - | - | Error: Return code non-zero... |
| BinClucMadV1 | ❌ | - | - | - | Error: Return code non-zero... |
| BuyAllSellAllStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| BuyOnly | ❌ | - | - | - | Error: Return code non-zero... |
| FrostAuraM21hStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| FrostAuraM315mStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| FrostAuraM31hStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| FrostAuraRandomStrategy | ❌ | - | - | - | Error: Return code non-zero... |
| GodCard | ❌ | - | - | - | Error: Return code non-zero... |
| BigZ07Next2 | ❌ | - | - | - | Error: Return code non-zero... |
