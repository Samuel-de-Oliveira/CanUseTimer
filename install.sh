#!/bin/bash

echo -e "\nThis program will install the following packages:\n\
CanUseTimer-Terminal, keyboard_python_lib"
echo -e "and will create a folder in /opt/"

echo -e "\nEstimated space used: 170Kb\nAre you sure you want to install? [Y/n]:";read num

if [ $num == 'y' ] || [ $num == 'Y' ]; then
	echo "The installing starts!"
	
	echo "Creating directories and files..."
	if [ ! -d /opt/CanUseTimer-Terminal ]; then
             sudo mkdir /opt/CanUseTimer-Terminal
	fi
	
	echo "Creating Keyboard Python lib"
	sudo cp -rf python-libs/keyboard/ /opt/CanUseTimer-Terminal/

	echo "Creating executer..."
	sudo cp lib/canusetimer-terminal /bin/

	sudo cp *.py /opt/CanUseTimer-Terminal/
	sudo cp -rf lib/ /opt/CanUseTimer-Terminal/
	
	echo "Everything is done!"

else
       	echo "abort!"
fi
