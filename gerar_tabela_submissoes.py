'''
Script para criar tabela submissões, antes de se pôr o server a correr.

Atenção que este script não lida com os checkpoints e projetos, pelo que tem de se ir à spreadsheet destes (https://docs.google.com/spreadsheets/d/1xIZDZ-9gFkajvn8MkNWQyT0mi70xmpoaTlj4YvYTj3k/edit#gid=00)
e trocar todos os valores que estão a 1 para 0 e depois novamente para 1.

'''

quiz_count = 4 # MUDAR PARA O NUMERO DE QUIZZES QUE JÁ TIVEREM SIDO PUBLICADOS


import requests as rq
import json
import pandas as pd
from utils import rplt_time_to_datetime, quiz_time_to_datetime

# Links para o endpoint da api interna do repl.it
link_submissoes = "https://repl.it/data/teacher/classrooms/184710/submissions"

# Cookie com o id da sessão iniciada no rep.it para passar nos requests
cookie = {'connect.sid' : 's%3AaaQEDIAb7_bv_8-CBILt9cfM4Dr_0Lza.Jq6WUmFnF6i%2F%2FM9m9cZsRCvpayP0MGX%2FjTo1kJihcSc'}

# Enviar request, processar json recebido. (json vem como dict de listas por assignment, converter em lista)
dict_submissoes = json.loads(rq.get(link_submissoes, cookies=cookie).content)
lista_submissoes = []
for a in dict_submissoes:
    lista_submissoes += dict_submissoes[a]

# Fazer um DataFrame do Pandas com a lista recebida
submissoes_df = pd.DataFrame(lista_submissoes)

# Só manter colunas que interessam
submissoes_df = submissoes_df.filter(['assignment_id', 'student_id', 'time_submitted'])

submissoes_df['time_submitted'] = submissoes_df.apply(lambda row: rplt_time_to_datetime(row['time_submitted']), axis=1)

quizs_dfs = [None]*quiz_count

for i in range(quiz_count):
    quizs_dfs[i] = pd.read_csv(f'quiz{i+1}.csv')
    quizs_dfs[i] = quizs_dfs[i].filter(['Timestamp', 'Email address'])
    quizs_dfs[i]['Timestamp'] = quizs_dfs[i].apply(lambda row: quiz_time_to_datetime(row['Timestamp']), axis=1)



# Armazenar df na base de dados

from flask import Flask
from tabelas_db import db, Submissao, Aluno, Tarefa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Iniciar base de dados
db.init_app(app)

with app.app_context():

    # Dropar tabela das submissoes e criar nova

    Submissao.__table__.drop(db.engine)
    Submissao.__table__.create(db.session.bind)

    # Iterar df das submissoes do replit e adicionar cada uma à tabela
    for index, row in submissoes_df.iterrows():

        aluno = Aluno.query.filter_by(id=row['student_id']).first()

        if aluno == None:
            continue

        submissao = Submissao(
            tarefa=Tarefa.query.filter_by(id=row['assignment_id']).first(),
            aluno=aluno,
            timestamp=row['time_submitted']
        )
        db.session.add(submissao)

    # Iterar quizzes
    for i in range(quiz_count):

        # Iterar submissões de cada quiz e adicionar à tabela
        for index, row in quizs_dfs[i].iterrows():

            aluno = Aluno.query.filter_by(mail=row['Email address']).first()

            if aluno == None:
                continue

            submissao = Submissao(
                tarefa=Tarefa.query.filter_by(descricao=f'quiz{i+1}').first(),
                aluno=aluno,
                timestamp=row['Timestamp']
            )
            db.session.add(submissao)

    # Calcular medalhas de cada aluno

    alunos = Aluno.query.all()

    for aluno in alunos:

        nivel_count = {'bronze' : 0, 'prata' : 0, 'ouro' : 0}

        for semana in range(1,8):

            for nivel in ['bronze', 'prata', 'ouro']:

                nivel_completo = True

                tarefas_nivel = Tarefa.query.filter_by(semana=semana, nivel=nivel).all()

                for tarefa in tarefas_nivel:
                    submissao = Submissao.query.filter_by(aluno=aluno, tarefa=tarefa).first()
                    if submissao is None:
                        nivel_completo = False
                        break
                if nivel_completo:
                    nivel_count[nivel] += 1
                else:
                    break

        aluno.bronze = nivel_count['bronze']
        aluno.prata = nivel_count['prata']
        aluno.ouro = nivel_count['ouro']

    print(Submissao.query.all())

    db.session.commit()
