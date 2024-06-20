import sys


def main():
    busybox = [
        "exit",
        "echo",
        "type"
    ]

    scripts = [
        "cat"
    ]

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input()

        # Exit the shell
        if command == busybox[0] or command == "exit 0":
            break

        if command.split(" ")[0] not in busybox:
            sys.stdout.write(f'{command}: command not found\n')
            continue

        if command.split(" ")[0] == busybox[1]:
            command = command.split(" ")
            message = " ".join(command[1:])
            sys.stdout.write(f"{message}\n")
            continue

        if command.split(" ")[0] == busybox[2]:
            command = command.split(" ")
            message = command[1]

            if message in busybox:
                sys.stdout.write(f"{message} is a shell builtin\n")
                continue
            elif message in scripts:
                sys.stdout.write(f"{message} is /bin/{message}\n")
                continue
            else:
                sys.stdout.write(f"{message}: not found\n")
                continue




if __name__ == "__main__":
    main()
