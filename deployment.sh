git clone https://github.com/afatpig/BabyInfo.git
cd babyInfo
sudo yum install -y mysql-devel
sudo yum install -y mysql-community-server
sudo yum install -y mysql-server
sudo python -m pip install -r requirements.txt
service mysqld start
sudo mysqladmin -u root password 'cnujireau3289h'
nano config.conf
python -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
python main.py