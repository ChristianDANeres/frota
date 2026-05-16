import enum
from datetime import datetime
from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class StatusViagem(enum.Enum):
    EM_ABERTO = 'EM_ABERTO'
    INICIADA = 'INICIADA'
    FINALIZADA = 'FINALIZADA'


class Viagem(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'viagem'

    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=False)
    km_inicial = db.Column(db.Numeric(10, 2), nullable=False)
    km_final = db.Column(db.Numeric(10, 2))
    destino = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.Enum(StatusViagem), nullable=False, default=StatusViagem.EM_ABERTO)
    data_inicial = db.Column(db.DateTime)
    data_final = db.Column(db.DateTime)
    tipo_viagem_id = db.Column(db.Integer, db.ForeignKey('tipo_viagem.id'))

    cliente = db.relationship('Cliente')
    veiculo = db.relationship('Veiculo', back_populates='viagens')
    motorista = db.relationship('Motorista', back_populates='viagens')
    tipo_viagem = db.relationship('TipoViagem', back_populates='viagens')
    pacientes = db.relationship('ViagemPaciente', back_populates='viagem', cascade='all, delete-orphan')


class ViagemPaciente(db.Model):
    __tablename__ = 'viagem_paciente'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False, index=True)
    viagem_id = db.Column(db.Integer, db.ForeignKey('viagem.id'), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    nome = db.Column(db.String(160), nullable=False)
    nome_mae = db.Column(db.String(160), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    cliente = db.relationship('Cliente')
    viagem = db.relationship('Viagem', back_populates='pacientes')
