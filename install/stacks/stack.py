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

from .file_templates.write_nginx_conf import write_nginx_conf
from .file_templates.write_uwsgi_daemon import write_uwsgi_daemon
from .file_templates.write_uwsgi_ini import write_uwsgi_ini
from .util import exec_cmd, exec_mysql_cmd

class Stack:
    
    flask_pip_packages = " ".join([
        "flask",
        "Flask-SQLAlchemy",
        "uwsgi",
        "python-dateutil",
        "PyMySQL",
    ])

    def __init__(self, os):
        self._username = None
        self._password = None
        self._app_name = None
        self._https = None
        self._site_name = None
        self._site = None


    
    def get_settings(self):
        print()
        print()
        print("#############################################")
        print("# Welcome to Nginx, Flask, and uWSGI setup. #")
        print("#############################################")
        print()
        self._username = input("What's the name the user? ")
        self._password = getpass.getpass(prompt = "Password: ")
        self._app_name = input("What's your app name? ")
        self._site = input("Site name? (e.g., cool-site.com) ")
        res = input("Setup HTTPS? (y/n) ")
        self._https = True if res.lower() == "y" else False
        print()

        self._site_name = self._site.split(".")[0]

    def prepare(self):
        raise NotImplementedError

    def install_dev_tools(self):
        raise NotImplementedError

    def create_user(self):
        raise NotImplementedError

    def firewall_setup(self):
        raise NotImplementedError

    def create_uwsgi_daemon(self):
        raise NotImplementedError

    def uwsgi_setup(self):
        print(
            """
        ###############
        # Setup uWSGI #
        ###############
        """
        )
        # Install pipenv
        exec_cmd(f"pip3 install {self.flask_pip_packages}")
        os.chdir("..")
        uwsgi_ini_path = os.getcwd() + f"/app/app.ini"
        write_uwsgi_ini(
            uwsgi_ini_path, self._username, self._password, self._app_name, self._site
        )

    def move_app_in_place(self):
        print("""
        #########################
        # Put App in Place      #
        #########################
        """)
        # Move the file to the user's directory.
        app_abs_path = f"/usr/share/nginx/{self._app_name}/"

        if os.path.exists(app_abs_path):
            exec_cmd(f"rm -rf {app_abs_path}")
            print("Deleted old files.")

        exec_cmd(f"""cp -r app/ {app_abs_path}
        chown -R nginx:nginx {app_abs_path}
        chmod -R 777 {app_abs_path}
        """)

    def setup_certificate(self):
        print("#############################################")
        print("# Time to setup HTTPs using Certbot         #")
        print("#############################################")
        exec_cmd("systemctl start nginx.service")

        exec_cmd(f"cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup")
        os.system(f"certbot -d {self._site} -d www.{self._site}")

        # Add cron job to automatically renew.
        exec_cmd("""echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q" | sudo tee -a /etc/crontab > /dev/null""")


    def setup_nginx(self):
        raise NotImplementedError

    def install_mariadb(self):
        raise NotImplementedError

    def setup_mariadb(self):
        print(f"""
        ############################################################
        # Creating DB {app_name} and user {app_name}               #
        ############################################################
        """)
        exec_mysql_cmd(f"""
        CREATE DATABASE {app_name};
        CREATE USER {app_name}@localhost IDENTIFIED BY '{password}';
        GRANT ALL PRIVILEGES ON {app_name}.* TO '{app_name}'@'localhost';
        FLUSH PRIVILEGES;
        """)

    def create_database_url_env_var(self):
        print(f"""
        ############################################################
        # Create the DATABASE_URL environment variable             #
        ############################################################
        """)
        exec_cmd(f"\necho '# Used by Flask app {self._app_name}' >> /home/{self._username}/.bash_profile")
        exec_cmd(f"echo 'export DATABASE_URL=mysql+pymysql://{self._app_name}:{self._password}@localhost/{self._app_name}' >> /home/{self._username}/.bash_profile")


    def create_app_symlink_for_user(self):
        print(f"""
        #########################
        # Creating symlink      #
        #########################
        """)
        exec_cmd(f"ln -s /usr/share/nginx/{self._app_name}/ /home/{self._username}/{self._app_name}")