.PHONY: install run test

default: test

install:
	pip install .

run:
	PYTHONPATH=./src python -m fb_group.run

test:
	PYTHONPATH=./src pytest