"""Program that imports and cryptographically verifies a python module

"""

# TODO: add . syntax for directory searches for module file



__author__ = 'rsimari'
__version__ = '0.1'

import os
import sys
from contextlib import suppress
import urllib.request
from crypto_utils import *

modules = {}      # emulate sys.modules

class SecureModule:

    def __init__(self, namespace):
        object.__setattr__(self, 'namespace', namespace)

    def __getattr__(self, attr):
        try:
            return self.namespace[attr]
        except KeyError:
            raise AttributeError(attr) from None # from None silences all previous errors
                                                 # in this case the KeyError which we dont
                                                 # want

    def _setattr__(self, attr, value):
        self.namespace[attr] = value

    def __dir__(self):
        return self.namespace.keys()

    def __repr__(self):
        return '<SecureModule %r in %r>' % (self.__name__, self.__file__)

    @property
    def signature(self): # TODO
        'Return digest of module'
        return ''

    @property
    def public_key(self): # TODO
        'Return public key to be used to verify signature'
        return ''


def get_key_sig(key_file, sig_file):
    try:
        key = open(key_file, "rb").read()
    except FileNotFoundError:
        print("Could Not Find Key File")
        return None, None

    try:
        sig = open(sig_file, "rb").read()
    except FileNotFoundError:
        print("Could Not Find Signature File")
        return key, None

    return key, sig


def secure_import(modname, public_key, signature):
    'Securely import local or remote module'
    """
    :param str modname: name or url of module to import
    :param bytes public_key: RSA public key of module source
    :param bytes signature: signature of module 
    """
    fullname = '' # used as a default value, if its set the module is remote
    # checks if import is a remote file
    if modname.startswith(('http://', 'https://')):
        fullname = modname                          # at this point its the entire url
        _, basename = fullname.rsplit('/', 1)       # splits the url from file name
        modname, ext = os.path.splitext(basename)   # splits the extension in the file name        

    # check to see if the module has been cached
    if modname in modules:
        globals()[modname] = modules[modname] # assign it in global() to be used
        return

    # if module is from remote source
    elif fullname.startswith(('http://', 'https://')):
        # retrieve code from remote source
        code = urllib.request.urlopen(fullname).read()
    else:
        # find, then build/run module
        filename = modname + '.py'
        for dirname in sys.path:
            fullname = os.path.join(dirname, filename)
            with suppress(FileNotFoundError):  # ignore file not found errors
                with open(fullname, 'rb') as f:      # try to open the file
                    code = f.read()
                break                          # if it gets to this line a file
                                               # has been found
        else:
            raise ModuleNotFoundError(f'No module name {modname!r}')


    namespace = dict(
        __name__ = modname,
        __file__ = fullname,
        __package__ = '',
        __loader__ = 'secure_import.py'
    )

    if not verify_sig(code, public_key, signature):
        # TODO: raise something here?
        print(f'{modname!r} could not be verified')
        return

    exec(code, namespace) # namespace -> locals(), this puts the locals()
                          # from the code into namespace
                          # we changed this to namespace for both so we
                          # can have __builtins__ in the dir()
                          # we want __builtins__ because then we can use
                          # them in our python module that we are loading
    mod = modules[modname] = SecureModule(namespace) # this saves the module so it can be cached
                                                     # this saves computation if the module gets
                                                     # imported more than once in a program

    globals()[modname] = mod         # this makes the module globally acessible
                                     # just like a normal module

"""
def reload(module):
    modname = module.__name__  # get name of module
    modules.pop(modname, None) # remove from modules cache, return None if its not there
    secure_import(modname)         # import the module again
    return modules[modname]
"""

if __name__ == '__main__':


    sys.path.append('../test/')
    public_key, signature = get_key_sig("../test/public_key.pem", "../test/signature.pem")
    secure_import('test_module', public_key, signature)
    s = test_module.SecureTest()
