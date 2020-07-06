import os

def write_uwsgi_ini(write_path, username, password, app_name, site, https):
    site_name = site.split(".")[0]

    https_block = ""
    if https:
        cert_path = f"/etc/letsencrypt/live/{site}/cert.pem"
        key_path = f"/etc/letsencrypt/live/{site}/privkey.pem"
        https_block = f"https = =0,{cert_path},{key_path},HIGH"

    file_str =\
f"""[uwsgi]
module = wsgi:app
uid = nginx
gid = nginx
{https_block}
chown-socket = nginx:nginx
chmod-socket = 777

processes = 5
thread = 5
pythonpath = /usr/bin/python3
socket = /usr/share/nginx/{app_name}/app.sock

harakiri = 15
"""
    with open(write_path, "w") as f:
        f.write(file_str)