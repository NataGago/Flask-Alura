from flask import (
    flash,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
)

from app import app, db
from models import Jogos, Usuarios

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

@app.get("/editar")
def editar():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login", proxima=url_for("editar")))
    return render_template("editar.html", titulo="Editando Jogo")

@app.post("/atualizar")
def atualizar():
    pass

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