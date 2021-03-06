[![Build Status](https://travis-ci.org/Crystalnix/entertain-me.svg)](https://travis-ci.org/Crystalnix/entertain-me)
[![Coverage Status](https://coveralls.io/repos/Crystalnix/entertain-me/badge.svg?branch=travis)](https://coveralls.io/r/Crystalnix/entertain-me?branch=travis)
##Demonstration:##
[Demo](http://entertain-me.crystalnix.com)

##Prerequisites:##
- Python 2.7
- MySQL
- RabbitMQ
- Coffeescript

##Dependencies: ##
``` 
$ pip install virtualenv 
$ pip install virtualenvwrapper 
$ export WORKON_HOME=$HOME/.virtualenvs
$ source /usr/local/bin/virtualenvwrapper.sh
$ source .bashrc
$ mkvirtualenv new_env 
$ pip install -r requirements.txt 
```
##How to start with Vagrant:##

Installing Virtualbox:
```
$ sudo apt-get install virtualbox
```
Installing Vagrant:
```
$ sudo apt-get install vagrant
```
Installing Puppet:
```
$ sudo apt-get install puppet
```
Launch Vagrant:
```
$ vagrant up
$ vagrant provision
$ vagrant ssh
```
Run server:
```
$ cd /var/www/entertain_me
$ python manage.py runserver 0.0.0.0:8000
```
##How to start without Vagrant:##
Installing MySQL:
```
$ sudo apt-get install mysql-server
```
Installing RabbitMQ:
```
$ sudo apt-get install rabbitmq-server
```
Installing Coffeescript:
```
$ sudo apt-get install coffeescript
```
Creating database:
``` 
$ mysql -u root -p
Enter password:           # Use the password you entered when installing MySql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.5.41-0ubuntu0.14.04.1 (Ubuntu)
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE DATABASE django_db CHARACTER SET utf8 COLLATE utf8_general_ci;
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
## Other usefull commands ##
Run celery worker:
```
$ python manage.py celery worker --loglevel=DEBUG -B
```
Run tests with coverage:
```
$ python manage.py test --with-coverage
```
Generate html with documentation:
```
$ cd docs/
$ make html
```
##How to deploy with SSH:##
Create or update ssh config
```
$ nano ~/ssh/config
```
Add next settings:
```
Host alias_name
HostName your_domen
User username
IdentityFile ~/.ssh/file_with_private_rsa_key
IdentitiesOnly yes
```

Configure files in the folder deploy: entertain-me(nginx config), entertain-me.conf(supervisor config). 

In fabfile.py configure hosts and PROJECT_PATH. Use automathic deploy script (from PROJECT_PATH): 
```
$ fab deploy
```
Now you can manage server with next comands:
```
$ fab status_server # get current status
$ fab start_server 
$ fab stop_server
$ fab run_test_server # run server with debug
```
