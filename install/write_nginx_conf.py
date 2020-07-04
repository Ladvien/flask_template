import os

def write_nginx_conf(write_path, username, password, app_name, site):
    site_name = site.split(".")[0]
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

    server {{
        listen 80;
        listen [::]:80;
        # real_ip_header X-Forwarded-For;
        # set_real_ip_from 127.0.0.1;
        server_name maddatum.com www.maddatum.com;
        
        location / {{
            include uwsgi_params;
            uwsgi_pass unix://usr/share/nginx/{app_name}/app.sock;
        }}
    }}

    # Settings for a TLS enabled server.
    # server {{
    #     listen       443 ssl http2 default_server;
    #     listen       [::]:443 ssl http2 default_server;
    #     real_ip_header X-Forwarded-For;
    #     set_real_ip_from 127.0.0.1;
    #     server_name localhost;

    #     ssl_certificate "/etc/letsencrypt/live/{site}/{site_name}.crt";
    #     ssl_certificate_key "/etc/letsencrypt/live/{site}/{site_name}.key";
    #     ssl_session_cache shared:SSL:1m;
    #     ssl_session_timeout  10m;
    #     # ssl_ciphers PROFILE=SYSTEM;
    #     ssl_prefer_server_ciphers on;
    #     ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;
        
    #     # Load configuration files for the default server block.
    #     include /etc/nginx/default.d/*.conf;

    #     location / {{
    #         include uwsgi_params;
    #         uwsgi_pass unix:/home/{username}/{app_name}/app.sock;
    #     }}

    #     error_page 404 /404.html;
    #         location = /40x.html {{
    #     }}

    #     error_page 500 502 503 504 /50x.html;
    #         location = /50x.html {{
    #     }}
    # }}

}}
"""
    with open(write_path, "w") as f:
        f.write(nginx_file)