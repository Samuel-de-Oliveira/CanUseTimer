#!/usr/bin/env bash
#-*-------------- The installer for GNU/Linux --------------*-#

clear
echo -e "\nThis program will install the following packages:\n\
CanUseTimer-Terminal, keyboard_python_lib"
echo -e "and will create a folder in /opt/"
echo -e "\nEstimated space used: 200Kb\nVersion of Program: \033[33m0.2.1.1 BETA\033[m\nAre you sure you want to install? [Y/n]:"; read num
clear

if [ $num == 'y' ] || [ $num == 'Y' ]; then

	# The program only move the python files to /opt/ and create a executer in /bin/
	# Is more simple than you think
	echo -e "\nThe installing starts! This not will take long.\n"

	echo "Checking if Git is installed..."
	if [ ! -f /usr/bin/git ]; then
		if [ -f /etc/debian_version ]; then
			sudo apt install git -y
		elif [ -f /etc/arch-release ]; then
			sudo pacman -Sy git | yes
		else
			echo -e "\033[31mYour distribuition is not supported, sorry :(\033[m"
			exit 1
		fi
	fi

	if [ ! -d /opt/CanUseTimer/ ]; then
		echo "Creating main directorie in /opt/..."
        	sudo mkdir /opt/CanUseTimer/
	else
		echo "removing cache..."
		if [ -d /opt/CanUseTimer/__pycache__ ]; then
			sudo rm -rf /opt/CanUseTimer/__pycache__
		fi
		if [ -d /opt/CanUseTimer/lib/__pycache__ ]; then
			sudo rm -rf /opt/CanUseTimer/lib/__pycache__
		fi
	fi
	
	echo "Cloning python keyboard library repository..."
	git clone https://github.com/boppreh/keyboard.git

	echo "moving keyboard Python lib to the program repository..."
	if [ ! -d /opt/CanUseTimer/keyboard ]; then
		sudo mv keyboard/ /opt/CanUseTimer/
	else
		rm -rf keyboard/
	fi

	echo "Creating executer..."
	sudo cp lib/canusetimer /usr/bin/
	if [ -f /usr/bin/python3 ]; then
		echo "python3 Main.py \$*" >> /usr/bin/canusetimer
	else
		echo "python Main.py \$*" >> /usr/bin/canusetimer
	fi

	echo "Coping files..."
	sudo cp -f *.py /opt/CanUseTimer/

	echo "Coping the code library..."
	sudo cp -rf lib/ /opt/CanUseTimer/
	
	echo -e "\nEverything is done!\n"
	echo -e "\033[34;1mPress return to exit...\033[m"; read
	clear
else
       	echo "abort!"
fi
