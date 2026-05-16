from datetime import datetime
from app.extensions import db
from app.models.mixins import TimestampMixin, TenantMixin


class Oficina(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'oficina'

    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(20))
    nome = db.Column(db.String(200), nullable=False)
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(50))
    municipio = db.Column(db.String(120))
    estado = db.Column(db.String(2))
    email = db.Column(db.String(200))
    telefone = db.Column(db.String(50))
    responsavel = db.Column(db.String(160))

    cliente = db.relationship('Cliente')
    veiculos = db.relationship('VeiculoOficina', back_populates='oficina', cascade='all, delete-orphan')


class VeiculoOficina(TenantMixin, TimestampMixin, db.Model):
    __tablename__ = 'veiculo_oficina'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False, index=True)
    oficina_id = db.Column(db.Integer, db.ForeignKey('oficina.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_saida = db.Column(db.DateTime)
    km_entrada = db.Column(db.Numeric(10, 2))
    km_saida = db.Column(db.Numeric(10, 2))
    motorista_entrada_id = db.Column(db.Integer, db.ForeignKey('motorista.id'))
    motivo = db.Column(db.String(4000))

    cliente = db.relationship('Cliente')
    oficina = db.relationship('Oficina', back_populates='veiculos')
    veiculo = db.relationship('Veiculo')
    motorista = db.relationship('Motorista')
    anexos = db.relationship('VeiculoOficinaAnexo', back_populates='veiculo_oficina', cascade='all, delete-orphan')


class VeiculoOficinaAnexo(db.Model):
    __tablename__ = 'veiculo_oficina_anexo'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False, index=True)
    veiculo_oficina_id = db.Column(db.Integer, db.ForeignKey('veiculo_oficina.id'), nullable=False)
    tipo_arquivo_id = db.Column(db.Integer, db.ForeignKey('tipo_arquivo.id'))
    nome_arquivo = db.Column(db.String(255), nullable=False)
    caminho_arquivo = db.Column(db.String(500), nullable=False)
    tamanho_arquivo = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    cliente = db.relationship('Cliente')
    veiculo_oficina = db.relationship('VeiculoOficina', back_populates='anexos')
    tipo_arquivo = db.relationship('TipoArquivo')
