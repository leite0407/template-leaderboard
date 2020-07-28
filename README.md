# Template Leaderboard After School

## O que é?
Template de um site que pode ser usado durante um curso After School para manter o registo das tarefas já feitas pelos alunos do curso. Originalmente, foi pensado para ser um leaderboard do curso, que mostraria o número de pontos/medalhas ganhos por um aluno (em que fazer tarefas => ganhar pontos/medalhas). Pode ser usado para isto ou alternativamente simplesmente como uma ferramenta do instrutor para manter conta de quem anda a fazer o quê.

## Como funciona?
Recebe e regista informação dos sitios onde os miúdos fazem as tarefas (quizzes em google forms, exercicios repl.it, badges atribuidas pelos instrutores no fórum, etc.) através de webhooks. Mostra essa informação num dado url.

Está escrito em python (claro), usa flask.

## O que tenho de fazer para criar um leaderboard para o meu After School? 
Ler o guia abaixo!

## Guia
TODO

## Como está estruturado o código?
* **leaderboard.py** - Ficheiro principal. App Flask.
* **tabelas_db.py** - Base de dados.

## Problemas
* Como registar alunos e tarefas?
	* Ficheiro json / csv e um script
	* Form online
* Guardar medalhas?