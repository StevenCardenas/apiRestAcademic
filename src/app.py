# 1 Requerimos los módulos
from flask import Flask, request, jsonify, Response
from flask_pymongo import pymongo
from pymongo import MongoClient
from bson import json_util

# 1 Requiero flask para inicializar a Flask le paso la propiedad _name_ y me da la instancia de la aplicación
app = Flask(__name__)
#Conexión con la BD
CONNECTION_STRING = "mongodb+srv://bscardenas:2016@cluster0.p3zey.mongodb.net/academicdb?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client['academicdb']
collection = db["students"]
#Creamos ruta de prueba:
@app.route('/')
def hello():
    return "Servidor levantado"
#Get all
@app.route('/academic/students', methods=['GET'])
def get_students():
    students = collection.find()
    response = json_util.dumps(students)
    return Response(response, mimetype='application/json')

#Get element by id, for _id {'_id': ObjectId(id)}
@app.route('/academic/student/<id>', methods=['GET'])
def get_student(id):
    client = collection.find_one({'id': int(id)})
    response = json_util.dumps(client) 
    return Response(response, mimetype='application/json')

#POST
@app.route('/academic/student', methods=['POST'])
def create_student():
    id = request.json['id']
    name = request.json['name']
    role = request.json['role']
    average = request.json['average']

    #Validación
    if id and name and role and average:
        collection.insert_one(
            {"id": id, "name": name,"role": role, "average": average}
        )
        response = {
            "id": int(id),
            "name": name,
            "role": role,
            "average": float(average)
        }
        return response
    else:
        {"message": "error"}

    return {"message": "received"}

#PUT actualizar
@app.route('/academic/student/<id>', methods=['PUT'])
def update_student(id):
    idd = request.json['id']
    name = request.json['name']
    role = request.json['role']
    average = request.json['average']
    
    if idd and name and role and average:
        collection.update_one({'id': int(id)}, {'$set': 
        {"id": idd, "name": name,"role": role, "average": average}
        })
        response = jsonify({'message': 'Student  was updated sucessfully'})
        return response
    else:
        {"message": "error"}
        
    return {"message": "received"}

#Delete by id
@app.route('/academic/student/<id>', methods=['DELETE'])
def delete_student(id):
    collection.delete_one({'id': int(id)})
    response = jsonify({'message': 'client ' + id + ' was deleted sucessfully'})
    return response
#Opcional: mensaje de error cuando la URL no existe (404)
#Opcional mensaje de error cuando la url no existe 404
@app.errorhandler(404)
def not_found(error=None):

    response = jsonify({
        'message': 'Resource not found in: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response
#Corrida del servidor
if __name__ == '_main_':
    app.run(debug=True)
