from datetime import datetime
from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Abastecimento(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'abastecimento'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    km = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade = db.Column(db.Numeric(10, 3), nullable=False)
    tipo_combustivel = db.Column(db.String(40))
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'))

    cliente = db.relationship('Cliente')
    veiculo = db.relationship('Veiculo', back_populates='abastecimentos')
    motorista = db.relationship('Motorista', back_populates='abastecimentos')
    anexos = db.relationship('AbastecimentoAnexo', back_populates='abastecimento', cascade='all, delete-orphan')


class AbastecimentoAnexo(db.Model):
    __tablename__ = 'abastecimento_anexo'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False, index=True)
    abastecimento_id = db.Column(db.Integer, db.ForeignKey('abastecimento.id'), nullable=False)
    tipo_arquivo_id = db.Column(db.Integer, db.ForeignKey('tipo_arquivo.id'))
    nome_arquivo = db.Column(db.String(255), nullable=False)
    caminho_arquivo = db.Column(db.String(500), nullable=False)
    tamanho_arquivo = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    cliente = db.relationship('Cliente')
    abastecimento = db.relationship('Abastecimento', back_populates='anexos')
    tipo_arquivo = db.relationship('TipoArquivo')
