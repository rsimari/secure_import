import pytest
import os
from sys import path

path.append(os.path.join(os.getcwd(), 'src'))
from secure_build import secure_build

def test_secure_build_default():
	module_file = 'test/test_module.py'
	private_key_file = 'test/private_key.pem'
	public_key_file = 'test/public_key.pem'
	sig_file = 'test/signature.pem'
	signature = secure_build(module_file, private_key_file,
							 public_key_file,
							 sig_file_name=sig_file)
	assert signature != None
	assert len(open(sig_file, 'rb').read()) > 0

def test_secure_build_no_module():
	module_file = 'test/no_module_here.py'
	private_key_file = 'test/private_key.pem'
	public_key_file = 'test/public_key.pem'
	sig_file = 'test/signature.pem'

	with pytest.raises(FileNotFoundError) as e_info:
		signature = secure_build(module_file, private_key_file,
							 public_key_file,
							 sig_file_name=sig_file)


def test_secure_build_no_keys():
	pass

def test_secure_build_w_keys():
	pass



