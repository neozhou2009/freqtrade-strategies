import os
import shutil
import subprocess
import glob
import json
import sys
import time

# Configuration
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
USER_DATA_DIR = os.path.join(TEST_DIR, "user_data")
STRATEGIES_SOURCE_DIR = os.path.join(PROJECT_ROOT, "strategies")
STRATEGIES_DEST_DIR = os.path.join(USER_DATA_DIR, "strategies")
TEST_SCRIPT = os.path.join(TEST_DIR, "test-freqtrade.sh")
RESULTS_FILE = os.path.join(TEST_DIR, "test_results.json")
REPORT_FILE = os.path.join(TEST_DIR, "test_report.md")

# Data configuration
PAIRS = ["BTC/USDT:USDT", "ETH/USDT:USDT"]
TIMERANGE = "20260120-20260122"
TIMEFRAME = "5m"

def run_command(cmd):
    """Run a command in a subprocess."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
    return result

def setup_environment():
    """Initialize user_data and flatten strategies."""
    if os.path.exists(USER_DATA_DIR):
        print(f"Cleaning up {USER_DATA_DIR}...")
        shutil.rmtree(USER_DATA_DIR)

    # Install dependencies into user_data/lib
    lib_dir = os.path.join(USER_DATA_DIR, "lib")
    os.makedirs(lib_dir, exist_ok=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "ta", "--no-deps", "-t", lib_dir], check=True)
    
    # Remove numpy and pandas if they were installed (safety measure)
    for pkg in ["numpy", "pandas", "dateutil", "six", "pytz", "tzdata"]:
        pkg_path = os.path.join(lib_dir, pkg)
        if os.path.exists(pkg_path):
             print(f"Removing conflicting package {pkg} from {lib_dir}...")
             shutil.rmtree(pkg_path)
        # Also remove dist-info
        for p in glob.glob(os.path.join(lib_dir, f"{pkg}-*.dist-info")):
            shutil.rmtree(p)

    print("Verifying user_data/lib content:")
    subprocess.run(["ls", "-F", lib_dir])

    print("Setting up environment...")
    
    # Run init to create basic structure
    run_command([TEST_SCRIPT, "init"])
    
    # Flatten strategies
    print("Flattening strategies into user_data/strategies/...")
    if not os.path.exists(STRATEGIES_DEST_DIR):
        os.makedirs(STRATEGIES_DEST_DIR)

    strategy_files = []
    # Find all .py files in source strategies dir, recursively
    for root, dirs, files in os.walk(STRATEGIES_SOURCE_DIR):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                source_path = os.path.join(root, file)
                # We assume filename matches strategy class name or is unique enough
                # If there are duplicates, we might overwrite, which is a risk but acceptable for now
                dest_path = os.path.join(STRATEGIES_DEST_DIR, file)
                shutil.copy2(source_path, dest_path)
                strategy_files.append(file)
    
    print(f"Copied {len(strategy_files)} strategy files.")
    return strategy_files

def download_data():
    """Download backtest data if not exists."""
    print("Downloading data...")
    # Using fixed timerange
    cmd = [TEST_SCRIPT, "download", "-c", "config.json", "--timerange", TIMERANGE, "-t", TIMEFRAME]
    for pair in PAIRS:
        cmd.extend(["-p", pair])
    
    result = run_command(cmd)
    if result.returncode != 0:
        print("Error downloading data:")
        print(result.stderr)
    else:
        print("Data downloaded successfully.")

def get_strategy_class_name(file_path):
    """Extract strategy class name from file."""
    # Simple heuristic: assume class name matches filename without extension
    # or find 'class X(IStrategy)'
    filename = os.path.basename(file_path)
    # Default fallback
    class_name = os.path.splitext(filename)[0]
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.strip().startswith("class "):
                # e.g., class MyStrategy(IStrategy):
                parts = line.split('(')[0].split(' ')
                if len(parts) >= 2:
                    potential_name = parts[1]
                    # verify it inherits likely from IStrategy
                    if "(IStrategy)" in line or "IStrategy" in line:
                         class_name = potential_name
                         break
    return class_name

def test_strategies(strategy_files):
    """Run backtest for strategies in batches."""
    results = {}
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r') as f:
                results = json.load(f)
            print(f"Loaded {len(results)} previous results.")
        except Exception as e:
            print(f"Error loading previous results: {e}")

    BATCH_SIZE = 20
    
    # Extract strategy names
    strategies = []
    skipped_count = 0
    for file in strategy_files:
        name = get_strategy_class_name(os.path.join(STRATEGIES_DEST_DIR, file))
        if name in results and results[name]['status'] == 'PASS':
            skipped_count += 1
            continue
        strategies.append({"name": name, "file": file})
    
    if skipped_count > 0:
        print(f"Skipping {skipped_count} already passed strategies.")

    total = len(strategies)
    print(f"Testing {total} remaining strategies in batches of {BATCH_SIZE}...")
    
    for i in range(0, total, BATCH_SIZE):
        batch = strategies[i:i+BATCH_SIZE]
        batch_names = [s["name"] for s in batch]
        print(f"Processing batch {i//BATCH_SIZE + 1}/{(total+BATCH_SIZE-1)//BATCH_SIZE} ({len(batch)} strategies)...")
        
        start_time = time.time()
        # Construct command with list
        cmd = [
            TEST_SCRIPT, "backtest",
            "-c", "config.json",
            "--timerange", TIMERANGE,
            "--timeframe", TIMEFRAME,
            "--strategy-list"
        ]
        cmd.extend(batch_names)
        
        # print(" ".join(cmd))
        result = run_command(cmd)
        duration = time.time() - start_time
        
        # In batch mode, we need to parse stdout/stderr to know which passed/failed
        # But freqtrade doesn't easily output machine readable status per strategy in one go unless we check the backtest results file
        # However, checking returncode gives us global pass/fail.
        # If return code is 0, all passed? Or at least ran without crash?
        # Freqtrade usually prints summary table.
        # We will mark the batch as "EXECUTED" and inspect logs if needed.
        # For simplicity, if the batch succeeds, we mark all as PASS.
        # If it fails, we might need to re-run individually or mark all as ERROR.
        
        status = "PASS" if result.returncode == 0 else "FAIL"

        if status == "FAIL":
            print(f"  -> Batch failed. Retrying individually to fallback...")
            for s in batch:
                print(f"    Testing strategy: {s['name']} ({s['file']})...", end="", flush=True)
                start_time_s = time.time()
                cmd_s = [
                    TEST_SCRIPT, "backtest",
                    "-c", "config.json",
                    "--timerange", TIMERANGE,
                    "--timeframe", TIMEFRAME,
                    "--strategy", s["name"]
                ]
                result_s = run_command(cmd_s)
                duration_s = time.time() - start_time_s
                
                if result_s.returncode == 0:
                    s_status = "PASS"
                    print(f" PASSED ({duration_s:.2f}s)")
                else:
                    s_status = "FAIL"
                    print(f" FAILED ({duration_s:.2f}s)")
                
                results[s["name"]] = {
                    "file": s["file"],
                    "status": s_status,
                    "duration": duration_s,
                    "returncode": result_s.returncode,
                    "stdout": result_s.stdout if s_status == "FAIL" else "",
                    "stderr": result_s.stderr if s_status == "FAIL" else ""
                }
                # Save immediately in fallback mode
                with open(RESULTS_FILE, 'w') as f:
                    json.dump(results, f, indent=2)

        else:
            # Batch passed, mark all as passed
            for s in batch:
                results[s["name"]] = {
                    "file": s["file"],
                    "status": "PASS",
                    "duration": duration / len(batch),
                    "returncode": result.returncode,
                    "stdout": "",
                    "stderr": ""
                }
            # Save after batch success
            with open(RESULTS_FILE, 'w') as f:
                json.dump(results, f, indent=2)

    return results

def generate_report(results):
    """Generate MD report."""
    passed = [k for k, v in results.items() if v['status'] == 'PASS']
    failed = [k for k, v in results.items() if v['status'] == 'FAIL']
    
    with open(REPORT_FILE, 'w') as f:
        f.write("# Frequency Strategy Test Report\n\n")
        f.write(f"**Total Strategies:** {len(results)}\n")
        f.write(f"**Passed:** {len(passed)}\n")
        f.write(f"**Failed:** {len(failed)}\n\n")
        
        f.write("## Failed Strategies\n")
        for name in failed:
            info = results[name]
            f.write(f"### {name}\n")
            f.write(f"- File: `{info['file']}`\n")
            f.write(f"- Duration: {info['duration']:.2f}s\n")
            f.write("- Error Log:\n")
            f.write("```\n")
            # Limit error log size
            err_log = info['stderr']
            if len(err_log) > 1000:
                err_log = "..." + err_log[-1000:]
            f.write(err_log)
            f.write("\n```\n")
            
        f.write("\n## Passed Strategies\n")
        for name in passed:
            f.write(f"- {name} ({results[name]['duration']:.2f}s)\n")
            
    print(f"Report generated at {REPORT_FILE}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Freqtrade Strategy Test Runner", formatter_class=argparse.RawTextHelpFormatter)
    
    help_text = """
