##Prerequisites:##
- Python 2.7
- MySQL
- RabbitMQ

##Dependencies: ##
``` 
$ pip install virtualenv 
$ pip install virtualenvwrapper 
$ mkvirtualenv new_env 
$ workon new_env 
$ export WORKON_HOME=$HOME/.virtualenvs
$ source /usr/local/bin/virtualenvwrapper.sh
$ source .bashrc
$ pip install -r requirements.txt 
$ deactivate new_env
```
##How to start:##
Installing MySQL:
```
$ sudo apt-get install libmysqlclient-dev
```
Installing RabbitMQ:
```
$ sudo apt-get install rabbitmq-server
```
Creating database:
``` 
$ mysql -u root -p
Enter password:           # Use the password you entered when installing MySql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.5.41-0ubuntu0.14.04.1 (Ubuntu)
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE DATABASE django_db;
Query OK, 1 row affected (0.01 sec)

mysql> GRANT ALL ON django_db.* TO 'djangouser'@'localhost' IDENTIFIED BY '888968';
Query OK, 0 rows affected (0.03 sec)

mysql> quit
```
Run virtual environment:
```
$ workon new_env
```
First launch local server:
```
$ python manage.py migrate
$ python manage.py runserver
```
Run celery worker:
```
$ python manage.py celery worker --loglevel=DEBUG -B
```
