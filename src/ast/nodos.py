"""
Nodos del Árbol Sintáctico Abstracto (AST) para SmartRule
"""


class NodoAST:
    """Clase base para todos los nodos del AST."""
    def __init__(self):
        pass
    
    def to_dict(self):
        """Convierte el nodo a diccionario para visualización."""
        result = {"tipo": self.__class__.__name__}
        for key, value in self.__dict__.items():
            if isinstance(value, NodoAST):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, NodoAST) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result
    
    def __str__(self, nivel=0):
        """Representación en árbol del AST."""
        prefijo = "  " * nivel
        resultado = f"{prefijo}{self.__class__.__name__}(\n"
        items = []
        for key, value in self.__dict__.items():
            if isinstance(value, NodoAST):
                items.append(f"{prefijo}  {key}=\n{value.__str__(nivel + 2)},")
            elif isinstance(value, list):
                if value and isinstance(value[0], NodoAST):
                    items.append(f"{prefijo}  {key}=[\n")
                    for item in value:
                        items.append(item.__str__(nivel + 2) + ",")
                    items.append(f"{prefijo}  ],")
                else:
                    items.append(f"{prefijo}  {key}={value},")
            else:
                items.append(f"{prefijo}  {key}={repr(value)},")
        resultado += "\n".join(items)
        resultado += f"\n{prefijo})"
        return resultado


class Programa(NodoAST):
    def __init__(self, reglas):
        super().__init__()
        self.reglas = reglas  # lista de Regla


class Regla(NodoAST):
    def __init__(self, condicion, acciones_then, acciones_else=None):
        super().__init__()
        self.condicion = condicion
        self.acciones_then = acciones_then
        self.acciones_else = acciones_else  # puede ser None o ListaAcciones


class Condicion(NodoAST):
    """Nodo base para condiciones."""
    pass


class BinOp(Condicion):
    def __init__(self, op, izq, der):
        super().__init__()
        self.op = op  # AND, OR, ==, !=, >, <, >=, <=
        self.izq = izq
        self.der = der


class UnOp(Condicion):
    def __init__(self, op, expr):
        super().__init__()
        self.op = op  # NOT
        self.expr = expr


class Literal(Condicion):
    def __init__(self, valor, tipo):
        super().__init__()
        self.valor = valor
        self.tipo = tipo  # NUM, BOOL


class Identificador(Condicion):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre


class ListaAcciones(NodoAST):
    def __init__(self, acciones):
        super().__init__()
        self.acciones = acciones


class Accion(NodoAST):
    """Nodo base para acciones."""
    pass


class Asignacion(Accion):
    def __init__(self, variable, valor):
        super().__init__()
        self.variable = variable
        self.valor = valor


class LlamadaAccion(Accion):
    def __init__(self, nombre, argumento=None):
        super().__init__()
        self.nombre = nombre
        self.argumento = argumento
