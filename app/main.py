import sys


def main():
    busybox = {}

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




if __name__ == "__main__":
    main()
