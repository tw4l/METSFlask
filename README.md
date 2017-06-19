# METSFlask  

A web application for human-friendly exploration of Archivematica METS files.

## Live site (try it out!):  
[http://bitarchivist.pythonanywhere.com/](http://bitarchivist.pythonanywhere.com/)  

All files uploaded to METSFlask are deleted after being read into the database. Database entries are deletable by all users at any time. That is to say - feel free to upload and view your own files! You can delete them from the web app as soon as you're done.  

## Install locally (dev):  
(Tested with Python 2.7 and 3.5)  

* Clone files and cd to directory:  
`git clone https://github.com/timothyryanwalsh/METSFlask && cd METSFlask`  
* Set up virtualenv:  
`virtualenv venv`  
* Activate virtualenv:  
`source venv/bin/activate`  
* Install requiremenents:  
`pip install -r requirements.txt`   
* Create database:  
`chmod a+x db_create.py`    
`./db_create.py`  
* Run (on localhost, port 5000):  
`./run.py`  
* Go to `localhost:5000` in browser.  

## Dates

The last modified date used in the AIP table view and detailed item page is captured by the "OIS File Information" tool used by FITS during the "Characterize and extract metadata" job. These dates will appear blank in METSFlask for file types that are not set to be characterized by FITS in your local Archivematica FPR.  
