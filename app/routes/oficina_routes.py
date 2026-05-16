from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from app.extensions import db
from app.models import Oficina
from app.forms.oficina_form import OficinaForm
from app.common.decorators import cliente_required, menu_required

oficina_bp = Blueprint('oficina', __name__, url_prefix='/oficina')


@oficina_bp.route('/')
@login_required
@cliente_required
@menu_required('oficina')
def listar():
    q = request.args.get('q', '')
    query = Oficina.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(Oficina.nome.ilike(f'%{q}%'))
    registros = query.order_by(Oficina.nome).all()
    return render_template('oficina/listar.html', registros=registros, q=q)


@oficina_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('oficina')
def novo():
    form = OficinaForm()
    if form.validate_on_submit():
        obj = Oficina(
            cliente_id=session['cliente_id'],
            cnpj=form.cnpj.data.strip() if form.cnpj.data else None,
            nome=form.nome.data,
            logradouro=form.logradouro.data,
            numero=form.numero.data,
            municipio=form.municipio.data,
            estado=form.estado.data,
            email=form.email.data,
            telefone=form.telefone.data,
            responsavel=form.responsavel.data,
        )
        db.session.add(obj)
        db.session.commit()
        flash('Oficina criada com sucesso.', 'success')
        return redirect(url_for('oficina.listar'))
    return render_template('oficina/form.html', form=form, titulo='Nova Oficina')


@oficina_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('oficina')
def editar(id):
    obj = Oficina.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = OficinaForm()
    if form.validate_on_submit():
        obj.cnpj = form.cnpj.data.strip() if form.cnpj.data else None
        obj.nome = form.nome.data
        obj.logradouro = form.logradouro.data
        obj.numero = form.numero.data
        obj.municipio = form.municipio.data
        obj.estado = form.estado.data
        obj.email = form.email.data
        obj.telefone = form.telefone.data
        obj.responsavel = form.responsavel.data
        db.session.commit()
        flash('Oficina atualizada.', 'success')
        return redirect(url_for('oficina.listar'))
    form.cnpj.data = obj.cnpj
    form.nome.data = obj.nome
    form.logradouro.data = obj.logradouro
    form.numero.data = obj.numero
    form.municipio.data = obj.municipio
    form.estado.data = obj.estado
    form.email.data = obj.email
    form.telefone.data = obj.telefone
    form.responsavel.data = obj.responsavel
    return render_template('oficina/form.html', form=form, titulo='Editar Oficina', obj=obj)


@oficina_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('oficina')
def visualizar(id):
    obj = Oficina.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('oficina/visualizar.html', obj=obj)


@oficina_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('oficina')
def excluir(id):
    obj = Oficina.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    db.session.delete(obj)
    db.session.commit()
    flash('Oficina removida.', 'warning')
    return redirect(url_for('oficina.listar'))
