import sys
import os
from .utils import *


class Shell:
    busybox: list[str] = [
        "exit",
        "echo",
        "type",
        "pwd",
        "cd",
    ]

    scripts = ["cat", "busybox"]

    def __init__(self):
        """
        Initializes an instance of MyClass.

        This method sets up the CommandHandler and initializes its attributes.

        Parameters:
        None

        Returns:
        None
        """
        self.handler = CommandHandler(
            self.busybox,
            self.scripts,
            path=os.environ.get("PATH", ""),
        )

    def run(self):
        """
        Runs the shell application.

        This method continuously prompts the user for input, handles the input command,
        and breaks the loop if the command is not handled.

        """
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            command_input = input().strip()

            if not self.handler.handle_command(command_input):
                break


if __name__ == "__main__":
    shell = Shell()
    shell.run()
