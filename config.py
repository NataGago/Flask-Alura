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

SECRET_KEY = "alura"

SQLALCHEMY_DATABASE_URI = f"{DB_SGBD}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_DATABASE}"