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


def secure_import(modname, public_key, signature):
    'Securely import local or remote module'
    """
    :param str modname: name or url of module to import
    :param bytes public_key: RSA public key of module source
    :param bytes signature: signature of module 
    """
    fullname = ''
    # checks if import is a remote file
    if modname.startswith(('http://', 'https://')):
        fullname = modname                          
        _, basename = fullname.rsplit('/', 1)      
        modname, ext = os.path.splitext(basename)        

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
                with open(fullname, 'rb') as f:     
                    code = f.read()
                break                       
        else:
            raise ModuleNotFoundError(f'No module name {modname!r}')


    namespace = dict(
        __name__ = modname,
        __file__ = fullname,
        __package__ = '',
        __loader__ = 'secure_import.py'
    )

    if not verify_sig(code, public_key, signature):
        raise ImportError("Could not verify module signature")

    exec(code, namespace) 
    mod = modules[modname] = SecureModule(namespace) # this saves the module so it can be cached

    globals()[modname] = mod # this makes the module globally acessible


if __name__ == '__main__':


    sys.path.append('../test/')
    key_file = os.path.join('..', 'test', 'public_key.pem')
    sig_file = os.path.join('..', 'test', 'signature.pem')
    module_name = 'test_module'

    public_key, signature = get_key_sig(key_file, sig_file)
    secure_import(module_name, public_key, signature)
    s = test_module.SecureTest()
