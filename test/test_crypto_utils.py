import pytest
from sys import path
import os
from mock import mock_open, patch

path.append(os.path.join(os.getcwd(), 'src'))
from crypto_utils import *

def test_gen_key_pair():
	assert gen_key_pair() != None, None

def test_write_key(tmpdir):
	key_data = bytearray(256) # 2048 / 8
	file_name = tmpdir.join('some_key.pem') # mock writing to file

	write_key(key_data, str(file_name))
	assert file_name.read() == key_data.decode()

def test_write_keys():
	pass

def test_hash_data():
	data = bytearray(2048)
	assert hash_data(data) != None