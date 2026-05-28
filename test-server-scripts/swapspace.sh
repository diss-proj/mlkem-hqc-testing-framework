# Run this before build.sh if you're on a device with low (<4GB) memory.
#! /bin/bash
if [ -f /swapfile ]; then
    echo "swapfile already exists"
    exit 1
fi

# https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-20-04
# ^ from this
sudo dd if=/dev/zero of=/swapfile bs=2M count=1024 status=progress
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo "Swap Space:"
sudo swapon --show

