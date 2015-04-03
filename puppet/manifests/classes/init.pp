class init {

    group { "puppet":
        ensure => "present",
    }

    # Let's update the system
    exec { "update-apt":
        command => "sudo apt-get update",
    }

    # Let's install the dependecies
    package {
        ["python", "python-dev", "python-pip", "mysql-server","libmysqlclient-dev", "rabbitmq-server", "coffeescript"]:
        ensure => installed,
        require => Exec['update-apt'] 
    }

    # Let's install the project dependecies from pip
    exec { "pip-install-requirements":
        command => "sudo /usr/bin/pip install -r $PROJ_DIR/requirements.txt",
        tries => 2,
        timeout => 1800,
        require => Package["python", "python-dev", "python-pip", "mysql-server","libmysqlclient-dev", "rabbitmq-server", "coffeescript"], 
        logoutput => on_failure
    }
    

}

class mysql ($root_password = '888968a3', $bin = '/usr/bin:/usr/sbin') {
#  $bin = '/usr/bin:/usr/sbin'

  service { 'mysql':
    alias   => 'mysql::mysql',
    enable  => 'true',
    ensure  => 'running',
    require => Package['mysql-server'],
  }

  # Set the root password.
  exec { 'mysql::set_root_password':
    unless  => "mysqladmin -uroot -p${root_password} status",
    command => "mysqladmin -uroot password ${root_password}",
    path    => $bin,
    require => Package["python", "python-dev", "python-pip", "mysql-server","libmysqlclient-dev", "rabbitmq-server", "coffeescript"]
  }
  include init
}

class migrations{
  exec { 'make-migrations':
    command => "python /var/www/entertain_me/manage.py makemigrations",
    require => Class['mysql'] 
  }
  exec { 'python_migrate':
    command => "python /var/www/entertain_me/manage.py migrate",
    require => Exec['make-migrations'] 
  }
}
