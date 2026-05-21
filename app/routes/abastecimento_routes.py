import os
import uuid
from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app.extensions import db
from app.models import Abastecimento, AbastecimentoAnexo, Veiculo, Motorista, TipoArquivo, Cliente
from app.forms.abastecimento_form import AbastecimentoForm, AbastecimentoAnexoForm
from app.common.decorators import cliente_required, menu_required

abastecimento_bp = Blueprint('abastecimento', __name__, url_prefix='/abastecimento')


def _preencher_choices(form, cliente_id):
    veiculos = Veiculo.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Veiculo.placa).all()
    form.veiculo_id.choices = [(0, 'Selecione...')] + [(v.id, f'{v.placa} – {v.modelo or ""}') for v in veiculos]
    motoristas = Motorista.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Motorista.nome).all()
    form.motorista_id.choices = [(0, 'Selecione...')] + [(m.id, m.nome) for m in motoristas]
    # combustivel choices são estáticas no formulário


@abastecimento_bp.route('/')
@login_required
@cliente_required
@menu_required('abastecimento')
def listar():
    q = request.args.get('q', '')
    query = Abastecimento.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.join(Veiculo).filter(Veiculo.placa.ilike(f'%{q}%'))
    registros = query.order_by(Abastecimento.data.desc()).all()
    return render_template('abastecimento/listar.html', registros=registros, q=q)


@abastecimento_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('abastecimento')
def novo():
    form = AbastecimentoForm()
    _preencher_choices(form, session['cliente_id'])
    if form.validate_on_submit():
        obj = Abastecimento(
            cliente_id=session['cliente_id'],
            data=form.data.data,
            veiculo_id=form.veiculo_id.data,
            motorista_id=form.motorista_id.data or None,
            km=form.km.data,
            quantidade=form.quantidade.data,
            tipo_combustivel=form.tipo_combustivel.data or None,
            valor=form.valor.data,
        )
        db.session.add(obj)
        db.session.commit()
        flash('Abastecimento registrado.', 'success')
        return redirect(url_for('abastecimento.listar'))
    return render_template('abastecimento/form.html', form=form, titulo='Novo Abastecimento')


@abastecimento_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('abastecimento')
def editar(id):
    obj = Abastecimento.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = AbastecimentoForm()
    _preencher_choices(form, session['cliente_id'])
    if form.validate_on_submit():
        obj.data = form.data.data
        obj.veiculo_id = form.veiculo_id.data
        obj.motorista_id = form.motorista_id.data or None
        obj.km = form.km.data
        obj.quantidade = form.quantidade.data
        obj.tipo_combustivel = form.tipo_combustivel.data or None
        obj.valor = form.valor.data
        db.session.commit()
        flash('Abastecimento atualizado.', 'success')
        return redirect(url_for('abastecimento.listar'))
    form.data.data = obj.data
    form.veiculo_id.data = obj.veiculo_id
    form.motorista_id.data = obj.motorista_id or 0
    form.km.data = obj.km
    form.quantidade.data = obj.quantidade
    form.tipo_combustivel.data = obj.tipo_combustivel or ''
    form.valor.data = obj.valor
    return render_template('abastecimento/form.html', form=form, titulo='Editar Abastecimento', obj=obj)


@abastecimento_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('abastecimento')
def visualizar(id):
    obj = Abastecimento.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('abastecimento/visualizar.html', obj=obj)


@abastecimento_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('abastecimento')
def excluir(id):
    obj = Abastecimento.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    db.session.delete(obj)
    db.session.commit()
    flash('Abastecimento excluído.', 'warning')
    return redirect(url_for('abastecimento.listar'))


@abastecimento_bp.route('/<int:id>/anexos', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('abastecimento')
def anexos(id):
    obj = Abastecimento.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = AbastecimentoAnexoForm()
    tipos = TipoArquivo.query.filter_by(cliente_id=session['cliente_id'], ativo=True).order_by(TipoArquivo.nome).all()
    form.tipo_arquivo_id.choices = [(0, 'Selecione...')] + [(t.id, t.nome) for t in tipos]
    if form.validate_on_submit():
        arquivo = form.arquivo.data
        nome_seguro = secure_filename(arquivo.filename)
        ext = os.path.splitext(nome_seguro)[1]
        nome_unico = f"{uuid.uuid4().hex}{ext}"
        pasta = os.path.join(current_app.root_path, 'static', 'uploads', 'abastecimento', str(obj.id))
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome_unico)
        arquivo.save(caminho)
        tamanho = os.path.getsize(caminho)
        anexo = AbastecimentoAnexo(
            cliente_id=session['cliente_id'],
            abastecimento_id=obj.id,
            tipo_arquivo_id=form.tipo_arquivo_id.data or None,
            nome_arquivo=nome_seguro,
            caminho_arquivo=caminho,
            tamanho_arquivo=tamanho,
        )
        db.session.add(anexo)
        db.session.commit()
        flash('Anexo enviado com sucesso.', 'success')
        return redirect(url_for('abastecimento.anexos', id=obj.id))
    return render_template('abastecimento/anexos.html', obj=obj, form=form, tipos=tipos)


