#!/bin/bash

sudo apt-get install build-essential libssl-dev
sudo apt-get install yasm libgmp-dev libpcap-dev libnss3-dev libkrb5-dev pkg-config libbz2-dev zlib1g-dev

mkdir ~/src
cd ~/src
git clone git://github.com/magnumripper/JohnTheRipper -b bleeding-jumbo john
cd ~/src/john/src
./configure && make -s clean && make -sj4
sudo ln -s ~/src/JohnTheRipper/run/john /usr/bin/john
