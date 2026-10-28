"""
Utilidades para visualización del AST
"""

import os
import subprocess


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


def generar_grafo_dot(ast, output_dot=None):
    if output_dot is None:
        output_dot = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  'docs', 'ast_regla.dot')
    os.makedirs(os.path.dirname(output_dot), exist_ok=True)
    
    lines = []
    lines.append('digraph AST {')
    lines.append('  node [shape=box, style=filled, fillcolor=lightblue];')
    lines.append('  rankdir=TB;')
    
    counter = [0]
    
    def get_id():
        counter[0] += 1
        return f'n{counter[0]}'
    
    def add_node(nodo, parent_id=None):
        if nodo is None:
            return None
        node_id = get_id()
        tipo = nodo.__class__.__name__
        if tipo == 'Programa':
            lines.append(f'  {node_id} [label="Programa"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            for regla in getattr(nodo, 'reglas', []):
                add_node(regla, node_id)
            return node_id
        elif tipo == 'Regla':
            lines.append(f'  {node_id} [label="Regla"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            if hasattr(nodo, 'condicion'):
                add_node(nodo.condicion, node_id)
            if hasattr(nodo, 'acciones_then'):
                add_node(nodo.acciones_then, node_id)
            if hasattr(nodo, 'acciones_else') and nodo.acciones_else:
                add_node(nodo.acciones_else, node_id)
            return node_id
        elif tipo == 'BinOp':
            lines.append(f'  {node_id} [label="BinOp\\n{nodo.op}", fillcolor=lightyellow];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            add_node(nodo.izq, node_id)
            add_node(nodo.der, node_id)
            return node_id
        elif tipo == 'UnOp':
            lines.append(f'  {node_id} [label="UnOp\\n{nodo.op}", fillcolor=lightyellow];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            add_node(nodo.expr, node_id)
            return node_id
        elif tipo == 'Literal':
            lines.append(f'  {node_id} [label="Literal\\n{nodo.tipo}={nodo.valor}", fillcolor=lightgreen];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            return node_id
        elif tipo == 'Identificador':
            lines.append(f'  {node_id} [label="Identificador\\n{nodo.nombre}", fillcolor=lightgreen];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            return node_id
        elif tipo == 'ListaAcciones':
            lines.append(f'  {node_id} [label="ListaAcciones"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            for accion in getattr(nodo, 'acciones', []):
                add_node(accion, node_id)
            return node_id
        elif tipo == 'Asignacion':
            lines.append(f'  {node_id} [label="Asignacion"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            if hasattr(nodo, 'variable'):
                var_id = get_id()
                lines.append(f'  {var_id} [label="var: {nodo.variable}", fillcolor=lightgreen];')
                lines.append(f'  {node_id} -> {var_id};')
            if hasattr(nodo, 'valor'):
                add_node(nodo.valor, node_id)
            return node_id
        elif tipo == 'LlamadaAccion':
            lines.append(f'  {node_id} [label="LlamadaAccion\\n{nodo.nombre}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            if hasattr(nodo, 'argumento') and nodo.argumento:
                add_node(nodo.argumento, node_id)
            return node_id
        else:
            lines.append(f'  {node_id} [label="{tipo}"];')
            if parent_id:
                lines.append(f'  {parent_id} -> {node_id};')
            return node_id
    
    add_node(ast)
    lines.append('}')
    
    with open(output_dot, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # Intentar generar PNG si existe dot
    png_path = output_dot.replace('.dot', '.png')
    try:
        result = subprocess.run(['dot', '-Tpng', output_dot, '-o', png_path], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        if result.returncode == 0:
            return output_dot, png_path
        else:
            return output_dot, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return output_dot, None


if __name__ == '__main__':
    from src.lexer.lexer import analizador_lexico
    from src.parser.parser_ll1 import ParserLL1
    entrada = "WHEN a > 1 AND b < 2 THEN x;\n"
    tokens = analizador_lexico(entrada)
    parser = ParserLL1(tokens)
    ast = parser.parse(modo_panic=False)
    generar_grafo_dot(ast)
    print("Generado")