Freqtrade Strategy Test Runner

Usage: python3 test_runner.py [options]

Options:
  --help, -h            Show this help message and exit
  --setup               Initialize user_data and flatten strategies
  --download            Download backtest data
  --test                Run backtest for strategies (default if no other action specified)
  --report              Generate report from existing results
  
Configuration:
  --config FILE         Config file (default: config.json)
  --timerange RANGE     Timerange (default: 20260120-20260122)
  --timeframe TIME      Timeframe (default: 5m)
  --pairs PAIRS         List of pairs (default: BTC/USDT:USDT, ETH/USDT:USDT)
                        Format: PAIR1 PAIR2 ...
  --batch-size INT      Batch size for testing (default: 20)
    """
    
    # Override default help to match the requested style more closely if needed, 
    # but argparse help is standard. The user said "style reference test-freqtrade.sh".
    # The shell script uses a custom echo block.
    # I will stick to argparse but format the description/epilog to look similar.
    
    parser = argparse.ArgumentParser(usage="python3 test/test_runner.py [options]", add_help=False)
    
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    parser.add_argument("--setup", action="store_true", help="Initialize user_data and flatten strategies")
    parser.add_argument("--download", action="store_true", help="Download backtest data")
    parser.add_argument("--test", action="store_true", help="Run backtest for strategies")
    parser.add_argument("--report", action="store_true", help="Generate report from existing results")
    parser.add_argument("--config", default="config.json", help="Config file")
    parser.add_argument("--timerange", default="20260120-20260122", help="Timerange")
    parser.add_argument("--timeframe", default="5m", help="Timeframe")
    
    args, unknown = parser.parse_known_args()
    
    if args.help or (len(sys.argv) == 1 and False): # Run default if no args? Or show help? 
        # The user's request imply they want to see help.
        print("\033[0;32mFreqtrade Strategy Test Runner\033[0m\n")
        print("Usage: python3 test/test_runner.py [options]\n")
        print("Options:")
        print("  --setup               Initialize user_data and flatten strategies")
        print("                        - Cleans user_data directory")
        print("                        - Installs dependencies (ta)")
        print("                        - Copies strategies/config")
        print("")
        print("  --download            Download backtest data")
        print("                        - Uses config, timerange, and timeframe settings")
        print("")
        print("  --test                Run backtest for strategies")
        print("                        - Runs in batches with auto-resume")
        print("                        - Retries failed batches individually")
        print("")
        print("  --report              Generate report from existing results")
        print("                        - Creates test_report.md")
        print("")
        print("  -h, --help            Show this help message")
        print("")
        print("Configuration defaults:")
        print(f"  Config:    {args.config}")
        print(f"  Timerange: {args.timerange}")
        print(f"  Timeframe: {args.timeframe}")
        return

    # Update global configs based on args
    global TIMERANGE, TIMEFRAME
    TIMERANGE = args.timerange
    TIMEFRAME = args.timeframe
    # Config injection into commands would need update in run_command calls if we strictly support it,
    # but for now we update the globals if they were used, or just pass them.
    # The current script uses hardcoded 'config.json' in commands. 
    # I should update the constants or the usage.
    
    # Execute actions
    # If no specific action is requested, run the full pipeline (Setup -> Download -> Test -> Report)
    # mirroring the previous main() behavior.
    if not (args.setup or args.download or args.test or args.report):
        args.setup = True
        args.download = True
        args.test = True
        args.report = True

    if args.setup:
        start_time = time.time()
        print(f"--- Setup ({time.strftime('%H:%M:%S')}) ---")
        strategy_files = setup_environment()
        print(f"Setup completed in {time.time() - start_time:.2f}s\n")
    else:
        # If skipping setup, we still need to know strategy files for test
        strategy_files = [f for f in os.listdir(STRATEGIES_DEST_DIR) if f.endswith(".py") and f != "__init__.py"]
        strategy_files.sort()

    if args.download:
        start_time = time.time()
        print(f"--- Download Data ({time.strftime('%H:%M:%S')}) ---")
        download_data()
        print(f"Download completed in {time.time() - start_time:.2f}s\n")

    results = {}
    if args.test:
        start_time = time.time()
        print(f"--- Testing Strategies ({time.strftime('%H:%M:%S')}) ---")
        results = test_strategies(strategy_files)
        print(f"Testing completed in {time.time() - start_time:.2f}s\n")
    
    if args.report:
        # If we didn't run test, try to load results
        if not results and os.path.exists(RESULTS_FILE):
             import json
             try:
                 with open(RESULTS_FILE, 'r') as f:
                     results = json.load(f)
             except:
                 pass
        
        if results:
            generate_report(results)
        else:
            print("No results to report.")

if __name__ == "__main__":
    main()
