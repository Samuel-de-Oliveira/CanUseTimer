#!/usr/bin/env sh
## CanUseTimer executer
if [ $USER == "root" ]; then
	echo "Please start it with your normal user..."
	exit 1
fi

cd /usr/share/CanUseTimer/
sudo ./canusetimer
