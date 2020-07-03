import os
import pip
import getpass
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
print()
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

#################
# Install Tools #
#################
# Install needed dev tools.
os.system(f"yum install {centos_dev_tools} -y")

# Install Nginx
os.system(f"yum install {nginx_and_tools} -y")

#################
# Env. Setup    #
#################

# 1. Setup user
os.system(f"adduser {username}")
os.system(f"""echo "{password}" | passwd --stdin {username}""")
os.system(f"usermod -aG wheel {username}")

# Move the file to the user's directory.
app_abs_path = f"/home/{username}/{app_name}/"
os.system(f"cp -r ../app/ {app_abs_path}")
os.system(f"chown -R {username}:{username} {app_abs_path}")

###############
# Setup Nginx #
###############
# Start Nginx
os.system("systemctl enable nginx")
os.system("systemctl start nginx")

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

#################
# Create Daemon #
#################
os.chdir("..")
daemon_file_path = os.getcwd() + f"/resources/{app_name}.service"
with open(daemon_file_path, "w") as f:
    f.write(f"""[Unit]
Description=uWSGI instance to serve {app_name}
After=network.target

[Service]
Restart=always
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

###############
# Setup uWSGI #
###############
# Install pipenv
os.system(f"pip3 install {pip_packages}")


###################
# Daemonize Flask #
###################
os.system(f"systemctl enable {app_name}.service")
os.system(f"systemctl start {app_name}.service")
