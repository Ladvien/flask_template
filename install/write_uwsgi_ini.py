import os

def write_uwsgi_ini(write_path, username, password, app_name, site):
    site_name = site.split(".")[0]
    file_str =\
f"""[uwsgi]
module = wsgi:app
uid = nginx
gid = nginx
https = =0,{app_name}.crt,{app_name}.key,HIGH
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