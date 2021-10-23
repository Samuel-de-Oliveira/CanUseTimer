#!/usr/bin/env bash
#-*-------------- The installer for GNU/Linux --------------*-#

clear
echo -e "\nThis program will install the following packages:\n\
CanUseTimer-Terminal, keyboard_python_lib"
echo -e "and will create a folder in /opt/"
echo -e "\nEstimated space used: 100Kb\nVersion of Program: \033[33m0.2.1 BETA\033[m\nAre you sure you want to install? [Y/n]:"; read num
clear 

if [ $num == 'y' ] || [ $num == 'Y' ]; then

	# The program only move the python files to /opt/ and create a executer in /bin/
	# Is more simple than you think
	echo -e "\nThe installing starts!\n"
	
	if [ ! -d /opt/CanUseTimer/ ]; then
		echo "Creating main directorie in /opt/..."
        	sudo mkdir /opt/CanUseTimer/
	else
	# Remove cache
		echo "removing cache"
		if [ -d /opt/CanUseTimer/__pycache__ ]; then
			sudo rm -rf /opt/CanUseTimer/__pycache__
		fi
		if [ -d /opt/CanUseTimer/lib/__pycache__ ]; then
			sudo rm -rf /opt/CanUseTimer/lib/__pycache__
		fi
	fi
	
	echo "Creating Keyboard Python lib..."
	sudo cp -rf python-libs/keyboard/ /opt/CanUseTimer/

	echo "Creating executer..."
	sudo cp lib/canusetimer /usr/bin/
	
	echo "Coping files..."
	sudo cp *.py /opt/CanUseTimer/

	echo "Coping libs..."
	sudo cp -rf lib/ /opt/CanUseTimer/
	
	echo -e "\nEverything is done!\n"
	echo -e "\033[34;1mPress return to exit...\033[m"; read
	clear
else
       	echo "abort!"
fi
