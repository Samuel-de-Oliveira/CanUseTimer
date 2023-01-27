#!/usr/bin/env bash
#-*------------------ The CanUseTimer Uninstaller ------------------*-#

clear
echo -e "\033[1mUninstall program...\033[m"
echo -e "\nEverything into /opt/CanUseTimer will be removed, are you sure about this? [Y/n]"; read num
clear

if [ $num == 'y' ] || [ $num == 'Y' ]; then

	echo -e "\nRemoving the program...\n"

	if [ -f /usr/bin/canusetimer ]; then
		echo "Removing executer..."
    		sudo rm /usr/bin/canusetimer
	fi
	if [ -d /opt/CanUseTimer/ ]; then
		echo "Removing directory..."
    		sudo rm -rf /opt/CanUseTimer/
	fi
	echo -e "\nEverything is removed!\n"
	echo -e "\033[34;1mPress return to exit...\033[m"; read
	clear
fi
