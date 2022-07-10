import shelve
import time
usersDBfile = 'DBusuarios.shlv'
interfacesDBfile = 'DBformacion.shlv'

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
    
def auth(args):
    usersDB = readDB(usersDBfile)
    if 'user' in args and 'passwd' in args:
        for user in usersDB.values():
            if user['user'] == args['user'] and user['passwd'] == args['passwd']:
                return True
            return '', 401 
    else:
        return 'query params no apropiados', 401


