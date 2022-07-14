import shelve
from hashlib import blake2b

h=blake2b(digest_size=16)
h.update(b'usuario:usuario')
token = h.hexdigest()

database = shelve.open('DBusuarios.shlv', flag ='n')
database['1'] = {'user':'eoi','passwd':'eoi'}
database['2'] = {'user':'guest','passwd':'guest'}
database['3'] = {'user': 'usuario1', 'passwd': 'usuario1'}
database['4'] = {'user': 'usuario2', 'passwd': 'usuario2'}
database['5'] = {'user': 'usuario3', 'passwd': 'usuario3'}
database.close()
