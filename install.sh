#!/usr/bin/env bash
# -*-- Installer for GNU/Linux --*- #

echo -e "\ninstalling... This will not take long.\n"

if [ ! -d /usr/share/CanUseTimer/ ]; then
	echo "Creating main directory..."
	mkdir -p /usr/share/CanUseTimer/
fi

echo "Moving binary..."
mv canusetimer /usr/share/CanUseTimer/
	
echo "Creating executer..."
cp linux_assets/executer.sh /usr/bin/canusetimer

echo -e "\nDone!\n"
