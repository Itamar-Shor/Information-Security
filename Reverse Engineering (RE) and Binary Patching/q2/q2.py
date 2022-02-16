from infosec.utils import assemble


def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    execute lines starting with #!, and print all other lines as-is.

    Use the `assemble` module to translate assembly to bytes. For help, in the
    command line run:

        ipython3 -c 'from infosec.utils import assemble; help(assemble)'

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    modify_program = bytearray(program)
    large_dead_zone = int("5CD" ,16)
    little_dead_zone = int("633", 16)
    redirect_patch = assemble.assemble_file("patch1.asm")
    actual_patch = assemble.assemble_file("patch2.asm")
    for idx in range(len(redirect_patch)):
        modify_program[little_dead_zone+idx] = redirect_patch[idx]
    for idx in range(len(actual_patch)):
        modify_program[large_dead_zone+idx] = actual_patch[idx]
    return bytes(modify_program)


def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <readfile-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
