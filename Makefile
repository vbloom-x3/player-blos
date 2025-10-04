# Default target
all: install install-player force-i install-player

# Install dependencies
install:
	pip install -r requirements.txt

force-i:
	pip install -r requirements.txt --break-system-packages

install-player:
	cd src
	chmod +x src/main.sh
	cp src/main.sh ~/.local/bin/player-blos
	cp src/main.py ~/.local/bin/player-blos.py
	cd ..
	@echo "player-blos	   -> Run the music player"

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "make install        -> Install dependencies"
	@echo "make force-i        -> Add --break-system-packages to pip
	@echo "make install-player -> Install player"
	@echo "make clean          -> Remove pycache and temporary files"
