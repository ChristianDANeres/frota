from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Perfil(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'perfil'
    __table_args__ = (db.UniqueConstraint('cliente_id', 'nome', name='uq_perfil_cliente_nome'),)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    cliente = db.relationship('Cliente')
    usuarios = db.relationship('UsuarioPerfil', back_populates='perfil', cascade='all, delete-orphan')
    menus = db.relationship('PerfilMenu', back_populates='perfil', cascade='all, delete-orphan')
