import sys
import os
from .utils import *


class Shell:
    def __init__(self):
        self.handler = CommandHandler(
            busybox={"exit": "exit", "echo": "echo", "type": "type"},
            scripts=["cat"],
            path=os.environ.get("PATH", ""),
        )

    def run(self):
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            command_input = input().strip()

            if not self.handler.handle_command(command_input):
                break


if __name__ == "__main__":
    shell = Shell()
    shell.run()
