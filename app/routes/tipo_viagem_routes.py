from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from app.extensions import db
from app.models import TipoViagem
from app.forms.tipo_viagem_form import TipoViagemForm
from app.common.decorators import cliente_required, menu_required

tipo_viagem_bp = Blueprint('tipo_viagem', __name__, url_prefix='/tipo-viagem')


@tipo_viagem_bp.route('/')
@login_required
@cliente_required
@menu_required('tipo_viagem')
def listar():
    q = request.args.get('q', '')
    query = TipoViagem.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(TipoViagem.nome.ilike(f'%{q}%'))
    registros = query.order_by(TipoViagem.nome).all()
    return render_template('tipo_viagem/listar.html', registros=registros, q=q)


@tipo_viagem_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('tipo_viagem')
def novo():
    form = TipoViagemForm()
    if form.validate_on_submit():
        obj = TipoViagem(cliente_id=session['cliente_id'], nome=form.nome.data,
                         descricao=form.descricao.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        flash('Tipo de viagem criado.', 'success')
        return redirect(url_for('tipo_viagem.listar'))
    return render_template('tipo_viagem/form.html', form=form, titulo='Novo Tipo de Viagem')


@tipo_viagem_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('tipo_viagem')
def editar(id):
    obj = TipoViagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = TipoViagemForm()
    if form.validate_on_submit():
        obj.nome = form.nome.data
        obj.descricao = form.descricao.data
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Tipo de viagem atualizado.', 'success')
        return redirect(url_for('tipo_viagem.listar'))
    form.nome.data = obj.nome
    form.descricao.data = obj.descricao
    form.ativo.data = obj.ativo
    return render_template('tipo_viagem/form.html', form=form, titulo='Editar Tipo de Viagem', obj=obj)


@tipo_viagem_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('tipo_viagem')
def visualizar(id):
    obj = TipoViagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('tipo_viagem/visualizar.html', obj=obj)


@tipo_viagem_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('tipo_viagem')
def excluir(id):
    obj = TipoViagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    obj.ativo = False
    db.session.commit()
    flash('Tipo de viagem inativado.', 'warning')
    return redirect(url_for('tipo_viagem.listar'))
