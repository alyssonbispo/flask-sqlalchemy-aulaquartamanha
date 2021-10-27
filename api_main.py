import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    cpf = db.Column(db.Integer)

#criando tabelas caso ainda não esteja criada
db.create_all()


@app.route('/', methods=['GET'])  # DEFAULT É SÓ GET
def chama_main():
    return jsonify({"message": "Sorria você está sendo filmado!"})

@app.route('/user', methods=['POST'])
def adicionar_user():
    my_params = request.form
    db.session.add(User(username=my_params["name"], email=my_params["email"], cpf=my_params["cpf"]))
    db.session.commit()
    return "Sucesso!", 200

@app.route('/user')
def get_all_user():
    users = User.query.all()
    T = []
    for user in users:
        data = {}
        data['username'] = user.username
        data['email'] = user.email
        data['cpf'] = user.cpf
        T.append(data)
    return json.dumps(T)

@app.route('/user/<id>')
def get_user(id):
    flaskUser = User.query.filter_by(id=id).first()
    data = {}
    data['username'] = flaskUser.username
    data['email'] = flaskUser.email
    data['cpf'] = flaskUser.cpf
    return json.dumps(data)

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return "Usuário deletado com sucesso", 200

@app.route('/user/<id>', methods=['PATCH'])
def update_user(id):
    my_params = request.form
    flaskUser = User.query.filter_by(id=id).first()
    flaskUser.username = my_params["name"]
    flaskUser.email = my_params["email"]
    flaskUser.cpf = my_params["cpf"]
    db.session.commit()
    return "Usuário alterado com sucesso", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
