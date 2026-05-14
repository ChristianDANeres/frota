from app.extensions import db
from app.models.mixins import TimestampMixin


class Cliente(TimestampMixin, db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False, unique=True)
    cnpj = db.Column(db.String(20))
    email = db.Column(db.String(160))
    telefone = db.Column(db.String(30))
    endereco = db.Column(db.String(255))
    municipio = db.Column(db.String(120))
    responsavel = db.Column(db.String(160))
    logo_esquerdo = db.Column(db.String(255))
    logo_direito = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    usuarios = db.relationship('UsuarioCliente', back_populates='cliente', cascade='all, delete-orphan')
