import shelve

database = shelve.open('DBformacion.shlv', flag ='n')
database['DevNet'] = {
    'Nombre':'DevNet',
    'Familia':'Informática y comunicaciones',
    'Propuestos':'2', 
    'Mínimos':'12',
    'Participantes': [
        'usuario1',
        'usuario2'
    ],
    'Recurso de consulta': '/api/formacion/cursos/DevNet'
    }
database['Big-Data'] = {
    'Nombre':'Big Data',
    'Familia':'Informática y comunicaciones',
    'Propuestos':'1', 
    'Mínimos':'8',
    'Participantes': [
        'eoi'
    ],
    'Recurso de consulta': '/api/formacion/cursos/Big-Data'
    }
database['Representación-de-proyectos-de-edificación'] = {
    'Nombre':'Representación de proyectos de edificación',
    'Familia':'Edificación y obra civil',
    'Propuestos':'1', 
    'Mínimos':'8',
    'Participantes': [
        'usuario1'
    ],
    'Recurso de consulta': '/api/formacion/cursos/Representación-de-proyectos-de-edificación'
    }
database.close()
