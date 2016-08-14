#!/bin/sh
#
# This script will uninstall your current glpk, install glpk build dependencies
# and then build glpk 4.4.7 and pyglpk-0.3
#
# Brett G. Olivier, July 2016
##############################################

# grab the source repository
git clone https://github.com/bgoli/cbmpy-glpk.git
cd cbmpy-glpk

# install glpk
cd glpk-4.47
sudo apt-get -y purge glpk
sudo apt-get -y install libgmp-dev
./configure --with-gmp
make
make check
sudo make install
sudo ldconfig

# install pyglpk
cd ../pyglpk-0.3
make
sudo make install

