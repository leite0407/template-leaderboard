#
from flask import Flask, request, render_template, send_file
from tabelas_db import db, Tarefa, Submissao, Aluno

from utils import rplt_time_to_datetime, quiz_time_to_datetime

import pandas as pd
from datetime import datetime


# Iniciar app Flask
app = Flask(__name__)
# Configurar base de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Iniciar base de dados
db.init_app(app)

@app.route('/debug')
def debug():

    submissoes = Submissao.query.all()
    return str(len(submissoes))

@app.route('/')
def index():

    leaderboard = []

    for aluno in Aluno.query.order_by(Aluno.nome).all():
        leaderboard += [aluno.__dict__]

    return render_template('leaderboard.html', leaderboard=leaderboard)


@app.route('/replit', methods=['POST'])
def replit():

    recebido = request.json

    tarefa=Tarefa.query.filter_by(id=recebido['assignment']['id']).first()
    aluno=Aluno.query.filter_by(id=recebido['student']['id']).first()

    # Verificar se já há submissão deste aluno para esta tarefa
    submissao = Submissao.query.filter_by(aluno=aluno, tarefa=tarefa).first()
    if submissao is not None:
        return '200'

    if aluno is None:
        return '200'

    nova_submissao = Submissao(
        tarefa=tarefa,
        aluno=aluno,
        timestamp=rplt_time_to_datetime(recebido['submission']['time_submitted'])
    )

    db.session.add(nova_submissao)

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

    db.session.commit()

    return '200'


@app.route('/quiz', methods=['POST'])
def quiz():

    recebido = request.json

    aluno = Aluno.query.filter_by(mail=recebido['email']).first()
    tarefa = Tarefa.query.filter_by(descricao=recebido['id']).first()

    # Verificar se já há submissão deste aluno para este assignment
    submissao = Submissao.query.filter_by(aluno=aluno, tarefa=tarefa).first()
    if submissao is not None:
        return '200'

    if aluno is None:
        return '200'

    nova_submissao = Submissao(
        tarefa = tarefa,
        aluno = Aluno.query.filter_by(mail=recebido['email']).first(),
        timestamp = quiz_time_to_datetime(recebido['Timestamp'])
    )

    db.session.add(nova_submissao)

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

    db.commit()

    return '200'


@app.route('/outras_tarefas', methods=['POST'])
def other_assignments():

    recebido = request.json

    aluno = Aluno.query.filter_by(id=recebido['student_id']).first()
    tarefa = Tarefa.query.filter_by(descricao=recebido['assignment_id']).first()

    if aluno is None:
        return '200'

    if recebido['value'] == '1':

        # Testar se já há uma submissão para esta tarefa e para este aluno
        submissao = Submissao.query.filter_by(aluno=aluno, tarefa=tarefa).first()
        if submissao is not None:
            return '200'

        nova_submissao = Submissao(
            tarefa=tarefa,
            aluno=aluno,
            timestamp=datetime.now()
        )

        db.session.add(nova_submissao)

    else:

        submissao = Submissao.query.filter_by(aluno=aluno, tarefa=tarefa).first()

        if submissao is None:
            return '200'

        db.session.delete(submissao)

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

    db.session.commit()

    return '200'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
