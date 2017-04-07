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
* `export FLASK_APP=metsflask.py`   
* Create database (in Python interpreter):  
`>>> from metsflask import db`  
`>>> db.create_all()`  
* `flask run`  

## To Do    
* Add info about preservation derivative to detail page?  
* Add more tool-specific extracted metadata to detail page  
* Style  
* Test  
* Deploy  
