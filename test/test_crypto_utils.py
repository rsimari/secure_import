import pytest
from sys import path
import os
from mock import mock_open, patch
from collections import namedtuple


path.append(os.path.join(os.getcwd(), 'src'))
from crypto_utils import *

@pytest.fixture
def keys():
	_keys = gen_key_pair()
	named_keys = namedtuple('keys', ['private', 'public'], verbose=True)
	return named_keys(_keys[0], _keys[1])

@pytest.fixture
def data():
	return bytes(bytearray(2048))

@pytest.fixture
def signature(keys, data):
	return sign_data(keys.private, data)[1]


def test_gen_key_pair():
	pub, pri = gen_key_pair()
	assert pub != None
	assert pri != None
	assert len(pub) > 0
	assert len(pri) > 0

def test_write_key(tmpdir, keys):
	key_data = keys.public
	file_name = tmpdir.join('some_key.pem') # mock a file

	write_key(key_data, str(file_name))
	file_contents = file_name.read(mode='rb')
	assert len(file_contents) > 0
	assert file_contents == key_data

def test_write_keys(tmpdir, keys):
	pub_file = tmpdir.join('some_key.pem') 
	pri_file = tmpdir.join('another_key.pem')

	write_keys(keys.private, pri_file, keys.public, pub_file)
	pri_contents = pri_file.read(mode='rb')
	pub_contents = pub_file.read(mode='rb')
	assert len(pri_contents) > 0
	assert pri_contents == keys.private
	assert len(pub_contents) > 0
	assert pub_contents == keys.public

def test_write_signature(tmpdir, signature):
	sig_file = tmpdir.join('some_signature.pem')

	write_signature(signature, str(sig_file))
	sig_contents = sig_file.read(mode='rb')

	assert sig_contents != None
	assert len(sig_contents) > 0
	assert sig_contents == signature


def test_load_key(tmpdir, keys):
	key_file = tmpdir.join('some_key.pem')
	# must be bytes because we write in bytes in load_key()
	_key = keys.public
	key_file.write(_key)

	key = load_key(str(key_file))
	assert key != None
	assert len(key) > 0
	assert key == _key

def test_load_key_no_file():
	key_file = 'not_a_file.pem'
	key = load_key(key_file)
	assert key == None

def test_load_keys(tmpdir, keys):
	pub_file = tmpdir.join('some_key.pem') 
	pri_file = tmpdir.join('another_key.pem')

	pub_file.write(keys.public)
	pri_file.write(keys.private)

	private, public = load_keys(pri_file, pub_file)
	assert private != None and public != None
	assert private == keys.private and public == keys.public

def test_get_hash_obj(data):
	_hash = get_hash_obj(data)
	assert _hash != None
	assert isinstance(_hash, SHA512.SHA512Hash)

def test_get_hash_obj_bad_data():
	with pytest.raises(ValueError):
		bad_data = 42
		get_hash_obj(bad_data)

def test_sign_data():
	pass

def test_verify_sig():
	pass

def test_encrypt_data():
	pass

def test_decrypt_data():
	pass

