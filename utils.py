from datetime import datetime


def rplt_time_to_datetime(time):
    ''' Transforma string do timestamp do repl.it em datetime '''

    # 2020-04-11T18:39:41.336Z

    return datetime(
        # ano
        int(time.split('-')[0]),
        # mês
        int(time.split('-')[1]),
        # dia
        int(time.split('-')[2].split('T')[0]),
        # hora
        int(time.split('T')[1].split(':')[0]),
        # minuto        
        int(time.split('T')[1].split(':')[1]),
        # segundo
        int(time.split('T')[1].split(':')[2].split('.')[0]),
    )

def quiz_time_to_datetime(time):
    ''' Transforma string do timestamp do quiz em datetime '''

    return datetime(
        int(time.split('/')[2].split(' ')[0]),   # ano
        int(time.split('/')[1]),                 # mês
        int(time.split('/')[0]),                 # dia
        int(time.split(' ')[1].split(':')[0]),   # hora
        int(time.split(' ')[1].split(':')[1]),   # minuto
        int(time.split(' ')[1].split(':')[2]),   # segundo
    )

from tabelas_db import *


'''
def calcular_medalhas(aluno, app):
    Calcula quantas medalhas aluno ganhou

    with app.app_context():

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
'''