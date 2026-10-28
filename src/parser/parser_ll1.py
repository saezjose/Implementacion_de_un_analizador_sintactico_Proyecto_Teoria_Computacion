"""
Parser LL(1) Descendente Recursivo para SmartRule
Implementado desde cero, sin generadores automáticos.
"""

from src.lexer.lexer import analizador_lexico
from src.ast.nodos import *


class ParserError(Exception):
    """Excepción para errores sintácticos."""
    def __init__(self, mensaje, token=None):
        self.mensaje = mensaje
        self.token = token
        super().__init__(mensaje)
    
    def __str__(self):
        if self.token:
            if hasattr(self.token, 'linea') and hasattr(self.token, 'columna'):
                return f"Error sintáctico (línea {self.token.linea}, columna {self.token.columna}): {self.mensaje}"
            else:
                return f"Error sintáctico en token {self.token}: {self.mensaje}"
        return f"Error sintáctico: {self.mensaje}"


class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errores = []
    
    def token_tipo(self, token):
        if hasattr(token, 'tipo'):
            return token.tipo
        if isinstance(token, (list, tuple)) and len(token) > 0:
            return token[0]
        return None
    
    def token_lexema(self, token):
        if hasattr(token, 'lexema'):
            return token.lexema
        if isinstance(token, (list, tuple)) and len(token) > 1:
            return token[1]
        return ''
    
    def token_linea(self, token):
        if hasattr(token, 'linea'):
            return token.linea
        if isinstance(token, (list, tuple)) and len(token) > 2:
            return token[2]
        return 1
    
    def token_columna(self, token):
        if hasattr(token, 'columna'):
            return token.columna
        if isinstance(token, (list, tuple)) and len(token) > 3:
            return token[3]
        return 1
    
    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        from src.lexer.lexer import Token
        return Token('EOF', '$', 1, 1)
    
    def avanzar(self):
        if self.pos < len(self.tokens):
            self.pos += 1
        return self.actual()
    
    def consumir(self, tipo_esperado, contexto=None):
        token = self.actual()
        if self.token_tipo(token) == tipo_esperado:
            self.avanzar()
            return token
        else:
            linea = self.token_linea(token)
            columna = self.token_columna(token)
            lexema = self.token_lexema(token)
            if tipo_esperado == 'EOF':
                esperado = 'fin de entrada'
            elif tipo_esperado == 'PUNTO_COMA':
                esperado = "';' al final de la regla"
            elif tipo_esperado == 'WHEN':
                esperado = "'WHEN'"
            elif tipo_esperado == 'THEN':
                esperado = "la palabra reservada THEN"
            elif tipo_esperado == 'ELSE':
                esperado = "'ELSE'"
            elif tipo_esperado == 'IGUAL':
                esperado = "'='"
            elif tipo_esperado == 'COMA':
                esperado = "','"
            elif tipo_esperado == 'ID':
                esperado = 'un identificador'
            elif tipo_esperado == 'NUM':
                esperado = 'un número'
            elif tipo_esperado == 'OP_REL':
                esperado = 'un operador relacional'
            else:
                esperado = f"'{tipo_esperado}'"
            if self.token_tipo(token) == 'EOF':
                encontrado = 'fin de entrada'
            else:
                encontrado = f"'{lexema}'"
            if contexto == 'then':
                mensaje = f"se esperaba {esperado}"
            elif contexto == 'punto_coma':
                mensaje = f"se esperaba ';' al final de la regla"
            elif contexto == 'when_inicio':
                mensaje = f"se esperaba 'WHEN' al inicio de una regla, se encontró {encontrado}"
            else:
                mensaje = f"se esperaba {esperado}, se encontró {encontrado}"
            error = ParserError(mensaje, token)
            raise error
    
    def sincronizar_punto_coma(self):
        """Avanzar hasta consumir PUNTO_COMA o detenerse antes de WHEN o en EOF"""
        while self.token_tipo(self.actual()) != 'EOF':
            if self.token_tipo(self.actual()) == 'PUNTO_COMA':
                try:
                    self.consumir('PUNTO_COMA')
                except Exception:
                    self.avanzar()
                break
            if self.token_tipo(self.actual()) == 'WHEN':
                break
            self.avanzar()
    
    def parse(self, modo_panic=False):
        """Prog -> Regla Prog | ε"""
        reglas = []
        self.errores = []
        while self.token_tipo(self.actual()) != 'EOF':
            if self.token_tipo(self.actual()) == 'WHEN':
                if modo_panic:
                    try:
                        regla = self.parse_regla()
                        reglas.append(regla)
                    except ParserError as e:
                        self.errores.append(e)
                        self.sincronizar_punto_coma()
                        continue
                else:
                    regla = self.parse_regla()
                    reglas.append(regla)
            else:
                token = self.actual()
                if modo_panic:
                    if self.token_tipo(token) == 'EOF':
                        break
                    lexema = self.token_lexema(token)
                    if self.token_tipo(token) == 'EOF':
                        encontrado = 'fin de entrada'
                    else:
                        encontrado = f"'{lexema}'"
                    self.errores.append(ParserError(f"se esperaba 'WHEN' al inicio de una regla, se encontró {encontrado}", token))
                    while self.token_tipo(self.actual()) != 'EOF':
                        if self.token_tipo(self.actual()) == 'WHEN':
                            break
                        if self.token_tipo(self.actual()) == 'PUNTO_COMA':
                            self.avanzar()
                            break
                        self.avanzar()
                    continue
                else:
                    lexema = self.token_lexema(token)
                    if self.token_tipo(token) == 'EOF':
                        encontrado = 'fin de entrada'
                    else:
                        encontrado = f"'{lexema}'"
                    raise ParserError(f"se esperaba 'WHEN' al inicio de una regla, se encontró {encontrado}", token)
        ast = Programa(reglas)
        if modo_panic:
            return ast, self.errores
        return ast
    
    def parse_regla(self):
        """Regla -> WHEN Cond THEN ListaAcciones ElsePart PUNTO_COMA"""
        self.consumir('WHEN')
        condicion = self.parse_cond()
        # Verificar THEN
        if self.token_tipo(self.actual()) != 'THEN':
            token = self.actual()
            raise ParserError("se esperaba la palabra reservada THEN", token)
        self.consumir('THEN')
        acciones_then = self.parse_lista_acciones()
        acciones_else = self.parse_else_part()
        if self.token_tipo(self.actual()) != 'PUNTO_COMA':
            token = self.actual()
            raise ParserError("se esperaba ';' al final de la regla", token)
        self.consumir('PUNTO_COMA')
        return Regla(condicion, acciones_then, acciones_else)
    
    def parse_else_part(self):
        """ElsePart -> ELSE ListaAcciones | ε"""
        if self.token_tipo(self.actual()) == 'ELSE':
            self.consumir('ELSE')
            return self.parse_lista_acciones()
        return None
    
    def parse_cond(self):
        """Cond -> OrExpr"""
        return self.parse_or_expr()
    
    def parse_or_expr(self):
        """OrExpr -> AndExpr OrTail"""
        nodo = self.parse_and_expr()
        return self.parse_or_tail(nodo)
    
    def parse_or_tail(self, nodo_izq):
        """OrTail -> OR AndExpr OrTail | ε"""
        if self.token_tipo(self.actual()) == 'OR':
            self.consumir('OR')
            nodo_der = self.parse_and_expr()
            nodo = BinOp('OR', nodo_izq, nodo_der)
            return self.parse_or_tail(nodo)
        return nodo_izq
    
    def parse_and_expr(self):
        """AndExpr -> NotExpr AndTail"""
        nodo = self.parse_not_expr()
        return self.parse_and_tail(nodo)
    
    def parse_and_tail(self, nodo_izq):
        """AndTail -> AND NotExpr AndTail | ε"""
        if self.token_tipo(self.actual()) == 'AND':
            self.consumir('AND')
            nodo_der = self.parse_not_expr()
            nodo = BinOp('AND', nodo_izq, nodo_der)
            return self.parse_and_tail(nodo)
        return nodo_izq
    
    def parse_not_expr(self):
        """NotExpr -> NOT NotExpr | RelExpr"""
        if self.token_tipo(self.actual()) == 'NOT':
            self.consumir('NOT')
            expr = self.parse_not_expr()
            return UnOp('NOT', expr)
        return self.parse_rel_expr()
    
    def parse_rel_expr(self):
        """RelExpr -> Factor RelExprTail"""
        factor1 = self.parse_factor()
        return self.parse_rel_expr_tail(factor1)
    
    def parse_rel_expr_tail(self, nodo_izq):
        """RelExprTail -> OP_REL Factor | ε"""
        if self.token_tipo(self.actual()) == 'OP_REL':
            op_token = self.actual()
            op = self.token_lexema(op_token)
            self.consumir('OP_REL')
            # Verificar que hay un valor después del operador
            tok = self.actual()
            if self.token_tipo(tok) == 'EOF':
                raise ParserError("se esperaba un valor (número, identificador, TRUE o FALSE) después del operador", tok)
            # Si viene THEN u otro token inesperado
            if self.token_tipo(tok) == 'THEN':
                raise ParserError(f"se esperaba un valor (número, identificador, TRUE o FALSE) después del operador '{op}'", tok)
            if self.token_tipo(tok) not in ['NUM', 'ID', 'TRUE', 'FALSE', 'NOT', 'PARENT_IZQ']:
                raise ParserError(f"se esperaba un valor (número, identificador, TRUE o FALSE) después del operador '{op}'", tok)
            factor2 = self.parse_factor()
            return BinOp(op, nodo_izq, factor2)
        return nodo_izq
    
    def parse_factor(self):
        """Factor -> NUM | ID | TRUE | FALSE"""
        token = self.actual()
        tipo = self.token_tipo(token)
        lexema = self.token_lexema(token)
        if tipo == 'NUM':
            self.consumir('NUM')
            return Literal(lexema, 'NUM')
        elif tipo == 'ID':
            self.consumir('ID')
            return Identificador(lexema)
        elif tipo == 'TRUE':
            self.consumir('TRUE')
            return Literal('TRUE', 'BOOL')
        elif tipo == 'FALSE':
            self.consumir('FALSE')
            return Literal('FALSE', 'BOOL')
        elif tipo == 'NOT':
            # Permitir NOT en factor si viene de not_expr? pero ya manejado
            return self.parse_not_expr()
        else:
            # Contexto - si viene después de OP_REL
            # Intentar detectar contexto
            raise ParserError(
                "se esperaba un valor (número, identificador, TRUE o FALSE)",
                token
            )
    
    def parse_lista_acciones(self):
        """ListaAcciones -> Accion AccionTail"""
        tok = self.actual()
        # Lista vacía tras THEN
        if self.token_tipo(tok) == 'ELSE':
            raise ParserError("se esperaba al menos una acción después de THEN", tok)
        if self.token_tipo(tok) == 'PUNTO_COMA':
            raise ParserError("se esperaba al menos una acción después de THEN", tok)
        if self.token_tipo(tok) == 'EOF':
            raise ParserError("se esperaba al menos una acción después de THEN", tok)
        try:
            accion = self.parse_accion()
        except ParserError:
            raise
        acciones = [accion]
        try:
            acciones.extend(self.parse_accion_tail())
        except ParserError:
            raise
        return ListaAcciones(acciones)
    
    def parse_accion_tail(self):
        """AccionTail -> COMA Accion AccionTail | ε"""
        if self.token_tipo(self.actual()) == 'COMA':
            coma_token = self.actual()
            self.consumir('COMA')
            tok = self.actual()
            # Coma sobrante o acción faltante
            if self.token_tipo(tok) == 'COMA' or self.token_tipo(tok) == 'ELSE' or self.token_tipo(tok) == 'PUNTO_COMA' or self.token_tipo(tok) == 'EOF':
                raise ParserError("se esperaba una acción después de ','", tok)
            try:
                accion = self.parse_accion()
            except ParserError:
                raise
            resto = self.parse_accion_tail()
            return [accion] + resto
        return []
    
    def parse_accion(self):
        """Accion -> ID AccionResto"""
        token = self.actual()
        if self.token_tipo(token) != 'ID':
            lexema = self.token_lexema(token)
            if self.token_tipo(token) == 'EOF':
                encontrado = 'fin de entrada'
            elif self.token_tipo(token) == 'COMA':
                raise ParserError("se esperaba una acción después de ','", token)
            elif self.token_tipo(token) == 'ELSE' or self.token_tipo(token) == 'PUNTO_COMA':
                raise ParserError("se esperaba al menos una acción después de THEN", token)
            else:
                encontrado = f"'{lexema}'"
                raise ParserError(
                    f"se esperaba un identificador para acción, se encontró {encontrado}",
                    token
                )
        nombre1 = self.token_lexema(token)
        self.consumir('ID')
        return self.parse_accion_resto(nombre1)
    
    def parse_accion_resto(self, nombre1):
        """AccionResto -> IGUAL Factor | ID ArgResto | NUM | TRUE | FALSE | ε"""
        tok = self.actual()
        tipo = self.token_tipo(tok)
        if tipo == 'IGUAL':
            self.consumir('IGUAL')
            valor = self.parse_factor()
            return Asignacion(nombre1, valor)
        elif tipo == 'ID':
            nombre2 = self.token_lexema(tok)
            self.consumir('ID')
            return self.parse_arg_resto(nombre1, nombre2)
        elif tipo in ['NUM', 'TRUE', 'FALSE']:
            arg = self.parse_factor()
            return LlamadaAccion(nombre1, arg)
        else:
            # ε
            return LlamadaAccion(nombre1, None)
    
    def parse_arg_resto(self, nombre1, nombre2):
        """ArgResto -> IGUAL Factor | ε"""
        tok = self.actual()
        if self.token_tipo(tok) == 'IGUAL':
            self.consumir('IGUAL')
            valor = self.parse_factor()
            return Asignacion(nombre2, valor)
        else:
            return LlamadaAccion(nombre1, Identificador(nombre2))
