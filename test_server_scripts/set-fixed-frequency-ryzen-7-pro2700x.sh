#! /bin/bash

echo 'Disabling boost...'
echo '0' | sudo tee /sys/devices/system/cpu/cpufreq/boost
echo 'Done.'

echo 'Setting min frequency...'
sudo cpupower frequency-set -g userspace
sudo cpupower frequency-set -u 2.20Ghz
sudo cpupower frequency-set -f 2.20Ghz
echo 'Done.'

echo 'Disabling hyperthreading...'
echo 'off' | sudo tee /sys/devices/system/cpu/smt/control
if [ "$(cat /sys/devices/system/cpu/smt/active)" != "0" ]; then
    echo 'Error! Failed to disable SMT'
else
    echo 'Done.'
fi


echo 'Verify output:'
sudo cpupower frequency-info
