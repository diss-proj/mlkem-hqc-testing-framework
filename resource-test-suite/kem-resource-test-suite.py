###### Imports
from tqdm import tqdm # progress bars
from time import sleep
import os
import pandas as pd
import subprocess
from datetime import datetime, timezone

###### Globals
TIMER_FORMAT = '{l_bar}{bar}| {n_fmt}/{total_fmt}s' # for nice tqdm timer
KEMS = [
    'HQC-128', 'HQC-192', 'HQC-256', 
    'ML-KEM-512', 'ML-KEM-768', 'ML-KEM-1024'
]
TEST_TIMESTAMP = datetime.now(timezone.utc).strftime("%G-%m-%d-%H:%M:%S:%f")
SPEEDTEST_DURATION = 30

###### Check Environment
#if os.geteuid() != 0:
#    print("This test suite must be run as root!")
#    exit(1)

if not os.path.isdir('./_build'):
    print("You must build the project's libraries with build.sh" + 
    "\n before running this test suite.")
    exit(1)

##### Create Results Directory
SERVER_NAME = input("Name of test server:\n> ")
RESULTS_PATH = f"./resource-test-results/{SERVER_NAME}-{TEST_TIMESTAMP}/"

os.makedirs(RESULTS_PATH)


######################### SPEED TEST #########################################

### Warmup

# To ensure that earlier KEMs don't run faster because the CPU hasn't 
# thermal throttled yet, it's important to "warm up" the CPU.

CPU_COUNT = os.cpu_count()

print("# Warming up the CPU")
subprocess.run(["stress-ng", "--cpu", f"{CPU_COUNT}", "--timeout", "60"])

### To store the results
speed_results_dict = {
    "KEM": [],
    "KeyGen Cost Mean": [],
    "KeyGen Cost StdDev": [],
    "KeyGen Time Mean": [],
    "KeyGen Time StdDev": [],
    "Encaps Cost Mean": [],
    "Encaps Cost StdDev": [],
    "Encaps Time Mean": [],
    "Encaps Time StdDev": [],
    "Decaps Cost Mean": [],
    "Decaps Cost StdDev": [],
    "Decaps Time Mean": [],
    "Decaps Time StdDev": [],
}

### Functions to add the results of each test to the dataframe.
def process_line(line: str):
    values = line.split("|")
    dictionary = {
        "time mean": float(values[3]),
        "time stddev": float(values[4]),
        "cost mean": float(values[5]),
        "cost stddev": float(values[6])
    }
    return dictionary

def store_speedtest_results(KEM: str, output: str):
    lines = output.split("\n")
    for line in lines:
        if line.startswith("keygen"):
            keygen = process_line(line)
        if line.startswith("encaps"):
            encaps = process_line(line)
        if line.startswith("decaps"):
            decaps = process_line(line)
    speed_results_dict["KEM"].append(KEM)
    speed_results_dict["KeyGen Cost Mean"].append(keygen["cost mean"])
    speed_results_dict["KeyGen Cost StdDev"].append(keygen["cost stddev"])
    speed_results_dict["KeyGen Time Mean"].append(keygen["time mean"])
    speed_results_dict["KeyGen Time StdDev"].append(keygen["time stddev"])
    speed_results_dict["Encaps Cost Mean"].append(encaps["cost mean"])
    speed_results_dict["Encaps Cost StdDev"].append(encaps["cost stddev"])
    speed_results_dict["Encaps Time Mean"].append(encaps["time mean"])
    speed_results_dict["Encaps Time StdDev"].append(encaps["time stddev"])
    speed_results_dict["Decaps Cost Mean"].append(decaps["cost mean"])
    speed_results_dict["Decaps Cost StdDev"].append(decaps["cost stddev"])
    speed_results_dict["Decaps Time Mean"].append(decaps["time mean"])
    speed_results_dict["Decaps Time StdDev"].append(decaps["time stddev"])
    

### Run speed tests
with tqdm(KEMS,
    bar_format="{l_bar}{bar}| KEM {n_fmt}/{total_fmt}") as pbar:
    for KEM in pbar:
        pbar.set_description(f"Testing {KEM}")
        result = subprocess.run(
            ["./_build/liboqs/build/tests/speed_kem", "-d", f"{SPEED_TEST_DURATION}", KEM],
            capture_output=True
        )
        store_speedtest_results(KEM, result.stdout.decode())

speed_results = pd.DataFrame(speed_results_dict)
print(speed_results.head(6))

### Write results to file
with open(f"{RESULTS_PATH}/kem_speed.csv", "w") as results_file:
    speed_results.to_csv(results_file, index=False)

######################### MEMORY USAGE TEST ##################################

keygen_memory_usage = {}


for KEM in KEMS:
    # Test KeyGen Usage
    keygen_batch_times = []
    with tqdm(total=1000,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} samples",
        desc=f"Testing {KEM} KeyGen"
    ) as pbar:
        for sample in range(1000):
            result = subprocess.run([
                    "/usr/bin/time",
                    "-f",
                    "%M",
                    "./_build/liboqs/build/tests/test_kem_mem",
                    KEM,
                    "0"], 
                    capture_output=True
            )
            keygen_batch_times.append(
                int(result.stderr.decode())
            )
            pbar.update(1)
    # Write results to file
    with open(f"{RESULTS_PATH}/{KEM}_keygen_memory.csv", "w") as output_file:
        keygen_results = pd.DataFrame({"Memory Usage": keygen_batch_times})
        keygen_results.to_csv(output_file, index=False)
        
    # Test Encaps Usage
    encaps_batch_times = []
    with tqdm(total=1000,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} samples",
        desc=f"Testing {KEM} Encaps"
    ) as pbar:
        for sample in range(1000):
            result = subprocess.run([
                    "/usr/bin/time",
                    "-f",
                    "%M",
                    "./_build/liboqs/build/tests/test_kem_mem",
                    KEM,
                    "1"], 
                    capture_output=True
            )
            encaps_batch_times.append(
                int(result.stderr.decode())
            )
            pbar.update(1)
    # Write results to file
    with open(f"{RESULTS_PATH}/{KEM}_encaps_memory.csv", "w") as output_file:
        encaps_results = pd.DataFrame({"Memory Usage": encaps_batch_times})
        encaps_results.to_csv(output_file, index=False)

    # Test Decaps Usage
    decaps_batch_times = []
    with tqdm(total=1000,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} samples",
        desc=f"Testing {KEM} Decaps"
    ) as pbar:
        for sample in range(1000):
            result = subprocess.run([
                    "/usr/bin/time",
                    "-f",
                    "%M",
                    "./_build/liboqs/build/tests/test_kem_mem",
                    KEM,
                    "2"], 
                    capture_output=True
            )
            decaps_batch_times.append(
                int(result.stderr.decode())
            )
            pbar.update(1)
    # Write results to file
    with open(f"{RESULTS_PATH}/{KEM}_decaps_memory.csv", "w") as output_file:
        decaps_results = pd.DataFrame({"Memory Usage": decaps_batch_times})
        decaps_results.to_csv(output_file, index=False)



