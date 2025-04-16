import pyotp

totp = pyotp.TOTP('ZQMLNNMF6M6NFX3G')
totp.now()
print('Code:', totp.now())
assert False
