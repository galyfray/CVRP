# TODO: check if this work on windows and mac

.ONESHELL:
SHELL=/bin/bash
CONDA_SCRIPT=source $$(conda info --base)/etc/profile.d/conda.sh ;
CONDA_ACTIVATE=$(CONDA_SCRIPT) conda activate ; conda activate ./venv

PYTHON=""

ifeq ($(OS),Windows_NT)
	ifeq (,$(shell python3 --version 2>nul))
    	PYTHON:=python3
	else
		PYTHON:=python
	endif
else
    PYTHON:=python3
endif

.PHONY: test

init:
	$(PYTHON) -m pip install --upgrade pip
	pip install conda
	conda update -n base -c defaults conda
	conda create -p ./venv python=3.9
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip install -r requirements.txt
	conda deactivate

test:
	make clean
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pytest
	conda deactivate

coverage:
	make clean
	$(CONDA_ACTIVATE)
	$(PYTHON) -m coverage erase >/dev/null
	$(PYTHON) -m coverage run -m pytest >/dev/null
	$(PYTHON) -m coverage html --skip-empty >/dev/null
	$(PYTHON) -m coverage report -m --skip-covered --skip-empty
	conda deactivate

update:
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip install -r requirements.txt
	conda deactivate

export:
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip freeze | grep -v "@ file" >requirements.txt;
	conda deactivate

run:
	make clean
	$(CONDA_ACTIVATE)
	$(PYTHON) -m main.py
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