from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.mixins import TimestampMixin


class Usuario(UserMixin, TimestampMixin, db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True, index=True)
    nome = db.Column(db.String(160), nullable=False)
    email = db.Column(db.String(160))
    telefone = db.Column(db.String(30))
    senha_hash = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    clientes = db.relationship('UsuarioCliente', back_populates='usuario', cascade='all, delete-orphan')
    perfis = db.relationship('UsuarioPerfil', back_populates='usuario', cascade='all, delete-orphan')

    @property
    def is_active(self):
        return self.ativo

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def tem_acesso_cliente(self, cliente_id):
        if self.is_admin:
            return True
        return any(uc.cliente_id == int(cliente_id) for uc in self.clientes)

    def tem_permissao_menu(self, codigo):
        if self.is_admin:
            return True
        for up in self.perfis:
            perfil = up.perfil
            if perfil and perfil.ativo:
                for pm in perfil.menus:
                    if pm.menu and pm.menu.codigo == codigo and pm.menu.ativo:
                        return True
        return False


class UsuarioCliente(db.Model):
    __tablename__ = 'usuario_cliente'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), primary_key=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    usuario = db.relationship('Usuario', back_populates='clientes')
    cliente = db.relationship('Cliente', back_populates='usuarios')


class UsuarioPerfil(db.Model):
    __tablename__ = 'usuario_perfil'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.id'), primary_key=True)

    usuario = db.relationship('Usuario', back_populates='perfis')
    perfil = db.relationship('Perfil', back_populates='usuarios')


class PerfilMenu(db.Model):
    __tablename__ = 'perfil_menu'

    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.id'), primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), primary_key=True)

    perfil = db.relationship('Perfil', back_populates='menus')
    menu = db.relationship('Menu', back_populates='perfis')
