#!/bin/bash

echo "The installing starts..."

# install keyboard library and pip if don't have
if [ -f '/etc/debian_version' ]; then
    apt install python3-pip
    pip3 install keyboard
elif [ -f '/etc/arch-release' ]; then
    pacman -Syu python-pip
    pip3 install keyboard
else # if your Linux distro is not supported exit
    echo "Your linux distribuition is not supported, sorry..."
    exit 1
fi

# copping canusetimer executer
chmod a+wrx lib/canusetimer
cp lib/canusetimer /bin/

# Creating CanUsetimer directory and copping files
if [ ! -d /opt/CanUseTimer ]; then
    mkdir /opt/CanUseTimer
fi
cp *.py /opt/CanUseTimer/
cp -rf lib/ /opt/CanUseTimer/

echo "Everything is done!"