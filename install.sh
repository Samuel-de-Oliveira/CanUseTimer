#!/bin/bash

echo "The installing starts..."
# install keyboard library and pip if don't have
apt install python3-pip
pip3 install keyboard

# copping canusetimer executer
chmod a+wrx lib/canusetimer
cp lib/canusetimer /bin/

# Creating CanUsetimer directory and copping files
mkdir /opt/CanUseTimer
cp Main.py /opt/CanUseTimer/
cp winConf.py /opt/CanUseTimer/
cp -rf lib/ /opt/CanUseTimer/

echo "Done."