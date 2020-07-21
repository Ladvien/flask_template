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

from file_configs.write_nginx_conf import write_nginx_conf
from write_uwsgi_daemon import write_uwsgi_daemon
from write_uwsgi_ini import write_uwsgi_ini
from util import exec_cmd, exec_mysql_cmd

from stack import Stack
from os import Centos7

stack = Stack()
stack.get_settings()