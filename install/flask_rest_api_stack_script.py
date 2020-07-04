import os
import pip
import getpass

from write_nginx_conf import write_nginx_conf

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
os.system("yum update -y")

# Install extra packages for RedHat
os.system("yum install epel-release -y")

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
os.system(f"yum install {centos_dev_tools} -y")

# Install Nginx
os.system(f"yum install {nginx_and_tools} -y")

print("""
#################
# Env. Setup    #
#################
""")

# 1. Setup user
os.system(f"adduser {username}")
os.system(f"""echo "{password}" | passwd --stdin {username}""")
os.system(f"usermod -aG wheel {username}")

# Open CentoS firewall
os.system("firewall-cmd --zone=public --permanent --add-service=http")
os.system("firewall-cmd --zone=public --permanent --add-service=https")
os.system("firewall-cmd --zone=public --add-port=5000/tcp --permanent")
os.system("firewall-cmd --reload")

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
with open(daemon_file_path, "w") as f:
    f.write(f"""[Unit]
Description=uWSGI instance to serve {app_name}
After=network.target

[Service]
User={username}
Group=nginx
WorkingDirectory=/home/{username}/{app_name}/
ExecStart=/usr/local/bin/uwsgi --ini /home/{username}/{app_name}/app.ini
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
""")
os.chdir("./install")
os.system(f"mv {daemon_file_path} /etc/systemd/system/{app_name}.service")
os.system(f"chmod +rw /etc/systemd/system/{app_name}.service")

print("""
###############
# Setup uWSGI #
###############
""")
# Install pipenv
os.system(f"pip3 install {pip_packages}")
os.chdir("..")
uwsgi_ini_path = os.getcwd() + f"/app/app.ini"
with open(uwsgi_ini_path, "w") as f:
    f.write(f"""[uwsgi]
module = wsgi:app

master = true
processes = 5

http-socket = :5000

uid = {username}
socket = /home/{username}/{app_name}/app.sock
chown-socket = {username}:nginx
chmod-socket = 660
vacuum = true

die-on-term = true
""")

print("""
#########################
# Put App in Place      #
#########################
""")
# Move the file to the user's directory.
app_abs_path = f"/home/{username}/{app_name}/"
os.system(f"cp -r app/ {app_abs_path}")
os.system(f"chown -R {username}:nginx {app_abs_path}")
os.system(f"chmod -R 710 /home/{username} ")

print("""
#########################
# Start App Service     #
#########################
""")
os.system(f"systemctl enable {app_name}.service")
os.system(f"systemctl start {app_name}.service")

print("""
#########################
# Setup HTTPs for Nginx #
#########################
""")

print("#############################################")
print("# Time to setup HTTPs using Certbot         #")
print("#############################################")
print()
os.system("systemctl start nginx.service")

# os.system(f"sudo certbot --nginx -d maddatum.com -d www.maddatum.com")

# Add cron job to automatically renew.
os.system("""echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q" | sudo tee -a /etc/crontab > /dev/null""")

print("""
###############
# Setup Nginx #
###############
""")
write_nginx_conf("/etc/nginx/nginx.conf", username, password, app_name, site)
os.system("systemctl daemon-reload")
os.system("systemctl restart nginx")

print("""
###################
# Daemonize Flask #
###################
""")
os.system(f"systemctl restart {app_name}.service")