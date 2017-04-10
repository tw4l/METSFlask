# METSFlask  

**NOTE: Very much in dev**  

Flask application for viewing detailed information on "original" files in an Archivematica METS file.  

## Install (dev)
* `git clone https://github.com/timothyryanwalsh/METSFlask && cd METSFlask`  
* `virtualenv venv`  
* `source venv/bin/activate`  
* `pip install -r requirements.txt`  
* `export FLASK_APP=metsflask.py`   
* Create database:  
`chmod a+x db_create.py`  
`chmod a+x db_migrate.py`   
`./db_create.py`  
`./db_migrate.py`  
* `./run.py`  

## To do
* Styling  
* Prevent user from attempting to upload same file more than once  
* Add dates to AIP view (which dates?)  
