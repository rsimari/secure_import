class SecureTest:
	'Test module to be signed and verified'

	def __init__(self):
		print("in SecureTest.__init__ ...")

	def test(self):
		return 'Success'

	def __repr__(self):
		print(f'<SecureTest here>')