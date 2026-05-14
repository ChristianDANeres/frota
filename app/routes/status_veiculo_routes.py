from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from app.extensions import db
from app.models import StatusVeiculo
from app.forms.status_veiculo_form import StatusVeiculoForm
from app.common.decorators import cliente_required, menu_required

status_veiculo_bp = Blueprint('status_veiculo', __name__, url_prefix='/status-veiculo')


@status_veiculo_bp.route('/')
@login_required
@cliente_required
@menu_required('status_veiculo')
def listar():
    q = request.args.get('q', '')
    query = StatusVeiculo.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(StatusVeiculo.nome.ilike(f'%{q}%'))
    registros = query.order_by(StatusVeiculo.nome).all()
    return render_template('status_veiculo/listar.html', registros=registros, q=q)


@status_veiculo_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('status_veiculo')
def novo():
    form = StatusVeiculoForm()
    if form.validate_on_submit():
        obj = StatusVeiculo(cliente_id=session['cliente_id'], nome=form.nome.data,
                            descricao=form.descricao.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        flash('Status de veículo criado.', 'success')
        return redirect(url_for('status_veiculo.listar'))
    return render_template('status_veiculo/form.html', form=form, titulo='Novo Status de Veículo')


@status_veiculo_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('status_veiculo')
def editar(id):
    obj = StatusVeiculo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = StatusVeiculoForm()
    if form.validate_on_submit():
        obj.nome = form.nome.data
        obj.descricao = form.descricao.data
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Status de veículo atualizado.', 'success')
        return redirect(url_for('status_veiculo.listar'))
    form.nome.data = obj.nome
    form.descricao.data = obj.descricao
    form.ativo.data = obj.ativo
    return render_template('status_veiculo/form.html', form=form, titulo='Editar Status de Veículo', obj=obj)


@status_veiculo_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('status_veiculo')
def visualizar(id):
    obj = StatusVeiculo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('status_veiculo/visualizar.html', obj=obj)


@status_veiculo_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('status_veiculo')
def excluir(id):
    obj = StatusVeiculo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    obj.ativo = False
    db.session.commit()
    flash('Status de veículo inativado.', 'warning')
    return redirect(url_for('status_veiculo.listar'))
