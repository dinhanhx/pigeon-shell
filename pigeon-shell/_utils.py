from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from pathlib import Path

from pickle import dumps, loads


def encode_encrypt(cmd: str, public_key: RSA.RsaKey):
    """Encode a command then encrypt with RSA public key

    Parameters:
        cmd: str << a command
        public_key: RSA.RsaKey << RSA.import_key()

    Returns:
        An encrypted byte string << pickle.dumps()
    """
    encoded_cmd = cmd.encode()
    session_key = get_random_bytes(16)

    cipher_RSA = PKCS1_OAEP.new(key=public_key)
    encrypted_session_key = cipher_RSA.encrypt(session_key)

    cipher_AES = AES.new(session_key, AES.MODE_EAX)
    encrypted_cmd, tag = cipher_AES.encrypt_and_digest(encoded_cmd)

    bundle = (encrypted_session_key, cipher_AES.nonce, tag, encrypted_cmd)
    return dumps(bundle)


def decrypt_decode(bundle: bytes, private_key: RSA.RsaKey):
    """Decrypt a command with RSA private key then encode

    Parameters:
        bundle: bytes << an encrypted byte string
        private_key: RSA.RsaKey << RSA.import_key()

    Returns:
        A string
    """
    session_key, nonce, tag, encrypted_cmd = loads(bundle)

    cipher_RSA = PKCS1_OAEP.new(key=private_key)
    session_key = cipher_RSA.decrypt(session_key)

    cipher_AES = AES.new(session_key, AES.MODE_EAX, nonce)
    encoded_cmd = cipher_AES.decrypt_and_verify(encrypted_cmd, tag)
    
    return encoded_cmd.decode()


def import_key(private_key_file: str, public_key_file):
    """Import keys from a directory

    Parameters:
        private_key_file: str << Filepath where private key is saved
        public_key_file: str << Filepath to where public key is saved
    
    Returns:
        private_key, public_key: RSA.RsaKey
    """
    private_key_file = Path(private_key_file)
    public_key_file = Path(public_key_file)

    private_key = RSA.import_key(open(private_key_file, 'r').read())
    public_key = RSA.import_key(open(public_key_file, 'r').read())
    return private_key, public_key


if __name__ == '__main__':
    private_key, public_key = import_key('client/private.pigeon.txt', 'client/public.pigeon.txt')

    cmd = 'ls'

    print(decrypt_decode(encode_encrypt(cmd, public_key), private_key))