from datetime import datetime
import re
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from app.extensions import db
from app.models import Viagem, ViagemPaciente, Veiculo, Motorista, TipoViagem
from app.models.viagem import StatusViagem
from app.forms.viagem_form import ViagemForm, ViagemPacienteForm
from app.common.decorators import cliente_required, menu_required

viagem_bp = Blueprint('viagem', __name__, url_prefix='/viagem')


def _preencher_choices(form, cliente_id):
    veiculos = Veiculo.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Veiculo.placa).all()
    form.veiculo_id.choices = [(0, 'Selecione...')] + [(v.id, f'{v.placa} – {v.modelo or ""}') for v in veiculos]
    motoristas = Motorista.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Motorista.nome).all()
    form.motorista_id.choices = [(0, 'Selecione...')] + [(m.id, m.nome) for m in motoristas]
    tipos = TipoViagem.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(TipoViagem.nome).all()
    form.tipo_viagem_id.choices = [(0, 'Selecione...')] + [(t.id, t.nome) for t in tipos]


@viagem_bp.route('/')
@login_required
@cliente_required
@menu_required('viagem')
def listar():
    q = request.args.get('q', '')
    query = Viagem.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(Viagem.destino.ilike(f'%{q}%'))
    registros = query.order_by(Viagem.criado_em.desc()).all()
    return render_template('viagem/listar.html', registros=registros, q=q)


@viagem_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('viagem')
def novo():
    form = ViagemForm()
    _preencher_choices(form, session['cliente_id'])
    if form.validate_on_submit():
        obj = Viagem(
            cliente_id=session['cliente_id'],
            veiculo_id=form.veiculo_id.data,
            motorista_id=form.motorista_id.data,
            tipo_viagem_id=form.tipo_viagem_id.data or None,
            local_origem=form.local_origem.data,
            destino=form.destino.data,
            descricao=form.descricao.data,
            km_inicial=form.km_inicial.data,
            status=StatusViagem[form.status.data],
            data_inicial=form.data_inicial.data,
        )
        db.session.add(obj)
        db.session.commit()
        flash('Viagem criada. Adicione os pacientes abaixo.', 'success')
        return redirect(url_for('viagem.pacientes', id=obj.id))
    return render_template('viagem/form.html', form=form, titulo='Nova Viagem')


@viagem_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('viagem')
def editar(id):
    obj = Viagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    form = ViagemForm()
    _preencher_choices(form, session['cliente_id'])
    if form.validate_on_submit():
        novo_status = StatusViagem[form.status.data]
        if novo_status == StatusViagem.FINALIZADA:
            if not form.km_final.data:
                flash('KM final obrigatório para finalizar a viagem.', 'danger')
                return render_template('viagem/form.html', form=form, titulo='Editar Viagem', obj=obj)
            if form.km_final.data < form.km_inicial.data:
                flash('KM final não pode ser menor que KM inicial.', 'danger')
                return render_template('viagem/form.html', form=form, titulo='Editar Viagem', obj=obj)
            obj.data_final = form.data_final.data or datetime.utcnow()
        obj.veiculo_id = form.veiculo_id.data
        obj.motorista_id = form.motorista_id.data
        obj.tipo_viagem_id = form.tipo_viagem_id.data or None
        obj.local_origem = form.local_origem.data
        obj.destino = form.destino.data
        obj.descricao = form.descricao.data
        obj.km_inicial = form.km_inicial.data
        obj.km_final = form.km_final.data
        obj.status = novo_status
        obj.data_inicial = form.data_inicial.data
        db.session.commit()
        flash('Viagem atualizada.', 'success')
        return redirect(url_for('viagem.listar'))
    form.veiculo_id.data = obj.veiculo_id
    form.motorista_id.data = obj.motorista_id
    form.tipo_viagem_id.data = obj.tipo_viagem_id or 0
    form.local_origem.data = obj.local_origem
    form.destino.data = obj.destino
    form.descricao.data = obj.descricao
    form.km_inicial.data = obj.km_inicial
    form.km_final.data = obj.km_final
    form.status.data = obj.status.name
    form.data_inicial.data = obj.data_inicial
    form.data_final.data = obj.data_final
    return render_template('viagem/form.html', form=form, titulo='Editar Viagem', obj=obj)


