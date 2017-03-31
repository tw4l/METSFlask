# METSFlask  

**NOTE: Very much in dev**  

Flask application for viewing detailed information on "original" files in an Archivematica METS file.  

## Install (dev)
* Clone repo
* `virtualenv venv`  
* `source venv/bin/activate`  
* `pip install Flask`  
* `pip install lxml` 
* `export FLASK_APP=metsflask.py`   
* `flask run`  

## To Do  
* Add file upload (currently reads only from one particular METS file in "uploads" dir)   
* Add PREMIS events info to detail page  
* Add info about preservation derivative to detail page  
* Style  
* Test  
* Deploy  
