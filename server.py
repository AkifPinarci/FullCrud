from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app  = Flask(__name__)
try:
    mongo = pymongo.MongoClient(host = 'localhost', port = 27017, serverSelectionTimeoutMS = 1000)
    mongo.server_info()
    db = mongo.company
except:
    print("Cannot connect to db")

@app.route('/users', methods = ['GET'])
def get_user():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(response = json.dumps(data), status = 500, mimetype='application/json')
        
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"Cannot read user"}), status = 500, mimetype='application/json')


@app.route('/users/<id>', methods = ['PATCH'])
def update_user(id):
    try:
        dbResponse = db.users.update_one({"_id": ObjectId(id)},{"$set": {"name":request.form["name"]}})   

        if dbResponse.modified_count == 1:
            return Response(response = json.dumps({"message":"User updated"}), status = 200, mimetype='application/json')
        else:
            return Response(response = json.dumps({"message":"Nothing to update"}), status = 200, mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"Sorry, cannot update"}), status = 500, mimetype='application/json')
        


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = {'name':request.form["name"], 'last_name':request.form["lastName"]}
        dbResponse = db.users.insert_one(user)
            
        return Response(response = json.dumps({"message":"user_created", "id":f"{dbResponse.inserted_id}"}), status = 200, mimetype='application/json')
    except Exception as ex:
        print(ex)


@app.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(response = json.dumps({"message":"User deleted", "id":f"{id}"}), status = 200, mimetype='application/json')
        return Response(response = json.dumps({"message":"User not found", "id":f"{id}"}), status = 200, mimetype='application/json')
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"Sorry, cannot delete user"}), status = 500, mimetype='application/json')





if __name__ == '__main__':
    app.run(debug=True)