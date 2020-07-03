import os

nginx_and_tools = " ".join([
    "epel-release",
    "nginx",
    "certbot",
    "python2-certbot-nginx",
])

os.system(f"sudo certbot --nginx -d maddatum.com -d www.maddatum.com")
os.system(f"mv /etc/letsencrypt/live/maddatum.com/cert.pem /home/ladvien/self_sensored/maddatum.crt")
os.system(f"mv /etc/letsencrypt/live/maddatum.com/privkey.pem /home/ladvien/self_sensored/maddatum.key")