from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from models import Pizza
from database import db
from datetime import date

bp_pizzas = Blueprint("pizzas", __name__, template_folder="templates")

@bp_pizzas.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=='GET':
        return render_template('pizzas_create.html')
    
    if request.method=='POST':
        sabor = request.form.get('sabor')
        ingredientes = request.form.get('ingredientes')
        preco = request.form.get('preco')
        p = Pizza(sabor, ingredientes, preco)
        db.session.add(p)
        db.session.commit()
        return 'Pizza cadastrada com sucesso'

@bp_pizzas.route('/recovery')
def recovery():
    pizzas = Pizza.query.all()
    return render_template('pizzas_recovery.html', pizzas=pizzas)

@bp_pizzas.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if id and request.method == 'GET':
        pizza = Pizza.query.get(id)
        return render_template('pizzas_update.html', pizza=pizza)
    
    if request.method == 'POST':
        pizza = Pizza.query.get(id)
        pizza.sabor = request.form.get('sabor')
        pizza.ingredientes = request.form.get('ingredientes')
        pizza.preco = request.form.get('preco')

        db.session.add(pizza)
        db.session.commit()
        flash('Dados atualizados com sucesso')
        return redirect(url_for('.recovery', id=id))

@bp_pizzas.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if id and request.method == 'GET':
        pizza = Pizza.query.get(id)
        return render_template('pizzas_delete.html', pizza=pizza)
    
    if request.method == 'POST':
        u = Pizza.query.get(id)
        db.session.delete(u)
        db.session.commit()

        pizzas = Pizza.query.all()
        return render_template('pizzas_recovery.html', pizzas=pizzas)    