import os

os.system(f"systemctl stop nginx.service")
os.system(f"systemctl stop self_sensored.service")