from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from models import Usuario
from database import db, lm
from datetime import date

bp_usuarios = Blueprint("usuarios", __name__, template_folder="templates")

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=='GET':
        return render_template('usuarios_create.html')
    
    if request.method=='POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        p = Usuario(nome, email, senha)
        db.session.add(p)
        db.session.commit()
        return 'Usuario cadastrado com sucesso'

@bp_usuarios.route('/recovery')
def recovery():
    usuarios = Usuario.query.all()
    return render_template('usuarios_recovery.html', usuarios=usuarios)

@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):    
    if id and request.method == 'GET':
        usuario = Usuario.query.get(id)
        return render_template('usuarios_update.html', usuario=usuario)

    if request.method == 'POST':
        usuario = Usuario.query.get(id)
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')

        if request.form.get('senha') and request.form.get('senha') == request.form.get('csenha'):
            usuario.senha = request.form.get('senha')
        else:
            flash('senhas não conferem')
            return redirect(url_for('.update', id=id))
        
        db.session.add(usuario)
        db.session.commit()
        flash('Dados atualizados com sucesso')
        return redirect(url_for('.recovery', id=id))

@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
     
    if id and request.method == 'GET':
        usuario = Usuario.query.get(id)
        return render_template('usuarios_delete.html', usuario=usuario)
    
    if request.method == 'POST':
        u = Usuario.query.get(id)
        db.session.delete(u)
        db.session.commit()

        usuarios = Usuario.query.all()
        return render_template('usuarios_recovery.html', usuarios=usuarios)


@lm.user_loader
def load_user(id):
    usuario = Usuario.query.filter_by(id=id).first()
    #usuario = Usuario.query.get(id)
    return usuario