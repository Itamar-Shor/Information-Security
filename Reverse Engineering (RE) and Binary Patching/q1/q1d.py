def patch_program_data(program: bytes) -> bytes:
    """
    Implement this function to return the patched program. This program should
    return 0 for all input files.

    :param data: The bytes of the source program.
    :return: The bytes of the patched program.
    """
    modify_program = bytearray(program)
    offset = int("594", 16)
    modify_program[offset] = int("90", 16)      # nop
    modify_program[offset + 1] = int("38", 16)  # cmp al, al
    modify_program[offset + 2] = int("c0", 16)
    return bytes(modify_program)



def patch_program(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    patched = patch_program_data(data)
    with open(path + '.patched', 'wb') as writer:
        writer.write(patched)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msgcheck-program>'.format(argv[0]))
        return -1
    path = argv[1]
    patch_program(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
