from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)

#configuração do banco de dados
db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

#definição das classes
Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column ("name", String)
    email = Column ("email", String)
    password = Column ("password", String)

    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Game(Base):
    __tablename__ = "games"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    price = Column("price", Float)
    owner = Column("owner", ForeignKey("usuarios.id"))

    def __init__(self, title, price, owner):
        self.title = title
        self.price = price
        self.owner = owner

#criação das tabelas
Base.metadata.create_all(bind=db)


#CREATE
@app.route("/users", methods=["POST"])
def criar_usuario():
    data = request.json

    novo_usuario = User(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    session.add(novo_usuario)
    session.commit()

    return jsonify({
        "id": novo_usuario.id,
        "name": novo_usuario.name,
        "email": novo_usuario.email
    }), 201


#READ
@app.route("/users", methods=["GET"])
def pegar_usuarios():
    usuarios = session.query(User).all()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email}
        for u in usuarios
    ])

# UPDATE
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json

    user = session.query(User).get(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]

    session.commit()

    return jsonify({"message": "Usuário atualizado"})


# DELETE
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = session.query(User).get(id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    session.delete(user)
    session.commit()

    return jsonify({"message": "Usuário removido"})


@app.route("/games", methods=["POST"])
def criar_game():
    data = request.json

    novo_game = Game(
        title=data["title"],
        price=data["price"],
        owner=data["owner"]  # id do usuário
    )

    session.add(novo_game)
    session.commit()

    return jsonify({
        "id": novo_game.id,
        "title": novo_game.title,
        "price": novo_game.price,
        "owner": novo_game.owner
    }), 201

@app.route("/games", methods=["GET"])
def pegar_games():
    games = session.query(Game).all()

    return jsonify([
        {
            "id": g.id,
            "title": g.title,
            "price": g.price,
            "owner": g.owner
        }
        for g in games
    ])

@app.route("/games/<int:id>", methods=["PUT"])
def update_game(id):
    data = request.json
    game = session.query(Game).get(id)

    if not game:
        return jsonify({"error": "Jogo não encontrado"}), 404

    game.title = data["title"]
    game.price = data["price"]
    game.owner = data["owner"]

    session.commit()
    return jsonify({"message": "Jogo atualizado"})

@app.route("/games/<int:id>", methods=["DELETE"])
def delete_game(id):
    game = session.query(Game).get(id)

    if not game:
        return jsonify({"error": "Jogo não encontrado"}), 404

    session.delete(game)
    session.commit()
    return jsonify({"message": "Jogo removido"})




@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)





