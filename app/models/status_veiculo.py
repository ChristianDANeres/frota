from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class StatusVeiculo(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'status_veiculo'
    __table_args__ = (db.UniqueConstraint('cliente_id', 'nome', name='uq_status_veiculo_cliente_nome'),)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    cliente = db.relationship('Cliente')
    veiculos = db.relationship('Veiculo', back_populates='status_veiculo')
