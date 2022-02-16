def check_message(path: str) -> bool:
    """
    Return True if `msgcheck` would return 0 for the file at the specified path,
    return False otherwise.
    :param path: The file path.
    :return: True or False.
    """
    with open(path, 'rb') as reader:
        # Read data from the file, do whatever magic you need
        data = reader.read(256 + 2)  # it's not neccessary to read more then 256 + 2 (256=max number of 1 byte, 2=first 2 bytes)
        if len(data) <= 1:
            return False
        xor_byte = bytearray([166])  # 0xA6
        nof_iterations = min(data[0] + 3, len(data))
        for idx in range(2, nof_iterations):
            xor_byte[0] ^= data[idx]
        return xor_byte[0] == data[1]


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    if check_message(path):
        print('valid message')
        return 0
    else:
        print('invalid message')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
