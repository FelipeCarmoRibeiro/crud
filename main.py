from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

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

Base.metadata.create_all(bind=db)

usuario1 = User(name="Alice", email="alice123@gmail.com", password="alice2024")
session.add(usuario1)
session.commit()

usuario2 = User(name="Bob", email="bob123@gmail.com", password="bob2024")
session.add(usuario2)
session.commit()

usuario3 = User(name="Charlie", email="charlie123@hotmail.com", password="charlie2024")
session.add(usuario3)
session.commit()

usuario4 = User(name="Diana", email="diana123@gmail.com", password="diana2024")
session.add(usuario4)
session.commit()

lista_usuarios = session.query(User).all()
print(lista_usuarios[0].name)



jogo1 = Game(title="The Legend of Python", price=59.99, owner=usuario1.id)
session.add(jogo1)
session.commit()


usuario1.name = "Alice Wonderland"
session.add(usuario1)
session.commit()