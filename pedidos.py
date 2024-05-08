from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from models import Pedido
from database import db
from datetime import date

bp_pedidos = Blueprint("pedidos", __name__, template_folder="templates")

@bp_pedidos.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=='GET':
        return render_template('pedidos_create.html')
    
    if request.method=='POST':
        usuario_id = request.form.get('usuario_id')
        pizza_id = request.form.get('pizza_id')
        data = date.today()
        p = Pedido(usuario_id, pizza_id, data)
        db.session.add(p)
        db.session.commit()
        return 'Pedido cadastrado com sucesso'

@bp_pedidos.route('/recovery')
def recovery():
    pedidos = Pedido.query.all()
    return render_template('pedidos_recovery.html', pedidos=pedidos)

@bp_pedidos.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if id and request.method == 'GET':
        pedido = Pedido.query.get(id)
        return render_template('pedidos_update.html', pedido=pedido)
    
    if request.method == 'POST':
        pedido = Pedido.query.get(id)
        pedido.pizza.id = request.form.get('piiza_id')
        pedido.usuario.id = request.form.get('usuario_id')
        pedido.data = request.form.get('data')

        db.session.add(pedido)
        db.session.commit()
        flash('Dados atualizados com sucesso')
        return redirect(url_for('.recovery', id=id))
    
@bp_pedidos.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if id and request.method == 'GET':
        pedido = Pedido.query.get(id)
        return render_template('pedidos_delete.html', pedido=pedido)
    
    if request.method == 'POST':
        u = Pedido.query.get(id)
        db.session.delete(u)
        db.session.commit()

        pedidos = Pedido.query.all()
        return render_template('pedidos_recovery.html', pedidos=pedidos)    