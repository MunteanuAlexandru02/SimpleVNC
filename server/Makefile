.PHONY: setup clean

setup:
	python3 -m pip install -r requirements.txt

run:
	python3 simplevncserver.py

clean:
	-rm -f ./*/__pycache__/*

uninstall:
	python3 -m pip uninstall -r requirements.txt
