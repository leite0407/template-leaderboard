from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tarefa(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), unique=True)
    tipo = db.Column(db.String(50))
    semana = db.Column(db.Integer)
    nivel = db.Column(db.String(50))

    def __repr__(self):
        return f'<Tarefa descricao : {self.descricao} | id : {self.id}>'


class Submissao(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_tarefa = db.Column(db.Integer, db.ForeignKey('tarefa.id'))
    tarefa = db.relationship('Tarefa', backref=db.backref('submissoes', lazy=True))
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    aluno = db.relationship('Aluno', backref=db.backref('submissoes', lazy=True))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Submissao aluno : {self.aluno.nome} | tarefa : {self.tarefa.descricao} | timestamp : {self.timestamp}>'

class Aluno(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    bronze = db.Column(db.Integer)
    prata = db.Column(db.Integer)
    ouro = db.Column(db.Integer)

    def __repr__(self):
        return f'<Aluno nome : {self.nome} | id : {self.id}>'
