import sys
import os
import subprocess


class CommandHandler:
    def __init__(self, busybox, scripts, path):
        self.busybox = busybox
        self.scripts = scripts
        self.paths = path.split(":")

    def handle_command(self, command_input):
        command_parts = command_input.split()
        if not command_parts:
            return True  # Continue running

        command = command_parts[0]
        args = command_parts[1:]

        if command in ("exit", "exit 0"):
            return False  # Stop running

        if command == "pwd":
            self.pwd_command()
        elif command == self.busybox["echo"]:
            self.echo_command(args)
        elif command == self.busybox["type"]:
            self.type_command(args)
        else:
            self.execute_external_command([command] + args)

        return True  # Continue running

    def pwd_command(self):
        sys.stdout.write(os.getcwd() + "\n")

    def execute_external_command(self, command_parts):
        try:
            result = subprocess.run(
                command_parts, check=True, capture_output=True, text=True
            )
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)
        except subprocess.CalledProcessError as e:
            sys.stderr.write(e.stderr)
        except FileNotFoundError:
            sys.stderr.write(f"{command_parts[0]}: command not found\n")

    def echo_command(self, args):
        sys.stdout.write(f"{' '.join(args)}\n")

    def type_command(self, args):
        if not args:
            sys.stdout.write("type: missing argument\n")
            return

        command_to_find = args[0]
        if command_to_find in self.busybox:
            sys.stdout.write(f"{command_to_find} is a shell builtin\n")
        elif command_to_find in self.scripts:
            sys.stdout.write(f"{command_to_find} is /bin/{command_to_find}\n")
        else:
            cmd_path = self.find_command_in_path(command_to_find)
            if cmd_path:
                sys.stdout.write(f"{command_to_find} is {cmd_path}\n")
            else:
                sys.stdout.write(f"{command_to_find}: not found\n")

    def unknown_command(self, command):
        sys.stdout.write(f"{command}: command not found\n")

    def find_command_in_path(self, command):
        for path in self.paths:
            cmd_path = os.path.join(path, command)
            if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                return cmd_path
        return None
