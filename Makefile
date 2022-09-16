# TODO: check if this work on windows and mac

.ONESHELL:
SHELL=/bin/bash
CONDA_SCRIPT=source $$(conda info --base)/etc/profile.d/conda.sh ;
CONDA_ACTIVATE=$(CONDA_SCRIPT) conda activate ; conda activate ./venv
.PHONY: test

init:
	python3 -m pip install --upgrade pip
	pip install conda
	conda update -n base -c defaults conda
	conda create -p ./venv python=3.9
	$(CONDA_ACTIVATE)
	python3 -m pip install -r requirements.txt
	conda deactivate

test:
	make clean
	$(CONDA_ACTIVATE)
	python3 -m pytest
	conda deactivate

coverage:
	make clean
	$(CONDA_ACTIVATE)
	python3 -m coverage erase >/dev/null
	python3 -m coverage run -m pytest >/dev/null
	python3 -m coverage html --skip-empty >/dev/null
	python3 -m coverage report -m --skip-covered --skip-empty
	conda deactivate

update:
	$(CONDA_ACTIVATE)
	python3 -m pip install -r requirements.txt
	conda deactivate

export:
	$(CONDA_ACTIVATE)
	python3 -m pip freeze | grep -v "@ file" >requirements.txt;
	conda deactivate

run:
	make clean
	$(CONDA_ACTIVATE)
	python3 -m main.py
	conda deactivate

reset:
	$(CONDA_SCRIPT) conda env remove -p ./venv

clean:
	rm __pycache__/*
	rm ./__pycache__/*
	rm ./*/__pycache__/*

help:
	echo "make <command>"
	echo "make available commads :"
	echo "init    | install conda, create a virtual environment and install all require depencies"
	echo "reset   | delete the current venv"
	echo "update  | update the venv to make sure it contains all the latest required depencies"
	echo "export  | export the curent state of the venv to share new required depencies. make sure your venv is clean before doing that"
	echo "test    | run all tests"
	echo "coverage| create a coverage report. A brief version will showed in the console a nicer and more compleate one can be found at htmlcov/index.html"
	echo "run     | run the main.py script"
	echo "clean   | empty all pycaches"