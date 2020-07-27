from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabela das Tarefas
class Tarefa(db.Model):

	# id numérico
	id = db.Column(db.Integer, primary_key=True)
	# 'Nome' da tarefa, e.g.: 'Aula 5 - Ex 4'
	descricao = db.Column(db.String(50), unique=True)
	# tipo <=> 'proveniencia', e.g.: replit, quiz, etc. 
	tipo = db.Column(db.String(50))
	# semana de que é a tarefa
	semana = db.Column(db.Integer)

	# É o que é chamado quando se faz print de uma tarefa
	def __repr__(self):
		return f'<Tarefa descricao : {self.descricao} | id : {self.id}>'	

# Tabela dos Alunos
class Aluno(db.Model):

	# id numérico
	id = db.Column(db.Integer, primary_key=True)
	# email do aluni
	mail = db.Column(db.String(50))
	# nome do aluno
	nome = db.Column(db.String(50))
	# contagem de medalhas do aluno
	bronze = db.Column(db.Integer)
	prata = db.Column(db.Integer)
	ouro = db.Column(db.Integer)

	# É o que é chamado quando se faz print de uma tarefa
	def __repr__(self):
		return f'<Aluno nome : {self.nome} | id : {self.id}>'


# Tabela das Submissões
class Submissao(db.Model):

	# id numérico
	id = db.Column(db.Integer, primary_key=True)
	# tarefa a que diz respeito a submissao
	id_tarefa = db.Column(db.Integer, db.ForeignKey('tarefa.id'))
	tarefa = db.relationship('Tarefa', backref=db.backref('submissoes', lazy=True))
	# aluno de quem é a submissao
	id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'))
	aluno = db.relationship('Aluno', backref=db.backref('submissoes', lazy=True))
	# Hora e data da submissao
	timestamp = db.Column(db.DateTime)

	# É chamada quando se faz print de uma submissao
	def __repr__(self):
		return f'<Submissao aluno : {self.aluno.nome} | tarefa : {self.tarefa.descricao} | timestamp : {self.timestamp}>'