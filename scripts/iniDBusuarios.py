import shelve
from hashlib import blake2b

h=blake2b(digest_size=16)
h.update(b'usuario:usuario')
token = h.hexdigest()

database = shelve.open('DBusuarios.shlv', flag ='n')
database['1'] = {'user':'eoi','passwd':'eoi'}
database['2'] = {'user':'guest','passwd':'guest'}
database.close()
