DEST_DIR := $(CURDIR)/../dest

.PHONY: build


build:
	pyinstaller --clean --onefile  --noconsole  --windowed --distpath ./../bin systemFrontend/menuGUI.py
	rm -rf build
	rm -rf menuGUI.spec
  