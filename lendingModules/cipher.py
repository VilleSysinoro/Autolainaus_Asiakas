"""A module to encrypt and decrypt text based data using symmetric encryption algorithm Fernet.
"""
# MODUULI SALAUSAVAINTEN LUOMISEEN, FERNET-SALAUKSEEN JA SEN PURKAMISEEN
# =============================================================

# KIRJASTOJEN JA MODUULIEN LATAUKSET
# ----------------------------------

from cryptography.fernet import Fernet

def newKey() -> str: 
    """Creates a new key for encrypting and decrypting messages

    Returns:
        str: a key in byte form
    """
    key = Fernet.generate_key()
    return key

def createChipher(key: str) -> object:
    """Creates a new chipher ie. encrypting machine

    Args:
        key (str): A fernet generated key

    Returns:
        object: The cipher objet to use to encrypt or decrypt
    """
    chipher = Fernet(key)
    return chipher

def encrypt(chipher: object, plainText: bytes) -> str:
    """Encrypts a message usinf Fernet algorithm

    Args:
        chipher (object): Fernet chiphering engine
        plainText (str): Text to be encrypted

    Returns:
        str: encrypted text in byte format
    """
    cryptoText = chipher.encrypt(plainText)
    return cryptoText

def decrypt(chipher: object, cryptoText: str, byteMode: bool=False) -> str:
    """Decrypts a message

    Args:
        chipher (object): Decrypting engine
        cryptoText (str): Encrypted text to be decrypted
        byteMode (bool, optional): If return value will be in byte form. Defaults to False.

    Returns:
        str: message in plain text
    """
    if byteMode == True:
        plaintext = chipher.decrypt(cryptoText)
    else:
        plaintext = chipher.decrypt(cryptoText).decode()
    return plaintext

def encryptString(plainText: str, key=b'8Zra5xvI3derJNwLCue1iDdw0lbZm_T0zXFaBknPXI4=') -> str:
    """Encrypts a block of plain text into Fernet string

    Args:
        plainText (str): The text to be encrypted
        key (bytes, optional): A secret key. Defaults to b'8Zra5xvI3derJNwLCue1iDdw0lbZm_T0zXFaBknPXI4='.

    Returns:
        str: Encrypted string
    """
    chipherEngine = createChipher(key) # Luodaan salausmoottori
    byteForm = plainText.encode() # Käytetään tavukoodiksi muuntoon kirjaston encode-metodia
    cryptoText = encrypt(chipherEngine, byteForm).decode() # Muunnetaan salattu teksti merkkijonoksi decode-metodilla
    return cryptoText

def decryptString(cryptoText: str, key=b'8Zra5xvI3derJNwLCue1iDdw0lbZm_T0zXFaBknPXI4=') -> str:
    """Decrypts a Fernet encrypted string to a plain text string

    Args:
        cryptoText (str): Encrypted block of text
        key (bytes, optional): A secret key. Defaults to b'8Zra5xvI3derJNwLCue1iDdw0lbZm_T0zXFaBknPXI4='.

    Returns:
        str: Plain text version of the encrypted text block
    """
    chipherEngine = createChipher(key)
    plainText = decrypt(chipherEngine, cryptoText)
    return plainText



if __name__ == "__main__":

    selko = 'Hippopotamus'
    sala = encryptString(selko)
    print('Salakirjoitettuna se on:', sala)
    purettu = decryptString(sala)
    print('Purettuna se on:', purettu)
