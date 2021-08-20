#!/bin/bash

echo "Removing the program..."
sudo pip3 uninstall keyboard # unistalling keyboard library.
if [ -f /bin/canusetimer-terminal ]; then
    sudo rm /bin/canusetimer-terminal # removing executer.
fi
if [ -d /opt/CanUseTimer-Terminal/ ]; then
    sudo rm -rf /opt/CanUseTimer-Terminal/ # removing program directory.
fi
echo "Everything is removed!"
