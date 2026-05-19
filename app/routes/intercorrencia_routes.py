from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, session, jsonify)
from datetime import datetime
from flask_login import login_required
from app.extensions import db
from app.models import Intercorrencia, Viagem, ViagemPaciente
from app.models.intercorrencia import StatusIntercorrencia, DestinoUsuario
from app.models.viagem import StatusViagem
from app.forms.intercorrencia_form import IntercorrenciaForm
from app.common.decorators import cliente_required, menu_required

intercorrencia_bp = Blueprint('intercorrencia', __name__,
                               url_prefix='/intercorrencia')

# ── helpers ───────────────────────────────────────────────────────────────────

def _preencher_choices(form, cliente_id):
    """Preenche selects de viagem e paciente."""
    viagens = (Viagem.query
               .filter_by(cliente_id=cliente_id, status=StatusViagem.INICIADA)
               .order_by(Viagem.data_inicial.desc())
               .all())
    form.viagem_id.choices = [(0, 'Selecione...')] + [
        (v.id, f'{v.data_inicial.strftime("%d/%m/%Y") if v.data_inicial else "s/d"} – {v.destino} [{v.motorista.nome if v.motorista else ""}]')
        for v in viagens
    ]
    # Pacientes: carregados via AJAX ou pré-populados na edição
    form.viagem_paciente_id.choices = [(0, 'Selecione...')]


def _preencher_pacientes(form, viagem_id):
    """Preenche choices de pacientes para uma viagem específica."""
    pacientes = (ViagemPaciente.query
                 .filter_by(viagem_id=viagem_id)
                 .order_by(ViagemPaciente.nome)
                 .all())
    form.viagem_paciente_id.choices = [(0, 'Selecione...')] + [
        (p.id, p.nome) for p in pacientes
    ]


def _form_para_obj(form, obj):
    """Transfere dados do form para o objeto de modelo."""
    obj.viagem_id          = form.viagem_id.data
    obj.viagem_paciente_id = form.viagem_paciente_id.data or None
    obj.local_origem       = form.local_origem.data
    obj.local_destino      = form.local_destino.data
    obj.data_transporte    = form.data_transporte.data
    obj.horario_ocorrencia = form.horario_ocorrencia.data
    obj.paciente_nome      = form.paciente_nome.data
    obj.paciente_idade     = form.paciente_idade.data
    obj.paciente_telefone  = form.paciente_telefone.data
    obj.paciente_acompanhante = form.paciente_acompanhante.data

    obj.cond_deambula                 = form.cond_deambula.data
    obj.cond_nao_deambula             = form.cond_nao_deambula.data
    obj.cond_acamado                  = form.cond_acamado.data
    obj.cond_cadeirante               = form.cond_cadeirante.data
    obj.cond_dispositivo_mobil        = form.cond_dispositivo_mobil.data
    obj.cond_traqueostomizado         = form.cond_traqueostomizado.data
    obj.cond_oxigenio_continuo        = form.cond_oxigenio_continuo.data
    obj.cond_portador_ostomias        = form.cond_portador_ostomias.data
    obj.cond_drenos_dispositivos      = form.cond_drenos_dispositivos.data
    obj.cond_acesso_venoso_periferico = form.cond_acesso_venoso_periferico.data
    obj.cond_acesso_venoso_central    = form.cond_acesso_venoso_central.data

    obj.descricao_ocorrencia = form.descricao_ocorrencia.data
    obj.endereco_ocorrencia  = form.endereco_ocorrencia.data
    obj.socorristas          = form.socorristas.data
    obj.destino_usuario      = DestinoUsuario[form.destino_usuario.data] if form.destino_usuario.data else None
    obj.data_atendimento     = form.data_atendimento.data
    obj.local_atendimento    = form.local_atendimento.data
    obj.observacoes          = form.observacoes.data
    obj.status               = StatusIntercorrencia[form.status.data]


