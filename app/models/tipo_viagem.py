from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class TipoViagem(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'tipo_viagem'
    __table_args__ = (db.UniqueConstraint('cliente_id', 'nome', name='uq_tipo_viagem_cliente_nome'),)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    cliente = db.relationship('Cliente')
    viagens = db.relationship('Viagem', back_populates='tipo_viagem')
