#!/bin/bash

# script: test-freqtrade.sh
# description: Wrapper script to run freqtrade commands via Docker
# usage: ./test-freqtrade.sh {download|backtest|backtest-gui} [args]
#        Use --timerange=YYYYMMDD-YYYYMMDD to specify backtest date range

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: docker could not be found. Please install docker."
    exit 1
fi

# Configuration
IMAGE_NAME="neozhou2009/freqtrade-full:latest"
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

# Function: Parse timerange from arguments
# Usage: TIMERANGE=$(parse_timerange "$@")
parse_timerange() {
    for arg in "$@"; do
        if [[ "$arg" == --timerange=* ]]; then
            echo "${arg#--timerange=}"
            return 0
        elif [[ "$arg" == "--timerange" ]]; then
            # Handle --timerange value (next argument)
            return 0
        fi
    done
    echo ""
}

# Function: Extract timerange value from arguments (handles both --timerange=VALUE and --timerange VALUE)
extract_timerange() {
    local found_timerange=false
    for arg in "$@"; do
        if [ "$found_timerange" = true ]; then
            echo "$arg"
            return 0
        fi
        if [[ "$arg" == "--timerange" ]]; then
            found_timerange=true
        elif [[ "$arg" == --timerange=* ]]; then
            echo "${arg#--timerange=}"
            return 0
        fi
    done
    echo ""
}

# Function: Convert timerange to start/end timestamps
# Input: 20210101-20210410 or 1624940400-1630447200
# Output: START_TIMESTAMP END_TIMESTAMP
parse_timerange_to_timestamps() {
    local timerange="$1"
    
    if [ -z "$timerange" ]; then
        echo ""
        return
    fi
    
    # Split by '-' (handle both formats: YYYYMMDD-YYYYMMDD or timestamp-timestamp)
    local start_date="${timerange%-*}"
    local end_date="${timerange#*-}"
    
    # If using YYYYMMDD format, convert to timestamp
    if [[ "$start_date" =~ ^[0-9]{8}$ ]]; then
        start_date=$(date -d "${start_date:0:4}-${start_date:4:2}-${start_date:6:2}" +%s 2>/dev/null || echo "")
    fi
    
    if [[ "$end_date" =~ ^[0-9]{8}$ ]]; then
        # For end date, use end of day
        end_date=$(date -d "${end_date:0:4}-${end_date:4:2}-${end_date:6:2} 23:59:59" +%s 2>/dev/null || echo "")
    fi
    
    if [ -n "$start_date" ] && [ -n "$end_date" ]; then
        echo "${start_date} ${end_date}"
    fi
}

