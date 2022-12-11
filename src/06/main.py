import os
from collections import deque

START_OF_PACKET_MARKER_LENGTH = 4
START_OF_MESSAGE_MARKER_LENGTH = 14


def main():
    with open(os.path.dirname(__file__) + "/input.txt") as f:
        lines = f.read().split("\n")

    print(get_start_of(lines[0], START_OF_PACKET_MARKER_LENGTH))
    print(get_start_of(lines[0], START_OF_MESSAGE_MARKER_LENGTH))


def get_start_of(data, length):
    window = deque()
    for index, char in enumerate(data):
        if len(window) == length:
            window.popleft()

        window.append(char)

        if len(set(window)) == length:
            return index + 1


if __name__ == '__main__':
    main()
