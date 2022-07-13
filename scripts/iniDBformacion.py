import shelve

database = shelve.open('DBformacion.shlv', flag ='n')
database['DevNet'] ={'Nombre':'DevNet','Participantes':'0', 'Mínimos':'12'}
database.close()
