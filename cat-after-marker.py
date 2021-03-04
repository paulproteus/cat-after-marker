#!/usr/bin/env python3

import os
import sys


def cat_to_stderr_until_marker(stdin, stderr):
    # Read stdin until we see MARKER. Copy data to stderr.
    marker = b'MARKER\n'
    buffer = b''

    byte = stdin.read(1)
    while byte != b'':  # If it's b'', then we're at end of file.
        next_expected_marker_byte = marker[len(buffer):len(buffer)+1]
        marker_match = byte == next_expected_marker_byte

        # If it's a match for the marker, store it. Otherwise, print the byte, flush the buffer, get next byte.
        if marker_match:
            buffer += byte
        else:
            stderr.write(byte)
            stderr.write(buffer)
            buffer = b''

        # If the buffer contents are the marker, print the marker to stderr, and return.
        if len(buffer) == len(marker) and buffer == marker:
            stderr.write(buffer)
            stderr.write(b"*** Connecting stdin and stdout now ***\n")
            return

        # Get next character
        byte = stdin.read(1)


def cat(stdin, stdout):
    # Copy stdin to stdout until stdin is empty.
    # Assume stdin & stdout are binary, unbuffered.
    # Read characters 1 at a time to avoid problems arising from buffering.
    while True:
        byte = stdin.read(1)
        if byte == b'':
            return  # Reached EOF; exit early.
        stdout.write(byte)


def main():
    # Create unbuffered stdio to avoid problems arising from buffering.
    stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
    stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)
    stderr = os.fdopen(sys.stderr.fileno(), 'wb', 0)

    cat_to_stderr_until_marker(stdin, stderr)
    cat(stdin, stdout)


if __name__ == '__main__':
    main()
