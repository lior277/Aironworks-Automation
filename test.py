import pyotp

totp = pyotp.TOTP('wwy4lhjxit7ra43h4swpnzccvwkfflzd')
totp.now()
print('Code:', totp.now())
assert False
