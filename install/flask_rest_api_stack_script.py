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
from util import exec_cmd

# Resources used
# https://phoenixnap.com/kb/how-to-install-nginx-on-centos-7

print()
print()
print("#############################################")
print("# Welcome to Nginx, Flask, and uWSGI setup. #")
print("#############################################")
print()
username = input("What's the name the user? ")
password = getpass.getpass(prompt = "Password: ")
app_name = input("What's your app name? ")
site = input("Site name? (e.g., cool-site.com) ")
print()

site_name = site.split(".")[0]

# Update the system.
exec_cmd("yum update -y")

# Install extra packages for RedHat
exec_cmd("yum install epel-release -y")

centos_dev_tools = " ".join([
        "python3-pip",
        "python3-devel",
        "gcc", 
        "gcc-c++",
        "make", 
        "openssl-devel",
        "libffi",
        "libffi-devel",
        "python3-setuptools",
])

nginx_and_tools = " ".join([
    "nginx",
    "certbot",
    "python2-certbot-nginx",
])

pip_packages = " ".join([
    "flask",
    "Flask-SQLAlchemy",
    "uwsgi",
])

print("""
#################
# Install Tools #
#################
""")
# Install needed dev tools.
exec_cmd(f"yum install {centos_dev_tools} -y")

# Install Nginx
exec_cmd(f"yum install {nginx_and_tools} -y")

print("""
#################
# Env. Setup    #
#################
""")

# Setup user
cmd_user_setup = f"""adduser {username}
echo "{password}" | passwd --stdin {username}
usermod -aG wheel {username}
"""
exec_cmd(cmd_user_setup)

# Open CentoS firewall
cmd_firewall_setup =\
"""firewall-cmd --zone=public --permanent --add-service=http
firewall-cmd --zone=public --permanent --add-service=https
firewall-cmd --reload
"""
exec_cmd(cmd_firewall_setup)

#################
# Setup Certbot #
#################

# TODO: Configure Nginx.
# TODO: Certbot
# TODO: Install MariaDB

print("""
#################
# Create Daemon #
#################
""")
os.chdir("..")
daemon_file_path = os.getcwd() + f"/resources/{app_name}.service"
write_uwsgi_daemon(daemon_file_path, username, password, app_name, site)
os.chdir("./install")
exec_cmd(f"mv {daemon_file_path} /etc/systemd/system/{app_name}.service")
exec_cmd(f"chmod +rw /etc/systemd/system/{app_name}.service")

print("""
###############
# Setup uWSGI #
###############
""")
# Install pipenv
exec_cmd(f"pip3 install {pip_packages}")
os.chdir("..")
uwsgi_ini_path = os.getcwd() + f"/app/app.ini"
write_uwsgi_ini(uwsgi_ini_path, username, password, app_name, site)

print("""
#########################
# Put App in Place      #
#########################
""")
# Move the file to the user's directory.
app_abs_path = f"/usr/share/nginx/{app_name}/"

if os.path.exists(app_abs_path):
    exec_cmd(f"rm -rf {app_abs_path}")
    print("Deleted old files.")

exec_cmd(f"""cp -r app/ {app_abs_path}
chown -R nginx:nginx {app_abs_path}
chmod -R 777 {app_abs_path}
""")

print("""
#########################
# Start App Service     #
#########################
""")
exec_cmd(f"""systemctl enable {app_name}.service
systemctl start {app_name}.service""")

print("""
#########################
# Setup HTTPs for Nginx #
#########################
""")

print("#############################################")
print("# Time to setup HTTPs using Certbot         #")
print("#############################################")
print()
exec_cmd("systemctl start nginx.service")

# os.system(f"sudo certbot --nginx -d maddatum.com -d www.maddatum.com")

# Add cron job to automatically renew.
exec_cmd("""echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q" | sudo tee -a /etc/crontab > /dev/null""")

print("""
###############
# Setup Nginx #
###############
""")
write_nginx_conf("/etc/nginx/nginx.conf", username, password, app_name, site)
exec_cmd("""systemctl daemon-reload
systemctl restart nginx
""")

print("""
###################
# Daemonize Flask #
###################
""")
exec_cmd(f"systemctl restart {app_name}.service")

print("""
####################################
# Add Nginx Permissions to SELinux #
####################################
""")
exec_cmd("""setenforce Permissive
grep nginx /var/log/audit/audit.log | audit2allow -M nginx
semodule -i nginx.pp
setenforce Enforcing
""")

print("""
####################################
# Installing MariaDB               #
####################################
""")
cmd_mariadb_setup = """
yum install wget -y
wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
chmod +x mariadb_repo_setup
./mariadb_repo_setup
rm mariadb_repo_setup
yum install MariaDB-server -y
systemctl enable mysql.service
systemctl start mysql.service
mysql_secure_installation
"""
exec_cmd(cmd_mariadb_setup)