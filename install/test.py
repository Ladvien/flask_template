import os

commands = """
sudo yum install wget -y
wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
chmod +x mariadb_repo_setup
sudo ./mariadb_repo_setup
"""
execute_command_block(commands)