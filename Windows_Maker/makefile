# Makefile for the runner
COMPILER = pyinstaller.exe
TARGET   = CanUseTimer.exe
FILE     = ..\Main.py
ICON     = ..\Images\icon.ico

all:
	$(COMPILER) -F $(FILE) -i $(ICON)

clean:
	rm -rf dist build *.spec