import pytest
from sys import path
import os

path.append(os.path.join(os.getcwd(), 'src'))
from crypto_utils import *

def test_gen_key_pair():
	pass