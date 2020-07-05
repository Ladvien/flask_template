def execute_command_block(commands):
    try:
        for command in commands.split("\n"):
            command = command.strip()
            os.system(command)
    except Exception as e:
        print(f"Error: {e}")
        return 