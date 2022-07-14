import shelve

database = shelve.open('DBformacion.shlv', flag ='n')
database['DevNet'] = {
    'Nombre':'DevNet',
    'Propuestos':'2',
    'Mínimos':'12',
    'Participantes': [
        'usuario1',
        'usuario2'
    ],
    'Recurso de consulta': '/api/formacion/DevNet'
    }
database['Big-Data'] = {
    'Nombre':'Big Data',
    'Propuestos':'1', 
    'Mínimos':'8',
    'Participantes': [
        'eoi'
    ],
    'Recurso de consulta': '/api/formacion/Big-Data'
    }
database.close()
