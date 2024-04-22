#!/usr/bin/env bash
#-*-------------- Installer for GNU/Linux --------------*-#

echo -e "\ninstalling... This will not take long.\n"

if [ ! -f /usr/bin/git ]; then
	echo -e "\033[31mPlease install git to continue...\033[m"
	exit
fi

if [ ! -d /opt/CanUseTimer/ ]; then
	echo "Creating main directory in /opt/..."
	mkdir /opt/CanUseTimer/
fi
	
if [ ! -d /opt/CanUseTimer/keyboard ]; then
	echo "Cloning needed library to /opt/CanUseTimer/..."
	git clone https://github.com/boppreh/keyboard &> /dev/null
	mv keyboard/keyboard /opt/CanUseTimer/
fi
rm -rf keyboard/

echo "Create executer..."
cp lib/canusetimer /usr/bin/
if [ -f /usr/bin/python3 ]; then
	echo "python3 Main.py \$*" >> /usr/bin/canusetimer
else
	echo "python Main.py \$*" >> /usr/bin/canusetimer
fi

echo "Coping files to opt..."
cp *.py /opt/CanUseTimer/
cp -rf lib/ /opt/CanUseTimer/
	
echo -e "\nDone!\n"
