'''
Script para criar tabela alunos na db, antes de se pôr o server a correr.
'''
import pandas as pd
from sqlalchemy import create_engine

alunos_df = pd.read_csv('alunos.csv')

alunos_df['bronze'] = alunos_df.apply(lambda row: 0, axis=1)
alunos_df['prata'] = alunos_df.apply(lambda row: 0, axis=1)
alunos_df['ouro'] = alunos_df.apply(lambda row: 0, axis=1)


# Armazenar df na base de dados

from flask import Flask
from tabelas_db import db, Aluno

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Iniciar base de dados
db.init_app(app)

with app.app_context():

    # Dropar tabela das tarefas
    Aluno.__table__.drop(db.engine)
    Aluno.__table__.create(db.session.bind)

    for index, row in alunos_df.iterrows():

        aluno = Aluno(
            id=row['id'],
            mail=row['mail'],
            nome=row['nome'],
            bronze=row['bronze'],
            prata=row['prata'],
            ouro=row['ouro']
        )
        db.session.add(aluno)

    print(Aluno.query.all())

    db.session.commit()