import os

def write_uwsgi_daemon(write_path, username, password, app_name, site):
    site_name = site.split(".")[0]
    file_str =\
f"""[Unit]
Description=uWSGI instance to serve {app_name}
After=network.target

[Service]
User=nginx
Group=nginx
Environment=DATABASE_URL=mysql+pymysql://{app_name}:{password}@localhost/{app_name},
WorkingDirectory=/usr/share/nginx/{app_name}/
ExecStart=/usr/local/bin/uwsgi --ini /usr/share/nginx/{app_name}/app.ini
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(write_path, "w") as f:
        f.write(file_str)