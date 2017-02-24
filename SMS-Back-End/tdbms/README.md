## TDBmS

![License](http://img.shields.io/badge/license-GPLv3-blue.svg)
![PythonVersion](https://img.shields.io/badge/python-2.7-blue.svg)
![coverage](https://img.shields.io/badge/coverage-30%25-orange.svg)

**Teaching Data Base micro Service** provide the relational data base that the app needs. The access to this service
is offer through an APIRest and all data is transmitted in JSON. 

![](sbd.png)

###### Requirements

To run this service we need have installed mysql-server engine. This service is thinking to run in Google Cloud Platform,
in [CloudSQL](https://cloud.google.com/sql/) where we only need create the service and connect it 
with our program in the same way that in local. 
This process is similar an in the both cases we only need use [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb-1.2.2) 
python library
To install MySQL engine we can use the script `mysql_install.sh` in this folder (it's only necesary out of GCP).

Beside this you need execute `requirements.txt` to provide to machine which run this code all libraries that python needs.

###### Run

Finally you can running the api executing the script `run.sh` in this folder.

If you want, you can provide that data to service executing the provisioner `provisioner.sh`.


###### Documentation:

This microservice is documented with Sphinx, before you read the doc you need generated it, running `make html` 
inside docs folder and then open *index.html* in `build/html` in the same folder, all doc is web based.

Also **fab doc_dbms** from main folder (firefox required).