from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user
from app.models import Cliente

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')


@cliente_bp.route('/selecionar', methods=['GET', 'POST'])
@login_required
def selecionar():
    if request.method == 'POST':
        cliente_id = int(request.form.get('cliente_id'))
        if current_user.tem_acesso_cliente(cliente_id):
            session['cliente_id'] = cliente_id
            return redirect(url_for('dashboard'))
        flash('Você não tem acesso a este cliente.', 'danger')

    if current_user.is_admin:
        clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    else:
        clientes = [uc.cliente for uc in current_user.clientes if uc.cliente.ativo]
    return render_template('cliente/selecionar.html', clientes=clientes)
