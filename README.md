# Freqtrade Strategies Repository

This repository is dedicated to sharing open-source trading strategies for the Freqtrade cryptocurrency trading bot. We encourage contributors to help keep these strategies up to date with the latest Freqtrade versions and to add new strategies to benefit the community.

## About Freqtrade

[Freqtrade](https://www.freqtrade.io/) is an open-source cryptocurrency trading bot that allows users to create, backtest, and execute trading strategies on various cryptocurrency exchanges.

## Getting Started

### Prerequisites

Before you start contributing to this project, ensure you have the following:

- [Freqtrade](https://www.freqtrade.io/) installed on your machine.
- Basic knowledge of Python and Freqtrade.
- Familiarity with version control using Git.
- Docker (for testing strategies with TA-Lib dependency)

## Docker Setup for TA-Lib Strategies

Many strategies in this repository require the TA-Lib library for technical analysis indicators. We provide a pre-configured Docker image with TA-Lib installed.

### Building the TA-Lib Docker Image

```bash
# Build the Docker image with TA-Lib support
docker build -f Dockerfile.freqtrade-talib -t freqtrade-talib:latest .
```

### Using the TA-Lib Docker Image

```bash
# Test a strategy with TA-Lib dependency
docker run --rm \
  -v $(pwd)/test:/work/freqtrade_test \
  -v $(pwd)/strategies:/work/freqtrade_test/user_data/strategies \
  freqtrade-talib:latest \
  backtesting --strategy BB_RSI --timerange 20250101-20250301

# List all available strategies
docker run --rm \
  -v $(pwd)/strategies:/work/freqtrade_test/user_data/strategies \
  freqtrade-talib:latest \
  list-strategies

# Verify TA-Lib installation
docker run --rm freqtrade-talib:latest python -c "import talib; print(talib.__version__)"
```

### Dockerfile Details

The `Dockerfile.freqtrade-talib` contains:
```dockerfile
FROM freqtradeorg/freqtrade:stable
RUN pip install TA-Lib
```

This image extends the official Freqtrade stable image and installs TA-Lib for technical analysis calculations.

### Strategies Requiring TA-Lib

Strategies that use TA-Lib functions (like SMA, RSI, MACD, etc.) should use the `freqtrade-talib` Docker image for testing. Examples include:
- BB_RSI
- SuperTrendPure
- ADXMomentum
- And many more (see `ALL_STRATEGIES_FIX_PLAN.md` for complete list)
