import pytest
from sys import path
import os
from mock import mock_open, patch

path.append(os.path.join(os.getcwd(), 'src'))
from crypto_utils import *

def test_gen_key_pair():
	pub, pri = gen_key_pair()
	assert pub != None
	assert pri != None
	assert len(pub) > 0
	assert len(pri) > 0

def test_write_key(tmpdir):
	key_data = bytearray(256) # 2048 / 8
	file_name = tmpdir.join('some_key.pem') # mock writing to file

	write_key(key_data, str(file_name))
	assert file_name.read() == key_data.decode()

def test_write_keys():
	pass

def test_write_signature():
	pass

def test_load_key():
	pass

def test_load_keys():
	pass

def test_hash_data():
	data = bytearray(2048)
	_hash = hash_data(data)
	assert _hash != None
	assert isinstance(_hash, SHA512.SHA512Hash)

def test_sign_data():
	pass

def test_verify_sig():
	pass

def test_encrypt_data():
	pass

def test_decrypt_data():
	pass

