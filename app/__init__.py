import os
from flask import Flask, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from config import Config
from app.extensions import db, migrate, login_manager, csrf
from app.models import (
    Usuario, Cliente, Menu, Perfil, PerfilMenu, UsuarioPerfil, UsuarioCliente
)
from app.common.decorators import cliente_required
from sqlalchemy import func
from app.models import Veiculo, Viagem, StatusVeiculo


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para continuar.'

    from app.auth.routes import auth_bp
    from app.cliente.routes import cliente_bp
    from app.routes.montadora_routes import montadora_bp
    from app.routes.cor_routes import cor_bp
    from app.routes.tipo_arquivo_routes import tipo_arquivo_bp
    from app.routes.tipo_viagem_routes import tipo_viagem_bp
    from app.routes.status_veiculo_routes import status_veiculo_bp
    from app.routes.veiculo_routes import veiculo_bp
    from app.routes.motorista_routes import motorista_bp
    from app.routes.viagem_routes import viagem_bp
    from app.routes.abastecimento_routes import abastecimento_bp
    from app.routes.adm_routes import adm_bp
    from app.routes.oficina_routes import oficina_bp
    from app.routes.veiculo_oficina_routes import veiculo_oficina_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(montadora_bp)
    app.register_blueprint(cor_bp)
    app.register_blueprint(tipo_arquivo_bp)
    app.register_blueprint(tipo_viagem_bp)
    app.register_blueprint(status_veiculo_bp)
    app.register_blueprint(veiculo_bp)
    app.register_blueprint(motorista_bp)
    app.register_blueprint(viagem_bp)
    app.register_blueprint(abastecimento_bp)
    app.register_blueprint(adm_bp)
    app.register_blueprint(oficina_bp)
    app.register_blueprint(veiculo_oficina_bp)

    @app.route('/')
    @login_required
    def dashboard():
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return redirect(url_for('cliente.selecionar'))
        menus = Menu.query.filter_by(cliente_id=cliente_id, ativo=True).order_by(Menu.ordem, Menu.nome).all()
        menus = [m for m in menus if current_user.tem_permissao_menu(m.codigo)]
        return render_template('dashboard.html', menus=menus)

    @app.route('/dashbird')
    @login_required
    @cliente_required
    def dashbird():
        cliente_id = session.get('cliente_id')
        # cartões resumidos
        total_veiculos = Veiculo.query.filter_by(cliente_id=cliente_id, ativo=True).count()
        # veículos por status
        veiculos_status = db.session.query(StatusVeiculo.nome, func.count(Veiculo.id))
        veiculos_status = veiculos_status.join(Veiculo, StatusVeiculo.id == Veiculo.status_veiculo_id)
        veiculos_status = veiculos_status.filter(Veiculo.cliente_id == cliente_id)
        veiculos_status = veiculos_status.group_by(StatusVeiculo.nome).all()

        # viagens por status
        viagens_status = db.session.query(Viagem.status, func.count(Viagem.id)).filter(Viagem.cliente_id == cliente_id)
        viagens_status = viagens_status.group_by(Viagem.status).all()

        # listagem de veículos (simplificada)
        veiculos = Veiculo.query.filter_by(cliente_id=cliente_id).order_by(Veiculo.placa).limit(50).all()

        # últimas viagens
        ultimas_viagens = Viagem.query.filter_by(cliente_id=cliente_id).order_by(Viagem.criado_em.desc()).limit(10).all()

        return render_template('dashbird.html', total_veiculos=total_veiculos,
                               veiculos_status=veiculos_status, viagens_status=viagens_status,
                               veiculos=veiculos, ultimas_viagens=ultimas_viagens)

    @app.context_processor
    def inject_context():
        cliente = None
        menus_nav = []
        if session.get('cliente_id'):
            cliente = Cliente.query.get(session['cliente_id'])
            if current_user.is_authenticated:
                todos = Menu.query.filter_by(cliente_id=session['cliente_id'], ativo=True).order_by(Menu.ordem, Menu.nome).all()
                menus_nav = [m for m in todos if current_user.tem_permissao_menu(m.codigo)]
        return {'cliente_atual': cliente, 'menus_nav': menus_nav}

    with app.app_context():
        db.create_all()
        seed_basico()

    # filtros de template
    from app.utils import format_cpf
    app.add_template_filter(format_cpf, name='format_cpf')

    return app


def seed_basico():
    admin_user = os.getenv('ADMIN_USER', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@frota.local')

    cliente = Cliente.query.filter_by(nome='Cliente Padrão').first()
    if not cliente:
        cliente = Cliente(nome='Cliente Padrão')
        db.session.add(cliente)
        db.session.flush()

    admin = Usuario.query.filter_by(username=admin_user).first()
    if not admin:
        admin = Usuario(username=admin_user, nome='Administrador', email=admin_email, ativo=True, is_admin=True)
        admin.set_senha(admin_password)
        db.session.add(admin)
        db.session.flush()

    if not UsuarioCliente.query.filter_by(usuario_id=admin.id, cliente_id=cliente.id).first():
        db.session.add(UsuarioCliente(usuario_id=admin.id, cliente_id=cliente.id))

    menus_base = [
        ('dashboard',      'Dashboard',       'dashboard',               'bi-speedometer2',  1),
        ('veiculo',        'Veículos',        'veiculo.listar',          'bi-car-front',     10),
        ('motorista',      'Motoristas',      'motorista.listar',        'bi-person-badge',  11),
        ('viagem',         'Viagens',         'viagem.listar',           'bi-map',           12),
        ('abastecimento',  'Abastecimentos',  'abastecimento.listar',    'bi-fuel-pump',     13),
        ('montadora',      'Montadoras',      'montadora.listar',        'bi-building-gear', 20),
        ('cor',            'Cores',           'cor.listar',              'bi-palette',       21),
        ('tipo_arquivo',   'Tipos de Arquivo','tipo_arquivo.listar',     'bi-file-earmark',  22),
        ('tipo_viagem',    'Tipos de Viagem', 'tipo_viagem.listar',      'bi-signpost-2',    23),
        ('status_veiculo', 'Status Veículo',  'status_veiculo.listar',   'bi-check-circle',  24),
        ('oficina',         'Oficinas',        'oficina.listar',          'bi-wrench',        25),
        ('veiculo_oficina', 'Veículos Oficina', 'veiculo_oficina.listar',  'bi-tools',         26),
    ]
    menus_criados = []
    for codigo, nome, endpoint, icone, ordem in menus_base:
        menu = Menu.query.filter_by(cliente_id=cliente.id, codigo=codigo).first()
        if not menu:
            menu = Menu(cliente_id=cliente.id, codigo=codigo, nome=nome,
                        endpoint=endpoint, icone=icone, ordem=ordem)
            db.session.add(menu)
            db.session.flush()
        menus_criados.append(menu)

    perfil = Perfil.query.filter_by(cliente_id=cliente.id, nome='Administrador').first()
    if not perfil:
        perfil = Perfil(cliente_id=cliente.id, nome='Administrador', descricao='Acesso total ao sistema')
        db.session.add(perfil)
        db.session.flush()

    for menu in menus_criados:
        if not PerfilMenu.query.filter_by(perfil_id=perfil.id, menu_id=menu.id).first():
            db.session.add(PerfilMenu(perfil_id=perfil.id, menu_id=menu.id))

    if not UsuarioPerfil.query.filter_by(usuario_id=admin.id, perfil_id=perfil.id).first():
        db.session.add(UsuarioPerfil(usuario_id=admin.id, perfil_id=perfil.id))

    db.session.commit()

