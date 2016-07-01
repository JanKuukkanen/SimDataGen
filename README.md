# SimDataGen
Data generator for simulating water currents.

##Installation
Instructions for installing SimDataGen.

###Requirements
* Ubuntu linux
* Python 2.7.6
* A working cassandra database with usable roles
* Cloned SimDataGen repository

###Configuring the database access
Create the required database schema into your Cassandra database by running the file cassandra.cql found in the resources directory with cassandra's query language cqlsh.

Run installation_sdg.sh file and answer all the questions, this creates a data_file with the database information that you gave which the program will use for accessing the database, you can later edit this file with a text editor if any information has been changed.

###Starting the program
Once you've configured the database, start the program by running the file start_sdg.sh.

##Development tools
Python 2.7.6  
Cassandra 2.2.6  
cqlsh 5.0.1  
