# Copyright (c) 2025 Jifeng Wu
# Licensed under the <license> License. See LICENSE file in the project root for full license information.
from base64 import b64encode
from io import DEFAULT_BUFFER_SIZE
from mimetypes import guess_type
from typing import Iterator, Text


def generate_chunks_to_b64encode(filepath, buffer_size=DEFAULT_BUFFER_SIZE):
    # type: (str, int) -> Iterator[bytes]
    with open(filepath, 'rb') as file_pointer:
        leftover_bytes_not_yet_yielded = b''

        while True:
            bytes_just_read_from_file = file_pointer.read(buffer_size)
            if not bytes_just_read_from_file:
                # No more data to read; exit the loop after handling leftovers
                break

            bytes_combined_for_encoding = leftover_bytes_not_yet_yielded + bytes_just_read_from_file

            # Base64 encoding operates on sequences of 3 bytes. Calculate how many full groups of 3 we have.
            number_of_full_3byte_groups = len(bytes_combined_for_encoding) // 3
            number_of_bytes_to_encode_now = number_of_full_3byte_groups * 3

            bytes_to_encode_now = bytes_combined_for_encoding[:number_of_bytes_to_encode_now]
            leftover_bytes_not_yet_yielded = bytes_combined_for_encoding[number_of_bytes_to_encode_now:]

            if len(bytes_to_encode_now) > 0:
                yield bytes_to_encode_now

        # After all file data has been read, yield any remaining bytes (1 or 2) for final base64 encoding.
        if len(leftover_bytes_not_yet_yielded) > 0:
            yield leftover_bytes_not_yet_yielded


def unicode_base64_data_uri_fragments_generator(filepath, buffer_size=DEFAULT_BUFFER_SIZE):
    # type: (str, int) -> Iterator[Text]
    """
    Yields fragments of a base64 data URI representing a file.

    This generator yields the header (with detected MIME type) and then base64-encoded chunks of the file, so the file is never fully loaded into memory at once.
    """
    # Guess MIME type
    mime, _ = guess_type(filepath)

    # Generate the URI head
    yield u'data:%s;base64,' % (mime or u'application/octet-stream',)

    # Generate base64 fragments from file chunks
    for chunk in generate_chunks_to_b64encode(filepath, buffer_size):
        yield b64encode(chunk).decode('ascii')


def file_to_unicode_base64_data_uri(filepath, buffer_size=DEFAULT_BUFFER_SIZE):
    # type: (str, int) -> Text
    """Returns the base64 data URI representing a file."""
    return u''.join(unicode_base64_data_uri_fragments_generator(filepath, buffer_size))
