from q2_atm import ATM, ServerResponse
import math

def extract_PIN(encrypted_PIN) -> int:
    """Extracts the original PIN string from an encrypted PIN."""
    # four digit number times 3 is always smaller then 2024 bit public key, so the modulo is doing nothing
    for first_digit in range(10):
        for second_digit in range(10):
            for third_digit in range(10):
                for fourth_digit in range(10):
                    pin = fourth_digit*1000 + third_digit*100 + second_digit*10 + first_digit
                    if (ATM().encrypt_PIN(pin)) == encrypted_PIN:
                        return pin



def extract_credit_card(encrypted_credit_card) -> int:
    """Extracts a credit card number string from its ciphertext."""
    return round(encrypted_credit_card**(1/3)) # e = 3


def forge_signature():
    """Forge a server response that passes verification."""
    # Return a ServerResponse instance.
    return ServerResponse(ATM.CODE_APPROVAL, 1)     # 1^e mod (n) == 1 
