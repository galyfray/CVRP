# TODO: check if this work on windows and mac

.ONESHELL:
SHELL=/bin/bash
CONDA_SCRIPT=""
CONDA_ACTIVATE=""

PYTHON=""

ifeq ($(OS),Windows_NT)
    NULL=nul
	RM=FOR /d /r . %%d IN ("__pycache__") DO @IF EXIST "%%d" rd /s /q "%%d"
	CONDA_SCRIPT=call conda.bat
	CONDA_ACTIVATE=activate ./venv
	ifeq (,$(shell python3 --version 2>nul))
    	PYTHON:=python
	else
		PYTHON:=python3
	endif
else
	NULL=/dev/null
	RM=rm -rf ./**/__pycache__;rm -rf __pycache__
    PYTHON:=python3
	CONDA_SCRIPT:=source $$(conda info --base)/etc/profile.d/conda.sh ;conda
	CONDA_ACTIVATE:=$(CONDA_SCRIPT) activate ; conda activate ./venv
endif

.PHONY: test

init:
	$(PYTHON) -m pip install --upgrade pip
	conda update -n base -c defaults conda
	conda create -p ./venv python=3.9
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip install -r requirements.txt

test:
	make clean
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pytest

coverage:
	make clean
	$(CONDA_ACTIVATE)
	$(PYTHON) -m coverage erase >$(NULL)
	$(PYTHON) -m coverage run -m pytest >$(NULL)
	$(PYTHON) -m coverage html --skip-empty >$(NULL)
	$(PYTHON) -m coverage report -m --skip-covered --skip-empty

update:
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip install -r requirements.txt

export:
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip freeze | grep -v "@ file" >requirements.txt;

run:
	make clean
	$(CONDA_ACTIVATE)
	$(PYTHON) -m main.py

reset:
	$(CONDA_SCRIPT) env remove -p ./venv

clean:
	$(RM)

lint:
	$(CONDA_ACTIVATE)
	$(PYTHON) -m bandit -r -f html -o bandit.html .
	$(PYTHON) -m pylint --exit-zero ./**/*.py >pylint.txt
	$(PYTHON) -m flake8 . --output-file=flake8.txt


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
	echo "lint    | will run bandit, pylint and flake8 accros the whole project. Outputs are bandit.html, pylint.txt, flake8.txt"