#!/bin/bash

#-*-------------- The installer for Linux distros --------------*-#

echo -e "\nThis program will install the following packages:\n\
CanUseTimer-Terminal, keyboard_python_lib"
echo -e "and will create a folder in /opt/"

echo -e "\nEstimated space used: 160Kb\nVersion of Program: 0.1.4\nAre you sure you want to install? [Y/n]:"; read num

if [ $num == 'y' ] || [ $num == 'Y' ]; then

	# The program only move the python files to /opt/ and create a executer in /bin/
	# Is more simple then you think
	echo -e "\nThe installing starts!\n"
	
	if [ ! -d /opt/CanUseTimer-Terminal/ ]; then
		echo "Creating main directories in /opt/..." 
        	sudo mkdir /opt/CanUseTimer-Terminal
	fi
	
	echo "Creating Keyboard Python lib..."
	sudo cp -rf python-libs/keyboard/ /opt/CanUseTimer-Terminal/

	echo "Creating executer..."
	sudo cp lib/canusetimer-terminal /bin/
	
	echo "Coping files..."
	sudo cp *.py /opt/CanUseTimer-Terminal/

	echo "Coping libs..."
	sudo cp -rf lib/ /opt/CanUseTimer-Terminal/
	
	echo -e "\nEverything is done!\n"

else
       	echo "abort!"
fi
