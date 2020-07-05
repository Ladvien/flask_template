import os
def exec_cmd(command_block):
    commands = command_block.split("\n")
    if len(commands) < 2:
        os.system(command_block)
        return
    else:
        try:
            for command in commands:
                command = command.strip()
                os.system(command)
        except Exception as e:
            print(f"Error: {e}")
            return 

def exec_mysql_cmd(command_block):
    commands = command_block.split("\n")
    if len(commands) < 2:
        os.system(_convert_to_sql_q(command_block))
        return
    else:
        raw_query = ""
        try:
            for command in commands:
                command = command.strip()
                if command == "":
                    continue
                if command[-1:] != ";":
                    raise Exception("MySQL query should end with a ';'.")
                raw_query += command
            os.system(_convert_to_sql_bash_query(raw_query))
        except Exception as e:
            print(f"Error: {e}")
            return  

def _convert_to_sql_bash_query(text):
    q = "mysql -e "
    q += "\""
    q += text
    q += "\""
    return q