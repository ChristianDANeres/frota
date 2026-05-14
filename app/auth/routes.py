from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required
from app.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_senha(senha) and usuario.ativo:
            login_user(usuario)
            return redirect(url_for('cliente.selecionar'))
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))
