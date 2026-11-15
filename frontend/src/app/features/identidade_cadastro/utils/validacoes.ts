export interface TelefoneModel {
  numero: string;
  tipo: 'celular' | 'residencial' | 'comercial';
  principal: boolean;
  whatsapp: boolean;
}

/**
 * Validação algorítmica de CPF brasileiro.
 */
export function validarCpf(cpf: string | null | undefined): boolean {
  if (!cpf) return true; // campo opcional quando vazio
  const digits = cpf.replace(/\D/g, '');
  if (digits.length !== 11) return false;
  if (/^(\d)\1{10}$/.test(digits)) return false;

  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += parseInt(digits[i], 10) * (10 - i);
  }
  let rev = (sum * 10) % 11;
  if (rev === 10 || rev === 11) rev = 0;
  if (rev !== parseInt(digits[9], 10)) return false;

  sum = 0;
  for (let i = 0; i < 10; i++) {
    sum += parseInt(digits[i], 10) * (11 - i);
  }
  rev = (sum * 10) % 11;
  if (rev === 10 || rev === 11) rev = 0;
  if (rev !== parseInt(digits[10], 10)) return false;

  return true;
}

/**
 * Formata um CPF no padrão xxx.xxx.xxx-xx.
 */
export function formatarCpf(value: string | null | undefined): string {
  if (!value) return '';
  const digits = value.replace(/\D/g, '').slice(0, 11);
  if (digits.length <= 3) return digits;
  if (digits.length <= 6) return `${digits.slice(0, 3)}.${digits.slice(3)}`;
  if (digits.length <= 9) return `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6)}`;
  return `${digits.slice(0, 3)}.${digits.slice(3, 6)}.${digits.slice(6, 9)}-${digits.slice(9, 11)}`;
}

/**
 * Validação de telefone brasileiro (DDD + 8 ou 9 dígitos).
 */
export function validarTelefone(numero: string | null | undefined, tipo?: 'celular' | 'residencial' | 'comercial'): boolean {
  if (!numero) return false;
  const digits = numero.replace(/\D/g, '');
  if (digits.length !== 10 && digits.length !== 11) return false;

  const ddd = parseInt(digits.slice(0, 2), 10);
  if (ddd < 11 || ddd > 99) return false;

  if (digits.length === 11) {
    // Celular no Brasil deve ter o nono dígito 9
    if (digits[2] !== '9') return false;
    if (tipo && tipo !== 'celular') return false;
  } else if (digits.length === 10) {
    // Fixo (residencial/comercial) começa com 2, 3, 4 ou 5
    if (!['2', '3', '4', '5'].includes(digits[2])) return false;
    if (tipo && tipo === 'celular') return false;
  }

  return true;
}

/**
 * Formata telefone no padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX.
 */
export function formatarTelefone(value: string | null | undefined): string {
  if (!value) return '';
  const digits = value.replace(/\D/g, '').slice(0, 11);
  if (digits.length <= 2) return digits ? `(${digits}` : '';
  if (digits.length <= 6) return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
  if (digits.length <= 10) {
    return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`;
  }
  return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7, 11)}`;
}

/**
 * Validação de formato de e-mail.
 */
export function validarEmail(email: string | null | undefined): boolean {
  if (!email) return false;
  const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return re.test(email.trim());
}

/**
 * Trata erros do backend (Pydantic, HTTP 400/422/500), garantindo
 * mensagens legíveis ao usuário e impedindo a aparição de "[object Object]".
 */
export function formatarMensagemErro(err: any, fallback: string = 'Ocorreu um erro ao processar a requisição.'): string {
  if (!err) return fallback;
  const errorObj = err?.error !== undefined ? err.error : err;

  // Se o detalhe for string direta
  if (typeof errorObj?.detail === 'string') {
    return mapearMensagemLegivel(errorObj.detail);
  }

  // Se for array de validação do Pydantic (HTTP 422)
  if (Array.isArray(errorObj?.detail)) {
    const mensagens = errorObj.detail.map((item: any) => {
      const campo = item.loc && item.loc.length > 0 ? item.loc[item.loc.length - 1] : '';
      if (campo === 'email') return 'Informe um e-mail válido.';
      if (campo === 'cpf') return 'Informe um CPF válido.';
      if (campo === 'telefones' || campo === 'numero') return 'Informe um número de telefone válido com DDD.';
      if (item.msg) {
        if (typeof item.msg === 'string' && item.msg.toLowerCase().includes('email address')) {
          return 'Informe um e-mail válido.';
        }
        return item.msg;
      }
      return typeof item === 'string' ? item : '';
    }).filter((m: string) => !!m);

    if (mensagens.length > 0) {
      return mensagens.join(' ');
    }
  }

  if (typeof errorObj?.message === 'string') {
    return mapearMensagemLegivel(errorObj.message);
  }

  if (typeof err?.message === 'string' && !err.message.includes('[object')) {
    return mapearMensagemLegivel(err.message);
  }

  return fallback;
}

function mapearMensagemLegivel(codigo: string): string {
  switch (codigo) {
    case 'CPF_INVALIDO':
    case 'value_error: CPF_INVALIDO: O CPF informado não é válido.':
      return 'CPF inválido. Verifique os dígitos informados.';
    case 'TIPO_TELEFONE_DUPLICADO':
      return 'Permitido cadastrar somente um telefone por tipo (celular, residencial, comercial).';
    case 'APENAS_UM_TELEFONE_PRINCIPAL':
      return 'Selecione exatamente um telefone como principal.';
    case 'TELEFONE_INVALIDO':
      return 'Número de telefone inválido. Informe o DDD e os dígitos corretos.';
    case 'VAGA_DUPLICADA':
      return 'Já existe uma vaga cadastrada com esta identificação.';
    case 'IDENTIFICACAO_OBRIGATORIA':
      return 'A identificação da vaga é obrigatória.';
    case 'PESSOA_POSSUI_CONTA':
      return 'Não é possível excluir esta pessoa pois ela possui conta ativa no sistema.';
    case 'PESSOA_POSSUI_OCUPACAO_ATIVA':
      return 'Não é possível excluir esta pessoa pois ela possui vínculo ativo com uma unidade.';
    default:
      if (codigo.includes('value is not a valid email address')) {
        return 'Informe um e-mail válido.';
      }
      return codigo;
  }
}
