#!/bin/bash
#-*------------------ The CanUseTimer Uninstaller ------------------*-#

echo -e "\nEverything in /opt/CanUseTimer-Terminal will be removed, are you sure? [Y/n]"; read num

if [ $num == 'y' ] || [ $num == 'Y' ]; then

	# The script only remove the CanUseTimer-Terminal directory from /opt/ and executer from /bin/

	echo -e "\nRemoving the program...\n"

	if [ -f /usr/bin/canusetimer-terminal ]; then
		echo "Removing executer..."
    		sudo rm /usr/bin/canusetimer-terminal
	fi
	if [ -d /opt/CanUseTimer-Terminal/ ]; then
		echo "Removing directory..."
    		sudo rm -rf /opt/CanUseTimer-Terminal/
	fi
	echo -e "\nEverything is removed!\n"

else
       	echo "Abort!"
fi
