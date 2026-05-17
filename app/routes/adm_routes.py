from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_required
from app.extensions import db
from app.models import Cliente, Usuario, UsuarioCliente, Perfil, UsuarioPerfil, Menu, PerfilMenu
from app.forms.cliente_form import ClienteForm
from app.forms.usuario_form import UsuarioForm
from app.forms.perfil_form import PerfilForm
from app.forms.menu_form import MenuForm
from app.common.decorators import admin_required, cliente_required, menu_required

import os
from werkzeug.utils import secure_filename


def _save_cliente_file(file_storage, cliente_id, name_prefix):
    if not file_storage:
        return None
    filename = secure_filename(file_storage.filename)
    if not filename:
        return None
    # read bytes
    try:
        file_storage.stream.seek(0)
    except Exception:
        pass
    data = file_storage.read()
    if not data:
        return None
    max_bytes = 3 * 1024 * 1024  # 3 MB
    from io import BytesIO
    try:
        from PIL import Image
    except Exception:
        flash('Pillow não instalado. Instale "Pillow" para permitir redimensionamento de imagens.', 'danger')
        return None

    # try to open image
    try:
        img = Image.open(BytesIO(data))
    except Exception:
        flash('Arquivo de imagem inválido.', 'danger')
        return None

    # if image large, attempt resize/compress
    if len(data) > max_bytes:
        # convert RGBA to RGB for JPEG
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        else:
            img = img.convert('RGB')
        # reduce dimensions
        img.thumbnail((1200, 1200))
        out = BytesIO()
        img.save(out, format='JPEG', quality=85)
        data = out.getvalue()
        if len(data) > max_bytes:
            flash('Imagem ainda excede 3MB após redimensionamento. Use uma imagem menor.', 'danger')
            return None

    # save final bytes as JPG
    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'cliente', str(cliente_id))
    os.makedirs(uploads_dir, exist_ok=True)
    target_name = f"{name_prefix}.jpg"
    target_path = os.path.join(uploads_dir, target_name)
    try:
        with open(target_path, 'wb') as f:
            f.write(data)
    except Exception:
        flash('Falha ao salvar arquivo no servidor.', 'danger')
        return None

    return f"uploads/cliente/{cliente_id}/{target_name}"

adm_bp = Blueprint('adm', __name__, url_prefix='/adm')

# ── Clientes ──────────────────────────────────────────────────────────────────

@adm_bp.route('/clientes')
@login_required
@admin_required
def clientes():
    q = request.args.get('q', '')
    query = Cliente.query
    if q:
        query = query.filter(Cliente.nome.ilike(f'%{q}%'))
    registros = query.order_by(Cliente.nome).all()
    return render_template('cliente_adm/listar.html', registros=registros, q=q)