def _obj_para_form(form, obj):
    """Preenche o form com dados do objeto de modelo."""
    form.viagem_id.data          = obj.viagem_id
    form.viagem_paciente_id.data = obj.viagem_paciente_id or 0
    form.local_origem.data       = obj.local_origem
    form.local_destino.data      = obj.local_destino
    form.data_transporte.data    = obj.data_transporte
    form.horario_ocorrencia.data = obj.horario_ocorrencia
    form.paciente_nome.data      = obj.paciente_nome
    form.paciente_idade.data     = obj.paciente_idade
    form.paciente_telefone.data  = obj.paciente_telefone
    form.paciente_acompanhante.data = obj.paciente_acompanhante

    form.cond_deambula.data                 = obj.cond_deambula
    form.cond_nao_deambula.data             = obj.cond_nao_deambula
    form.cond_acamado.data                  = obj.cond_acamado
    form.cond_cadeirante.data               = obj.cond_cadeirante
    form.cond_dispositivo_mobil.data        = obj.cond_dispositivo_mobil
    form.cond_traqueostomizado.data         = obj.cond_traqueostomizado
    form.cond_oxigenio_continuo.data        = obj.cond_oxigenio_continuo
    form.cond_portador_ostomias.data        = obj.cond_portador_ostomias
    form.cond_drenos_dispositivos.data      = obj.cond_drenos_dispositivos
    form.cond_acesso_venoso_periferico.data = obj.cond_acesso_venoso_periferico
    form.cond_acesso_venoso_central.data    = obj.cond_acesso_venoso_central

    form.descricao_ocorrencia.data = obj.descricao_ocorrencia
    form.endereco_ocorrencia.data  = obj.endereco_ocorrencia
    form.socorristas.data          = obj.socorristas
    form.destino_usuario.data      = obj.destino_usuario.name if obj.destino_usuario else ''
    form.data_atendimento.data     = obj.data_atendimento
    form.local_atendimento.data    = obj.local_atendimento
    form.observacoes.data          = obj.observacoes
    form.status.data               = obj.status.name


# ── API auxiliar ──────────────────────────────────────────────────────────────

@intercorrencia_bp.route('/api/viagem/<int:viagem_id>/pacientes')
@login_required
@cliente_required
def api_pacientes(viagem_id):
    """Retorna JSON com pacientes de uma viagem (para AJAX no form)."""
    viagem = Viagem.query.filter_by(id=viagem_id,
                                    cliente_id=session['cliente_id']).first_or_404()
    pacientes = (ViagemPaciente.query
                 .filter_by(viagem_id=viagem.id)
                 .order_by(ViagemPaciente.nome)
                 .all())
    return jsonify([{'id': p.id, 'nome': p.nome} for p in pacientes])


# ── CRUD ──────────────────────────────────────────────────────────────────────

@intercorrencia_bp.route('/')
@login_required
@cliente_required
@menu_required('intercorrencia')
def listar():
    q      = request.args.get('q', '')
    status = request.args.get('status', '')
    query  = Intercorrencia.query.filter_by(cliente_id=session['cliente_id'])
    if q:
        query = query.filter(Intercorrencia.paciente_nome.ilike(f'%{q}%'))
    if status:
        try:
            query = query.filter_by(status=StatusIntercorrencia[status])
        except KeyError:
            pass
    registros = query.order_by(Intercorrencia.criado_em.desc()).all()
    return render_template('intercorrencia/listar.html',
                           registros=registros, q=q, status_filtro=status,
                           StatusIntercorrencia=StatusIntercorrencia)


