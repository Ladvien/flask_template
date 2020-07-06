import os

def write_nginx_conf(write_path, username, password, app_name, site, https):
    site_name = site.split(".")[0]

    server_block = ""
    if https:
        server_block = f"""# Settings for a TLS enabled server.
    server {{
        listen       443 ssl http2 default_server;
        listen       [::]:443 ssl http2 default_server;
        server_name {site} www.{site};

        ssl on;
        # Use certificate and key provided by Let's Encrypt:
        ssl_certificate /etc/letsencrypt/live/{site}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/{site}/privkey.pem;
        ssl_session_timeout 5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
        
        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {{
            include uwsgi_params;
            uwsgi_pass unix://usr/share/nginx/{app_name}/app.sock;
        }}

        error_page 404 /404.html;
            location = /40x.html {{
        }}

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {{
        }}
    }}"""
    else:
        server_block = f"""server {{
        listen 80;
        listen [::]:80;
        server_name {site} www.{site};
        
        location / {{
            include uwsgi_params;
            uwsgi_pass unix://usr/share/nginx/{app_name}/app.sock;
        }}
    }}"""


    nginx_file =\
f"""
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
# include /usr/share/nginx/modules/*.conf;

events {{
    worker_connections 1024;
}}

http {{
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    # include /etc/nginx/conf.d/*.conf;

    {server_block}

}}
"""
    with open(write_path, "w") as f:
        f.write(nginx_file)