@adm_bp.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def cliente_novo():
    form = ClienteForm()
    if form.validate_on_submit():
        obj = Cliente(nome=form.nome.data, cnpj=form.cnpj.data,
                      email=form.email.data, telefone=form.telefone.data,
                      endereco=form.endereco.data, municipio=form.municipio.data,
                      responsavel=form.responsavel.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        # handle file uploads after we have obj.id
        if form.logo_esquerdo.data:
            caminho = _save_cliente_file(form.logo_esquerdo.data, obj.id, 'logo_esquerdo')
            if caminho:
                obj.logo_esquerdo = caminho
        if form.logo_direito.data:
            caminho = _save_cliente_file(form.logo_direito.data, obj.id, 'logo_direito')
            if caminho:
                obj.logo_direito = caminho
        db.session.commit()
        flash('Cliente criado.', 'success')
        return redirect(url_for('adm.clientes'))
    return render_template('cliente_adm/form.html', form=form, titulo='Novo Cliente')


@adm_bp.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def cliente_editar(id):
    obj = Cliente.query.get_or_404(id)
    form = ClienteForm()
    if form.validate_on_submit():
        obj.nome = form.nome.data
        obj.cnpj = form.cnpj.data
        obj.email = form.email.data
        obj.telefone = form.telefone.data
        obj.endereco = form.endereco.data
        obj.municipio = form.municipio.data
        obj.responsavel = form.responsavel.data
        obj.ativo = form.ativo.data
        # handle logo updates
        if form.logo_esquerdo.data:
            # remove existing file if present
            if obj.logo_esquerdo:
                try:
                    p = os.path.join(current_app.root_path, 'static', obj.logo_esquerdo)
                    if os.path.exists(p):
                        os.remove(p)
                except Exception:
                    pass
            caminho = _save_cliente_file(form.logo_esquerdo.data, obj.id, 'logo_esquerdo')
            if caminho:
                obj.logo_esquerdo = caminho
        if form.logo_direito.data:
            if obj.logo_direito:
                try:
                    p = os.path.join(current_app.root_path, 'static', obj.logo_direito)
                    if os.path.exists(p):
                        os.remove(p)
                except Exception:
                    pass
            caminho = _save_cliente_file(form.logo_direito.data, obj.id, 'logo_direito')
            if caminho:
                obj.logo_direito = caminho
        db.session.commit()
        flash('Cliente atualizado.', 'success')
        return redirect(url_for('adm.clientes'))
    form.nome.data = obj.nome
    form.cnpj.data = obj.cnpj
    form.email.data = obj.email
    form.telefone.data = obj.telefone
    form.endereco.data = obj.endereco
    form.municipio.data = obj.municipio
    form.responsavel.data = obj.responsavel
    form.ativo.data = obj.ativo
    return render_template('cliente_adm/form.html', form=form, titulo='Editar Cliente', obj=obj)


@adm_bp.route('/clientes/<int:id>/visualizar')
@login_required
@admin_required
def cliente_visualizar(id):
    obj = Cliente.query.get_or_404(id)
    return render_template('cliente_adm/visualizar.html', obj=obj)


@adm_bp.route('/clientes/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def cliente_excluir(id):
    obj = Cliente.query.get_or_404(id)
    obj.ativo = False
    db.session.commit()
    
@adm_bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    q = request.args.get('q', '')
    query = Usuario.query
    if q:
        query = query.filter(Usuario.nome.ilike(f'%{q}%') | Usuario.username.ilike(f'%{q}%'))
    registros = query.order_by(Usuario.nome).all()
    return render_template('usuario/listar.html', registros=registros, q=q)


@adm_bp.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def usuario_novo():
    form = UsuarioForm()
    # popular choices dinâmicas
    clientes_list = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    form.clientes.choices = [(c.id, c.nome) for c in clientes_list]
    perfis_list = Perfil.query.filter_by(ativo=True).order_by(Perfil.nome).all()
    form.perfis.choices = [(p.id, p.nome) for p in perfis_list]
    if form.validate_on_submit():
        # validação de CPF único
        if form.cpf.data:
            existing = Usuario.query.filter_by(cpf=form.cpf.data).first()
            if existing:
                form.cpf.errors.append('CPF já cadastrado para outro usuário.')
                return render_template('usuario/form.html', form=form, titulo='Novo Usuário')
        obj = Usuario(username=form.username.data, nome=form.nome.data,
                      email=form.email.data, telefone=form.telefone.data,
                      is_admin=form.is_admin.data, ativo=form.ativo.data)
        obj.cpf = form.cpf.data.strip() if form.cpf.data else None
        if form.senha.data:
            obj.set_senha(form.senha.data)
        else:
            flash('Senha obrigatória para novo usuário.', 'danger')
            return render_template('usuario/form.html', form=form, titulo='Novo Usuário')
        db.session.add(obj)
        db.session.commit()
        # Associação de clientes (municípios vinculados)
        selected_clients = request.form.getlist('clientes')
        for cid in selected_clients:
            try:
                cid_int = int(cid)
            except Exception:
                continue
            db.session.add(UsuarioCliente(usuario_id=obj.id, cliente_id=cid_int))
        # Associação de perfis
        selected_perfis = request.form.getlist('perfis')
        for pid in selected_perfis:
            try:
                pid_int = int(pid)
            except Exception:
                continue
            db.session.add(UsuarioPerfil(usuario_id=obj.id, perfil_id=pid_int))
        db.session.commit()
        flash('Usuário criado.', 'success')
        return redirect(url_for('adm.usuarios'))
    return render_template('usuario/form.html', form=form, titulo='Novo Usuário')


@adm_bp.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def usuario_editar(id):
    obj = Usuario.query.get_or_404(id)
    form = UsuarioForm()
    # popular choices dinâmicas
    clientes_list = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    form.clientes.choices = [(c.id, c.nome) for c in clientes_list]
    perfis_list = Perfil.query.filter_by(ativo=True).order_by(Perfil.nome).all()
    form.perfis.choices = [(p.id, p.nome) for p in perfis_list]
    if form.validate_on_submit():
        obj.username = form.username.data
        obj.nome = form.nome.data
        obj.email = form.email.data
        obj.telefone = form.telefone.data
        obj.cpf = form.cpf.data.strip() if form.cpf.data else None
        obj.is_admin = form.is_admin.data
        obj.ativo = form.ativo.data
        if form.senha.data:
            obj.set_senha(form.senha.data)
        db.session.commit()
        # validar CPF único no editar
        if obj.cpf:
            existing = Usuario.query.filter(Usuario.cpf == obj.cpf, Usuario.id != obj.id).first()
            if existing:
                form.cpf.errors.append('CPF já cadastrado para outro usuário.')
                # repopular escolhas e exibir formulário novamente
                return render_template('usuario/form.html', form=form, titulo='Editar Usuário', obj=obj)
        # atualizar associações de clientes
        UsuarioCliente.query.filter_by(usuario_id=obj.id).delete()
        selected_clients = request.form.getlist('clientes')
        for cid in selected_clients:
            try:
                cid_int = int(cid)
            except Exception:
                continue
            db.session.add(UsuarioCliente(usuario_id=obj.id, cliente_id=cid_int))
        # atualizar associações de perfis
        UsuarioPerfil.query.filter_by(usuario_id=obj.id).delete()
        selected_perfis = request.form.getlist('perfis')
        for pid in selected_perfis:
            try:
                pid_int = int(pid)
            except Exception:
                continue
            db.session.add(UsuarioPerfil(usuario_id=obj.id, perfil_id=pid_int))
        db.session.commit()
        flash('Usuário atualizado.', 'success')
        return redirect(url_for('adm.usuarios'))
    form.username.data = obj.username
    form.nome.data = obj.nome
    form.email.data = obj.email
    form.telefone.data = obj.telefone
    form.is_admin.data = obj.is_admin
    form.ativo.data = obj.ativo
    # preencher seleções existentes
    form.clientes.data = [uc.cliente_id for uc in obj.clientes]
    form.perfis.data = [up.perfil_id for up in obj.perfis]
    return render_template('usuario/form.html', form=form, titulo='Editar Usuário', obj=obj)


@adm_bp.route('/usuarios/<int:id>/visualizar')
@login_required
@admin_required
def usuario_visualizar(id):
    obj = Usuario.query.get_or_404(id)
    return render_template('usuario/visualizar.html', obj=obj)


@adm_bp.route('/usuarios/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def usuario_excluir(id):
    obj = Usuario.query.get_or_404(id)
    obj.ativo = False
    db.session.commit()
    flash('Usuário inativado.', 'warning')
    return redirect(url_for('adm.usuarios'))

# ── Perfis ────────────────────────────────────────────────────────────────────

@adm_bp.route('/perfis')
@login_required
@admin_required
def perfis():
    q = request.args.get('q', '')
    query = Perfil.query
    if q:
        query = query.filter(Perfil.nome.ilike(f'%{q}%'))
    registros = query.order_by(Perfil.nome).all()
    return render_template('perfil/listar.html', registros=registros, q=q)


@adm_bp.route('/perfis/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def perfil_novo():
    form = PerfilForm()
    cliente_id = session.get('cliente_id')
    menus_pai = Menu.query.filter_by(cliente_id=cliente_id, menu_pai_id=None, ativo=True).order_by(Menu.ordem, Menu.nome).all()
    if form.validate_on_submit():
        obj = Perfil(cliente_id=cliente_id, nome=form.nome.data,
                     descricao=form.descricao.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        for mid in request.form.getlist('menus'):
            try:
                db.session.add(PerfilMenu(perfil_id=obj.id, menu_id=int(mid)))
            except Exception:
                pass
        db.session.commit()
        flash('Perfil criado.', 'success')
        return redirect(url_for('adm.perfis'))
    return render_template('perfil/form.html', form=form, titulo='Novo Perfil',
                           menus_pai=menus_pai, menus_selecionados=set())


@adm_bp.route('/perfis/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def perfil_editar(id):
    obj = Perfil.query.get_or_404(id)
    form = PerfilForm()
    cliente_id = session.get('cliente_id') or obj.cliente_id
    menus_pai = Menu.query.filter_by(cliente_id=cliente_id, menu_pai_id=None, ativo=True).order_by(Menu.ordem, Menu.nome).all()
    if form.validate_on_submit():
        obj.nome = form.nome.data
        obj.descricao = form.descricao.data
        obj.ativo = form.ativo.data
        db.session.commit()
        PerfilMenu.query.filter_by(perfil_id=obj.id).delete()
        for mid in request.form.getlist('menus'):
            try:
                db.session.add(PerfilMenu(perfil_id=obj.id, menu_id=int(mid)))
            except Exception:
                pass
        db.session.commit()
        flash('Perfil atualizado.', 'success')
        return redirect(url_for('adm.perfis'))
    form.nome.data = obj.nome
    form.descricao.data = obj.descricao
    form.ativo.data = obj.ativo
    menus_selecionados = {pm.menu_id for pm in obj.menus}
    return render_template('perfil/form.html', form=form, titulo='Editar Perfil', obj=obj,
                           menus_pai=menus_pai, menus_selecionados=menus_selecionados)


@adm_bp.route('/perfis/<int:id>/visualizar')
@login_required
@admin_required
def perfil_visualizar(id):
    obj = Perfil.query.get_or_404(id)
    return render_template('perfil/visualizar.html', obj=obj)


@adm_bp.route('/perfis/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def perfil_excluir(id):
    obj = Perfil.query.get_or_404(id)
    obj.ativo = False
    db.session.commit()
    flash('Perfil inativado.', 'warning')
    return redirect(url_for('adm.perfis'))

# ── Menus ─────────────────────────────────────────────────────────────────────

@adm_bp.route('/menus')
@login_required
@admin_required
def menus():
    q = request.args.get('q', '')
    query = Menu.query
    if q:
        query = query.filter(Menu.nome.ilike(f'%{q}%'))
    registros = query.order_by(Menu.ordem, Menu.nome).all()
    return render_template('menu/listar.html', registros=registros, q=q)


@adm_bp.route('/menus/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def menu_novo():
    form = MenuForm()
    if form.validate_on_submit():
        cliente_id = session.get('cliente_id')
        obj = Menu(cliente_id=cliente_id, codigo=form.codigo.data, nome=form.nome.data,
                   icone=form.icone.data, endpoint=form.endpoint.data,
                   ordem=form.ordem.data, ativo=form.ativo.data)
        db.session.add(obj)
        db.session.commit()
        flash('Menu criado.', 'success')
        return redirect(url_for('adm.menus'))
    return render_template('menu/form.html', form=form, titulo='Novo Menu')


@adm_bp.route('/menus/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def menu_editar(id):
    obj = Menu.query.get_or_404(id)
    form = MenuForm()
    if form.validate_on_submit():
        obj.codigo = form.codigo.data
        obj.nome = form.nome.data
        obj.icone = form.icone.data
        obj.endpoint = form.endpoint.data
        obj.ordem = form.ordem.data
        obj.ativo = form.ativo.data
        db.session.commit()
        flash('Menu atualizado.', 'success')
        return redirect(url_for('adm.menus'))
    form.codigo.data = obj.codigo
    form.nome.data = obj.nome
    form.icone.data = obj.icone
    form.endpoint.data = obj.endpoint
    form.ordem.data = obj.ordem
    form.ativo.data = obj.ativo
    return render_template('menu/form.html', form=form, titulo='Editar Menu', obj=obj)


@adm_bp.route('/menus/<int:id>/visualizar')
@login_required
@admin_required
def menu_visualizar(id):
    obj = Menu.query.get_or_404(id)
    return render_template('menu/visualizar.html', obj=obj)


@adm_bp.route('/menus/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def menu_excluir(id):
    obj = Menu.query.get_or_404(id)
    obj.ativo = False
    db.session.commit()
    flash('Menu inativado.', 'warning')
    return redirect(url_for('adm.menus'))
