from flask import Flask, flash, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = 'alura'
# app.run(host='0.0.0.0', port=8080, debug=True)

# export FLASK_APP=app.py
# export FLASK_ENV=development


class Jogo():
    
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
    
lista = [jogo1, jogo2, jogo3]

@app.get('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.get('/novo')
def novo():
    return render_template('novo.html', titulo='Novo Jogo')

@app.post('/criar')
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')

@app.get('/login')
def login():
    return render_template('login.html')

@app.post('/autenticar')
def autenticar():
    if 'mestra' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(f"{session['usuario_logado']} logado com sucesso!")
        return redirect('/')
    else:
        flash('Usuário não logado.')
        return redirect('/login')
