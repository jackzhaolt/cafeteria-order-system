DEST_DIR := $(CURDIR)/../dest

.PHONY: build

build:
	pyinstaller --clean --onefile  --noconsole  --windowed --distpath ./../bin orderGUI.py
	rm -rf build
	rm -rf menuGUI.spec
  