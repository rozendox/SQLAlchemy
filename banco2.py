from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import pymongo

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    endereco = Column(String(200))

    contas = relationship("Conta", backref=backref('cliente', uselist=False))

class Conta(Base):
    __tablename__ = 'contas'

    id = Column(Integer, primary_key=True)
    saldo = Column(Integer)
    tipo = Column(String(50))
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    
engine = create_engine('sqlite:///banco.db', echo=True)
Base.metadata.create_all(engine)

# Conecta ao Mongo Atlas
client = pymongo.MongoClient("<inserir_uri_do_mongo_atlas>")
db = client["banco"]

# Cria a coleção "clientes"
clientes = db["clientes"]

# Insere alguns documentos na coleção "clientes"
cliente1 = {"nome": "João da Silva", "cpf": "111.111.111-11", "idade": 30}
cliente2 = {"nome": "Maria Souza", "cpf": "222.222.222-22", "idade": 25}
cliente3 = {"nome": "José Santos", "cpf": "333.333.333-33", "idade": 40}

clientes.insert_many([cliente1, cliente2, cliente3])
