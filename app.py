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

app = Flask(__name__)
app.secret_key = "alura"
# app.run(host='0.0.0.0', port=8080, debug=True)

# export FLASK_APP=app.py
# export FLASK_ENV=development


class Jogo:
    def __init__(self, nome, categoria, console) -> None:
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo("Super Mario", "Ação", "SNES")
jogo2 = Jogo("Pokemon Gold", "RPG", "GBA")
jogo3 = Jogo("Mortal Kombat", "Luta", "SNES")
lista = [jogo1, jogo2, jogo3]


class Usuario:
    def __init__(self, nome, nickname, senha) -> None:
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Natã Gago", "natagago", "mestra")
usuario2 = Usuario("Gabriel Gago", "bielgago", "210799")
usuario3 = Usuario("Ronaldo Gago", "rogago", "gabitan")

usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3,
}


@app.get("/")
def index():
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
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for("index"))


@app.get("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)


@app.post("/autenticar")
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(f"{usuario.nome} logado com sucesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
    else:
        flash("Usuário não logado.")
        return redirect(url_for("login"))


@app.get("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
