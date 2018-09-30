import pytest
import os
from sys import path

path.append(os.path.join(os.getcwd(), 'src'))
from secure_import import secure_import

def test_secure_import():
	pass

