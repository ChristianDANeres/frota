from datetime import datetime
from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Diario(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'diario'

    id           = db.Column(db.Integer, primary_key=True)
    codigo       = db.Column(db.String(30), nullable=False)
    veiculo_id   = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    motorista_id = db.Column(db.Integer, db.ForeignKey('motorista.id'), nullable=True)
    data         = db.Column(db.Date, nullable=False)
    km           = db.Column(db.Numeric(10, 2), nullable=False)
    texto        = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint('cliente_id', 'codigo', name='uq_diario_cliente_codigo'),
    )

    cliente   = db.relationship('Cliente')
    veiculo   = db.relationship('Veiculo', backref=db.backref('diarios', lazy='dynamic'))
    motorista = db.relationship('Motorista', backref=db.backref('diarios', lazy='dynamic'))
    anexos    = db.relationship('DiarioAnexo', back_populates='diario',
                                cascade='all, delete-orphan')


class DiarioAnexo(db.Model):
    __tablename__ = 'diario_anexo'

    id             = db.Column(db.Integer, primary_key=True)
    cliente_id     = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False, index=True)
    diario_id      = db.Column(db.Integer, db.ForeignKey('diario.id'), nullable=False)
    tipo_arquivo_id = db.Column(db.Integer, db.ForeignKey('tipo_arquivo.id'))
    nome_arquivo   = db.Column(db.String(255), nullable=False)
    caminho_arquivo = db.Column(db.String(500), nullable=False)
    tamanho_arquivo = db.Column(db.Integer)
    criado_em      = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    cliente      = db.relationship('Cliente')
    diario       = db.relationship('Diario', back_populates='anexos')
    tipo_arquivo = db.relationship('TipoArquivo')
