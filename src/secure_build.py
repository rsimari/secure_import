""" Securely wraps a module so it can be securely imported
"""

from crypto_utils import *

# TODO: to make this many functions or one with many options?

def secure_build(module_file, private_key_file='private_key.pem', 
				 public_key_file='public_key.pem', mode='v',
				 sig_file_name='signature.pem'):
	''
	# read module file
	print(f"Reading Module {module_file!r}...")
	try:
		code = open(module_file, "rb").read()
	except FileNotFoundError:
		print("No Module File Found")
		return None

	# check if key exists, if not generate a key pair
	private_key, public_key = load_keys(private_key_file, public_key_file)
	if private_key is None or public_key is None:
		print("Generating New Keys...")
		private_key, public_key = gen_key_pair()
		write_keys(private_key, private_key_file, 
					public_key, public_key_file)
		print(f"Wrote Keys to {private_key_file!r} \
				and {public_key_file!r}")
	
	digest, sig = sign_data(private_key, code)
	if digest is None or sig is None:
		print("Unable To Sign Module")
		return None
	
	if 'v' in mode:
		print("Verifying Signature...")
		# quick verify test
		if verify_sig(code, public_key, sig):
			print("Successful Signature Verification")
		else:
			print("Could Not Verify Signature")

	write_signature(sig, sig_file_name)
	print(f"Wrote Signature To {sig_file_name!r}")

	return sig
