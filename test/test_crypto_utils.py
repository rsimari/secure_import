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
	file_name = tmpdir.join('some_key.pem') # mock a file

	write_key(key_data, str(file_name))
	file_contents = file_name.read()
	assert len(file_contents) > 0
	assert file_contents == key_data.decode()

def test_write_keys(tmpdir):
	pub_file = tmpdir.join('some_key.pem') 
	pri_file = tmpdir.join('another_key.pem')

	pub_key = bytearray(256)
	pri_key = bytearray(256)

	write_keys(pri_key, pri_file, pub_key, pub_file)
	pri_contents = pri_file.read()
	pub_contents = pub_file.read()
	assert len(pri_contents) > 0
	assert pri_contents == pri_key.decode()
	assert len(pub_contents) > 0
	assert pub_contents == pub_key.decode()


def test_write_signature():
	pass

def test_load_key():
	pass

def test_load_key_no_file():
	key_file = 'not_a_file.pem'
	key = load_key(key_file)
	assert key == None

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

