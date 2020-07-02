import os
import pip


# For safe password entering.
pip.main(["install", "stdiomask"])
import stdiomask

print("Welcome to Nginx, Flask, and uWSGI setup.")
username = input("What's the name the user? ")
password = stdiomask.getpass()

# Update the system.
# os.system("yum update -y")

# Install needed dev tools.
# os.system("""yum install python3-pip python36-devel.x86_64 gcc gcc-c++\
#              make openssl-devel libffi libffi-devel python3-setuptools -y""")

# Install Nginx
# os.system("yum install epel-release nginx -y")

# 1. Setup user
os.system(f"adduser {username}")
os.system(f"""echo "{password}" | passwd --stdin {username}""")
os.system(f"usermod -aG wheel {username}")

# 2. Setup Nginx.

# 3. Setup uWSGI.
# Install pipenv
# os.system("pip3 install pipenv")
# Setup environment
# os.system("pipenv install flask Flask-SQLAlchemy uwsgi")

