import requests as rq
import json
import csv
import pandas as pd
import sqlite3

# Links para os endpoints da api interna do repl.it
link_assignments = "https://repl.it/data/classrooms/184710/assignments"
link_students = "https://repl.it/data/teacher/classrooms/184710/students"
link_submissions = "https://repl.it/data/teacher/classrooms/184710/submissions"

# Cookie com o id da sessão iniciada no rep.it para passar nos requests
cookie = {'connect.sid' : 's%3ASUMBXm17E4SrTeeioWZrTfBtszFRgslZ.J4V8v5z5jQX9BE3qyaM%2BRmMh%2FhkB1gmbvE7LPbVJERc'}

# Enviar requests, processar json recebido
assignments_list = json.loads(rq.get(link_assignments, cookies=cookie).content)
students_list = json.loads(rq.get(link_students, cookies=cookie).content)

# json das submissions vem como um dict com as submissions divididas por assignment
submissions_dict = json.loads(rq.get(link_submissions, cookies=cookie).content)
submissions_list = []
for a in submissions_dict:
    submissions_list += submissions_dict[a]

# Fazer um DataFrame do Pandas com cada lista
assignments_df = pd.DataFrame(assignments_list)
students_df = pd.DataFrame(students_list)
submissions_df = pd.DataFrame(submissions_list)




# Tratar os dados e criar tabelas:

# Criar base de dados
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Assignments:

# Criar coluna com a week de cada assignment e com o type do assignment (silver em todos)
assignments_df['week'] = assignments_df.apply(lambda row: row['name'].split(' ')[1], axis=1)
assignments_df['type'] = assignments_df.apply(lambda row: 'silver', axis=1)

# Manter apenas colunas que interessam
assingments_df = assignments_df.filter(['id', 'type', 'week'])

# Adicionar quizzes e checkpoints

# Criar tabela na 

# Students


with open('submissions.csv', 'w') as f:
    writer = csv.writer(f)

    writer.writerow([
        'assignment_id',
        'student_id',
        'timestamp'
    ])

for submission in submissions_list:
    with open('submissions.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow([
            submission['assignment_id'],
            submission['student_id'],
            submission['time_submitted']
        ])

with open('assignments.csv', 'w') as f:
    writer = csv.writer(f)

    writer.writerow([
        'id',
        'type',
        'week'
    ])