#!/bin/bash

echo "The installing starts..."
# install keyboard library and pip if don't have
if [ -f '/etc/debian_version' ]; then # Debian based distribuition
    sudo apt install python3-pip
    sudo pip3 install keyboard
elif [ -f '/etc/arch-release' ]; then # Arch based distribuition
    sudo pacman -Syu python-pip
    sudo pip3 install keyboard
else # if your Linux distro is not supported exit
    echo "Your linux distribuition is not supported, sorry. :("
    exit 1
fi

echo "Creating executer..."
sudo cp lib/canusetimer-terminal /bin/

echo "Creting directories and files..."
if [ ! -d /opt/CanUseTimer-terminal ]; then
    sudo mkdir /opt/CanUseTimer-terminal
fi
sudo cp *.py /opt/CanUseTimer-terminal/
sudo cp -rf lib/ /opt/CanUseTimer-terminal/

echo "Everything is done!"