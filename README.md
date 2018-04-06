
# FetBASE
-----------
FetBASE© - Fettucine Human LINE-1 & HERV Transposable Elements Platform is a fast, reliable and user-friendly interface for exploring Long Interspersed Nuclear Elements 1 (LINE-1) and Human Endogenous Virus (HERV) retrotransposons and their protein expression. This software was developed by the “Fettuccine” student group of Queen Mary University of London for the purposes of a software development group project (School of Biological Sciences and Chemistry – MSc Bioinformatics) under the invaluable guidance of Professor Conrad Bessant (https://bessantlab.org/) and Dr Fabrizio Smeraldi (https://goo.gl/k6jxCr). 

The FetBASE© documentation can be found [here](https://github.com/digrigor/Fettuccine_MSc_Group_Project/blob/master/Website_Design/static/Fettuccine-Documentation.pdf).

# Fettuccine_MSc_Group_Project
- Ensure you have the following modules install on your pc (by any means necessary e.g using pip install)
- Flask
- Pandas (Provides pytz, numpy)
- Pytz
- MySQLdb
- Numpy
- Biopython
- Pylab
- Matplotlib
- Pygraphviz (and graphviz, not via pip)

- You also need to download MAMP or AAMP for linux (which does the MYSQL hosting for you) otherwise there will be no database
- https://www.mamp.info/en/

# README FOR INSTALL

------------------------------
USE python 32bit or 64bit. (different library files will be provided for each version)

Use virtualenv at your own discretion

Open up CMD terminal and run:
pip install -r /path/to/requirements.txt
------------------------------

Download the DB files from:

- Dropbox (Download first): https://www.dropbox.com/s/x78gylbh9hindvu/genome_data_export1.sql?dl=0
- Dropbox (2nd backup version): https://www.dropbox.com/s/stniwg8msanx5ku/genome_data_2_1.sql?dl=0
- Dropbox (3rd version): https://www.dropbox.com/s/0ajx2p0t9wbe3ib/genome_data_export.sql?dl=0

Download the DB files from Apocrita located on:
- /data/SBCS-MSc-Bioinf/fettbase_sql

Install Your Own MYSQL server of Choice (we Used MAMP for windows to make it simple to turn on / off)

Download https://www.graphviz.org/download/ V2.38 and install

The software was ran and tested using MySQK 5.7.20 in Windows 32-bit, 64-bit and Linux 64-bit.

Copy the MySQLdb (MySQL python connector) and pygraphviz folders + pylab files to your C:\Python27\Lib\site-packages\ or equivalent folders for your OS or if using virtualenv. (These files have been provided in the compressed zip format)

PyGraphviz May not work on 64bit python, python 64bit is reccomended as the 32bit will cause memory errors if you try to upload files > 300MB (however pygraphviz works on 32bit)

If Pygraphviz does not load, you are still able to run the website as it is not needed for the main sections of the site
(The SECOND custom tree will not load on the webpage after submission of ph file, however you can visit the url custom_tree2 > "localhost:5000/custom_tree2" to see how it would look if it had rendered properly with the functional plugin)

# MYSQL
-----------

Create a database called genome_data:

> CREATE DATABASE genome_data;

Import the SQL file into MySQL using:

Use genome_data_export1.sql first

If it doesn't work try the other ones.

Import the file to the DB:

> Path/to/Mysql.exe -u root -p genome_data < "path/to/genome_data.sql"

User can also create an identical database from scratch by
following the instructions  inside SQL_db_instructions folder.
This file also contains random data from our database that can
populate the new db.

---------------
# RUNNING FLASK
-----------

To run the software go to Website_Design and execute the commands based on OS:

# run flask on WINDOWS using:
OPEN COMMAND PROMPT, GO TO CORRECT DIRECTORY of file (cd ..\..)
- set FLASK_APP=project.py
- set FLASK_DEBUG=1
- flask run

# run flask on LINUX using:
- export FLASK_APP=project.py
- export FLASK_DEBUG=1
- flask run

----------------------

