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

# Check if we are in the correct directory (optional safety check)
# if [ ! -f "$USER_DATA_DIR/config.json" ]; then
#     echo "Warning: config.json not found in $USER_DATA_DIR. Make sure you are in the correct directory."
# fi

# Check argument for help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    CMD="help"
else
    CMD=$1
    shift
fi

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Help function
show_help() {
    echo -e "${GREEN}Freqtrade Test Helper Script${NC}"
    echo ""
    echo "Usage: $0 {command} [process_options]"
    echo ""
    echo "Commands:"
    echo "  init          Initialize user_data directory and copy config/strategies"
    echo "                - Creates user_data directory"
    echo "                - Copies config.json, strategies/, hyperopts/, notebooks/"
    echo ""
    echo "  download      Download data (wrapper for 'freqtrade download-data')"
    echo "                Example: $0 download -c config.json --days 30 -t 5m"
    echo ""
    echo "  list-data     List downloaded data (wrapper for 'freqtrade list-data')"
    echo "                Example: $0 list-data -c config.json"
    echo ""
    echo "  backtest      Run backtesting (wrapper for 'freqtrade backtesting')"
    echo "                Example: $0 backtest -c config.json --strategy SampleStrategy"
    echo ""
    echo "  backtest-gui  Run backtesting and start FreqUI webserver"
    echo "                - Runs backtest first to generate results"
    echo "                - Starts webserver on http://localhost:9080"
    echo "                Example: $0 backtest-gui -c config.json --strategy SampleStrategy"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo ""
    exit 0
}

case "$CMD" in
    init)
        echo -e "${GREEN}Initializing user_data directory...${NC}"
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
        
        echo -e "${GREEN}Initialization complete.${NC}"
        ;;
    download)
        echo -e "${YELLOW}Running: freqtrade download-data $@${NC}"
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" -e PYTHONPATH=/freqtrade/user_data/lib "$IMAGE_NAME" download-data --userdir . "$@"
        ;;
    list-data)
        echo -e "${YELLOW}Running: freqtrade list-data $@${NC}"
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" -e PYTHONPATH=/freqtrade/user_data/lib "$IMAGE_NAME" list-data --userdir . "$@"
        ;;
    backtest)
        echo -e "${YELLOW}Running: freqtrade backtesting $@${NC}"
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" -e PYTHONPATH=/freqtrade/user_data/lib "$IMAGE_NAME" backtesting --userdir . "$@"
        ;;
    backtest-gui)
        echo -e "${YELLOW}Running: freqtrade backtesting (to generate results for UI)...${NC}"
        # 1. Run backtesting to generate the results in user_data/backtest_results/
        docker run --rm --workdir /freqtrade/user_data -v "$USER_DATA_DIR:/freqtrade/user_data" -e PYTHONPATH=/freqtrade/user_data/lib "$IMAGE_NAME" backtesting --userdir . "$@"
        
        if [ $? -eq 0 ]; then
            echo "------------------------------------------------------------"
            echo -e "${GREEN}Starting Freqtrade WebServer (FreqUI)...${NC}"
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
    help)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
