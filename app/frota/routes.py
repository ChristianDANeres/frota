from flask import Blueprint, render_template, session
from flask_login import login_required
from app.common.decorators import cliente_required, menu_required
from app.models import Veiculo

frota_bp = Blueprint('frota', __name__, url_prefix='/frota')


@frota_bp.route('/veiculos')
@login_required
@cliente_required
@menu_required('frota')
def veiculos():
    dados = Veiculo.query.filter_by(cliente_id=session['cliente_id']).order_by(Veiculo.placa).all()
    return render_template('frota/veiculos.html', veiculos=dados)
