"""
Analizador Léxico para SmartRule
Basado en el analizador provisto, extendido con operadores '=' y ',' para acciones/else.
"""

import re


class LexerError(Exception):
    """Excepción para errores léxicos."""
    pass


def analizador_lexico(cadena):
    """
    Convierte una cadena de entrada en una lista de tokens.
    
    Returns:
        [(TIPO_TOKEN, lexema), ...]
    """
    especificacion_tokens = [
        ('NUM',        r'\d+'),
        ('OP_REL',     r'>=|<=|==|!=|>|<'),
        ('IGUAL',      r'='),
        ('COMA',       r','),
        ('PUNTO_COMA', r';'),
        ('PARENT_IZQ', r'\('),
        ('PARENT_DER', r'\)'),
        ('ID',         r'[A-Za-z_][A-Za-z0-9_]*'),
        ('ESPACIO',    r'[ \t\n\r]+'),
        ('ERROR',      r'.')
    ]

    patron = '|'.join(
        f'(?P<{nombre}>{expresion})'
        for nombre, expresion in especificacion_tokens
    )

    palabras_reservadas = {
        'WHEN',
        'THEN',
        'ELSE',
        'AND',
        'OR',
        'NOT',
        'TRUE',
        'FALSE'
    }

    tokens = []

    for coincidencia in re.finditer(patron, cadena):
        tipo = coincidencia.lastgroup
        lexema = coincidencia.group()

        if tipo == 'ESPACIO':
            continue

        elif tipo == 'ID' and lexema.upper() in palabras_reservadas:
            tipo = lexema.upper()

        elif tipo == 'ERROR':
            raise LexerError(f"Símbolo no reconocido: '{lexema}'")

        tokens.append((tipo, lexema))

    # Añadir token EOF
    tokens.append(('EOF', '$'))
    return tokens
