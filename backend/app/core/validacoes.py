import re


def validar_cpf(cpf: str | None) -> bool:
    """Valida se o CPF é matematicamente válido pelos dígitos verificadores."""
    if not cpf:
        return True
    digits = [int(c) for c in str(cpf) if c.isdigit()]
    if len(digits) != 11:
        return False
    if len(set(digits)) == 1:
        return False

    # Primeiro dígito verificador
    soma1 = sum(d * w for d, w in zip(digits[:9], range(10, 1, -1)))
    resto1 = (soma1 * 10) % 11
    d1 = 0 if resto1 in (10, 11) else resto1
    if digits[9] != d1:
        return False

    # Segundo dígito verificador
    soma2 = sum(d * w for d, w in zip(digits[:10], range(11, 1, -1)))
    resto2 = (soma2 * 10) % 11
    d2 = 0 if resto2 in (10, 11) else resto2
    return digits[10] == d2


def formatar_cpf(cpf: str | None) -> str:
    """Formata um CPF no padrão xxx.xxx.xxx-xx."""
    if not cpf:
        return ''
    digits = re.sub(r'\D', '', str(cpf))
    if len(digits) != 11:
        return cpf
    return f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}'


def validar_telefone(numero: str | None, tipo: str | None = None) -> bool:
    """Valida formato e comprimento de telefone brasileiro (DDD + 8 ou 9 dígitos)."""
    if not numero:
        return False
    digits = re.sub(r'\D', '', str(numero))
    if len(digits) not in (10, 11):
        return False

    # Validação de DDD (11 a 99)
    ddd = int(digits[:2])
    if ddd < 11 or ddd > 99:
        return False

    # Celular: 11 dígitos, primeiro dígito após DDD deve ser 9
    if len(digits) == 11:
        if digits[2] != '9':
            return False
        if tipo and tipo != 'celular':
            # Se for fixo com 11 dígitos, não é válido
            return False
    elif len(digits) == 10:
        # Fixo: 10 dígitos, primeiro dígito após DDD normalmente 2, 3, 4, 5
        if digits[2] not in ('2', '3', '4', '5'):
            return False
        if tipo and tipo == 'celular':
            # Celular deve ter 11 dígitos
            return False

    return True


def formatar_telefone(numero: str | None) -> str:
    """Formata número no padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX."""
    if not numero:
        return ''
    digits = re.sub(r'\D', '', str(numero))
    if len(digits) == 11:
        return f'({digits[:2]}) {digits[2:7]}-{digits[7:]}'
    if len(digits) == 10:
        return f'({digits[:2]}) {digits[2:6]}-{digits[6:]}'
    return numero
