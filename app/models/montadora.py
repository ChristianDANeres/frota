from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Montadora(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'montadora'
    __table_args__ = (db.UniqueConstraint('cliente_id', 'nome', name='uq_montadora_cliente_nome'),)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    cliente = db.relationship('Cliente')
    veiculos = db.relationship('Veiculo', back_populates='montadora')
