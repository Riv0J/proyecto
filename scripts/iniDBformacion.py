import shelve

database = shelve.open('DBformacion.shlv', flag ='n')
database['1'] ={'Curso':'DevNet','Centro':'Escuela de Organización Industrial / EOI','Inicia':'Septiembre','Participantes':'0', 'Plazas':'12'}
database.close()
