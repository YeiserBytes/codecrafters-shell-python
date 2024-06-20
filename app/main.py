import sys


def main():
    busybox = [
        "echo"
    ]

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input()

        # Exit the shell
        if command == "exit" or command == "exit 0":
            break

        if command not in busybox:
            sys.stdout.write(f'{command}: command not found\n')
            continue

        # Execute the command
        for input in command.split(" "):
            sys.stdout.write(f"{input[2]}\n")
            continue




if __name__ == "__main__":
    main()
