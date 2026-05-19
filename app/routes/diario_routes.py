import os
import uuid
from datetime import date, datetime
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, session, current_app)
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Diario, DiarioAnexo, Veiculo, Motorista, TipoArquivo
from app.forms.diario_form import DiarioForm, DiarioAnexoForm
from app.common.decorators import cliente_required, menu_required

diario_bp = Blueprint('diario', __name__, url_prefix='/diario')

# ── helpers ───────────────────────────────────────────────────────────────────

def _preencher_choices(form, cliente_id):
    veiculos = (Veiculo.query
                .filter_by(cliente_id=cliente_id, ativo=True)
                .order_by(Veiculo.placa).all())
    form.veiculo_id.choices = [(0, 'Selecione...')] + [
        (v.id, f'{v.placa} – {v.modelo or ""}') for v in veiculos
    ]
    motoristas = (Motorista.query
                  .filter_by(cliente_id=cliente_id, ativo=True)
                  .order_by(Motorista.nome).all())
    form.motorista_id.choices = [(0, 'Selecione...')] + [
        (m.id, m.nome) for m in motoristas
    ]


def _proximo_codigo(cliente_id):
    """Gera código sequencial no formato DI-YYYY-NNNN."""
    ano = date.today().year
    prefixo = f'DI-{ano}-'
    ultimo = (Diario.query
               .filter_by(cliente_id=cliente_id)
               .filter(Diario.codigo.like(f'{prefixo}%'))
               .order_by(Diario.id.desc())
               .first())
    if ultimo:
        try:
            seq = int(ultimo.codigo.split('-')[-1]) + 1
        except (ValueError, IndexError):
            seq = 1
    else:
        seq = 1
    return f'{prefixo}{seq:04d}'


# ── CRUD ──────────────────────────────────────────────────────────────────────

@diario_bp.route('/')
@login_required
@cliente_required
@menu_required('diario')
def listar():
    q = request.args.get('q', '')
    query = Diario.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = (query
                 .join(Veiculo)
                 .filter(
                     Veiculo.placa.ilike(f'%{q}%') |
                     Diario.codigo.ilike(f'%{q}%')
                 ))
    registros = query.order_by(Diario.data.desc()).all()
    return render_template('diario/listar.html', registros=registros, q=q)


@diario_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('diario')
def novo():
    form = DiarioForm()
    _preencher_choices(form, session['cliente_id'])
    if request.method == 'GET':
        form.codigo.data = _proximo_codigo(session['cliente_id'])
        form.data.data = date.today()
    if form.validate_on_submit():
        # Verifica unicidade do código
        existe = Diario.query.filter_by(
            cliente_id=session['cliente_id'],
            codigo=form.codigo.data.strip()
        ).first()
        if existe:
            flash('Este código já está em uso. Informe outro.', 'danger')
            return render_template('diario/form.html', form=form, titulo='Novo Diário')
        obj = Diario(
            cliente_id=session['cliente_id'],
            codigo=form.codigo.data.strip(),
            veiculo_id=form.veiculo_id.data,
            motorista_id=form.motorista_id.data or None,
            data=form.data.data,
            km=form.km.data,
            texto=form.texto.data,
        )
        db.session.add(obj)
        db.session.commit()
        flash('Diário registrado com sucesso.', 'success')
        return redirect(url_for('diario.visualizar', id=obj.id))
    return render_template('diario/form.html', form=form, titulo='Novo Diário')


@diario_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('diario')
def editar(id):
    obj = Diario.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = DiarioForm()
    _preencher_choices(form, session['cliente_id'])
    if form.validate_on_submit():
        novo_cod = form.codigo.data.strip()
        if novo_cod != obj.codigo:
            existe = Diario.query.filter_by(
                cliente_id=session['cliente_id'],
                codigo=novo_cod
            ).first()
            if existe:
                flash('Este código já está em uso. Informe outro.', 'danger')
                return render_template('diario/form.html', form=form,
                                       titulo='Editar Diário', obj=obj)
        obj.codigo       = novo_cod
        obj.veiculo_id   = form.veiculo_id.data
        obj.motorista_id = form.motorista_id.data or None
        obj.data         = form.data.data
        obj.km           = form.km.data
        obj.texto        = form.texto.data
        db.session.commit()
        flash('Diário atualizado.', 'success')
        return redirect(url_for('diario.visualizar', id=obj.id))
    # GET — preencher form
    form.codigo.data       = obj.codigo
    form.veiculo_id.data   = obj.veiculo_id
    form.motorista_id.data = obj.motorista_id or 0
    form.data.data         = obj.data
    form.km.data           = obj.km
    form.texto.data        = obj.texto
    return render_template('diario/form.html', form=form, titulo='Editar Diário', obj=obj)


