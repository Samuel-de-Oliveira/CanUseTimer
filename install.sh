#!/bin/bash

echo "The installing starts!"
# install keyboard library and pip if don't have
echo "Installing libraries"
if [ -f '/etc/debian_version' ]; then # Debian based distribuition
    sudo apt install python3-pip -y
    sudo pip3 install keyboard
elif [ -f '/etc/arch-release' ]; then # Arch based distribuition
    sudo pacman -Syy python-pip
    sudo pip install keyboard
else # if your Linux distro is not supported exit
    echo "Your linux distribuition is not supported, sorry. :("
    exit 1
fi

echo "Creating executer..."
sudo cp lib/canusetimer-terminal /bin/

echo "Creting directories and files..."
if [ ! -d /opt/CanUseTimer-Terminal ]; then
    sudo mkdir /opt/CanUseTimer-Terminal
fi
sudo cp *.py /opt/CanUseTimer-Terminal/
sudo cp -rf lib/ /opt/CanUseTimer-Terminal/

echo "Everything is done!"