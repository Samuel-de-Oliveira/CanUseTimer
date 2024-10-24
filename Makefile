FILE = Main.py
PIP  = bin/pip
CXX  = bin/pyinstaller

all:
	$(CXX) -F ..\Main.py -i ..\Images\icon.ico

setup:
	python -m venv .
	$(PIP) install -r requirements.txt
