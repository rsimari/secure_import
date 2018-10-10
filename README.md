# Secure Import
A package for securely importing signed python modules

[![Build Status](https://travis-ci.com/rsimari/secure_import.svg?branch=master)](https://travis-ci.org/rsimari/secure_import)
[![codecov](https://codecov.io/gh/rsimari/secure_import/branch/master/graph/badge.svg)](https://codecov.io/gh/rsimari/secure_import)

## Example

Build Module:

```python
module_file = 'test/test_module.py'
private_key_file = 'test/private_key.pem'
public_key_file = 'test/public_key.pem'
sig_file = 'test/signature.pem'
signature = secure_build(module_file, private_key_file,
             public_key_file,
             sig_file_name=sig_file)
```

Import Module:

```python
key_file = 'test/public_key.pem'
sig_file = 'test/signature.pem'
module_name = 'test_module'

public_key, signature = get_key_sig(key_file, sig_file)
secure_import(module_name, public_key, signature)
s = test_module.SecureTest()
print(s.test())
```
