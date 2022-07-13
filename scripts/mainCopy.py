from flask import Flask, jsonify, request, url_for
import mymodule as m
import shelve
from flask_httpauth import HTTPBasicAuth
import re
patronIf = '^[g,f][0,2,3]_[1-20]$'

#  ^ = Inicio de linea
# $ = final de linea
# . = cualquier caracter menos barra n
# ? = 0 o 1
# * = 0 o más
# + = 1 o más
usersDBfile = 'usersDB.shlv'
interfacesDBfile = 'interfacesDB.shlv'

#generamos objeto auth de clase HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(usuario):
    users = m.readDB(usersDBfile)
    for user in users.values():
        if user['user'] == usuario:
            return user['passwd']
    return None 
app = Flask(__name__)
app.config['DEBUG']=True

@app.route('/', methods=['GET','POST'])
def web():
    return '<h1>hola</h1>'

@app.route('/api/v1/users', methods=['GET'])
@auth.login_required
def getUsers():
	return jsonify(m.readDB(usersDBfile))
	
@app.route('/api/v1/interfaces/all', methods=['GET']) #ALL con query params ?user=usuario & passwd=usuario, si no coincide devuelve error 401 prohibido entrar al recurso
def getIfAll():
    #if 'user' in request.args and 'passwd' in request.args:
        #if m.testUser(request.args['user'],request.args['passwd']):
    return jsonify(m.readDB(interfacesDBfile))
        #return '', 401 
    #else:
        #return 'query params no existen', 401
           
@app.route('/api/v1/interfaces', methods=['GET']) #QUERY PARAMS indicar al intentar acceder #al ruta ifname=g0_1&req=ip no se suele utilizar
def getIfQP():
    interface = request.args['ifname']
    if re.match(patronIf,interface):
        interfacesDB = m.readDB(interfacesDBfile)
        if interface in interfacesDB:
            interfaceData = interfacesDB[interface]
            return jsonify(interfaceData)
        else:
            return 'interface no existente',404
    else:
        return 'ifname incorrecto',410
    
@app.route('/api/v1/interfaces/<ifname>', methods=['GET','PUT','POST']) #URI ifname=g0_2&req=ip INTENTAR HACERLOS CON UN EXCEPT 1:11video
def getIfUri(ifname):
    if request.method == 'GET':
        interfacesDB = m.readDB(interfacesDBfile)
        if ifname in interfacesDB:
            return jsonify(interfacesDB[ifname])
        return jsonify ({'error':'interface no existente'}), 404
        
    elif request.method =='PUT':
        if request.json:
            if 'ip' in request.json and 'status' in request.json:
                interfacesDB = shelve.open(interfacesDBfile)
                interfacesDB[ifname] = {'ip':request.json['ip'], 'status':request.json['status'],'uri':url_for('getIfUri',ifname=ifname)}
                interfacesDB.close()
                return jsonify(request.json),201
            else:
                return jsonify({'error':'json incompleto'}),404
        else:
            return jsonify({'put error':'solicitud deber ser formato json'}),404
            
    elif request.method =='POST':
        if request.json:
            if 'ip' in request.json or 'status' in request.json:
                interfacesDB = shelve.open(interfacesDBfile)
                interfacesDB[ifname] = {'ip':request.json.get('ip',interfacesDB[ifname]['ip']), 'status':request.json.get('status',interfacesDB[ifname]['status']),'uri':url_for('getIfUri',ifname=ifname)}
                interfacesDB.close()
                return jsonify(request.json),201
            else:
                return jsonify({'error':'json incompleto'}),404
        else:
            return jsonify({'post error':'solicitud deber ser formato json'}),404
                
        
                

@app.route('/api/v1/interfaces/<ifname>', methods=['DELETE']) 
def deleteIfUri(ifname):
    interfacesDB = shelve.open(interfacesDBfile)
    if ifname in interfacesDB:
        del interfacesDB[ifname]
        interfacesDB.close()
        return ifname + ' deleted'
    return 'esa interfaz no existe',404

app.run(host='0.0.0.0', port='8080')
