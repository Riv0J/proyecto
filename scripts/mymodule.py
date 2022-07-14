import shelve
import time
usersDBfile = 'DBusuarios.shlv'
interfacesDBfile = 'DBformacion.shlv'
DBformacion = 'DBformacion.shlv'

def readDB(DBfile):
    database = shelve.open(DBfile, flag = 'r')
    database_dic = dict(database)
    database.close()
    return database_dic
    
def testUser(usuario, password):
    usersDB = readDB(usersDBfile)
    for user in usersDB.values():
        if user['user'] == usuario and user['passwd'] == password:
            return True
    return False
    
def ofertasFamilia(familiaRequest):
    database = shelve.open(DBformacion, flag = 'r')
    databaseDic = dict(database)
    familiaDic = {}
    for curso in databaseDic.values():
        if curso['Familia'] == familiaRequest:
            familiaDic[curso['Nombre']] = curso
    database.close()
    return familiaDic
    
def checkFamilia(varFamilia):
    familias = {'Actividades físicas y deportivas',
    'Administración y gestión',
    'Agraria',
    'Artes gráficas',
    'Artes y artesanías',
    'Comercio y marketing',
    'Edificación y obra civil',
    'Electricidad y electrónica',
    'Energía y agua',
    'Fabricación mecánica',
    'Hostelería y turismo',
    'Imagen personal',
    'Imagen y sonido',
    'Industrias alimentarias',
    'Industrias extractivas',
    'Informática y comunicaciones',
    'Instalación y mantenimiento',
    'Madera, mueble y corcho',
    'Marítimo pesquera',
    'Química',
    'Sanidad',
    'Seguridad y medio ambiente',
    'Servicios socioculturales y a la comunidad',
    'Textil, confección y piel',
    'Transporte y mantenimiento de vehículos',
    'Vidrio y cerámica',
    }
    if varFamilia in familias:
        return True
    else:
        return False
