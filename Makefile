FILE   = Main.py
PIP    = bin/pip
CXX    = bin/pyinstaller
BIN    = /bin
SHARE  = /usr/share
TARGET = canusetimer

all:
	$(CXX) -F Main.py -i Images\icon.ico
	mv dist/Main $(TARGET)
	rm -rf dist

setup:
	python -m venv .
	$(PIP) install -r requirements.txt

clean:
	rm -rf build/ Main.spec
