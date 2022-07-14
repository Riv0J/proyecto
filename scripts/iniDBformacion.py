import shelve

database = shelve.open('DBformacion.shlv', flag ='n')
database['DevNet'] = {
    'Nombre':'DevNet',
    'Número_Participantes':'2', 
    'Mínimos':'12',
    'Participantes': [
        'usuario1',
        'usuario2'
    ]
    }
database['Big_Data'] = {
    'Nombre':'Big Data',
    'Número_Participantes':'0', 
    'Mínimos':'8',
    'Participantes': []
    }
database.close()
