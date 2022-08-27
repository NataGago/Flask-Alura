
from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
import tomli

# Carregando variaveis de banco de dados
with open("config.toml", mode="rb") as fp:
    config = tomli.load(fp)

DB_SGBD = config["database"]["DB_SGBD"]
DB_USER = config["database"]["DB_USER"]
DB_PASSWORD = config["database"]["DB_PASSWORD"]
DB_SERVER = config["database"]["DB_SERVER"]
DB_PORT = config["database"]["DB_PORT"]
DB_DATABASE = config["database"]["DB_DATABASE"]


app = Flask(__name__)
app.secret_key = "alura"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"{DB_SGBD}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_DATABASE}"

db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome = db.Column(db.String(50), nullable = False)
    categoria = db.Column(db.String(40), nullable = False)
    console = db.Column(db.String(20), nullable = False)
    
    def __repr__(self) -> str:
        return '<Name %r' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key= True)
    nome = db.Column(db.String(20), nullable = False)
    senha = db.Column(db.String(100), nullable = False)
    
    def __repr__(self) -> str:
        return '<Name %r' % self.name



@app.get("/")
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template("lista.html", titulo="Jogos", jogos=lista)


@app.get("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login", proxima=url_for("novo")))
    return render_template("novo.html", titulo="Novo Jogo")


@app.post("/criar")
def criar():
    nome = request.form["nome"]
    categoria = request.form["categoria"]
    console = request.form["console"]
    
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("Jogo já existente.")
        return redirect(url_for("index"))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for("index"))


@app.get("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@app.post("/autenticar")
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.get("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
