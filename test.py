import bcrypt

password = b'pass1'

hashed = b'$2b$12$ATceo79oZgp6L7xuG1QTa.Nd6Iq6fdi1aew/2R7Qqe0povEkhi6lK'

if bcrypt.checkpw(password,hashed):
    print('matches')
else:
    print('failed')
