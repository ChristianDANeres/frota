from app import create_app
from app.extensions import db
from app.models import Cliente, Oficina, Veiculo, Motorista, VeiculoOficina, VeiculoOficinaAnexo, TipoArquivo
import os
from datetime import datetime

app = create_app()
with app.app_context():
    # criar cliente de teste se não existir
    cliente = Cliente.query.filter_by(nome='Cliente Teste CI').first()
    if not cliente:
        cliente = Cliente(nome='Cliente Teste CI')
        db.session.add(cliente)
        db.session.commit()
    # criar oficina
    oficina = Oficina.query.filter_by(nome='Oficina Teste CI', cliente_id=cliente.id).first()
    if not oficina:
        oficina = Oficina(cliente_id=cliente.id, nome='Oficina Teste CI')
        db.session.add(oficina)
        db.session.commit()
    # criar veiculo simples
    veiculo = Veiculo.query.filter_by(placa='TEST-CI', cliente_id=cliente.id).first()
    if not veiculo:
        veiculo = Veiculo(cliente_id=cliente.id, placa='TEST-CI')
        db.session.add(veiculo)
        db.session.commit()
    # criar motorista
    motorista = Motorista.query.filter_by(nome='Motorista Teste CI', cliente_id=cliente.id).first()
    if not motorista:
        motorista = Motorista(cliente_id=cliente.id, cpf='00000000000', nome='Motorista Teste CI', cnh='123456')
        db.session.add(motorista)
        db.session.commit()
    # criar registro veiculo_oficina
    vo = VeiculoOficina(cliente_id=cliente.id, oficina_id=oficina.id, veiculo_id=veiculo.id, data_entrada=datetime.utcnow(), motivo='Teste de integração')
    db.session.add(vo)
    db.session.commit()
    # criar tipo arquivo (opcional)
    tipo = TipoArquivo.query.filter_by(nome='Teste', cliente_id=cliente.id).first()
    if not tipo:
        tipo = TipoArquivo(cliente_id=cliente.id, nome='Teste', ativo=True)
        db.session.add(tipo)
        db.session.commit()
    # criar arquivo dummy
    pasta = os.path.join(app.root_path, 'static', 'uploads', 'veiculo_oficina', str(vo.id))
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, 'dummy.txt')
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write('arquivo de teste')
    tamanho = os.path.getsize(caminho)
    anexo = VeiculoOficinaAnexo(cliente_id=cliente.id, veiculo_oficina_id=vo.id, tipo_arquivo_id=tipo.id, nome_arquivo='dummy.txt', caminho_arquivo=caminho, tamanho_arquivo=tamanho)
    db.session.add(anexo)
    db.session.commit()
    print('Criado registro:', vo.id, 'anexo id:', anexo.id)
    rel = os.path.relpath(anexo.caminho_arquivo, os.path.join(app.root_path, 'static')).replace('\\','/')
    print('URL pública:', f"/static/{rel}")
