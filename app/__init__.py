import os
from datetime import date, timedelta
from flask import Flask, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from config import Config
from app.extensions import db, migrate, login_manager, csrf
from app.models import (
    Usuario, Cliente, Menu, Perfil, PerfilMenu, UsuarioPerfil, UsuarioCliente
)
from app.common.decorators import cliente_required
from sqlalchemy import func
from app.models import Veiculo, Viagem, StatusVeiculo, VeiculoOficina, Abastecimento, TipoViagem


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


def _aplicar_patches_banco():
    """Aplica alterações de esquema de forma idempotente a cada startup.

    Usa blocos DO $$ ... $$ do PostgreSQL para verificar antes de criar,
    garantindo que rodar múltiplas vezes não cause erros.
    """
    from sqlalchemy import text
    patches = [
        # 0005 — coluna cpf em usuario
        "ALTER TABLE usuario ADD COLUMN IF NOT EXISTS cpf VARCHAR(20)",
        # 0007 — coluna tipo_combustivel em abastecimento
        "ALTER TABLE abastecimento ADD COLUMN IF NOT EXISTS tipo_combustivel VARCHAR(40)",
        # 0005 — constraint unique de cpf em usuario
        """DO $$ BEGIN
             IF NOT EXISTS (
               SELECT 1 FROM pg_constraint WHERE conname = 'uq_usuario_cpf'
             ) THEN
               ALTER TABLE usuario ADD CONSTRAINT uq_usuario_cpf UNIQUE (cpf);
             END IF;
           END $$""",
        # 0006 — constraint unique de cnh em motorista
        """DO $$ BEGIN
             IF NOT EXISTS (
               SELECT 1 FROM pg_constraint WHERE conname = 'uq_motorista_cliente_cnh'
             ) THEN
               ALTER TABLE motorista ADD CONSTRAINT uq_motorista_cliente_cnh UNIQUE (cliente_id, cnh);
             END IF;
           END $$""",
    ]
    with db.engine.connect() as conn:
        for sql in patches:
            try:
                conn.execute(text(sql))
            except Exception:
                pass
        conn.commit()


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
        ('dashboard',      'Acesso Rápido',   'dashboard',               'bi-grid-3x3-gap',  1),
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
        # A página principal padrão deve ser as Análises (dashbird)
        return redirect(url_for('dashbird'))

    @app.route('/dashbird')
    @login_required
    @cliente_required
    def dashbird():
        from app.models.viagem import StatusViagem
        cliente_id = session.get('cliente_id')

        hoje        = date.today()
        inicio_sem  = hoje - timedelta(days=hoje.weekday())
        inicio_mes  = hoje.replace(day=1)

        # ── Frota ─────────────────────────────────────────────
        total_veiculos = Veiculo.query.filter_by(cliente_id=cliente_id, ativo=True).count()

        veiculos_status = (
            db.session.query(StatusVeiculo.nome, func.count(Veiculo.id))
            .join(Veiculo, StatusVeiculo.id == Veiculo.status_veiculo_id)
            .filter(Veiculo.cliente_id == cliente_id, Veiculo.ativo == True)
            .group_by(StatusVeiculo.nome)
            .all()
        )

        veiculos_em_oficina = (
            VeiculoOficina.query
            .filter_by(cliente_id=cliente_id)
            .filter(VeiculoOficina.data_saida == None)
            .order_by(VeiculoOficina.data_entrada.desc())
            .all()
        )
        total_em_oficina = len(veiculos_em_oficina)

        # ── Viagens ───────────────────────────────────────────
        viagens_em_andamento = (
            Viagem.query
            .filter_by(cliente_id=cliente_id)
            .filter(Viagem.status == StatusViagem.INICIADA)
            .order_by(Viagem.data_inicial.desc())
            .all()
        )

        viagens_status = (
            db.session.query(Viagem.status, func.count(Viagem.id))
            .filter(Viagem.cliente_id == cliente_id)
            .group_by(Viagem.status)
            .all()
        )

        viagens_semana = (
            Viagem.query
            .filter(
                Viagem.cliente_id == cliente_id,
                func.date(Viagem.criado_em) >= inicio_sem
            ).count()
        )
        viagens_mes = (
            Viagem.query
            .filter(
                Viagem.cliente_id == cliente_id,
                func.date(Viagem.criado_em) >= inicio_mes
            ).count()
        )

        km_semana = float(
            db.session.query(func.sum(Viagem.km_final - Viagem.km_inicial))
            .filter(
                Viagem.cliente_id == cliente_id,
                Viagem.status == StatusViagem.FINALIZADA,
                func.date(Viagem.criado_em) >= inicio_sem,
                Viagem.km_final != None
            ).scalar() or 0
        )
        km_mes = float(
            db.session.query(func.sum(Viagem.km_final - Viagem.km_inicial))
            .filter(
                Viagem.cliente_id == cliente_id,
                Viagem.status == StatusViagem.FINALIZADA,
                func.date(Viagem.criado_em) >= inicio_mes,
                Viagem.km_final != None
            ).scalar() or 0
        )

        viagens_por_tipo_mes = (
            db.session.query(TipoViagem.nome, func.count(Viagem.id))
            .join(Viagem, TipoViagem.id == Viagem.tipo_viagem_id)
            .filter(
                Viagem.cliente_id == cliente_id,
                func.date(Viagem.criado_em) >= inicio_mes
            )
            .group_by(TipoViagem.nome)
            .order_by(func.count(Viagem.id).desc())
            .all()
        )

        # ── Abastecimentos ────────────────────────────────────
        def _abast(desde):
            r = (
                db.session.query(
                    func.sum(Abastecimento.quantidade),
                    func.sum(Abastecimento.valor)
                )
                .filter(
                    Abastecimento.cliente_id == cliente_id,
                    Abastecimento.data >= desde
                ).first()
            )
            return float(r[0] or 0), float(r[1] or 0)

        abast_sem_litros, abast_sem_valor = _abast(inicio_sem)
        abast_mes_litros, abast_mes_valor = _abast(inicio_mes)

        # ── Últimas viagens ───────────────────────────────────
        ultimas_viagens = (
            Viagem.query
            .filter_by(cliente_id=cliente_id)
            .order_by(Viagem.criado_em.desc())
            .limit(10).all()
        )

        return render_template('dashbird.html',
            total_veiculos=total_veiculos,
            veiculos_status=veiculos_status,
            veiculos_em_oficina=veiculos_em_oficina,
            total_em_oficina=total_em_oficina,
            viagens_em_andamento=viagens_em_andamento,
            viagens_status=viagens_status,
            viagens_semana=viagens_semana,
            viagens_mes=viagens_mes,
            km_semana=km_semana,
            km_mes=km_mes,
            viagens_por_tipo_mes=viagens_por_tipo_mes,
            abast_sem_litros=abast_sem_litros,
            abast_sem_valor=abast_sem_valor,
            abast_mes_litros=abast_mes_litros,
            abast_mes_valor=abast_mes_valor,
            ultimas_viagens=ultimas_viagens,
            hoje=hoje,
            inicio_sem=inicio_sem,
            inicio_mes=inicio_mes,
        )

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
        _aplicar_patches_banco()

    # filtros de template
    from app.utils import format_cpf
    app.add_template_filter(format_cpf, name='format_cpf')
    from app.utils import format_money
    app.add_template_filter(format_money, name='format_money')

    return app


