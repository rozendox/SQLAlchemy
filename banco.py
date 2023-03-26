# Importe as bibliotecas necessárias
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crie uma conexão com o banco de dados SQLite
engine = create_engine('sqlite:///banco.db', echo=True)

# Crie uma classe que representa a tabela no banco de dados
Base = declarative_base()


# Defina as classes para as tabelas "clientes", "contas" e "transacoes"
class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    contas = relationship('Conta', back_populates='cliente')

    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', cpf='{self.cpf}')>"


class Conta(Base):
    __tablename__ = 'contas'
    id = Column(Integer, primary_key=True)
    numero = Column(String)
    saldo = Column(Float)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('Cliente', back_populates='contas')
    transacoes = relationship('Transacao', back_populates='conta')

    def __repr__(self):
        return f"<Conta(numero='{self.numero}', saldo={self.saldo})>"


class Transacao(Base):
    __tablename__ = 'transacoes'
    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    conta_id = Column(Integer, ForeignKey('contas.id'))
    conta = relationship('Conta', back_populates='transacoes')

    def __repr__(self):
        return f"<Transacao(valor={self.valor})>"


# Crie as tabelas no banco de dados
Base.metadata.create_all(engine)

# Crie uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Adicione alguns clientes ao banco de dados
c1 = Cliente(nome='João da Silva', cpf='123.456.789-10')
c2 = Cliente(nome='Maria dos Santos', cpf='987.654.321-10')
session.add_all([c1, c2])
session.commit()

# Crie algumas contas para os clientes
conta1 = Conta(numero='12345-6', saldo=1000, cliente=c1)
conta2 = Conta(numero='65432-1', saldo=2000, cliente=c2)
session.add_all([conta1, conta2])
session.commit()

# Realize três transações nas contas
t1 = Transacao(valor=-500, conta=conta1)
t2 = Transacao(valor=1000, conta=conta2)
t3 = Transacao(valor=-200, conta=conta1)
session.add_all([t1, t2, t3])
session.commit()

# Exiba os dados das transações
print("Transações:")
transacoes = session.query(Transacao).all()
for transacao in transacoes:
    print(f"- {transacao.conta.cliente.nome} ({transacao.conta.numero}): {transacao.valor}")

# Exiba os saldos das contas
print("Saldos:")
contas = session.query(Conta).all()
for conta in contas:
    print(f"- {conta.cliente.nome} ({conta.numero}): {conta.saldo}")
