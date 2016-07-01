# installation file for SimDataGen

chmod -R u+x .

apt-get update

apt-get -y install python2.7

pip install -y -U pip

pip install -y cassandra-driver

apt-get -y install python-matplotlib

python resources/sdg_install.py