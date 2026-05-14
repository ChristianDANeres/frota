import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Motorista, MotoristaAnexo, TipoArquivo
from app.forms.motorista_form import MotoristaForm, MotoristaAnexoForm
from app.common.decorators import cliente_required, menu_required

motorista_bp = Blueprint('motorista', __name__, url_prefix='/motorista')


@motorista_bp.route('/')
@login_required
@cliente_required
@menu_required('motorista')
def listar():
    q = request.args.get('q', '')
    query = Motorista.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(Motorista.nome.ilike(f'%{q}%') | Motorista.cpf.ilike(f'%{q}%'))
    registros = query.order_by(Motorista.nome).all()
    return render_template('motorista/listar.html', registros=registros, q=q)


@motorista_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('motorista')
def novo():
    form = MotoristaForm()
    if form.validate_on_submit():
        obj = Motorista(
            cliente_id=session['cliente_id'],
            cpf=form.cpf.data.strip(),
            nome=form.nome.data,
            data_nascimento=form.data_nascimento.data,
            cnh=form.cnh.data.strip(),
            ativo=form.ativo.data,
        )
        db.session.add(obj)
        db.session.commit()
        flash('Motorista criado com sucesso.', 'success')
        return redirect(url_for('motorista.listar'))
    return render_template('motorista/form.html', form=form, titulo='Novo Motorista')


@motorista_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('motorista')
def editar(id):
    obj = Motorista.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = MotoristaForm()
    if form.validate_on_submit():
        obj.cpf = form.cpf.data.strip()
        obj.nome = form.nome.data
        obj.data_nascimento = form.data_nascimento.data
        obj.cnh = form.cnh.data.strip()
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Motorista atualizado.', 'success')
        return redirect(url_for('motorista.listar'))
    form.cpf.data = obj.cpf
    form.nome.data = obj.nome
    form.data_nascimento.data = obj.data_nascimento
    form.cnh.data = obj.cnh
    form.ativo.data = obj.ativo
    return render_template('motorista/form.html', form=form, titulo='Editar Motorista', obj=obj)


@motorista_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('motorista')
def visualizar(id):
    obj = Motorista.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('motorista/visualizar.html', obj=obj)


@motorista_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('motorista')
def excluir(id):
    obj = Motorista.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    obj.ativo = False
    db.session.commit()
    flash('Motorista inativado.', 'warning')
    return redirect(url_for('motorista.listar'))


@motorista_bp.route('/<int:id>/anexos', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('motorista')
def anexos(id):
    obj = Motorista.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = MotoristaAnexoForm()
    tipos = TipoArquivo.query.filter_by(cliente_id=session['cliente_id'], ativo=True).order_by(TipoArquivo.nome).all()
    form.tipo_arquivo_id.choices = [(0, 'Selecione...')] + [(t.id, t.nome) for t in tipos]
    if form.validate_on_submit():
        arquivo = form.arquivo.data
        nome_seguro = secure_filename(arquivo.filename)
        ext = os.path.splitext(nome_seguro)[1]
        nome_unico = f"{uuid.uuid4().hex}{ext}"
        pasta = os.path.join(current_app.root_path, 'static', 'uploads', 'motorista', str(obj.id))
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome_unico)
        arquivo.save(caminho)
        tamanho = os.path.getsize(caminho)
        anexo = MotoristaAnexo(
            cliente_id=session['cliente_id'],
            motorista_id=obj.id,
            tipo_arquivo_id=form.tipo_arquivo_id.data or None,
            nome_arquivo=nome_seguro,
            caminho_arquivo=caminho,
            tamanho_arquivo=tamanho,
        )
        db.session.add(anexo)
        db.session.commit()
        flash('Anexo enviado com sucesso.', 'success')
        return redirect(url_for('motorista.anexos', id=obj.id))
    return render_template('motorista/anexos.html', obj=obj, form=form)


@motorista_bp.route('/<int:id>/anexos/<int:anexo_id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('motorista')
def excluir_anexo(id, anexo_id):
    anexo = MotoristaAnexo.query.filter_by(id=anexo_id, motorista_id=id,
                                           cliente_id=session['cliente_id']).first_or_404()
    if os.path.exists(anexo.caminho_arquivo):
        os.remove(anexo.caminho_arquivo)
    db.session.delete(anexo)
    db.session.commit()
    flash('Anexo removido.', 'warning')
    return redirect(url_for('motorista.anexos', id=id))
