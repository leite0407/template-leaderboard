'''
Código Template para um leaderboard / sistema controlo submissões para um curso After School.

Este é o ficheiro principal de toda a coisa. Contém a app de Flask e respetivos endpoints.
Ver também ficheiro da db, se calhar começar por aí até.

Endpoints separadas em duas partes:
  * Register - Para receber e registar informação de submissões feitas pelos alunos.
  * Display - Para produzir os htmls, enviar csvs, etc.

Para quaisquer duvidas, contactar: Manuel Leite leite0407@gmail.com
'''

# Importar coisas do flask
from flask import Flask, request, render_template, send_file, redirect
# Importar coisas relacionadas com a base de dados
from tabelas_db import db, Tarefa, Submissao, Aluno
# Importar dados do ficheiro de config
#from config import *
# Importar funções uteis do ficheiro utils
from utils import rplt_time_to_datetime, quiz_time_to_datetime
# Importar várias cenas que vão ser necessárias em vários pontos
import pandas as pd
from datetime import datetime


# Iniciar app Flask
app = Flask(__name__)

# Configurar base de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciar base de dados
db.init_app(app)

'''
PARTE REGISTER

Endpoints aqui:
  * /replit - Receber dados de submissões de exercícios do repl.it
    É preciso, claro, primeiro configurar o webhook no repl.it.
    Pesquisar 'How to setup webhook replit classroom'

    Em 'amostras.txt', podem encontrar um exemplo da estrutura de como vêm os dados enviados pelo webhook.
    (é um ficheiro json, claro)
	
	Reparem que aqui não estamos de facto a confirmar se a submissão foi marcada como correta ou não.
	No entanto, não será muito dificil implementar isso. Ver 'amostras.txt'. Algures há um field que indica se a submissão foi marcada correta.
	
  * /quiz - Receber dados vindos de quizzes feitos usando o google forms.
  	É preciso configurar um script em cada quiz para isto funcionar.
  	Instruções sobre como o fazer [algures noutro ficheiro]. Spoiler - Basta fazer copy paste de um já escrito (I mean, altera-se um campo com o id do quiz) 

  * /forum - Receber dados de webhook forum. Forum manda POST request sempre que é atribuido um badge. 	
'''

@app.route('/replit', methods=['POST'])
def replit():

	# dict com info recebida. Ver 'amostras.txt'
	recebido = request.json

	# Encontrar na db 
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

	# Trocar por 'calcular_medalhas'
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
	print(recebido)

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
		timestamp = quiz_time_to_datetime(recebido['timestamp'])
	)

	db.session.add(nova_submissao)

	# Trocar por 'calcular_medalhas'
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

'''
PARTE DISPLAY

Endpoints aqui:

HTML:
  * /leaderboard - Tabela com o número de medalhas que cada aluno tem.
    Pode-se alterar facilmente para mostar o número de pontos que tem cada miúdo, se se optar por usar esse sistema.
    (nesse caso teria, claro, de se mudar o esquema da db, em vez de em cada aluno se registar o número de medalhas, pode-se registar número de pontos)
    Ver a respetiva template: leaderboard.html

  * /dashboard - Tabela com as tarefas que cada aluno já fez.
    Ver respetiva template: dashboard.html

CSV:
  * /csv/<tabela> - Fazer download de uma das tabelas da db em formato csv.
    Faz redirect para outro endpoint (/download/<filename>) para ficheiro ficar com nome certo
    Problema: Gera no servidor um ficheiro csv sempre que o endpoint é acessado, o que é chato e wasteful.
              Não encontrei nenhuma forma de lidar com isso automaticamente (ou seja, fazer delete de ficheiros antigos)
              Confesso que não procurei muito.
              De qualquer forma, ir ao server e fazer rm dos ficheiros todos de vez em quando também resolve.
'''	


@app.route('/leaderboard', methods=['GET'])
def leaderboard():
	''' Mostra tabela com o número de medalhas que cada miúdo tem '''

	# Gerar lista de dicionários com info sobre quantas medalhas cada aluno tem
	leaderboard = []
	for aluno in Aluno.query.order_by(Aluno.nome).all():
		leaderboard.append(aluno.__dict__)

	# Devolver render da template. Ver template em templates/leaderboad.html
	return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/dashboard', methods=['GET'])
def dashboard():
	''' Mostra tabela com as tarefas que cada miúdo já fez '''

	# Obter lista de todos os alunos
	alunos = Aluno.query.order_by(Aluno.nome).all()
	tarefas = Tarefa.query.all()

	# Dict que vai guardar info. Inicializado com valores todos a False.
	dashboard = {}
	for aluno in alunos:
		dashboard[aluno.nome] = {}
		for tarefa in tarefas:
			# Dict será da forma: {'[nome aluno]' : {'[tarefa 1]' : False, ...}}
			dashboard[aluno.nome][tarefa.descricao] = False
	
	# Percorrer todas as submissoes e marcar respetivas entradas no dict criado em cima
	for submissao in Submissao.query.all():
		dashboard[submissao.aluno.nome][submissao.tarefa.descricao]  = True

	# Criar lista de listas com as tarefas de cada semana
	tarefas_por_semana = []
	for i in range(1, num_semanas):
		semanas.append([tarefa.descricao for tarefa in Tarefa.query.all()])

	# Criar lista com nome dos alunos
	alunos = [aluno.nome for aluno in alunos]

	# Retornar a template renderizada com info arranjada antes. Ver 'templates/dashboard.html'
	return render_template('dashboard.html', alunos=alunos, semanas=semanas, dashboard=dashboard)

@app.route('/csv/<tabela>', methods=['GET'])
def get_csv(tabela):
	''' Gera .csv com toda a info de uma das tabelas da db '''

	# Verificar se tabela de facto tem nome de tabela.
	if tabela not in ['aluno', 'submissao', 'tarefa']:
		return '<h1> Deve ser \'aluno\', \'submissao\', \'tarefa\' </h1>'

	# Criar df de pandas com base na tabela
	df = pd.read_sql_table(tabela, 'sqlite:///data.db')

	# Nome do ficheiro para guardar df. Usa o tempo atual para garantir que ficheiro é único.
	filename = tabela + '_' + datetime.now().strftime('%m%d%Y_%H%M%S') + '.csv'

	# Guardar ficheiro. Noutra pasta para organizar as coisas
	df.to_csv('/csv_downloads/' + filename)

	# Para garantir que ficheiro descarregado tem o nome certo, fazer redirect:
	return redirect('/download_csv/' + filename)

@app.route('/download_csv/<filename>')
def download_csv(filename):
	''' Envia .csv gerado por 'get_csv' para o user '''

	return send_file('/csv_downloads/' + filename)

if __name__ == '__main__':
	app.run()