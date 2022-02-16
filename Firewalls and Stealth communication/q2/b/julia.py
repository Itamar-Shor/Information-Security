import socket
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding

KEY = b'Its Leviosa not Leviosar!!!!!!!!'
IV  = b'***I\'m BATMAN***'

def receive_message(port: int) -> str:
    """Receive *encrypted* messages on the given TCP port.

    As Winston sends encrypted messages, re-implement this function so to
    be able to decrypt the messages.

    Notes:
    1. The encryption is based on AES.
    2. Julia and Winston already have a common shared key, just define it on your own.
    3. Mind the padding! AES works in blocks of 16 bytes.
    """
    cipher = AES.new(key=KEY, mode=AES.MODE_CBC, IV=IV)
    unpadder = padding.PKCS7(128).unpadder()     # 16 * 8 = 128
    listener = socket.socket()
    try:
        listener.bind(('', port))
        listener.listen(1)
        connection, address = listener.accept()
        try:
            padded_data = cipher.decrypt(connection.recv(1024))
            data = unpadder.update(padded_data) + unpadder.finalize()
            return data.decode("latin-1")
        finally:
            connection.close()
    finally:
        listener.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