# Function: Check if data exists for given pairs and timeframe
# Usage: check_data_exists "BTC/USDT:USDT,ETH/USDT:USDT" "5m" "timerange"
check_data_exists() {
    local pairs="$1"
    local timeframe="$2"
    local timerange="$3"
    local exchange="binance"
    local missing_pairs=()
    local incomplete_pairs=()
    
    # Convert timerange to timestamps if provided
    local timerange_ts=""
    if [ -n "$timerange" ]; then
        timerange_ts=$(parse_timerange_to_timestamps "$timerange")
    fi
    
    # Convert pairs to the format used in data directory (replace / with _ and : with _)
    # e.g., BTC/USDT:USDT -> BTC_USDT_USDT
    IFS=',' read -ra PAIR_ARRAY <<< "$pairs"
    
    for pair in "${PAIR_ARRAY[@]}"; do
        pair=$(echo "$pair" | xargs)
        pair_filename=$(echo "$pair" | tr '/' '_' | tr ':' '_')
        data_file="$DATA_DIR/${exchange}/futures/${pair_filename}-${timeframe}-futures.feather"
        
        if [ ! -f "$data_file" ]; then
            missing_pairs+=("$pair")
        elif [ -n "$timerange_ts" ]; then
            start_ts="${timerange_ts% *}"
            end_ts="${timerange_ts#* }"
            timerange_ok=0
            
            python3 -c "
import pandas as pd
import sys
try:
    df = pd.read_feather('$data_file')
    if 'date' not in df.columns:
        if 'datetime' in df.columns:
            df['date'] = df['datetime']
        else:
            sys.exit(1)
    df['date'] = pd.to_datetime(df['date'])
    file_start = int(df['date'].min().timestamp())
    file_end = int(df['date'].max().timestamp())
    start_ts = $start_ts
    end_ts = $end_ts
    # Check if file covers the timerange with 3-day tolerance (allow for minor gaps at edges)
    tolerance = 259200
    if file_start <= (start_ts + tolerance) and file_end >= (end_ts - tolerance):
        sys.exit(0)
    else:
        sys.exit(1)
except Exception:
    sys.exit(1)
" 2>&1
            if [ $? -eq 0 ]; then
                timerange_ok=1
            fi
            
            if [ $timerange_ok -eq 0 ]; then
                incomplete_pairs+=("$pair")
            fi
        fi
    done
    
    if [ ${#missing_pairs[@]} -eq 0 ] && [ ${#incomplete_pairs[@]} -eq 0 ]; then
        return 0  # All data exists and is complete
    else
        if [ ${#missing_pairs[@]} -gt 0 ]; then
            echo "Missing data for pairs: ${missing_pairs[*]}"
        fi
        if [ ${#incomplete_pairs[@]} -gt 0 ]; then
            echo "Incomplete timerange data for pairs: ${incomplete_pairs[*]}"
        fi
        return 1  # Missing or incomplete data
    fi
}

# Function: Auto-download data if needed
auto_download_data() {
    local pairs="$1"
    local timeframe="$2"
    local timerange="$3"
    local download_args="${4:-}"  
    
    echo "=========================================="
    echo "Checking if data exists for backtesting..."
    echo "  Pairs: $pairs"
    echo "  Timeframe: $timeframe"
    if [ -n "$timerange" ]; then
        echo "  Timerange: $timerange"
    fi
    echo "=========================================="
    
    if check_data_exists "$pairs" "$timeframe" "$timerange"; then
        echo "✓ Data already exists for all pairs. Proceeding with backtest."
        return 0
    else
        echo "⚠ Data not found or incomplete!"
        
        local pair_count=$(echo "$pairs" | tr ',' '\n' | wc -l)
        if [ -n "$timerange" ]; then
            echo "⚠ Timerange specified: will download $pair_count pairs with all timeframes (1m 5m 15m 1h 4h 1d)"
            echo "⚠ This may take several minutes..."
        fi
        
        echo "Starting data download..."
        
        local pairs_spaced=$(echo "$pairs" | tr ',' ' ')
        
        local timerange_args=""
        local timeframe_args="--timeframes $timeframe"
        
        if [ -n "$timerange" ]; then
            timerange_args="--timerange $timerange"
            timeframe_args="--timeframes 1m 5m 15m 1h 4h 1d"
            download_args="$download_args --erase"
        fi
        
        docker run --rm --workdir /freqtrade/user_data \
            -v "$USER_DATA_DIR:/freqtrade/user_data" \
            "$IMAGE_NAME" download-data \
            --userdir . \
            --exchange binance \
            $timeframe_args \
            -p $pairs_spaced \
            $timerange_args \
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
TIMEFRAME="5m"  
TIMERANGE=""
USER_PAIRS=""

# Try to get pairs from config file
if [ -f "$CONFIG_FILE" ]; then
    PAIRS=$(get_pairs_from_config "$CONFIG_FILE")
fi

# Extract -p/--pairs from command line to override config pairs
USER_PAIRS=""
prev_arg=""
for arg in "$@"; do
    if [[ "$prev_arg" == "-p" ]]; then
        USER_PAIRS="$arg"
        break
    elif [[ "$arg" == -p\ * ]]; then
        USER_PAIRS="${arg#-p }"
        break
    elif [[ "$prev_arg" == "--pairs" ]]; then
        USER_PAIRS="$arg"
        break
    elif [[ "$arg" == --pairs\ * ]]; then
        USER_PAIRS="${arg#--pairs }"
        break
    fi
    prev_arg="$arg"
done

# Use user-specified pairs if provided, otherwise use config pairs
if [ -n "$USER_PAIRS" ]; then
    PAIRS="$USER_PAIRS"
fi

TIMERANGE=$(extract_timerange "$@")

# Extract --timeframes from command line arguments
TIMEFRAMES=""
for arg in "$@"; do
    if [[ "$arg" == --timeframes=* ]]; then
        TIMEFRAMES="${arg#--timeframes=}"
        break
    elif [[ "$arg" == "--timeframes" ]]; then
        for next_arg in "$@"; do
            if [[ "$next_arg" != "--timeframes" ]]; then
                TIMEFRAMES="$next_arg"
                break
            fi
        done
        break
    fi
done

# Convert --timeframes to --timeframe for freqtrade compatibility
if [ -n "$TIMEFRAMES" ]; then
    set -- "${@//--timeframes=/--timeframe=}"
    set -- "${@//--timeframes /--timeframe }"
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

# Override TIMEFRAME if --timeframes was provided
if [ -n "$TIMEFRAMES" ]; then
    TIMEFRAME="$TIMEFRAMES"
fi

# Auto-download data for backtest commands
if [ "$CMD" == "backtest" ] || [ "$CMD" == "backtest-gui" ]; then
    if [ -n "$PAIRS" ]; then
        if [ -n "$TIMERANGE" ]; then
            auto_download_data "$PAIRS" "$TIMEFRAME" "$TIMERANGE" ""
        else
            auto_download_data "$PAIRS" "$TIMEFRAME" "$TIMERANGE" "--days 30"
        fi
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
        echo "  $0 backtest -c config.json --strategy MyStrategy --timerange=20210101-20210410"
        echo "  $0 backtest-gui -c config.json --strategy MyStrategy"
        exit 1
        ;;
esac
