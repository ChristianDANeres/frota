import enum
from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class StatusIntercorrencia(enum.Enum):
    EM_ABERTO  = 'EM_ABERTO'
    EM_ANALISE = 'EM_ANALISE'
    FINALIZADO = 'FINALIZADO'


class DestinoUsuario(enum.Enum):
    DOMICILIO = 'DOMICILIO'
    UPA       = 'UPA'
    HOSPITAL  = 'HOSPITAL'


class Intercorrencia(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'intercorrencia'

    id                        = db.Column(db.Integer, primary_key=True)
    viagem_id                 = db.Column(db.Integer, db.ForeignKey('viagem.id'), nullable=False)
    viagem_paciente_id        = db.Column(db.Integer, db.ForeignKey('viagem_paciente.id'), nullable=True)

    # Cabeçalho do formulário
    local_origem              = db.Column(db.String(255), nullable=False)
    local_destino             = db.Column(db.String(255))
    data_transporte           = db.Column(db.Date, nullable=False)
    horario_ocorrencia        = db.Column(db.Time, nullable=False)

    # Dados do paciente
    paciente_nome             = db.Column(db.String(160), nullable=False)
    paciente_idade            = db.Column(db.Integer)
    paciente_telefone         = db.Column(db.String(20))
    paciente_acompanhante     = db.Column(db.String(160))

    # Condição física (checkboxes)
    cond_deambula             = db.Column(db.Boolean, default=False, nullable=False)
    cond_nao_deambula         = db.Column(db.Boolean, default=False, nullable=False)
    cond_acamado              = db.Column(db.Boolean, default=False, nullable=False)
    cond_cadeirante           = db.Column(db.Boolean, default=False, nullable=False)
    cond_dispositivo_mobil    = db.Column(db.Boolean, default=False, nullable=False)
    cond_traqueostomizado     = db.Column(db.Boolean, default=False, nullable=False)
    cond_oxigenio_continuo    = db.Column(db.Boolean, default=False, nullable=False)
    cond_portador_ostomias    = db.Column(db.Boolean, default=False, nullable=False)
    cond_drenos_dispositivos  = db.Column(db.Boolean, default=False, nullable=False)
    cond_acesso_venoso_periferico = db.Column(db.Boolean, default=False, nullable=False)
    cond_acesso_venoso_central    = db.Column(db.Boolean, default=False, nullable=False)

    # Dados da ocorrência
    descricao_ocorrencia      = db.Column(db.Text)
    endereco_ocorrencia       = db.Column(db.String(500))
    socorristas               = db.Column(db.String(500))
    destino_usuario           = db.Column(db.Enum(DestinoUsuario))
    data_atendimento          = db.Column(db.Date)
    local_atendimento         = db.Column(db.String(255))
    observacoes               = db.Column(db.Text)

    # Controle
    status = db.Column(db.Enum(StatusIntercorrencia), nullable=False,
                       default=StatusIntercorrencia.EM_ABERTO)

    # Relacionamentos
    viagem          = db.relationship('Viagem',
                                      backref=db.backref('intercorrencias', lazy='dynamic'))
    viagem_paciente = db.relationship('ViagemPaciente',
                                      backref=db.backref('intercorrencias', lazy='dynamic'))
