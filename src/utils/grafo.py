"""
Utilidades para visualización del AST
"""


def mostrar_ast_simple(nodo, nivel=0):
    """Muestra el AST de forma simple y legible."""
    prefijo = "    " * nivel
    rama = "+-- " if nivel >= 0 else ""
    
    if nodo is None:
        print(f"{prefijo}{rama}None")
        return
    
    tipo = nodo.__class__.__name__
    
    if tipo == 'Programa':
        print(f"{prefijo}{rama}Programa")
        for regla in nodo.reglas:
            mostrar_ast_simple(regla, nivel + 1)
    
    elif tipo == 'Regla':
        print(f"{prefijo}{rama}Regla")
        print(f"{prefijo}    +-- Condicion:")
        mostrar_ast_simple(nodo.condicion, nivel + 2)
        print(f"{prefijo}    +-- AccionesTHEN:")
        mostrar_ast_simple(nodo.acciones_then, nivel + 2)
        if nodo.acciones_else:
            print(f"{prefijo}    +-- AccionesELSE:")
            mostrar_ast_simple(nodo.acciones_else, nivel + 2)
        else:
            print(f"{prefijo}    +-- AccionesELSE: None")
    
    elif tipo == 'BinOp':
        print(f"{prefijo}{rama}BinOp({nodo.op})")
        mostrar_ast_simple(nodo.izq, nivel + 1)
        mostrar_ast_simple(nodo.der, nivel + 1)
    
    elif tipo == 'UnOp':
        print(f"{prefijo}{rama}UnOp({nodo.op})")
        mostrar_ast_simple(nodo.expr, nivel + 1)
    
    elif tipo == 'Literal':
        print(f"{prefijo}{rama}Literal({nodo.tipo}={nodo.valor})")
    
    elif tipo == 'Identificador':
        print(f"{prefijo}{rama}Identificador({nodo.nombre})")
    
    elif tipo == 'ListaAcciones':
        print(f"{prefijo}{rama}ListaAcciones")
        for accion in nodo.acciones:
            mostrar_ast_simple(accion, nivel + 1)
    
    elif tipo == 'Asignacion':
        print(f"{prefijo}{rama}Asignacion")
        print(f"{prefijo}    +-- variable: {nodo.variable}")
        print(f"{prefijo}    +-- valor:")
        mostrar_ast_simple(nodo.valor, nivel + 2)
    
    elif tipo == 'LlamadaAccion':
        print(f"{prefijo}{rama}LlamadaAccion({nodo.nombre})")
        if nodo.argumento:
            print(f"{prefijo}    +-- argumento:")
            mostrar_ast_simple(nodo.argumento, nivel + 2)
        else:
            print(f"{prefijo}    +-- argumento: None")
    
    else:
        print(f"{prefijo}{rama}{tipo}")
        for k, v in nodo.__dict__.items():
            print(f"{prefijo}    {k}: {v}")
