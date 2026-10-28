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
            return f"Error sintáctico en token {self.token}: {self.mensaje}"
        return f"Error sintáctico: {self.mensaje}"


class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '$')
    
    def avanzar(self):
        if self.pos < len(self.tokens):
            self.pos += 1
        return self.actual()
    
    def consumir(self, tipo_esperado):
        token = self.actual()
        if token[0] == tipo_esperado:
            self.avanzar()
            return token
        else:
            raise ParserError(
                f"Se esperaba '{tipo_esperado}', se encontró '{token[0]}' con lexema '{token[1]}'",
                token
            )
    
    def parse(self):
        """Prog -> Regla Prog | ε"""
        reglas = []
        while self.actual()[0] != 'EOF':
            if self.actual()[0] == 'WHEN':
                regla = self.parse_regla()
                reglas.append(regla)
            else:
                token = self.actual()
                raise ParserError(
                    f"Se esperaba 'WHEN' al inicio de una regla, se encontró '{token[0]}' '{token[1]}'",
                    token
                )
        return Programa(reglas)
    
    def parse_regla(self):
        """Regla -> WHEN Cond THEN ListaAcciones ElsePart PUNTO_COMA"""
        self.consumir('WHEN')
        condicion = self.parse_cond()
        self.consumir('THEN')
        acciones_then = self.parse_lista_acciones()
        acciones_else = self.parse_else_part()
        self.consumir('PUNTO_COMA')
        return Regla(condicion, acciones_then, acciones_else)
    
    def parse_else_part(self):
        """ElsePart -> ELSE ListaAcciones | ε"""
        if self.actual()[0] == 'ELSE':
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
        if self.actual()[0] == 'OR':
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
        if self.actual()[0] == 'AND':
            self.consumir('AND')
            nodo_der = self.parse_not_expr()
            nodo = BinOp('AND', nodo_izq, nodo_der)
            return self.parse_and_tail(nodo)
        return nodo_izq
    
    def parse_not_expr(self):
        """NotExpr -> NOT NotExpr | RelExpr"""
        if self.actual()[0] == 'NOT':
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
        if self.actual()[0] == 'OP_REL':
            op = self.actual()[1]
            self.consumir('OP_REL')
            factor2 = self.parse_factor()
            return BinOp(op, nodo_izq, factor2)
        return nodo_izq
    
    def parse_factor(self):
        """Factor -> NUM | ID | TRUE | FALSE"""
        token = self.actual()
        if token[0] == 'NUM':
            self.consumir('NUM')
            return Literal(token[1], 'NUM')
        elif token[0] == 'ID':
            self.consumir('ID')
            return Identificador(token[1])
        elif token[0] == 'TRUE':
            self.consumir('TRUE')
            return Literal('TRUE', 'BOOL')
        elif token[0] == 'FALSE':
            self.consumir('FALSE')
            return Literal('FALSE', 'BOOL')
        else:
            raise ParserError(
                f"Se esperaba un factor (NUM, ID, TRUE, FALSE), se encontró '{token[0]}' '{token[1]}'",
                token
            )
    
    def parse_lista_acciones(self):
        """ListaAcciones -> Accion AccionTail"""
        accion = self.parse_accion()
        acciones = [accion]
        acciones.extend(self.parse_accion_tail())
        return ListaAcciones(acciones)
    
    def parse_accion_tail(self):
        """AccionTail -> COMA Accion AccionTail | ε"""
        if self.actual()[0] == 'COMA':
            self.consumir('COMA')
            accion = self.parse_accion()
            resto = self.parse_accion_tail()
            return [accion] + resto
        return []
    
    def parse_accion(self):
        """Accion -> ID AccionResto"""
        token = self.actual()
        if token[0] != 'ID':
            raise ParserError(
                f"Se esperaba un identificador para acción, se encontró '{token[0]}' '{token[1]}'",
                token
            )
        nombre1 = token[1]
        self.consumir('ID')
        return self.parse_accion_resto(nombre1)
    
    def parse_accion_resto(self, nombre1):
        """AccionResto -> IGUAL Factor | ID ArgResto | NUM | TRUE | FALSE | ε"""
        tok = self.actual()
        if tok[0] == 'IGUAL':
            self.consumir('IGUAL')
            valor = self.parse_factor()
            return Asignacion(nombre1, valor)
        elif tok[0] == 'ID':
            nombre2 = tok[1]
            self.consumir('ID')
            return self.parse_arg_resto(nombre1, nombre2)
        elif tok[0] in ['NUM', 'TRUE', 'FALSE']:
            arg = self.parse_factor()
            return LlamadaAccion(nombre1, arg)
        else:
            # ε
            return LlamadaAccion(nombre1, None)
    
    def parse_arg_resto(self, nombre1, nombre2):
        """ArgResto -> IGUAL Factor | ε"""
        tok = self.actual()
        if tok[0] == 'IGUAL':
            self.consumir('IGUAL')
            valor = self.parse_factor()
            # encender luces = 100 -> asignación al objetivo
            return Asignacion(nombre2, valor)
        else:
            # llamada con argumento
            return LlamadaAccion(nombre1, Identificador(nombre2))
