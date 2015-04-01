__author__ = 'anmekin'
from fabric.api import *

env.use_ssh_config = True
# env.hosts = ['your-alias-name']
PROJECT_PATH = '/your/path/to/entertain-me' # customize it

def vagrant():
    env.user = 'vagrant' # for vagrant
    env.hosts = ['127.0.0.1:2222'] # for vagrant
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]
    PROJECT_PATH = '/var/www/entertain_me'

#vagrant()


def clone():
    sudo('apt-get -y install git')
    with cd(PROJECT_PATH + '/..'):
        run('git clone https://github.com/Crystalnix/entertain-me.git')


def virt_env():
    sudo('pip install virtualenv')
    with cd (PROJECT_PATH):
        run('mkdir ./.virtualenv')
        run("cd ./.virtualenv && virtualenv entertain-me")
        venv = 'source ./.virtualenv/entertain-me/bin/activate && '
        run(venv + 'pip install -r requirements.txt')


def install_mysql():
    while True:
        mysql_password = prompt('Please enter MySQL root password:')
        mysql_password_confirmation = prompt('Please confirm your password: ')
        if mysql_password == mysql_password_confirmation:
            break
        else:
            print "Passwords don't match"

    # set the value in debconf
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),
              warn_only=True):
        sudo('echo "mysql-server-5.5 mysql-server/root_password password '
            '%s" | debconf-set-selections' % mysql_password)
        sudo('echo "mysql-server-5.5 mysql-server/root_password_again '
             'password %s" | debconf-set-selections' % mysql_password)
    sudo('apt-get -y install mysql-server-5.5', shell=False)
    sudo('sudo apt-get -y install libmysqlclient-dev', shell=False)

    run("mysql -uroot -p%s -e 'create database django_db CHARACTER SET utf8 COLLATE utf8_general_ci'" % mysql_password)
    run("mysql -uroot -p%s -e \"GRANT ALL ON django_db.* TO 'djangouser'@'localhost' IDENTIFIED BY '888968'\"" % mysql_password)


def project_setting():
    clone()
    sudo("apt-get -y install python-pip")
    install_mysql()
    sudo('apt-get -y install rabbitmq-server')
    sudo('apt-get -y install coffeescript')
    virt_env()



def deploy():
    with settings(warn_only=True):
        sudo('apt-get update')
        sudo('apt-get -y install python-dev')
        sudo('apt-get -y install nginx')
        sudo('cp %s/deploy/entertain-me /etc/nginx/sites-available' % PROJECT_PATH)
        sudo('ln -s /etc/nginx/sites-available/entertain-me /etc/nginx/sites-enabled/entertain-me')
        sudo('service nginx restart')
        sudo('apt-get -y install supervisor')
        sudo('cp %s/deploy/entertain-me.conf /etc/supervisor/conf.d/' % PROJECT_PATH)
        sudo('mkdir /var/log/entertain-me/')
        project_setting()
        sudo('supervisorctl reread')
        sudo('supervisorctl update')


def run_test_server():
    venv = 'source ./.virtualenv/entertain-me/bin/activate && '
    with cd(PROJECT_PATH):
        run(venv + 'python manage.py makemigrations')
        run(venv + 'python manage.py migrate')
        run(venv + 'python manage.py runserver 0.0.0.0:8000')


def start_server():
    sudo('supervisorctl start entertain-me')


def stop_server():
    sudo('supervisorctl stop entertain-me')

def status_server():
    sudo('supervisorctl status')

