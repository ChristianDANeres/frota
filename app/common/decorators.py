from functools import wraps
from flask import redirect, url_for, flash, session
from flask_login import current_user


def cliente_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('cliente_id'):
            flash('Selecione um cliente para continuar.', 'warning')
            return redirect(url_for('cliente.selecionar'))
        return f(*args, **kwargs)
    return wrapper


def menu_required(codigo):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if not current_user.tem_permissao_menu(codigo):
                flash('Você não tem permissão para acessar este menu.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('Acesso restrito ao administrador.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return wrapper
