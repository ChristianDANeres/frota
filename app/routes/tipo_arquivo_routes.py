from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from app.extensions import db
from app.models import TipoArquivo
from app.forms.tipo_arquivo_form import TipoArquivoForm
from app.common.decorators import cliente_required, menu_required

tipo_arquivo_bp = Blueprint('tipo_arquivo', __name__, url_prefix='/tipo-arquivo')


@tipo_arquivo_bp.route('/')
@login_required
@cliente_required
@menu_required('tipo_arquivo')
def listar():
    q = request.args.get('q', '')
    query = TipoArquivo.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(TipoArquivo.nome.ilike(f'%{q}%'))
    registros = query.order_by(TipoArquivo.nome).all()
    return render_template('tipo_arquivo/listar.html', registros=registros, q=q)


@tipo_arquivo_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('tipo_arquivo')
def novo():
    form = TipoArquivoForm()
    if form.validate_on_submit():
        obj = TipoArquivo(cliente_id=session['cliente_id'], nome=form.nome.data,
                          descricao=form.descricao.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        flash('Tipo de arquivo criado.', 'success')
        return redirect(url_for('tipo_arquivo.listar'))
    return render_template('tipo_arquivo/form.html', form=form, titulo='Novo Tipo de Arquivo')


@tipo_arquivo_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('tipo_arquivo')
def editar(id):
    obj = TipoArquivo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = TipoArquivoForm()
    if form.validate_on_submit():
        obj.nome = form.nome.data
        obj.descricao = form.descricao.data
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Tipo de arquivo atualizado.', 'success')
        return redirect(url_for('tipo_arquivo.listar'))
    form.nome.data = obj.nome
    form.descricao.data = obj.descricao
    form.ativo.data = obj.ativo
    return render_template('tipo_arquivo/form.html', form=form, titulo='Editar Tipo de Arquivo', obj=obj)


@tipo_arquivo_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('tipo_arquivo')
def visualizar(id):
    obj = TipoArquivo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('tipo_arquivo/visualizar.html', obj=obj)


@tipo_arquivo_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('tipo_arquivo')
def excluir(id):
    obj = TipoArquivo.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    obj.ativo = False
    db.session.commit()
    flash('Tipo de arquivo inativado.', 'warning')
    return redirect(url_for('tipo_arquivo.listar'))
