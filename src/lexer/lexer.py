"""
Analizador Léxico para SmartRule
"""
import re


class Token:
    def __init__(self, tipo, lexema, linea=1, columna=1):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
    
    def __iter__(self):
        # Para compatibilidad con código que acceda como token[0], token[1]
        yield self.tipo
        yield self.lexema
        yield self.linea
        yield self.columna
    
    def __getitem__(self, index):
        if index == 0:
            return self.tipo
        elif index == 1:
            return self.lexema
        elif index == 2:
            return self.linea
        elif index == 3:
            return self.columna
        raise IndexError("Index out of range")
    
    def __repr__(self):
        return f"({self.tipo}, '{self.lexema}', {self.linea}, {self.columna})"
    
    def __str__(self):
        return f"({self.tipo}, '{self.lexema}')"


class LexerError(Exception):
    """Excepción para errores léxicos."""
    def __init__(self, mensaje, linea=None, columna=None, lexema=None):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        self.lexema = lexema
        if linea is not None and columna is not None:
            if lexema is not None:
                super().__init__(f"Error léxico (línea {linea}, columna {columna}): símbolo no reconocido '{lexema}'")
            else:
                super().__init__(f"Error léxico (línea {linea}, columna {columna}): {mensaje}")
        else:
            super().__init__(mensaje)


def analizador_lexico(cadena):
    """
    Convierte una cadena de entrada en una lista de tokens.
    
    Returns:
        Lista de objetos Token con tipo, lexema, linea, columna
    """
    especificacion_tokens = [
        ('NUM',        r'\d+'),
        ('OP_REL',     r'>=|<=|==|!=|>|<'),
        ('IGUAL',      r'='),
        ('COMA',       r','),
        ('PUNTO_COMA', r';'),
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
    # Calcular línea y columna
    line_start = 0
    current_line = 1
    
    for coincidencia in re.finditer(patron, cadena):
        tipo = coincidencia.lastgroup
        lexema = coincidencia.group()
        start = coincidencia.start()
        end = coincidencia.end()
        
        # Calcular línea y columna
        # Contar saltos de línea antes del token
        linea = cadena.count('\n', 0, start) + 1
        # Calcular columna: posición desde el inicio de la línea
        last_nl = cadena.rfind('\n', 0, start)
        if last_nl == -1:
            columna = start + 1
        else:
            columna = start - last_nl

        if tipo == 'ESPACIO':
            continue

        elif tipo == 'ID' and lexema.upper() in palabras_reservadas:
            tipo = lexema.upper()

        elif tipo == 'ERROR':
            raise LexerError(f"Símbolo no reconocido: '{lexema}'", linea=linea, columna=columna, lexema=lexema)

        tokens.append(Token(tipo, lexema, linea, columna))

    # Añadir token EOF
    # Calcular posición al final
    if cadena:
        linea_eof = cadena.count('\n') + 1
        last_nl = cadena.rfind('\n')
        if last_nl == -1:
            columna_eof = len(cadena) + 1
        else:
            columna_eof = len(cadena) - last_nl
    else:
        linea_eof = 1
        columna_eof = 1
    tokens.append(Token('EOF', '$', linea_eof, columna_eof))
    return tokens
