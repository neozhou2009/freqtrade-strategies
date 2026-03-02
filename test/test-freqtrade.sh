#!/bin/bash

# script: test-freqtrade.sh
# description: Wrapper script to run freqtrade commands via Docker
# usage: ./test-freqtrade.sh {download|backtest|backtest-gui} [args]

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: docker could not be found. Please install docker."
    exit 1
fi

# Configuration
IMAGE_NAME="freqtradeorg/freqtrade:stable"
# Mount the user_data directory inside the container
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_DATA_DIR="$BASE_DIR/user_data"
DATA_DIR="$USER_DATA_DIR/data"

# Default config file
CONFIG_FILE="$BASE_DIR/config.json"

# Check if we are in the correct directory (optional safety check)
# if [ ! -f "$USER_DATA_DIR/config.json" ]; then
#     echo "Warning: config.json not found in $USER_DATA_DIR. Make sure you are in the correct directory."
# fi

# Function: Check if data exists for given pairs and timeframe
# Usage: check_data_exists "BTC/USDT:USDT,ETH/USDT:USDT" "5m"
check_data_exists() {
    local pairs="$1"
    local timeframe="$2"
    local exchange="binance"
    local missing_pairs=()
    
    # Convert pairs to the format used in data directory (replace / with _ and : with _)
    # e.g., BTC/USDT:USDT -> BTC_USDT_USDT
    IFS=',' read -ra PAIR_ARRAY <<< "$pairs"
    
    for pair in "${PAIR_ARRAY[@]}"; do
        # Trim whitespace
        pair=$(echo "$pair" | xargs)
        
        # Convert pair format for filename: BTC/USDT:USDT -> BTC_USDT_USDT
        pair_filename=$(echo "$pair" | tr '/' '_' | tr ':' '_')
        
        # Check if parquet file exists for this pair
        local data_file="$DATA_DIR/${exchange}/${pair_filename}-${timeframe}.parquet"
        
        if [ ! -f "$data_file" ]; then
            missing_pairs+=("$pair")
        fi
    done
    
    if [ ${#missing_pairs[@]} -eq 0 ]; then
        return 0  # All data exists
    else
        echo "Missing data for pairs: ${missing_pairs[*]}"
        return 1  # Missing data
    fi
}

# Function: Auto-download data if needed
auto_download_data() {
    local pairs="$1"
    local timeframe="$2"
    local download_args="${3:-}"  # Optional additional args
    
    echo "=========================================="
    echo "Checking if data exists for backtesting..."
    echo "  Pairs: $pairs"
    echo "  Timeframe: $timeframe"
    echo "=========================================="
    
    if check_data_exists "$pairs" "$timeframe"; then
        echo "✓ Data already exists for all pairs. Proceeding with backtest."
        return 0
    else
        echo "⚠ Data not found or incomplete!"
        echo "Starting data download..."
        
        # Parse pairs for download-data command (convert BTC/USDT:USDT to BTC/USDT:USDT)
        # download-data expects pairs without the :USDT suffix for futures in some cases
        # But let's try with the full pair first
        local pair_args=""
        IFS=',' read -ra PAIR_ARRAY <<< "$pairs"
        for pair in "${PAIR_ARRAY[@]}"; do
            pair=$(echo "$pair" | xargs)
            pair_args="$pair_args -p $pair"
        done
        
        # Run download
        docker run --rm --workdir /freqtrade/user_data \
            -v "$USER_DATA_DIR:/freqtrade/user_data" \
            "$IMAGE_NAME" download-data \
            --userdir . \
            --exchange binance \
            --timeframes "$timeframe" \
            $pair_args \
            $download_args
        
        if [ $? -eq 0 ]; then
            echo "✓ Data download completed."
            return 0
        else
            echo "✗ Data download failed!"
            return 1
        fi
    fi
}

# Function: Extract pairs from config file
get_pairs_from_config() {
    local config_file="$1"
    
    if [ -f "$config_file" ]; then
        # Use python to parse JSON and extract pairs
        python3 -c "
import json
import sys
try:
    with open('$config_file', 'r') as f:
        config = json.load(f)
    pairs = config.get('exchange', {}).get('pair_whitelist', [])
    print(','.join(pairs))
except Exception as e:
    print('')
" 2>/dev/null
    fi
}

# Function: Extract timeframe from strategy file
get_timeframe_from_strategy() {
    local strategy_file="$1"
    
    if [ -f "$strategy_file" ]; then
        python3 -c "
import re
try:
    with open('$strategy_file', 'r') as f:
        content = f.read()
    # Match timeframe = "5m" or timeframe = '5m'
    match = re.search(r'timeframe\s*=\s*[\"\'](\w+)[\"\']', content)
    if match:
        print(match.group(1))
except:
    pass
" 2>/dev/null
    fi
}

CMD=$1
shift

# Parse common arguments to find config and strategy
PAIRS=""
TIMEFRAME="5m"  # default

# Try to get pairs from config file
if [ -f "$CONFIG_FILE" ]; then
    PAIRS=$(get_pairs_from_config "$CONFIG_FILE")
fi

# Try to get timeframe from strategy (if specified in args)
for arg in "$@"; do
    if [[ "$arg" == *"--strategy"* ]]; then
        # Extract strategy name
        strategy_name=$(echo "$arg" | cut -d'=' -f2 || echo "$2")
        if [ -n "$strategy_name" ] && [ "$strategy_name" != "$arg" ]; then
            :
        else
            strategy_name="$2"
        fi
        
        # Look for strategy file
        for sf in "$USER_DATA_DIR/strategies/"*.py; do
            if [ -f "$sf" ]; then
                tf=$(get_timeframe_from_strategy "$sf")
                if [ -n "$tf" ]; then
                    TIMEFRAME="$tf"
                    break
                fi
            fi
        done
        break
    fi
done

# Auto-download data for backtest commands
if [ "$CMD" == "backtest" ] || [ "$CMD" == "backtest-gui" ]; then
    if [ -n "$PAIRS" ]; then
        auto_download_data "$PAIRS" "$TIMEFRAME" "--days 30"
    else
        echo "Warning: Could not determine pairs from config. Skipping data check."
    fi
fi

case "$CMD" in
    init)
        echo "Initializing user_data directory..."
        # Create user_data directory if it doesn't exist to prevent permission issues
        mkdir -p "$USER_DATA_DIR"
        
        # Run create-userdir to generate standard structure
        docker run --rm -v "$USER_DATA_DIR:/freqtrade/user_data" "$IMAGE_NAME" create-userdir --userdir /freqtrade/user_data
        
        # Copy custom files
        echo "Copying custom config and strategies..."
        [ -f "$BASE_DIR/config.json" ] && cp "$BASE_DIR/config.json" "$USER_DATA_DIR/"
        [ -d "$BASE_DIR/strategies" ] && cp -r "$BASE_DIR/strategies/"* "$USER_DATA_DIR/strategies/"
        [ -d "$BASE_DIR/hyperopts" ] && cp -r "$BASE_DIR/hyperopts/"* "$USER_DATA_DIR/hyperopts/"
        [ -d "$BASE_DIR/notebooks" ] && cp -r "$BASE_DIR/notebooks/"* "$USER_DATA_DIR/notebooks/"
        
        echo "Initialization complete."
        ;;
    download)
        echo "Running: freqtrade download-data $@"
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" "$IMAGE_NAME" download-data --userdir . "$@"
        ;;
    list-data)
        echo "Running: freqtrade list-data $@"
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" "$IMAGE_NAME" list-data --userdir . "$@"
        ;;
    backtest)
        echo "Running: freqtrade backtesting $@"
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" "$IMAGE_NAME" backtesting --userdir . "$@"
        ;;
    backtest-gui)
        echo "Running: freqtrade backtesting (to generate results for UI)..."
        # 1. Run backtesting to generate the results in user_data/backtest_results/
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" "$IMAGE_NAME" backtesting --userdir . "$@"
        
        if [ $? -eq 0 ]; then
            echo "------------------------------------------------------------"
            echo "Starting Freqtrade WebServer (FreqUI)..."
            echo "Open http://localhost:9080/ in your browser."
            echo "Login with the credentials in config.json:"
            echo "  Username: freqtrader"
            echo "  Password: 123456"
            echo "Press Ctrl+C to stop the server."
            echo "------------------------------------------------------------"
            
            # 2. Start the webserver. 
            # Note: config.json sets listen_port to 8080, so we map 9080(host) -> 8080(container).
            docker run --rm -it -p 9080:8080 \
                --name freqtrade-webserver \
                --workdir /freqtrade/user_data \
                -v "$USER_DATA_DIR:/freqtrade/user_data" \
                "$IMAGE_NAME" \
                webserver --userdir . -c config.json
        fi
        ;;
    *)
        echo "Usage: $0 {init|download|list-data|backtest|backtest-gui} [freqtrade_options]"
        echo "Examples:"
        echo "  $0 init"
        echo "  $0 download -c config.json --days 30 -t 5m"
        echo "  $0 list-data -c config.json"
        echo "  $0 backtest -c config.json --strategy MyStrategy"
        echo "  $0 backtest-gui -c config.json --strategy MyStrategy"
        exit 1
        ;;
esac
