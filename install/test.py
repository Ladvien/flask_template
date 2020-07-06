import os
from util import exec_cmd



exec_cmd("""
openssl genrsa -out /usr/share/nginx/self_sensored/foobar.key 2048
openssl req -new -key /usr/share/nginx/self_sensored/foobar.key -out /usr/share/nginx/self_sensored/foobar.csr
openssl x509 -req -days 365 -in /usr/share/nginx/self_sensored/foobar.csr -signkey /usr/share/nginx/self_sensored/foobar.key -out /usr/share/nginx/self_sensored/foobar.crt
""")