@abastecimento_bp.route('/<int:id>/anexos/<int:anexo_id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('abastecimento')
def excluir_anexo(id, anexo_id):
    anexo = AbastecimentoAnexo.query.filter_by(id=anexo_id, abastecimento_id=id,
                                                cliente_id=session['cliente_id']).first_or_404()
    if os.path.exists(anexo.caminho_arquivo):
        os.remove(anexo.caminho_arquivo)
    db.session.delete(anexo)
    db.session.commit()
    flash('Anexo removido.', 'warning')
    return redirect(url_for('abastecimento.anexos', id=id))


# ---------------------------------------------------------------------------
# Relatório de abastecimentos
# ---------------------------------------------------------------------------

def _dados_relatorio(cliente_id):
    """Lê os parâmetros da query string e devolve um dict com todos os dados
    necessários para renderizar o relatório (tela ou impressão)."""
    import calendar

    veiculo_id_str = request.args.get('veiculo_id', '')
    data_inicial_str = request.args.get('data_inicial', '')
    data_final_str = request.args.get('data_final', '')

    hoje = date.today()
    data_inicial_default = hoje.replace(day=1)
    ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
    data_final_default = hoje.replace(day=ultimo_dia)

    try:
        data_inicial = datetime.strptime(data_inicial_str, '%Y-%m-%d').date() if data_inicial_str else data_inicial_default
    except ValueError:
        data_inicial = data_inicial_default

    try:
        data_final = datetime.strptime(data_final_str, '%Y-%m-%d').date() if data_final_str else data_final_default
    except ValueError:
        data_final = data_final_default

    try:
        veiculo_id = int(veiculo_id_str) if veiculo_id_str else None
    except ValueError:
        veiculo_id = None

    # query base
    q = (
        db.session.query(Abastecimento)
        .filter(
            Abastecimento.cliente_id == cliente_id,
            Abastecimento.data >= data_inicial,
            Abastecimento.data <= data_final,
        )
    )
    if veiculo_id:
        q = q.filter(Abastecimento.veiculo_id == veiculo_id)
    registros = q.order_by(Abastecimento.data.desc()).all()

    total_valor = sum(float(r.valor) for r in registros)
    total_litros = sum(float(r.quantidade) for r in registros)
    total_registros = len(registros)

    # ranking por veículo
    rv_q = (
        db.session.query(
            Veiculo.placa,
            Veiculo.modelo,
            func.count(Abastecimento.id).label('qtd'),
            func.sum(Abastecimento.quantidade).label('total_litros'),
            func.sum(Abastecimento.valor).label('total_valor'),
        )
        .join(Abastecimento, Abastecimento.veiculo_id == Veiculo.id)
        .filter(
            Abastecimento.cliente_id == cliente_id,
            Abastecimento.data >= data_inicial,
            Abastecimento.data <= data_final,
        )
    )
    if veiculo_id:
        rv_q = rv_q.filter(Veiculo.id == veiculo_id)
    ranking_veiculo = rv_q.group_by(Veiculo.placa, Veiculo.modelo).order_by(func.sum(Abastecimento.valor).desc()).all()

    # ranking por tipo de combustível
    rc_q = (
        db.session.query(
            Abastecimento.tipo_combustivel,
            func.count(Abastecimento.id).label('qtd'),
            func.sum(Abastecimento.quantidade).label('total_litros'),
            func.sum(Abastecimento.valor).label('total_valor'),
        )
        .filter(
            Abastecimento.cliente_id == cliente_id,
            Abastecimento.data >= data_inicial,
            Abastecimento.data <= data_final,
        )
    )
    if veiculo_id:
        rc_q = rc_q.filter(Abastecimento.veiculo_id == veiculo_id)
    ranking_combustivel = rc_q.group_by(Abastecimento.tipo_combustivel).order_by(func.sum(Abastecimento.valor).desc()).all()

    veiculos = Veiculo.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Veiculo.placa).all()

    return dict(
        registros=registros,
        veiculos=veiculos,
        ranking_veiculo=ranking_veiculo,
        ranking_combustivel=ranking_combustivel,
        total_valor=total_valor,
        total_litros=total_litros,
        total_registros=total_registros,
        data_inicial=data_inicial,
        data_final=data_final,
        veiculo_id=veiculo_id,
    )


@abastecimento_bp.route('/relatorio')
@login_required
@cliente_required
@menu_required('abastecimento')
def relatorio():
    dados = _dados_relatorio(session['cliente_id'])
    return render_template('abastecimento/relatorio.html', **dados)


@abastecimento_bp.route('/relatorio/imprimir')
@login_required
@cliente_required
@menu_required('abastecimento')
def relatorio_imprimir():
    cliente_id = session['cliente_id']
    dados = _dados_relatorio(cliente_id)
    cliente = Cliente.query.get(cliente_id)
    return render_template(
        'abastecimento/relatorio_imprimir.html',
        **dados,
        cliente=cliente,
        agora=datetime.now(),
    )

