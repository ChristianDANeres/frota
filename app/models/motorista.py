from datetime import datetime
from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Motorista(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'motorista'
    __table_args__ = (
        db.UniqueConstraint('cliente_id', 'cpf', name='uq_motorista_cliente_cpf'),
        db.UniqueConstraint('cliente_id', 'cnh', name='uq_motorista_cliente_cnh'),
    )

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), nullable=False)
    nome = db.Column(db.String(160), nullable=False)
    data_nascimento = db.Column(db.Date)
    cnh = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    cliente = db.relationship('Cliente')
    anexos = db.relationship('MotoristaAnexo', back_populates='motorista', cascade='all, delete-orphan')
    viagens = db.relationship('Viagem', back_populates='motorista')
    abastecimentos = db.relationship('Abastecimento', back_populates='motorista')


class MotoristaAnexo(db.Model):
    __tablename__ = 'motorista_anexo'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False, index=True)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=False)
    tipo_arquivo_id = db.Column(db.Integer, db.ForeignKey('tipo_arquivo.id'))
    nome_arquivo = db.Column(db.String(255), nullable=False)
    caminho_arquivo = db.Column(db.String(500), nullable=False)
    tamanho_arquivo = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    cliente = db.relationship('Cliente')
    motorista = db.relationship('Motorista', back_populates='anexos')
    tipo_arquivo = db.relationship('TipoArquivo')
