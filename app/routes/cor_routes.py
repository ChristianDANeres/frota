from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from app.extensions import db
from app.models import Cor
from app.forms.cor_form import CorForm
from app.common.decorators import cliente_required, menu_required

cor_bp = Blueprint('cor', __name__, url_prefix='/cor')


@cor_bp.route('/')
@login_required
@cliente_required
@menu_required('cor')
def listar():
    q = request.args.get('q', '')
    query = Cor.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(Cor.nome.ilike(f'%{q}%'))
    registros = query.order_by(Cor.nome).all()
    return render_template('cor/listar.html', registros=registros, q=q)


@cor_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('cor')
def novo():
    form = CorForm()
    if form.validate_on_submit():
        obj = Cor(cliente_id=session['cliente_id'], nome=form.nome.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        flash('Cor criada com sucesso.', 'success')
        return redirect(url_for('cor.listar'))
    return render_template('cor/form.html', form=form, titulo='Nova Cor')


@cor_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('cor')
def editar(id):
    obj = Cor.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = CorForm()
    if form.validate_on_submit():
        obj.nome = form.nome.data
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Cor atualizada.', 'success')
        return redirect(url_for('cor.listar'))
    form.nome.data = obj.nome
    form.ativo.data = obj.ativo
    return render_template('cor/form.html', form=form, titulo='Editar Cor', obj=obj)


@cor_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('cor')
def visualizar(id):
    obj = Cor.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('cor/visualizar.html', obj=obj)


@cor_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('cor')
def excluir(id):
    obj = Cor.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    obj.ativo = False
    db.session.commit()
    flash('Cor inativada.', 'warning')
    return redirect(url_for('cor.listar'))
