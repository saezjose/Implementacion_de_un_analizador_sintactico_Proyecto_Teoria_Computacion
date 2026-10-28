"""
Verificación de la gramática LL(1) para SmartRule
"""

import sys
from src.gramatica import GRAMATICA, TERMINALES, NO_TERMINALES, SIMBOLO_INICIAL, EPSILON


def _resolver(gramatica, terminales, no_terminales):
    """Usa la gramática de SmartRule por defecto; permite pasar otra (p. ej. de prueba)."""
    if gramatica is None:
        gramatica = GRAMATICA
    if terminales is None:
        terminales = TERMINALES
    if no_terminales is None:
        no_terminales = set(gramatica.keys()) if gramatica is not GRAMATICA else NO_TERMINALES
    return gramatica, terminales, no_terminales


def _first_de_cadena(cadena, first, terminales, no_terminales):
    """FIRST de una secuencia de símbolos. Devuelve (conjunto sin ε, puede_derivar_ε)."""
    resultado = set()
    for sym in cadena:
        if sym == EPSILON:
            continue
        if sym in no_terminales:
            resultado.update(f for f in first[sym] if f != EPSILON)
            if EPSILON not in first[sym]:
                return resultado, False
        else:  # terminal (o símbolo desconocido tratado como terminal)
            resultado.add(sym)
            return resultado, False
    return resultado, True


def calcular_first(gramatica=None, terminales=None, no_terminales=None):
    gramatica, terminales, no_terminales = _resolver(gramatica, terminales, no_terminales)
    first = {nt: set() for nt in no_terminales}

    changed = True
    while changed:
        changed = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                f, deriva_eps = _first_de_cadena(prod, first, terminales, no_terminales)
                if deriva_eps:
                    f = f | {EPSILON}
                antes = len(first[nt])
                first[nt].update(f)
                if len(first[nt]) != antes:
                    changed = True
    return first


def calcular_follow(first=None, gramatica=None, terminales=None, no_terminales=None, simbolo_inicial=None):
    gramatica, terminales, no_terminales = _resolver(gramatica, terminales, no_terminales)
    if first is None:
        first = calcular_first(gramatica, terminales, no_terminales)
    if simbolo_inicial is None:
        simbolo_inicial = SIMBOLO_INICIAL if SIMBOLO_INICIAL in gramatica else next(iter(gramatica))

    follow = {nt: set() for nt in no_terminales}
    follow[simbolo_inicial].add('$')

    changed = True
    while changed:
        changed = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                for i, sym in enumerate(prod):
                    if sym not in no_terminales:
                        continue
                    first_rest, resto_eps = _first_de_cadena(prod[i + 1:], first, terminales, no_terminales)
                    antes = len(follow[sym])
                    follow[sym].update(first_rest)
                    if resto_eps:
                        follow[sym].update(follow[nt])
                    if len(follow[sym]) != antes:
                        changed = True
    return follow


def construir_tabla_ll1(gramatica=None, terminales=None, no_terminales=None):
    gramatica, terminales, no_terminales = _resolver(gramatica, terminales, no_terminales)

    # FIRST y FOLLOW se calculan sobre la gramática recibida (no sobre la global)
    first = calcular_first(gramatica, terminales, no_terminales)
    follow = calcular_follow(first, gramatica, terminales, no_terminales)

    tabla = {}
    conflictos = []

    for nt, producciones in gramatica.items():
        for prod in producciones:
            first_prod, deriva_eps = _first_de_cadena(prod, first, terminales, no_terminales)

            seleccion = set(first_prod)
            if deriva_eps:
                seleccion |= follow[nt]

            for a in seleccion:
                key = (nt, a)
                if key in tabla and tabla[key] != prod:
                    conflictos.append({
                        'tipo': 'FIRST/FIRST' if a in first_prod else 'FIRST/FOLLOW',
                        'nt': nt,
                        'terminal': a,
                        'prod1': tabla[key],
                        'prod2': prod
                    })
                tabla[key] = prod

    return tabla, first, follow, conflictos


def mostrar_first_follow():
    first = calcular_first()
    follow = calcular_follow(first)
    
    print("=" * 70)
    print("GRAMATICA SMARTRULE - PRODUCCIONES NUMERADAS")
    print("=" * 70)
    idx = 1
    for nt in ['Prog', 'Regla', 'ElsePart', 'Cond', 'OrExpr', 'OrTail', 'AndExpr', 'AndTail', 
              'NotExpr', 'RelExpr', 'RelExprTail', 'Factor', 'ListaAcciones', 'AccionTail', 
              'Accion', 'AsigOrCall', 'AsigTail']:
        if nt in GRAMATICA:
            for prod in GRAMATICA[nt]:
                if prod == [EPSILON]:
                    print(f"{idx:2d}. {nt} ::= epsilon")
                else:
                    print(f"{idx:2d}. {nt} ::= {' '.join(prod)}")
                idx += 1
    print(f"\nTotal producciones: {idx-1}")
    
    print("\n" + "=" * 70)
    print("CONJUNTOS FIRST")
    print("=" * 70)
    for nt in ['Prog', 'Regla', 'ElsePart', 'Cond', 'OrExpr', 'OrTail', 'AndExpr', 'AndTail',
              'NotExpr', 'RelExpr', 'RelExprTail', 'Factor', 'ListaAcciones', 'AccionTail',
              'Accion', 'AsigOrCall', 'AsigTail']:
        if nt in NO_TERMINALES:
            elems = sorted([e if e != EPSILON else 'epsilon' for e in first[nt]])
            print(f"FIRST({nt}) = {{ {', '.join(elems)} }}")
    
    print("\n" + "=" * 70)
    print("CONJUNTOS FOLLOW")
    print("=" * 70)
    for nt in ['Prog', 'Regla', 'ElsePart', 'Cond', 'OrExpr', 'OrTail', 'AndExpr', 'AndTail',
              'NotExpr', 'RelExpr', 'RelExprTail', 'Factor', 'ListaAcciones', 'AccionTail',
              'Accion', 'AsigOrCall', 'AsigTail']:
        if nt in NO_TERMINALES:
            elems = []
            for e in sorted(follow[nt]):
                if e == '$':
                    elems.append('$')
                else:
                    elems.append(e)
            print(f"FOLLOW({nt}) = {{ {', '.join(elems)} }}")
    
    print("\n" + "=" * 70)
    print("TABLA LL(1)")
    print("=" * 70)
    tabla, first_res, follow_res, conflictos = construir_tabla_ll1()
    print(f"Entradas en tabla LL(1): {len(tabla)}")
    print(f"Conflictos detectados: {len(conflictos)}")
    if conflictos:
        for c in conflictos:
            print(f"  - {c['tipo']} en M[{c['nt']}, {c['terminal']}]: {c['prod1']} vs {c['prod2']}")
        print("\nLa gramática NO es LL(1).")
        sys.exit(1)
    else:
        print("\nNinguno: la gramática es LL(1).")
    
    return first, follow


if __name__ == '__main__':
    mostrar_first_follow()
    sys.exit(0)
