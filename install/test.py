import os

nginx_and_tools = " ".join([
    "epel-release",
    "nginx",
    "certbot",
    "python2-certbot-nginx",
])

os.system(f"yum install {nginx_and_tools} -y")