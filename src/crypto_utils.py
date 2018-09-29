""" Crypto functions for secure_import module

"""

# TODO: i need to do a key exchange to get a symmetric key, using asymmetric keys
# TODO: add doctest functionality
# TODO: add tests
# TODO: Salse20 does not guarantee authenticity, use HMAC for that!

__author__ = 'rsimari'
__version__ = '0.1'

from Crypto.PublicKey import RSA 
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import Salsa20
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode
from os import path


NONCE_LEN = 8

def gen_key_pair(bits=2048):
    'Generate a RSA key pair'
    """
    :param: bits: (int) size of key to generate
    :return: (private_key, public_key): (bytes, bytes) key data
    """
    new_key = RSA.generate(bits, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 

    return private_key, public_key


def write_key(key_data, file_name):
    'Write RSA key to file'
    """
    :param: key_data: (bytes) key data
    :param: file_name: (string) name of key file 
    """
    with open(file_name, 'wb+') as key_file:
        key_file.write(key_data)


def write_keys(private_key, private_file, public_key, public_file):
    'Write RSA key pair to files'
    """
    :param: private_key: (bytes) private key data
    :param: private_file: (string) name of private key file
    :param: public_key: (bytes) public key data
    :param: public_file: (string) name of public key file
    """
    write_key(private_key, private_file)
    write_key(public_key, public_file)


def write_signature(sig_data, file_name): # this is the same as write_key() ?
    'Writes a signature to a file'
    """
    :param: key_data: (bytes) signature data
    :param: file_name: (string) name of key file 
    """
    with open(file_name, 'wb+') as sig_file:
        sig_file.write(sig_data)   


def load_keys(private_file, public_file):
    'Load RSA key pair from files'
    """
    :param: private_file: (string) file name of private key
    :param: public_file: (string) file name of public key
    :return: private_key, public_key: (bytes, bytes) key data
    """
    private_key = load_key(private_file)
    public_key = load_key(public_file)

    return private_key, public_key


def load_key(file_name):
    'Load RSA key from a file'
    """
    :param: file_name: (string) file name of key
    :return: key: (bytes) key data
    """
    try:
        with open(file_name, 'rb') as key_file:
            key = key_file.read()
        return key
    except FileNotFoundError:
        return None


def hash_data(data):
    return SHA256.new(bytearray(data))


def sign_data(private_key, data):
    'Cryptographically sign given data'
    """
    :param: private_key: (bytes) private key data
    :param: module_file: (string) data to be signed
    :return: (digest, signature): (Crypto.Hash.SHA256.SHA256Hash, bytes)
        digest of module and signed digest
    """
    digest = hash_data(data)
    try:
        key = RSA.import_key(private_key) # TODO: can probably be factored out
        signature = pkcs1_15.new(key).sign(digest)
    except (KeyError, ValueError):
        print("Unable to sign module")
        return None, None

    return digest, signature


def verify_sig(data, public_key, signature):
    'Verify signature of digest with public key'
    """
    :param: data: (string) data to be verified
    :param: public_key: (bytes) public key data
    :param: signature: (bytes) signed digest
    :return: True/False: (Bool) True indicates a successful verification
    """
    digest = hash_data(data)
    try:
        key = RSA.import_key(public_key)
        pkcs1_15.new(key).verify(digest, signature)
        return True
    except (ValueError, TypeError):
        return False


def encrypt_data(data, key):
    'Encrypts a file with a key, assumes you have a shared symmetric key'
    """
    """
    if len(key) != 16 and len(key) != 32:
        raise ValueError("Key must of length 16 or 32 bytes")
        
    # creates cipher which can encrypt and product 8 byte nonce
    cipher = Salsa20.new(key)
    return cipher.nonce + cipher.encrypt(data)


def decrypt_data(enc_data, key):
    'Decrypts data with a shared symmetric key'
    """
    """
    if len(key) != 16 and len(key) != 32:
        raise ValueError("Key must of length 16 or 32 bytes")

    nonce = enc_data[:NONCE_LEN]
    cipher_text = enc_data[NONCE_LEN:]

    cipher = Salsa20.new(key, nonce)
    return cipher.decrypt(cipher_text)



if __name__ == "__main__":

    test_dir = '../test'
    key_ext = '.pem'
    private_file = "private_key" + key_ext
    private_path = path.join(test_dir, private_file)

    public_file = "public_key" + key_ext
    public_path = path.join(test_dir, public_file)

    module_name = "test_module"
    module_file = path.join(test_dir, module_name + ".py")

    # check if keys exist, if not generate a key pair
    private_key, public_key = load_keys(private_path, public_path)
    if private_key is None or public_key is None:
        print("Generating Keys...")
        private_key, public_key = gen_key_pair()
        write_keys(private_key, private_path, public_key, public_path)
    
    # sign test module
    try:
        code = open(module_file, "rb").read()
    except FileNotFoundError:
        print("No Module File Found")
        quit()

    digest, sig = sign_data(private_key, code)
    if digest is None or sig is None:
        quit()
    
    # quick verify test
    if verify_sig(code, public_key, sig):
        print("Successful Signature Verification")
    else:
        print("Could Not Verify")

    write_signature(sig, "../test/signature.pem")

    key = b'aaaaaaaaaaaaaaaa'

    # run encryption test
    before_module = open(module_file, 'rb').read()
    enc = encrypt_data(before_module, key)

    after_module = decrypt_data(enc, key)
    
    if before_module == after_module:
        print("Crypto Test Successful!")
    else:
        print("Something went wrong :(")