@viagem_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('viagem')
def visualizar(id):
    obj = Viagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    return render_template('viagem/visualizar.html', obj=obj)


@viagem_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('viagem')
def excluir(id):
    obj = Viagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    db.session.delete(obj)
    db.session.commit()
    flash('Viagem excluída.', 'warning')
    return redirect(url_for('viagem.listar'))


@viagem_bp.route('/<int:id>/pacientes', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('viagem')
def pacientes(id):
    obj = Viagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    if request.method == 'POST':
        cpf = request.form.get('cpf', '').strip()
        # sanitizar CPF: manter somente dígitos
        cpf_digits = re.sub(r"\D", "", cpf)
        nome = request.form.get('nome', '').strip()
        nome_mae = request.form.get('nome_mae', '').strip()
        data_nasc_str = request.form.get('data_nascimento', '').strip()
        erros = []
        if not nome:
            erros.append('Nome é obrigatório.')
        if not data_nasc_str:
            erros.append('Data de nascimento é obrigatória.')
        # validações de tamanho para evitar erros de truncamento no banco
        if not cpf_digits:
            erros.append('CPF deve conter apenas números.')
        elif len(cpf_digits) != 11:
            erros.append('CPF deve conter exatamente 11 dígitos.')
        if nome and len(nome) > 160:
            erros.append('Nome não pode ter mais que 160 caracteres.')
        if nome_mae and len(nome_mae) > 160:
            erros.append('Nome da mãe não pode ter mais que 160 caracteres.')
        dn = None
        if data_nasc_str:
            try:
                dn = datetime.strptime(data_nasc_str, '%d/%m/%Y').date()
            except ValueError:
                erros.append('Data de nascimento inválida. Use DD/MM/AAAA.')
        if erros:
            for e in erros:
                flash(e, 'danger')
        else:
            paciente = ViagemPaciente(
                cliente_id=session['cliente_id'],
                viagem_id=obj.id,
                cpf=cpf_digits,
                nome=nome,
                nome_mae=nome_mae,
                data_nascimento=dn,
            )
            db.session.add(paciente)
            db.session.commit()
            flash('Paciente adicionado.', 'success')
        # redirect to anchor so user sees the list immediately
        return redirect(url_for('viagem.pacientes', id=obj.id) + '#pacientes')

    # load pacientes ordered by criado_em desc so newest appear first
    pacientes = ViagemPaciente.query.filter_by(viagem_id=obj.id, cliente_id=session['cliente_id']).order_by(ViagemPaciente.criado_em.desc()).all()
    return render_template('viagem/pacientes.html', obj=obj, pacientes=pacientes)


@viagem_bp.route('/<int:id>/pacientes/<int:pac_id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('viagem')
def excluir_paciente(id, pac_id):
    pac = ViagemPaciente.query.filter_by(id=pac_id, viagem_id=id,
                                          cliente_id=session['cliente_id']).first_or_404()
    db.session.delete(pac)
    db.session.commit()
    flash('Paciente removido.', 'warning')
    return redirect(url_for('viagem.pacientes', id=id))


@viagem_bp.route('/<int:id>/imprimir')
@login_required
@cliente_required
def imprimir(id):
    obj = Viagem.query.filter_by(id=id, cliente_id=session['cliente_id']).first_or_404()
    pacientes = (ViagemPaciente.query
                 .filter_by(viagem_id=obj.id, cliente_id=session['cliente_id'])
                 .order_by(ViagemPaciente.nome)
                 .all())
    return render_template('viagem/imprimir.html', obj=obj, pacientes=pacientes,
                           agora=datetime.now())
