import os
port_num = "5000"
print(f"Disabling the firewall for port {port_num}.")
os.system("sudo firewall-cmd --zone=public --add-port=5000/tcp --permanent")
os.system("sudo firewall-cmd --reload")
try:
    os.system("python3 app.py")
except:
    pass
finally:
    print(f"Re-enabling the firewall for port {port_num}.")
    os.system("sudo firewall-cmd --zone=public --remove-port=5000/tcp --permanent")
    os.system("sudo firewall-cmd --reload")