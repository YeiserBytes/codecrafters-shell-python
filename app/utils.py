import sys
import os
import subprocess


class CommandHandler:
    def __init__(self, busybox, scripts, path):
        """
        Initialize a new instance of the Utils class.

        Args:
            busybox (str): The path to the BusyBox executable.
            scripts (str): The path to the scripts directory.
            path (str): The value of the PATH environment variable.

        Returns:
            None
        """
        self.busybox = busybox
        self.scripts = scripts
        self.paths = path.split(":")

    def handle_command(self, command_input):
        """
        Handles the given command input.

        Args:
            command_input (str): The input command to be handled.

        Returns:
            bool: True if the program should continue running, False otherwise.
        """
        command_parts = command_input.split()
        if not command_parts:
            return True  # Continue running

        command = command_parts[0]
        args = command_parts[1:]

        if command in (self.busybox[0], "exit 0"):
            return False  # Stop running

        if command == self.busybox[3]:
            self.pwd_command()
        elif command == self.busybox[4]:
            self.cd_command(args)
        elif command == self.scripts[1]:
            commands = ''.join(', '.join(self.busybox) + ', ' + ', '.join(self.scripts))
            sys.stdout.write(commands + "\n")
        elif command == self.busybox[1]:
            self.echo_command(args)
        elif command == self.busybox[2]:
            self.type_command(args)
        else:
            self.execute_external_command([command] + args)

        return True  # Continue running

    def pwd_command(self):
        """
        Prints the current working directory to the standard output.
        """
        sys.stdout.write(os.getcwd() + "\n")

    def cd_command(self, args):
        """
        Change the current working directory.

        Args:
            args (list): List of arguments passed to the command. The first argument is the target directory.

        Raises:
            FileNotFoundError: If the target directory does not exist.
            NotADirectoryError: If the target directory is not a directory.
            PermissionError: If permission is denied to access the target directory.
        """
        if len(args) == 0:
            target_directory = os.path.expanduser(
                "~"
            )  # Go to the home directory if no argument is given
        else:
            target_directory = args[0].replace(
                "~", os.path.expanduser("~")
            )  # Replace ~ with actual home directory path

        try:
            os.chdir(target_directory)
        except FileNotFoundError:
            sys.stderr.write(f"cd: {target_directory}: No such file or directory\n")
        except NotADirectoryError:
            sys.stderr.write(f"cd: {target_directory}: Not a directory\n")
        except PermissionError:
            sys.stderr.write(f"cd: {target_directory}: Permission denied\n")

    def execute_external_command(self, command_parts):
        """
        Executes an external command and prints the output to stdout or stderr.

        Args:
            command_parts (list): A list of strings representing the command and its arguments.

        Raises:
            FileNotFoundError: If the command executable is not found.
        """
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
        """
        Prints the given arguments to the standard output.

        Args:
            args (list): A list of strings representing the arguments to be printed.

        Returns:
            None
        """
        sys.stdout.write(f"{' '.join(args)}\n")

    def type_command(self, args):
        """
        Prints the type of a given command.

        Args:
            args (list): A list of command-line arguments.

        Returns:
            None
        """
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
        """
        Prints an error message indicating that the given command is unknown.

        Parameters:
        - command (str): The unknown command.

        Returns:
        None
        """
        sys.stdout.write(f"{command}: command not found\n")

    def find_command_in_path(self, command):
        """
        Finds the specified command in the paths defined in the object.

        Args:
            command (str): The name of the command to find.

        Returns:
            str or None: The full path to the command if found, None otherwise.
        """
        for path in self.paths:
            cmd_path = os.path.join(path, command)
            if os.path.isfile(cmd_path) and os.access(cmd_path, os.X_OK):
                return cmd_path
        return None
