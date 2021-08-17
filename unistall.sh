#!/bin/bash

echo "Removing the program..."
if [ -f /bin/canusetimer-terminal ]; then
    sudo rm /bin/canusetimer-terminal
fi
if [ -d /opt/CanUseTimer-terminal/ ]; then
    rm -rf /opt/CanUseTimer-terminal/
fi
echo "Everything is removed!"