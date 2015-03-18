import "classes/*.pp"
import "db/*.pp"
import "user/*.pp"

$PROJ_DIR = "/var/www/entertain_me"

Exec {
    path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

class dev {
  class {'mysql': }
  mysql::db::create {'django_db': }
  mysql::user::grant { 'djangouser':
    user     => 'djangouser',
    host     => 'localhost',
    password => '888968',
    database => 'django_db',
  }
  class {
      init:;
  }
}

include dev
