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
$ cd var/www/entertain_me
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
Connect to server with SSH:
```
$ ssh alias_name
```
Install nginx:
```
sudo apt-get install nginx
```
Create nginx config:
```
$ sudo nano /etc/nginx/sites-avalable/entertain-me
```
with
```
server {
        server_name your_domen;
        access_log off;

        location /static/ {
            alias /path/to/entertain-me/staticfiles/;
        }

        location / {
                proxy_pass http://127.0.0.1:8020;
                proxy_set_header X-Forwarded-Host $server_name;
                proxy_set_header X-Real-IP $remote_addr;
                add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
    }
```
Create a symbolic link:
```
$ sudo ln -s /etc/nginx/sites-available/hello /etc/nginx/sites-enabled/hello
```
Restart Nginx:
```
$ sudo service nginx restart 
```
Install supervisor:
```
sudo apt-get install supervisor
```
Clone from repository, set up without Vagrant and create deploy_settings per sample:
```
$ git clone git@github.com:Crystalnix/entertain-me.git
```
Create script gunicorn_start:
```
cd /home/admin/entertain_me/
source /home/admin/.virtualenvs/entertain_me/bin/activate
/home/admin/.virtualenvs/entertain_me/bin/gunicorn entertain_me.wsgi:application --bind 127.0.0.1:8020
```
Make script executable:
```
$ chmod +x gunicorn_start
```
Create Supervisor config file:
```
$ sudo nano /etc/supervisor/conf.d/hello.conf
```
with configs:
```
[program:entertain-me]
directory=/path/to/entertain-me
user = entertain-me
command=sh /path/to/entertain-me/gunicorn_start
stdout_logfile = /var/log/entertain-me/supervisor.log
redirect_stderr = true
```
Update Supervisor:
```
$ sudo supervisorctl reread
$ sudo supervisorctl update
```
