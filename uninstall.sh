#!/usr/bin/env bash
# -*-- CanUseTimer Uninstaller --*- #

echo -e "\033[1mUninstalling CanUseTimer...\033[m"

if [ -f /usr/bin/canusetimer ]; then
	echo "Removing executer..."
  rm /usr/bin/canusetimer
fi

if [ -d /opt/CanUseTimer/ ]; then
	echo "Removing directory..."
  rm -rf /usr/share/CanUseTimer/
fi

echo -e "\nDone!\n"
