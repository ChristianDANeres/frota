import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app, send_file, abort
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import VeiculoOficina, VeiculoOficinaAnexo, Veiculo, Oficina, Motorista, TipoArquivo
from app.forms.veiculo_oficina_form import VeiculoOficinaForm, VeiculoOficinaAnexoForm
from app.common.decorators import cliente_required, menu_required

veiculo_oficina_bp = Blueprint('veiculo_oficina', __name__, url_prefix='/veiculo_oficina')


@veiculo_oficina_bp.route('/')
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def listar():
    q = request.args.get('q', '')
    query = VeiculoOficina.query.filter_by(cliente_id=session['cliente_id'])
    registros = query.order_by(VeiculoOficina.data_entrada.desc()).all()
    return render_template('veiculo_oficina/listar.html', registros=registros, q=q)


@veiculo_oficina_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def novo():
    form = VeiculoOficinaForm()
    tipos = Oficina.query.filter_by(cliente_id=session['cliente_id']).order_by(Oficina.nome).all()
    form.oficina_id.choices = [(0, 'Selecione...')] + [(t.id, t.nome) for t in tipos]
    veiculos = Veiculo.query.filter_by(cliente_id=session['cliente_id']).order_by(Veiculo.placa).all()
    form.veiculo_id.choices = [(0, 'Selecione...')] + [(v.id, v.placa) for v in veiculos]
    motoristas = Motorista.query.filter_by(cliente_id=session['cliente_id'], ativo=True).order_by(Motorista.nome).all()
    form.motorista_entrada_id.choices = [(0, 'Selecione...')] + [(m.id, m.nome) for m in motoristas]
    if form.validate_on_submit():
        obj = VeiculoOficina(
            cliente_id=session['cliente_id'],
            oficina_id=form.oficina_id.data,
            veiculo_id=form.veiculo_id.data,
            data_entrada=form.data_entrada.data,
            data_saida=form.data_saida.data or None,
            km_entrada=form.km_entrada.data or None,
            km_saida=form.km_saida.data or None,
            motorista_entrada_id=form.motorista_entrada_id.data or None,
            motivo=form.motivo.data or None,
        )
        db.session.add(obj)
        db.session.commit()
        flash('Registro de veículo em oficina criado.', 'success')
        return redirect(url_for('veiculo_oficina.listar'))
    return render_template('veiculo_oficina/form.html', form=form, titulo='Novo Registro Oficina')


@veiculo_oficina_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def editar(id):
    obj = VeiculoOficina.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = VeiculoOficinaForm()
    tipos = Oficina.query.filter_by(cliente_id=session['cliente_id']).order_by(Oficina.nome).all()
    form.oficina_id.choices = [(0, 'Selecione...')] + [(t.id, t.nome) for t in tipos]
    veiculos = Veiculo.query.filter_by(cliente_id=session['cliente_id']).order_by(Veiculo.placa).all()
    form.veiculo_id.choices = [(0, 'Selecione...')] + [(v.id, v.placa) for v in veiculos]
    motoristas = Motorista.query.filter_by(cliente_id=session['cliente_id'], ativo=True).order_by(Motorista.nome).all()
    form.motorista_entrada_id.choices = [(0, 'Selecione...')] + [(m.id, m.nome) for m in motoristas]
    if form.validate_on_submit():
        obj.oficina_id = form.oficina_id.data
        obj.veiculo_id = form.veiculo_id.data
        obj.data_entrada = form.data_entrada.data
        obj.data_saida = form.data_saida.data or None
        obj.km_entrada = form.km_entrada.data or None
        obj.km_saida = form.km_saida.data or None
        obj.motorista_entrada_id = form.motorista_entrada_id.data or None
        obj.motivo = form.motivo.data or None
        db.session.commit()
        flash('Registro atualizado.', 'success')
        return redirect(url_for('veiculo_oficina.listar'))
    form.oficina_id.data = obj.oficina_id
    form.veiculo_id.data = obj.veiculo_id
    form.data_entrada.data = obj.data_entrada
    form.data_saida.data = obj.data_saida
    form.km_entrada.data = obj.km_entrada
    form.km_saida.data = obj.km_saida
    form.motorista_entrada_id.data = obj.motorista_entrada_id
    form.motivo.data = obj.motivo
    return render_template('veiculo_oficina/form.html', form=form, titulo='Editar Registro Oficina', obj=obj)


