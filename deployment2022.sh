#!/bin/sh
#git clone https://github.com/lingpearl/ITP4121-EA-assignment-2.git
#cd ITP4121-EA-assignment-2
sudo yum -y update
sudo yum install -y mysql-server
sudo rpm -e --nodeps mariadb-libs-10.2.38-1.amzn2.0.1.x86_64
sudo rpm -e --nodeps mariadb-10.2.38-1.amzn2.0.1.x86_64
sudo rpm -e --nodeps mariadb-server-10.2.38-1.amzn2.0.1.x86_64
sudo rpm -e --nodeps mariadb-server-utils-10.2.38-1.amzn2.0.1.x86_64
sudo rpm -e --nodeps mariadb-config-10.2.38-1.amzn2.0.1.x86_64
sudo rpm -ivh mysql-community-release-el7-5.noarch.rpm
sudo service mysqld start
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
sudo yum install -y mysql-devel
pip install -r requirements1.txt
chmod 755 setup.sh
chmod 755 get_preview_link.sh
./setup.sh
./get_preview_link.sh
python3 main.py