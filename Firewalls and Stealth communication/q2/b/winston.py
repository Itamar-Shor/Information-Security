import socket
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding

KEY = b'Its Leviosa not Leviosar!!!!!!!!'
IV  = b'***I\'m BATMAN***'

def send_message(ip: str, port: int):
    """Send an *encrypted* message to the given ip + port.

    Julia expects the message to be encrypted, so re-implement this function accordingly.

    Notes:
    1. The encryption is based on AES.
    2. Julia and Winston already have a common shared key, just define it on your own.
    3. Mind the padding! AES works in blocks of 16 bytes.
    """
    cipher = AES.new(key=KEY, mode=AES.MODE_CBC, IV=IV)
    padder = padding.PKCS7(128).padder()     # 16 * 8 = 128
    padded_data = padder.update(b'I love you') + padder.finalize()
    connection = socket.socket()
    try:
        connection.connect((ip, port))
        connection.send(cipher.encrypt(padded_data))
    finally:
        connection.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
