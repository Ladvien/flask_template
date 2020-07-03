import os

nginx_and_tools = " ".join([
    "epel-release",
    "nginx",
    "certbot",
    "python2-certbot-nginx",
])

os.system(f"sudo certbot -d maddatum.com -d www.maddatum.com")