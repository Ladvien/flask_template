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