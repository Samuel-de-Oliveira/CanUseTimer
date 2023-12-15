#!/usr/bin/env bash
#-*------------------ CanUseTimer Uninstaller ------------------*-#

clear
echo -e "\033[1mUninstall program...\033[m"

if [ -f /usr/bin/canusetimer ]; then
	echo "Removing executer..."
  rm /usr/bin/canusetimer
fi
if [ -d /opt/CanUseTimer/ ]; then
	echo "Removing directory..."
  rm -rf /opt/CanUseTimer/
fi

echo -e "\nEverything is removed!\n"
echo -e "\033[34;1mPress return to exit...\033[m"; read
clear
