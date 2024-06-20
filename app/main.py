import sys
import os

def get_command_message(command):
    return " ".join(command[1:])

def is_builtin_command(command, builtins):
    return command in builtins

def is_script_command(command, scripts):
    return command in scripts

def find_command_in_path(command, paths):
    for path in paths:
        cmd_path = os.path.join(path, command)
        if os.path.isfile(cmd_path):
            return cmd_path
    return None

def main():
    busybox = {
        "exit": "exit",
        "echo": "echo",
        "type": "type"
    }

    scripts = ["cat"]
    PATH = os.environ.get("PATH", "")
    paths = PATH.split(":")

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command_input = input().strip()

        if command_input in ("exit", "exit 0"):
            break

        command_parts = command_input.split()
        if not command_parts:
            continue

        command = command_parts[0]

        if command == busybox["echo"]:
            sys.stdout.write(f"{get_command_message(command_parts)}\n")
        elif command == busybox["type"]:
            command_to_find = command_parts[1] if len(command_parts) > 1 else ""
            if is_builtin_command(command_to_find, busybox):
                sys.stdout.write(f"{command_to_find} is a shell builtin\n")
            elif is_script_command(command_to_find, scripts):
                sys.stdout.write(f"{command_to_find} is /bin/{command_to_find}\n")
            else:
                cmd_path = find_command_in_path(command_to_find, paths)
                if cmd_path:
                    sys.stdout.write(f"{command_to_find} is {cmd_path}\n")
                else:
                    sys.stdout.write(f"{command_to_find}: not found\n")
        else:
            sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    main()
