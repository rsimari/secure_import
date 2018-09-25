""" Crypto functions for secure_import module

"""

# TODO: add doctest functionality

__author__ = 'rsimari'
__version__ = '0.1'

from Crypto.PublicKey import RSA 
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode
from os import path


def load_keys(private_file, public_file):
    'Load RSA key pair from files'
    """
    @param private_file: (string) file name of private key
    @param public_file: (string) file name of public key
    @return private_key, public_key: (bytes, bytes) key data
    """
    private_key = load_key(private_file)
    public_key = load_key(public_file)

    return private_key, public_key

def load_key(file_name):
    'Load RSA key from a file'
    """
    @param file_name: (string) file name of key
    @return key: (bytes) key data
    """
    try:
        with open(file_name, 'rb') as key_file:
            key = key_file.read()
        return key
    except FileNotFoundError:
        return None

def write_key(key_data, file_name):
    'Write RSA key to file'
    """
    @param key_data: (bytes) key data
    @param file_name: (string) name of key file 
    """
    with open(file_name, 'wb+') as key_file:
        key_file.write(key_data)

def write_keys(private_key, private_file, public_key, public_file):
    'Write RSA key pair to files'
    """
    @param private_key: (bytes) private key data
    @param private_file: (string) name of private key file
    @param public_key: (bytes) public key data
    @param public_file: (string) name of public key file
    """
    write_key(private_key, private_file)
    write_key(public_key, public_file)

def gen_key_pair(bits=2048):
    'Generate a RSA key pair'
    """
    @param bits: (int) size of key to generate
    @return (private_key, public_key): (bytes, bytes) key data
    """
    new_key = RSA.generate(bits, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 

    return private_key, public_key

def sign_file(private_key, module_file):
    'Cryptographically sign given module'
    """
    @param private_key: (bytes) private key data
    @param module_file: (string) name of module file
    @return (digest, signature): (Crypto.Hash.SHA256.SHA256Hash, bytes)
        digest of module and signed digest
    """
    try:
        data = open(module_file, "rb").read()
    except FileNotFoundError:
        print("No Module File Found")
        return None, None

    digest = SHA256.new(bytearray(data))
    try:
        key = RSA.import_key(private_key) # TODO: can probably be factored out
        signature = pkcs1_15.new(key).sign(digest)
        print(type(signature))
    except (KeyError, ValueError):
        print("Unable to sign module")
        return None, None

    return digest, signature


def verify_sig(public_key, digest, signature):
    'Verify signature of digest with public key'
    """
    @param public_key: (bytes) public key data
    @param digest: (Crypto.Hash.SHA256.SHA256Hash) digest of module
    @param signature: (bytes) signed digest
    @return True/False: (Bool) True indicates a successful verification
    """
    try:
        key = RSA.import_key(public_key)
        pkcs1_15.new(key).verify(digest, signature)
        return True
    except (ValueError, TypeError):
        return False


if __name__ == "__main__":

    test_dir = 'test'
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
    digest, sig = sign_file(private_key, module_file)
    if digest is None or sig is None:
        quit()
    
    # quick verify test
    if verify_sig(public_key, digest, sig):
        print("Successful verification")
    else:
        print("Could not verify")


