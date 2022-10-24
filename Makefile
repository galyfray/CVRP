# TODO: check if this work on windows and mac

ifeq ($(OS),Windows_NT)
	ifeq (,$(shell python3 --version 2>nul))# Python detection
		PYTHON:=python
	else
		PYTHON:=python3
	endif

	NULL=nul

# Anaconda integration
	CONDA_SCRIPT=call conda.bat
	PY_CONDA=$(CONDA_SCRIPT) activate ./venv & $(PYTHON)

# Command generalization
	RM_CMD=FOR /d /r . %%d IN ("__pycache__") DO @IF EXIST "%%d" rd /s /q "%%d"
	EXPORT_CMD=make wexport

else
# The default shel used on unix doesn't support `source`
	SHELL=/bin/bash 
    PYTHON:=python3 # Python detection
	
	NULL=/dev/null

# Anaconda integration
	CONDA_SCRIPT:=source $$(conda info --base)/etc/profile.d/conda.sh ;conda
	PY_CONDA:=$(CONDA_SCRIPT) activate ; conda activate ./venv; $(PYTHON)

# Command generalization
	RM_CMD=rm -rf ./**/__pycache__;rm -rf __pycache__
	EXPORT_CMD=$(PY_CONDA) -m pip freeze | grep -v "@ file" >requirements.txt;

endif

.PHONY: test

test:
	make clean
	$(PY_CONDA) -m pytest

init:
	$(PYTHON) -m pip install --upgrade pip
	conda update -n base -c defaults conda
	conda create -p ./venv python=3.9
	$(PY_CONDA) -m pip install -r requirements.txt

coverage:
	make clean
	$(PY_CONDA) -m coverage erase >$(NULL)
	$(PY_CONDA) -m coverage run -m pytest >$(NULL)
	$(PY_CONDA) -m coverage html --skip-empty >$(NULL)
	$(PY_CONDA) -m coverage report -m --skip-covered --skip-empty

update:
	$(PY_CONDA) -m pip install -r requirements.txt

export:
	$(EXPORT_CMD)

wexport:
	$(PY_CONDA) -m pip freeze >requirement.txt
	findstr /v "@ file" requirement.txt >requirements.txt
	del .\requirement.txt

# TODO: re create the make run command
run:
	make clean
	$(PY_CONDA) -m main.py

reset:
	$(CONDA_SCRIPT) env remove -p ./venv

clean:
	$(RM_CMD)

lint:
	$(PY_CONDA) -m bandit -c ./bandit.yaml -r -f html -o bandit.html .
	$(PY_CONDA) -m pylint --exit-zero src/cvrp src/server test/ >pylint.txt
	$(PY_CONDA) -m flake8 . --output-file=flake8.txt
	$(PY_CONDA) -m pydocstyle . -e -s > pydocstyle.txt || exit 0
	


help:
	echo "make <command>"
	echo "make available commands :"
	echo "init    | install conda, create a virtual environment and install all require dependencies"
	echo "reset   | delete the current venv"
	echo "update  | update the venv to make sure it contains all the latest required dependencies"
	echo "export  | export the curent state of the venv to share new required dependencies. make sure your venv is clean before doing that"
	echo "test    | run all tests"
	echo "coverage| create a coverage report. A brief version will showed in the console a nicer and more complete one can be found at htmlcov/index.html"
	echo "run     | run the main.py script"
	echo "clean   | empty all pycaches"
	echo "lint    | will run bandit, pydocstyle, pylint and flake8 accros the whole project. Outputs are bandit.html, pydocstyle.txt, pylint.txt, flake8.txt"
