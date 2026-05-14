import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required
from app.extensions import db
from app.models import Montadora
from app.forms.montadora_form import MontadoraForm
from app.common.decorators import cliente_required, menu_required

montadora_bp = Blueprint('montadora', __name__, url_prefix='/montadora')


@montadora_bp.route('/')
@login_required
@cliente_required
@menu_required('montadora')
def listar():
    q = request.args.get('q', '')
    query = Montadora.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(Montadora.nome.ilike(f'%{q}%'))
    registros = query.order_by(Montadora.nome).all()
    return render_template('montadora/listar.html', registros=registros, q=q)


@montadora_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('montadora')
def novo():
    form = MontadoraForm()
    if form.validate_on_submit():
        obj = Montadora(cliente_id=session['cliente_id'], nome=form.nome.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        flash('Montadora criada com sucesso.', 'success')
        return redirect(url_for('montadora.listar'))
    return render_template('montadora/form.html', form=form, titulo='Nova Montadora')


@montadora_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('montadora')
def editar(id):
    obj = Montadora.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = MontadoraForm(obj=obj)
    if form.validate_on_submit():
        obj.nome = form.nome.data
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Montadora atualizada.', 'success')
        return redirect(url_for('montadora.listar'))
    form.nome.data = obj.nome
    form.ativo.data = obj.ativo
    return render_template('montadora/form.html', form=form, titulo='Editar Montadora', obj=obj)


@montadora_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('montadora')
def visualizar(id):
    obj = Montadora.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('montadora/visualizar.html', obj=obj)


@montadora_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('montadora')
def excluir(id):
    obj = Montadora.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    obj.ativo = False
    db.session.commit()
    flash('Montadora inativada.', 'warning')
    return redirect(url_for('montadora.listar'))
