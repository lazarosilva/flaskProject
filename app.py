from flask import Flask, render_template, request
import json
from flask import flash, redirect
from database import db, lm
from flask_migrate import Migrate
#from models import Usua
from usuarios import bp_usuarios
from pizzas import bp_pizzas
from pedidos import bp_pedidos

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

conexao = "sqlite:///meubanco.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')
app.register_blueprint(bp_pizzas, url_prefix='/pizzas')
app.register_blueprint(bp_pedidos, url_prefix='/pedidos')

db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/cardapio')
def cardapio():
  return render_template('cardapio.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.errorhandler(401)
def acesso_negado(e):
    # note that we set the 404 status explicitly
    return render_template('acesso_negado.html'), 404

""" 
@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    if usuario != 'admin' or senha != 'senha123':
      if (usuario == 'admin'):
          flash('O login está correto. ', "warning")
      else:
          flash('O login está incorreto. ', "danger")
      
      if (senha == 'senha123'):
          flash('A senha está correta. ', "warning")
      else:
          flash('A senha está incorreta. ', "danger")

      return redirect("/login")
    else:
	    return "Os dados recebidos foram: usuario = {} e senha = {}".format(usuario, senha)

@app.route("/teste_insert")
def teste_insert():
  u = Usuario("Lazaro Souza", "lss.lazaro@gmail.com", "123456")
  db.session.add(u)
  db.session.commit()
  return 'Dados inseridos com sucesso'

@app.route("/teste_select")
def teste_select():
  u = Usuario.query.all()
  if len(u) > 0:
    print(u)
    u = Usuario.query.get(1)
    return u.nome
  else:
    return 'sem usuarios cadastrados'

@app.route("/teste_update")
def teste_update():
  u = Usuario.query.get(1)
  u.nome = "Lazaro S."
  db.session.add(u)
  db.session.commit()
  return 'Dados atualizados com sucesso'

@app.route("/teste_delete")
def teste_delete():
  u = Usuario.query.get(1)
  db.session.delete(u)
  db.session.commit()
  return 'Dados removidos com sucesso'
 """
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)