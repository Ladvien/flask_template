import os

# Update the system.
os.system("yum update -y")

# Install needed dev tools.
os.system("""yum install python3-pip python36-devel.x86_64 gcc gcc-c++\
             make openssl-devel libffi libffi-devel python3-setuptools -y""")

# Install Nginx
os.system("yum install epel-release nginx -y")

# Install pipenv
os.system("pip3 install pipenv")

# Setup environment
os.system("pipenv install flask Flask-SQLAlchemy uwsgi")

