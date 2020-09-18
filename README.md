# METSFlask  

A web application for human-friendly exploration of Archivematica METS files.

![demo](metsflask-demo.gif)

## Live site (try it out!):  
[http://bitarchivist.pythonanywhere.com/](http://bitarchivist.pythonanywhere.com/)  

All files uploaded to METSFlask are deleted after being read into the database. Database entries are deletable by all users at any time. That is to say - feel free to upload and view your own files! You can delete them from the web app as soon as you're done.  

## Install locally (dev):  
(Tested with Python 2.7 and 3.5. It's recommended that you use Python 3, as there could be some Unicode handling issues with Python 2.)  

* Clone files and cd to directory:  
`git clone https://github.com/tw4l/METSFlask && cd METSFlask`  
* Set up virtualenv:  
`virtualenv venv`  
* Activate virtualenv:  
`source venv/bin/activate`  
* Install requirements:  
`pip install -r requirements.txt`   
* Create database:  
`chmod a+x db_create.py`    
`./db_create.py`  
* Run (on localhost, port 5000):  
`./run.py`  
* Go to `localhost:5000` in browser.  

## Creators

* Canadian Centre for Architecture
* Tessa Walsh

This project was initially developed in 2016-2017 for the [Canadian Centre for Architecture](https://www.cca.qc.ca) by Tessa Walsh, Digital Archivist, as part of the development of the Archaeology of the Digital project.
