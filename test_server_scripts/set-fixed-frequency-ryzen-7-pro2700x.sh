#! /bin/bash

echo 'disabling boost...'
echo '0' | sudo tee /sys/devices/system/cpu/cpufreq/boost
echo 'done.'

echo 'Setting min frequency...'
sudo cpupower frequency-set -g userspace
sudo cpupower frequency-set -u 2.20Ghz
sudo cpupower frequency-set -f 2.20Ghz
echo 'done.'

echo 'verify output:'
sudo cpupower frequency-info