@veiculo_oficina_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def visualizar(id):
    obj = VeiculoOficina.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('veiculo_oficina/visualizar.html', obj=obj)


@veiculo_oficina_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def excluir(id):
    obj = VeiculoOficina.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    db.session.delete(obj)
    db.session.commit()
    flash('Registro removido.', 'warning')
    return redirect(url_for('veiculo_oficina.listar'))


@veiculo_oficina_bp.route('/<int:id>/anexos', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def anexos(id):
    obj = VeiculoOficina.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = VeiculoOficinaAnexoForm()
    tipos = TipoArquivo.query.filter_by(cliente_id=session['cliente_id'], ativo=True).order_by(TipoArquivo.nome).all()
    form.tipo_arquivo_id.choices = [(0, 'Selecione...')] + [(t.id, t.nome) for t in tipos]
    if form.validate_on_submit():
        arquivo = form.arquivo.data
        nome_seguro = secure_filename(arquivo.filename)
        ext = os.path.splitext(nome_seguro)[1]
        nome_unico = f"{uuid.uuid4().hex}{ext}"
        pasta = os.path.join(current_app.root_path, 'static', 'uploads', 'veiculo_oficina', str(obj.id))
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome_unico)
        arquivo.save(caminho)
        tamanho = os.path.getsize(caminho)
        anexo = VeiculoOficinaAnexo(
            cliente_id=session['cliente_id'],
            veiculo_oficina_id=obj.id,
            tipo_arquivo_id=form.tipo_arquivo_id.data or None,
            nome_arquivo=nome_seguro,
            caminho_arquivo=caminho,
            tamanho_arquivo=tamanho,
        )
        db.session.add(anexo)
        db.session.commit()
        flash('Anexo enviado com sucesso.', 'success')
        return redirect(url_for('veiculo_oficina.anexos', id=obj.id))
    return render_template('veiculo_oficina/anexos.html', obj=obj, form=form)
    # calcular URL pública para cada anexo (relativo a /static)
    for a in obj.anexos:
        try:
            rel = os.path.relpath(a.caminho_arquivo, os.path.join(current_app.root_path, 'static'))
            rel = rel.replace('\\', '/')
            a.url = url_for('static', filename=rel)
        except Exception:
            a.url = '#'
    return render_template('veiculo_oficina/anexos.html', obj=obj, form=form)


@veiculo_oficina_bp.route('/<int:id>/anexos/<int:anexo_id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def excluir_anexo(id, anexo_id):
    anexo = VeiculoOficinaAnexo.query.filter_by(id=anexo_id, veiculo_oficina_id=id,
                                                cliente_id=session['cliente_id']).first_or_404()
    if os.path.exists(anexo.caminho_arquivo):
        os.remove(anexo.caminho_arquivo)
    db.session.delete(anexo)
    db.session.commit()
    flash('Anexo removido.', 'warning')
    return redirect(url_for('veiculo_oficina.anexos', id=id))


@veiculo_oficina_bp.route('/<int:id>/anexos/<int:anexo_id>/download')
@login_required
@cliente_required
@menu_required('veiculo_oficina')
def download_anexo(id, anexo_id):
    anexo = VeiculoOficinaAnexo.query.filter_by(id=anexo_id, veiculo_oficina_id=id,
                                                cliente_id=session['cliente_id']).first_or_404()
    if not os.path.exists(anexo.caminho_arquivo):
        abort(404)
    try:
        return send_file(anexo.caminho_arquivo, as_attachment=True, download_name=anexo.nome_arquivo)
    except Exception:
        abort(500)