@intercorrencia_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('intercorrencia')
def novo():
    form = IntercorrenciaForm()
    _preencher_choices(form, session['cliente_id'])

    # Pré-selecionar viagem via query string (link direto da viagem)
    viagem_pre = request.args.get('viagem_id', 0, type=int)

    if form.validate_on_submit():
        # Garante que a viagem pertence ao cliente e está INICIADA
        viagem = Viagem.query.filter_by(id=form.viagem_id.data,
                                        cliente_id=session['cliente_id']).first()
        if not viagem:
            flash('Viagem inválida.', 'danger')
            return render_template('intercorrencia/form.html', form=form,
                                   titulo='Nova Intercorrência', viagem_pre=viagem_pre)
        if viagem.status != StatusViagem.INICIADA:
            flash('Só é possível registrar intercorrências em viagens com status "Iniciada".', 'danger')
            return render_template('intercorrencia/form.html', form=form,
                                   titulo='Nova Intercorrência', viagem_pre=viagem_pre)

        obj = Intercorrencia(cliente_id=session['cliente_id'])
        _form_para_obj(form, obj)
        db.session.add(obj)
        db.session.commit()
        flash('Intercorrência registrada com sucesso.', 'success')
        return redirect(url_for('intercorrencia.listar'))

    return render_template('intercorrencia/form.html', form=form,
                           titulo='Nova Intercorrência', viagem_pre=viagem_pre)


@intercorrencia_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@cliente_required
@menu_required('intercorrencia')
def editar(id):
    obj = Intercorrencia.query.filter_by(id=id,
                                         cliente_id=session['cliente_id']).first_or_404()
    if obj.status == StatusIntercorrencia.FINALIZADO:
        flash('Intercorrências finalizadas não podem ser alteradas.', 'warning')
        return redirect(url_for('intercorrencia.visualizar', id=id))

    form = IntercorrenciaForm()
    _preencher_choices(form, session['cliente_id'])

    if form.validate_on_submit():
        viagem = Viagem.query.filter_by(id=form.viagem_id.data,
                                        cliente_id=session['cliente_id']).first()
        if not viagem:
            flash('Viagem inválida.', 'danger')
            _preencher_pacientes(form, obj.viagem_id)
            return render_template('intercorrencia/form.html', form=form,
                                   titulo='Editar Intercorrência', obj=obj)
        if viagem.status != StatusViagem.INICIADA:
            flash('Só é possível vincular intercorrências a viagens com status "Iniciada".', 'danger')
            _preencher_pacientes(form, obj.viagem_id)
            return render_template('intercorrencia/form.html', form=form,
                                   titulo='Editar Intercorrência', obj=obj)

        _form_para_obj(form, obj)
        db.session.commit()
        flash('Intercorrência atualizada.', 'success')
        return redirect(url_for('intercorrencia.listar'))

    # GET — preencher form
    _obj_para_form(form, obj)
    _preencher_pacientes(form, obj.viagem_id)
    return render_template('intercorrencia/form.html', form=form,
                           titulo='Editar Intercorrência', obj=obj)


@intercorrencia_bp.route('/<int:id>/visualizar')
@login_required
@cliente_required
@menu_required('intercorrencia')
def visualizar(id):
    obj = Intercorrencia.query.filter_by(id=id,
                                          cliente_id=session['cliente_id']).first_or_404()
    return render_template('intercorrencia/visualizar.html', obj=obj,
                           StatusIntercorrencia=StatusIntercorrencia)


@intercorrencia_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
@cliente_required
@menu_required('intercorrencia')
def excluir(id):
    obj = Intercorrencia.query.filter_by(id=id,
                                          cliente_id=session['cliente_id']).first_or_404()
    if obj.status == StatusIntercorrencia.FINALIZADO:
        flash('Intercorrências finalizadas não podem ser excluídas.', 'warning')
        return redirect(url_for('intercorrencia.listar'))
    db.session.delete(obj)
    db.session.commit()
    flash('Intercorrência excluída.', 'success')
    return redirect(url_for('intercorrencia.listar'))


@intercorrencia_bp.route('/<int:id>/imprimir')
@login_required
@cliente_required
def imprimir(id):
    obj = Intercorrencia.query.filter_by(id=id,
                                          cliente_id=session['cliente_id']).first_or_404()
    return render_template('intercorrencia/imprimir.html', obj=obj,
                           StatusIntercorrencia=StatusIntercorrencia,
                           agora=datetime.now())
