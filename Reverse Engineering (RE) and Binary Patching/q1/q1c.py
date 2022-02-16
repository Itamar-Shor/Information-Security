def fix_message_data(data: bytes) -> bytes:
    """
    Implement this function to return the "fixed" message content. This message
    should have minimal differences from the original message, but should pass
    the check of `msgcheck`.

    The fix in this file should be *different* than the fix in q1b.py.

    :param data: The source message data.
    :return: The fixed message data.
    """
    if len(data) >= 2:
        modify_data = bytearray(data)
        nof_iterations = min(data[0] + 2, len(data))
        xor_byte = bytearray([166])                     # 0xA6
        for idx in range(2, nof_iterations):
            xor_byte[0] ^= data[idx]
        modify_data[1] = xor_byte[0]
    else:                                               # just in case
        modify_data = bytearray(6)
        modify_data[0] = 2
        modify_data[1] = 166 ^ 44 ^ 55
        modify_data[2] = 44
        modify_data[3] = 55
    return bytes(modify_data)

def fix_message(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    fixed_data = fix_message_data(data)
    with open(path + '.fixed', 'wb') as writer:
        writer.write(fixed_data)


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    fix_message(path)
    print('done')


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
