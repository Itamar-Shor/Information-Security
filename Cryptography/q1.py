class RepeatedKeyCipher:

    def __init__(self, key: bytes = bytes([0, 0, 0, 0, 0])):
        """Initializes the object with a list of integers between 0 and 255."""
        # WARNING: DON'T EDIT THIS FUNCTION!
        self.key = list(key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypts a given plaintext string and returns the ciphertext."""
        message = bytearray(plaintext, 'latin1')  # bytearray is mutable
        for i in range(len(message)):
            message[i] ^= self.key[i%len(self.key)]
        return bytes(message)  # return bytes and not bytearray

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypts a given ciphertext string and returns the plaintext."""
        text = str(ciphertext, 'latin1')
        res_bytes = self.encrypt(text)      # double xor with the key to decrypt
        return res_bytes.decode('latin1')

class BreakerAssistant:

    letter_frequencies = {' ':8.5, 'a': 8.2, 'b':1.5, 'c':2.5, 'd':4.3, 'e':13, 'f':2.2, 'g':2, 'h':6.1, 'i':7, 'j':0.15, 'k':0.77, 'l':4, 'm':2.4, 'n':6.7, 'o':7.5, 'p':1.9, 'q':0.095, 'r':6, 's':6.3, 't':9.1, 'u':2.8, 'v':0.98, 'w':2.4, 'x':0.15, 'y':2, 'z':0.074} 

    def plaintext_score(self, plaintext: str) -> float:
        """Scores a candidate plaintext string, higher means more likely."""
        # Please don't return complex numbers, that would be just annoying.
        # idea taken from: https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
        N_obs = {letter:0 for letter in self.letter_frequencies}
        for char in plaintext:
            if char in N_obs:
                N_obs[char.lower()] += 1
        score = sum([((N_obs[c]-self.letter_frequencies[c]*len(plaintext))**2)/(self.letter_frequencies[c]*len(plaintext)) for c in self.letter_frequencies])
        return (1 / (1+score))


    def brute_force(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        if key_length == 0:
            print("got key lenght = 0, aborting break")
            exit(-1)
        key = 0             # init key = 0x0
        cipher = RepeatedKeyCipher(key.to_bytes(key_length, byteorder='big'))
        max_score = -1     # init
        text = ""
        nof_keys = 1<<(key_length * 8)
        for i in range(nof_keys - 1):
            curr_try = cipher.decrypt(cipher_text)
            curr_score = self.plaintext_score(curr_try)
            if curr_score > max_score:
                max_score, text = curr_score, curr_try
            key += 1
            cipher.key = key.to_bytes(key_length, byteorder='big')  # next key
        curr_try = cipher.decrypt(cipher_text)
        curr_score = self.plaintext_score(curr_try)
        if curr_score > max_score:
            max_score, text = curr_score, curr_try
        return text
        
    def smarter_break(self, cipher_text: bytes, key_length: int) -> str:
        """Breaks a Repeated Key Cipher any way you like."""
        same_key_byte_text = [[] for i in range(key_length)]
        for text_byte_idx in range(len(cipher_text)):
            same_key_byte_text[text_byte_idx%key_length].append(cipher_text[text_byte_idx])
        text = ["" for i in range(len(cipher_text))]

        for key_byte_idx in range(key_length):
            count = 0
            curr_text = self.brute_force(bytes(same_key_byte_text[key_byte_idx]), 1)
            for char in curr_text:
                text[key_byte_idx + key_length*count] = char
                count += 1
        return "".join(text)