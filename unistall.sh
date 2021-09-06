#!/bin/bash

echo "Everything in /opt/canUseTimer-Terminal will be removed, are you sure? [Y/n]"; read num

if [ $num == 'y' ] || [$num == 'Y']; then
echo -e "Removing the program..."

if [ -f /bin/canusetimer-terminal ]; then
    sudo rm /bin/canusetimer-terminal # removing executer.
fi
if [ -d /opt/CanUseTimer-Terminal/ ]; then
    sudo rm -rf /opt/CanUseTimer-Terminal/ # removing program directory.
fi
echo "Everything is removed!"
else
echo "Abort!"
fi
