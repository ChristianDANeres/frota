from flask import Blueprint, render_template
from flask_login import login_required
from app.common.decorators import admin_required
from app.models import Usuario, Perfil, Menu, Cliente

security_bp = Blueprint('security', __name__, url_prefix='/security')


@security_bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    return render_template('security/lista.html', titulo='Usuários', registros=Usuario.query.order_by(Usuario.nome).all())


@security_bp.route('/perfis')
@login_required
@admin_required
def perfis():
    return render_template('security/lista.html', titulo='Perfis', registros=Perfil.query.order_by(Perfil.nome).all())


@security_bp.route('/menus')
@login_required
@admin_required
def menus():
    return render_template('security/lista.html', titulo='Menus', registros=Menu.query.order_by(Menu.ordem, Menu.nome).all())


@security_bp.route('/clientes')
@login_required
@admin_required
def clientes():
    return render_template('security/lista.html', titulo='Clientes', registros=Cliente.query.order_by(Cliente.nome).all())
