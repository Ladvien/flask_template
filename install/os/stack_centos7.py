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

from write_nginx_conf import write_nginx_conf
from write_uwsgi_daemon import write_uwsgi_daemon
from write_uwsgi_ini import write_uwsgi_ini
from util import exec_cmd, exec_mysql_cmd
from stack import Stack


class Centos7Stack(Stack):
    def __init__(self, os):
        self.centos_dev_tools = " ".join(
            [
                "python3-pip",
                "python3-devel",
                "gcc",
                "gcc-c++",
                "make",
                "openssl-devel",
                "libffi",
                "libffi-devel",
                "python3-setuptools",
            ]
        )

        self.nginx_and_tools = " ".join(["nginx", "certbot", "python2-certbot-nginx",])

    def update(self):
        # Update the system.
        exec_cmd("yum update -y")

    def install_dev_tools(self):
        print(
            """
        #################
        # Install Tools #
        #################
        """
        )
        # Install extra packages for RedHat
        exec_cmd("yum install epel-release -y")
        # Install needed dev tools.
        exec_cmd(f"yum install {self.centos_dev_tools} -y")

        # Install Nginx
        exec_cmd(f"yum install {self.nginx_and_tools} -y")

    def create_user(self):
        print(
            f"""
        ####################################
        # Creating Linux User {self._username}   #
        ####################################
        """
        )
        # Setup user
        cmd_user_setup = f"""adduser {self._username}
        echo "{self._password}" | passwd --stdin {self._username}
        usermod -aG wheel {self._username}
        """
        exec_cmd(cmd_user_setup)

    def firewall_setup(self):
        print(
            f"""
        ####################################
        # Opening needed ports in firewall #
        ####################################
        """
        )
        # Open CentoS firewall
        cmd_firewall_setup = """firewall-cmd --zone=public --permanent --add-service=http
        firewall-cmd --zone=public --permanent --add-service=https
        firewall-cmd --reload
        """
        exec_cmd(cmd_firewall_setup)

    def create_uwsgi_daemon(self):
        print(
            """
        #################
        # Create Daemon #
        #################
        """
        )
        daemon_file_path = os.getcwd() + f"/{self._app_name}.service"
        write_uwsgi_daemon(
            daemon_file_path, self._username, self._password, self._app_name, self._site
        )
        exec_cmd(f"mv {daemon_file_path} /etc/systemd/system/{self._app_name}.service")
        exec_cmd(f"chmod +rw /etc/systemd/system/{self._app_name}.service")
        exec_cmd(f"rm -rf {daemon_file_path}")

    