@diario_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('diario')
def visualizar(id):
    obj = Diario.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('diario/visualizar.html', obj=obj)


@diario_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('diario')
def excluir(id):
    obj = Diario.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    # Remove arquivos físicos
    for anexo in obj.anexos:
        if os.path.exists(anexo.caminho_arquivo):
            os.remove(anexo.caminho_arquivo)
    db.session.delete(obj)
    db.session.commit()
    flash('Diário excluído.', 'warning')
    return redirect(url_for('diario.listar'))


# ── Anexos ────────────────────────────────────────────────────────────────────

@diario_bp.route('/<int:id>/anexos')
@login_required
@cliente_required
@menu_required('diario')
def anexos(id):
    obj = Diario.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    tipos_arquivo = (TipoArquivo.query
                     .filter_by(cliente_id=session['cliente_id'], ativo=True)
                     .order_by(TipoArquivo.nome).all())
    form = DiarioAnexoForm()
    form.tipo_arquivo_id.choices = [(0, 'Selecione...')] + [
        (t.id, t.nome) for t in tipos_arquivo
    ]
    return render_template('diario/anexos.html', obj=obj, form=form)


@diario_bp.route('/<int:id>/anexos/upload', methods=['POST'])
@login_required
@cliente_required
@menu_required('diario')
def upload_anexo(id):
    obj = Diario.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    tipos_arquivo = (TipoArquivo.query
                     .filter_by(cliente_id=session['cliente_id'], ativo=True)
                     .order_by(TipoArquivo.nome).all())
    form = DiarioAnexoForm()
    form.tipo_arquivo_id.choices = [(0, 'Selecione...')] + [
        (t.id, t.nome) for t in tipos_arquivo
    ]
    if form.validate_on_submit():
        arquivo = form.arquivo.data
        nome_seguro = secure_filename(arquivo.filename)
        ext = os.path.splitext(nome_seguro)[1]
        nome_unico = f'{uuid.uuid4().hex}{ext}'
        pasta = os.path.join(current_app.root_path, 'static', 'uploads',
                             'diario', str(obj.id))
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, nome_unico)
        arquivo.save(caminho)
        tamanho = os.path.getsize(caminho)
        anexo = DiarioAnexo(
            cliente_id=session['cliente_id'],
            diario_id=obj.id,
            tipo_arquivo_id=form.tipo_arquivo_id.data or None,
            nome_arquivo=nome_seguro,
            caminho_arquivo=caminho,
            tamanho_arquivo=tamanho,
        )
        db.session.add(anexo)
        db.session.commit()
        flash('Anexo enviado com sucesso.', 'success')
    else:
        for field, erros in form.errors.items():
            for erro in erros:
                flash(f'{erro}', 'danger')
    return redirect(url_for('diario.anexos', id=id))


@diario_bp.route('/<int:id>/anexos/<int:anexo_id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('diario')
def excluir_anexo(id, anexo_id):
    anexo = DiarioAnexo.query.filter_by(
        id=anexo_id, diario_id=id,
        cliente_id=session['cliente_id']
    ).first_or_404()
    if os.path.exists(anexo.caminho_arquivo):
        os.remove(anexo.caminho_arquivo)
    db.session.delete(anexo)
    db.session.commit()
    flash('Anexo removido.', 'warning')
    return redirect(url_for('diario.anexos', id=id))


@diario_bp.route('/<int:id>/imprimir')
@login_required
@cliente_required
def imprimir(id):
    obj = Diario.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('diario/imprimir.html', obj=obj, agora=datetime.now())
