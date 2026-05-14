from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Menu(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'menu'
    __table_args__ = (db.UniqueConstraint('cliente_id', 'codigo', name='uq_menu_cliente_codigo'),)

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(60), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    icone = db.Column(db.String(60))
    endpoint = db.Column(db.String(120))
    ordem = db.Column(db.Integer, default=0, nullable=False)
    menu_pai_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    cliente = db.relationship('Cliente')
    perfis = db.relationship('PerfilMenu', back_populates='menu', cascade='all, delete-orphan')
    submenus = db.relationship('Menu', backref=db.backref('menu_pai', remote_side=[id]))
