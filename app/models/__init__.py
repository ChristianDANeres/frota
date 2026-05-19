from app.models.cliente import Cliente
from app.models.perfil import Perfil
from app.models.menu import Menu
from app.models.usuario import Usuario, UsuarioCliente, UsuarioPerfil, PerfilMenu
from app.models.montadora import Montadora
from app.models.cor import Cor
from app.models.tipo_arquivo import TipoArquivo
from app.models.tipo_viagem import TipoViagem
from app.models.status_veiculo import StatusVeiculo
from app.models.veiculo import Veiculo
from app.models.motorista import Motorista, MotoristaAnexo
from app.models.viagem import Viagem, ViagemPaciente
from app.models.abastecimento import Abastecimento, AbastecimentoAnexo
from app.models.oficina import Oficina, VeiculoOficina, VeiculoOficinaAnexo
from app.models.intercorrencia import Intercorrencia, StatusIntercorrencia, DestinoUsuario
from app.models.diario import Diario, DiarioAnexo

__all__ = [
    'Cliente', 'Perfil', 'Menu', 'Usuario', 'UsuarioCliente', 'UsuarioPerfil', 'PerfilMenu',
    'Montadora', 'Cor', 'TipoArquivo', 'TipoViagem', 'StatusVeiculo',
    'Veiculo', 'Motorista', 'MotoristaAnexo',
    'Viagem', 'ViagemPaciente',
    'Abastecimento', 'AbastecimentoAnexo',
    'Oficina', 'VeiculoOficina', 'VeiculoOficinaAnexo',
    'Intercorrencia', 'StatusIntercorrencia', 'DestinoUsuario',
    'Diario', 'DiarioAnexo',
]
