from flask import Flask, jsonify, request, url_for
import mymodule as m
import shelve
from flask_httpauth import HTTPBasicAuth
import re
patronIf = '^[g,f][0,2,3]_[1-20]$'

# ^ = Inicio de linea
# $ = final de linea
# . = cualquier caracter menos barra n
# ? = 0 o 1
# * = 0 o más
# + = 1 o más
DBusuarios = 'DBusuarios.shlv'
DBformacion = 'DBformacion.shlv'
errorFamilia = 'error: familia no existe, consultar familias en: https://sepe.es/HomeSepe/Personas/formacion/certificados-profesionalidad/familias-profesionales.html'
error404 = 'error: recurso no existente'
#generamos objeto auth de clase HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(usuario):
    users = m.readDB(DBusuarios)
    for user in users.values():
        if user['user'] == usuario:
            return user['passwd']
    return None 
app = Flask(__name__)
app.config['DEBUG']=True

@app.route('/', methods=['GET'])
@auth.login_required
def web():
    return '<h1>hola</h1>'
          
@app.route('/api/usuarios', methods=['GET'])
@auth.login_required
def getUsers():
	return jsonify(m.readDB(DBusuarios))
	
@app.route('/api/formacion/familias/<familia>', methods=['GET']) #ver solo cursos de una familia concreta
def getCursosFamilia(familia):
    familiaUri = familia.replace("-", " ")
    familiaExiste = m.checkFamilia(familiaUri)
    if familiaExiste == False: #si la familia no coincide con las 26 establecidas, hacemos return error, de lo contrario seguimos
        return errorFamilia, 400
    else:
        ofertasPorFamiliaDic = m.ofertasFamilia(familiaUri)
        if len(ofertasPorFamiliaDic) == 0: #si la lognitud del diccionario resultante es 0 entonces no hay ofertas de esa familia.
            return 'No hay ofertas para esta familia todavia!', 200
        return jsonify(ofertasPorFamiliaDic)
            
@app.route('/api/formacion/cursos/all', methods=['GET']) #ver todos los cursos
def getAll():
    #if 'user' in request.args and 'passwd' in request.args:
        #if m.testUser(request.args['user'],request.args['passwd']):
    return jsonify(m.readDB(DBformacion))
        #return '', 401 
    #else:
        #return 'query params no existen', 401
              
@app.route('/api/formacion/cursos/<curso>', methods=['GET','POST']) #get <curso> y post cuando curso = 'proponer', para el post poner un json en el body
@auth.login_required
def getCurso(curso): 
    ofertasDB = m.readDB(DBformacion)
    if curso in ofertasDB:
         return jsonify(ofertasDB[curso])
    else:
        if request.method == 'POST' and curso == 'all' and request.json: #atrapa el error de tratar de hacer 'GET' all, teniendo seleccionado POST.
            return 'error: no utilices POST al tratar de hacer GET all',400
        if request.method == 'POST' and curso == 'proponer' and request.json: #intenta agregar curso si se utiliza post y si 'curso' es 'proponer' y si hay un json en el body.
            if 'Nombre' and 'Familia' in request.json: #requiere json con NOMBRE y FAMILIA. 
                familiaExiste = m.checkFamilia(request.json['Familia'])
                if familiaExiste == False: #si la familia no coincide con las 26 establecidas, hacemos return error, de lo contrario seguimos
                    return errorFamilia, 400
                ofertasDB = shelve.open(DBformacion)
                uriString = request.json['Nombre'].replace(" ", "-") #.replace reemplaza espacios por "-" para crear una uri utilizable
                ofertasDB[uriString] = {'Nombre':request.json['Nombre'], 'Familia':request.json['Familia'], 'Propuestos':'1', 'Recurso de consulta':url_for('getCurso',curso=uriString)}
                ofertasDB.close()
                return jsonify(request.json),201
            else:
                return jsonify({'error':'json incompleto'}),404
    return error404, 404

#añadir participante al curso especificado
@app.route('/api/formacion/cursos/<curso>/participantes', methods=['POST'])
@auth.login_required
def addUserToCourse(curso):
    if curso == 'all':
        return 'error: no uses all cuando trates de hacer un post'
        
    ofertasDB = m.readDB(DBformacion)

    #comprobar que el curso exista
    if curso not in ofertasDB:
        return 'error: recurso no existente', 404
    
    nombreCurso = ofertasDB[curso]['Nombre']
    usuario = auth.current_user() #devuelve el usuario con el que se ha autenticado
    
    #comprobar que el usuario aún no esta inscrito en el curso
    if usuario in ofertasDB[curso]['Participantes']:
        return 'error: usuario ya está inscrito en el curso', 404
    
    #guardar usuario
    ofertasDB = shelve.open(DBformacion)
    cursoDB = ofertasDB[curso]
    cursoDB['Participantes'] += [usuario]

    #reasignar el curso a la BD porque shelve solo se acutaliza cuando identifica un cambio en 
    #una variable de primer nível (ofertasDB[curso] sí se actualiza, ofertasDB[curso]['Participante'] no)
    ofertasDB[curso] = cursoDB 

    #guardar cambios
    ofertasDB.close()

    return jsonify('Usuario ' + usuario + ' añadido al curso ' + nombreCurso ),201
    
    '''
        interfacesDB = m.readDB(interfacesDBfile)
        if ifname in interfacesDB:
            return jsonify(interfacesDB[ifname])
        return jsonify ({'error':'interface no existente'}), 404

    elif request.method =='POST':
    @auth.login_required
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
                
      '''  
                
'''
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
'''
app.run(host='0.0.0.0', port='8080')
