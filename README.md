基督教香港崇真會恩樂園

#Migration Script

#WebServer
yum install -y git
yum install -y mysql-devel
git clone https://github.com/kitson618/babyinfo.git
cd babyinfo
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip3 install -r requirements.txt
#sudo service mysqld start (Test with Local Mysql)
#sudo mysqladmin -u root password 'cnujireau3289h' (Test with Local Mysql)
vim config.conf #update db host and password
python main.py

https://docs.google.com/document/d/1N-Reftk7pJeTaEloI99jxSmkwf292bFKjMXTx6CjQ5g/edit#heading=h.lc5tgqbmetm6

*********************************
https://www.geeksforgeeks.org/default-arguments-in-python/
https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/s3-example-presigned-urls.html

Database Trigger 
https://stackoverflow.com/questions/23382499/run-python-script-on-database-event
https://tomaztsql.wordpress.com/2018/06/18/real-time-data-visualization-with-sql-server-and-python-dash/

Mysql 
- Database trigger 
- Stored Procedures
two ponmit
how long send one time
how many time are there , time rare 0 -send
check one time -send 
1. Parent page add date filter, default show cuurent date
2. Parent page add tabs for showing different children 
3. Staff admin can search child by name
4.Once a child with record fever, for a specic time range and number of times, then trigger an email
admin receive email

one group 6 per each 50, 300 people, visualization to show data (excel)

5. add a tabke "disabled" 
(Y/N) to represent a child is being discharged
parent can not login
-account
-child information
6.Staff 可以決定出左院小孩既家長，唔可以再登入
disable childer account disable parent acco...

disable child record
disable parent account 
*********************************