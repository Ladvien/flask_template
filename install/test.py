import os

nginx_and_tools = " ".join([
    "epel-release",
    "nginx",
    "certbot",
    "python2-certbot-nginx",
])

os.system(f"chown $USER:$USER /home/{username}/{app_name}/{site_name}.crt /home/{username}/{app_name}/{site_name}.key")