# MED-sequential-patterns
Requirements:
python
venv
## 1. Create virtual env
### On macOS and Linux:

`python3 -m venv env`

### On Windows:

`py -m venv env`

## 2. Activating a virtual environment
### On macOS and Linux:

`source env/bin/activate`

### On Windows:

`.\env\Scripts\activate`

## 3. Requirements Files
### Unix/macOS 

`python -m pip install -r requirements.txt`

### Windows

`py -m pip install -r requirements.txt`

### Remember!

If you install new packages, update requirements.txt using:

`pip freeze > requirements.txt`

## 4. Run program

### Configuration file
Program needs configuration file in .conf format as an argument. 
Example setup.conf
```
[configuration]
algorithm = GSP
limit = 100
input = data/short_d.spmf
output = output.json
min_support = 0.5
max_length = 3
min_length = 1
splitter = ,
```
### Run - UNIX/macOS
```
source env/bin/activate
python main.py setup.conf
```
