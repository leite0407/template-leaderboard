import requests as rq
import json
import csv
import pandas as pd
from sqlalchemy import create_engine

# Links para o endpoint da api interna do repl.it
link_assignments = "https://repl.it/data/classrooms/184710/assignments"

# Cookie com o id da sessão iniciada no rep.it para passar nos requests
cookie = {'connect.sid' : 's%3ASUMBXm17E4SrTeeioWZrTfBtszFRgslZ.J4V8v5z5jQX9BE3qyaM%2BRmMh%2FhkB1gmbvE7LPbVJERc'}

# Enviar requests, processar json recebido
assignments_list = json.loads(rq.get(link_assignments, cookies=cookie).content)

# Fazer um DataFrame do Pandas com a lista recebida
assignments_df = pd.DataFrame(assignments_list)

# Criar colunas com a week de cada assignment, com o level (prata em todos) e type (replit)
assignments_df['semana'] = assignments_df.apply(lambda row: int(row['name'].split(' ')[1]), axis=1)
assignments_df['nivel'] = assignments_df.apply(lambda row: 'prata', axis=1)
assignments_df['tipo'] = assignments_df.apply(lambda row: 'replit', axis=1)
# Mudar nome coluna 'name'
assignments_df = assignments_df.rename(columns={'name' : 'descricao'})

# Manter apenas colunas que interessam
assignments_df = assignments_df.filter(['id', 'descricao', 'tipo', 'semana', 'nivel'])

labels = ['id', 'descricao', 'tipo', 'semana', 'nivel']

# Adicionar quizzes, checkpoints e projetos
for i in range(1,8):
    # quiz
    assignments_df = assignments_df.append(pd.DataFrame([[10 + i, 'quiz'+str(i), 'quiz', i, 'prata']], columns=labels))
    # checkpoint
    assignments_df = assignments_df.append(pd.DataFrame([[20 + i, 'check'+str(i), 'checkpoint', i, 'bronze']], columns=labels))
    # projeto
    assignments_df = assignments_df.append(pd.DataFrame([[30 + i, 'proj'+str(i), 'projeto', i, 'ouro']] , columns=labels))


print(assignments_df)

# Armazenar df na base de dados

from flask import Flask
from tabelas_db import db, Tarefa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Iniciar base de dados
db.init_app(app)

with app.app_context():

    # Dropar tabela das tarefas
    Tarefa.__table__.drop(db.engine)
    Tarefa.__table__.create(db.session.bind)

    for index, row in assignments_df.iterrows():

        tarefa = Tarefa(
            id=row['id'],
            descricao=row['descricao'],
            tipo=row['tipo'],
            semana=row['semana'],
            nivel=row['nivel']
        )
        db.session.add(tarefa)

    db.session.commit()

