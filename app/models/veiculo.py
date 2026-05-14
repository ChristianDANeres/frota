from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Veiculo(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'veiculo'
    __table_args__ = (db.UniqueConstraint('cliente_id', 'placa', name='uq_veiculo_cliente_placa'),)

    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False)
    montadora_id = db.Column(db.Integer, db.ForeignKey('montadora.id'))
    modelo = db.Column(db.String(120))
    cor_id = db.Column(db.Integer, db.ForeignKey('cor.id'))
    ano_fabricacao = db.Column(db.Integer)
    tipo_combustivel = db.Column(db.String(40))
    status_veiculo_id = db.Column(db.Integer, db.ForeignKey('status_veiculo.id'))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    cliente = db.relationship('Cliente')
    montadora = db.relationship('Montadora', back_populates='veiculos')
    cor = db.relationship('Cor', back_populates='veiculos')
    status_veiculo = db.relationship('StatusVeiculo', back_populates='veiculos')
    viagens = db.relationship('Viagem', back_populates='veiculo')
    abastecimentos = db.relationship('Abastecimento', back_populates='veiculo')
