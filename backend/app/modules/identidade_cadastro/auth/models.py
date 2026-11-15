# Submódulo Auth - modelos de domínio associados
from app.modules.identidade_cadastro.usuarios.models import Usuario, MembroCondominio, OcupacaoUnidade
from app.modules.identidade_cadastro.pessoas.models import Pessoa
from app.modules.condominio.estrutura.models import Condominio
from app.modules.governanca.seguranca_auditoria.models import EventoAuditoria

__all__ = ['Usuario', 'MembroCondominio', 'OcupacaoUnidade', 'Pessoa', 'Condominio', 'EventoAuditoria']
