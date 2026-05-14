from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from app.extensions import db
from app.models import Veiculo, Montadora, Cor, StatusVeiculo
from app.forms.veiculo_form import VeiculoForm
from app.common.decorators import cliente_required, menu_required

veiculo_bp = Blueprint('veiculo', __name__, url_prefix='/veiculo')


def _preencher_choices(form, cliente_id):
    montadoras = Montadora.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Montadora.nome).all()
    form.montadora_id.choices = [(0, 'Selecione...')] + [(m.id, m.nome) for m in montadoras]
    cores = Cor.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Cor.nome).all()
    form.cor_id.choices = [(0, 'Selecione...')] + [(c.id, c.nome) for c in cores]
    statuses = StatusVeiculo.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(StatusVeiculo.nome).all()
    form.status_veiculo_id.choices = [(0, 'Selecione...')] + [(s.id, s.nome) for s in statuses]


@veiculo_bp.route('/')
@login_required
@cliente_required
@menu_required('veiculo')
def listar():
    q = request.args.get('q', '')
    query = Veiculo.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(Veiculo.placa.ilike(f'%{q}%') | Veiculo.modelo.ilike(f'%{q}%'))
    registros = query.order_by(Veiculo.placa).all()
    return render_template('veiculo/listar.html', registros=registros, q=q)


@veiculo_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('veiculo')
def novo():
    form = VeiculoForm()
    _preencher_choices(form, session['cliente_id'])
    if form.validate_on_submit():
        obj = Veiculo(
            cliente_id=session['cliente_id'],
            placa=form.placa.data.upper().strip(),
            montadora_id=form.montadora_id.data or None,
            modelo=form.modelo.data,
            cor_id=form.cor_id.data or None,
            ano_fabricacao=form.ano_fabricacao.data,
            tipo_combustivel=form.tipo_combustivel.data or None,
            status_veiculo_id=form.status_veiculo_id.data or None,
            ativo=form.ativo.data,
        )
        db.session.add(obj)
        db.session.commit()
        flash('Veículo criado com sucesso.', 'success')
        return redirect(url_for('veiculo.listar'))
    return render_template('veiculo/form.html', form=form, titulo='Novo Veículo')


@veiculo_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('veiculo')
def editar(id):
    obj = Veiculo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = VeiculoForm()
    _preencher_choices(form, session['cliente_id'])
    if form.validate_on_submit():
        obj.placa = form.placa.data.upper().strip()
        obj.montadora_id = form.montadora_id.data or None
        obj.modelo = form.modelo.data
        obj.cor_id = form.cor_id.data or None
        obj.ano_fabricacao = form.ano_fabricacao.data
        obj.tipo_combustivel = form.tipo_combustivel.data or None
        obj.status_veiculo_id = form.status_veiculo_id.data or None
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Veículo atualizado.', 'success')
        return redirect(url_for('veiculo.listar'))
    form.placa.data = obj.placa
    form.montadora_id.data = obj.montadora_id or 0
    form.modelo.data = obj.modelo
    form.cor_id.data = obj.cor_id or 0
    form.ano_fabricacao.data = obj.ano_fabricacao
    form.tipo_combustivel.data = obj.tipo_combustivel or ''
    form.status_veiculo_id.data = obj.status_veiculo_id or 0
    form.ativo.data = obj.ativo
    return render_template('veiculo/form.html', form=form, titulo='Editar Veículo', obj=obj)


@veiculo_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('veiculo')
def visualizar(id):
    obj = Veiculo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('veiculo/visualizar.html', obj=obj)


@veiculo_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('veiculo')
def excluir(id):
    obj = Veiculo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    obj.ativo = False
    db.session.commit()
    flash('Veículo inativado.', 'warning')
    return redirect(url_for('veiculo.listar'))
