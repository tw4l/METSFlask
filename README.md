# METSFlask  

**NOTE: Very much in dev**  

Flask application for viewing detailed information on "original" files in an Archivematica METS file.  

## Install (dev)
* `git clone https://github.com/timothyryanwalsh/METSFlask && cd METSFlask`  
* `virtualenv venv`  
* `source venv/bin/activate`  
* `pip install Flask`  
* `pip install lxml` 
* `pip install Flask-SQLAlchemy`  
* `pip install sqlalchemy-migrate`
* `export FLASK_APP=metsflask.py`   
* Create database:  
`chmod a+x db_create.py`  
`chmod a+x db_migrate.py`   
`./db_create.py`   
`./db_migrate.py`   
* `flask run`  
