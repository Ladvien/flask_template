"""
On CentOS 7:
    For problems using nginx as to reverse proxy uWSGI, check the logs at:
        /var/log/nginx/access.log
        /var/log/nginx/error.log
    If not collected, these can be set in the nginx.conf
        error_log /var/log/nginx/error.log;
        http { access_log  /var/log/nginx/access.log  main; }

    It appears SELinux caused the "permission denied while connection to upstream" when using nginx to reverse proxy.
        https://stackoverflow.com/a/49492644
      
"""
import os
import pip
import getpass

from stacks.stack_centos7 import Centos7Stack

stack = Centos7Stack()
stack.get_settings()
stack.prepare()
stack.install_dev_tools()
stack.create_user()
stack.firewall_setup()
stack.create_uwsgi_daemon()
stack.uwsgi_setup()
stack.move_app_in_place()
# stack.setup_certificate()
stack.setup_nginx()
stack.install_mariadb()
stack.setup_mariadb()
stack.create_database_url_env_var()
stack.create_app_symlink_for_user()
stack.start_app_daemon()
stack.debrief()