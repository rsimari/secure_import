import pytest
from sys import path
import os

path.append(os.path.join(os.getcwd(), 'src'))
from crypto_utils import *

def test_gen_key_pair():
	pass

def test_write_key():
	key = bytearray(2048)
	# write_key(key, '.test_key')

def test_hash_data():
	data = bytearray(2048)
	assert hash_data(data) != None