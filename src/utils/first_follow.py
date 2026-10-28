"""
Verificación de la gramática LL(1) para SmartRule
"""

import sys
from src.gramatica import GRAMATICA, TERMINALES, NO_TERMINALES, SIMBOLO_INICIAL, EPSILON


def es_terminal(sym):
    return sym in TERMINALES


def es_no_terminal(sym):
    return sym in NO_TERMINALES


def es_epsilon(sym):
    return sym == EPSILON


def calcular_first():
    first = {nt: set() for nt in NO_TERMINALES}
    
    changed = True
    while changed:
        changed = False
        for nt, producciones in GRAMATICA.items():
            for prod in producciones:
                if not prod or prod == [EPSILON]:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        changed = True
                    continue
                
                all_eps = True
                for sym in prod:
                    if sym == EPSILON:
                        continue
                    if es_terminal(sym):
                        if sym not in first[nt]:
                            first[nt].add(sym)
                            changed = True
                        all_eps = False
                        break
                    elif es_no_terminal(sym):
                        before = len(first[nt])
                        for f in first[sym]:
                            if f != EPSILON:
                                first[nt].add(f)
                        if len(first[nt]) != before:
                            changed = True
                        if EPSILON not in first[sym]:
                            all_eps = False
                            break
                    else:
                        if sym not in first[nt]:
                            first[nt].add(sym)
                            changed = True
                        all_eps = False
                        break
                if all_eps:
                    if EPSILON not in first[nt]:
                        first[nt].add(EPSILON)
                        changed = True
    return first


def calcular_follow(first=None):
    if first is None:
        first = calcular_first()
    
    follow = {nt: set() for nt in NO_TERMINALES}
    follow[SIMBOLO_INICIAL].add('$')
    
    changed = True
    while changed:
        changed = False
        for nt, producciones in GRAMATICA.items():
            for prod in producciones:
                for i, sym in enumerate(prod):
                    if es_no_terminal(sym):
                        rest = prod[i+1:]
                        if not rest:
                            before = len(follow[sym])
                            follow[sym].update(follow[nt])
                            if len(follow[sym]) != before:
                                changed = True
                        else:
                            cola_puede_eps = True
                            first_rest = set()
                            for s2 in rest:
                                if s2 == EPSILON:
                                    continue
                                if es_terminal(s2):
                                    first_rest.add(s2)
                                    cola_puede_eps = False
                                    break
                                elif es_no_terminal(s2):
                                    for f in first[s2]:
                                        if f != EPSILON:
                                            first_rest.add(f)
                                    if EPSILON not in first[s2]:
                                        cola_puede_eps = False
                                        break
                                else:
                                    first_rest.add(s2)
                                    cola_puede_eps = False
                                    break
                            before = len(follow[sym])
                            follow[sym].update(first_rest)
                            if len(follow[sym]) != before:
                                changed = True
                            if cola_puede_eps:
                                before = len(follow[sym])
                                follow[sym].update(follow[nt])
                                if len(follow[sym]) != before:
                                    changed = True
    return follow


def construir_tabla_ll1(gramatica=None, terminales=None, no_terminales=None):
    if gramatica is None:
        gramatica = GRAMATICA
    if terminales is None:
        terminales = TERMINALES
    if no_terminales is None:
        no_terminales = NO_TERMINALES
    
    first = calcular_first()
    follow = calcular_follow(first)
    
    tabla = {}
    conflictos = []
    
    for nt, producciones in gramatica.items():
        for i, prod in enumerate(producciones):
            first_prod = set()
            if not prod or prod == [EPSILON]:
                first_prod = {EPSILON}
            else:
                all_eps = True
                for sym in prod:
                    if sym == EPSILON:
                        continue
                    if sym in terminales:
                        first_prod.add(sym)
                        all_eps = False
                        break
                    elif sym in no_terminales:
                        for f in first[sym]:
                            if f != EPSILON:
                                first_prod.add(f)
                        if EPSILON not in first[sym]:
                            all_eps = False
                            break
                    else:
                        first_prod.add(sym)
                        all_eps = False
                        break
                if all_eps:
                    first_prod.add(EPSILON)
            
            for a in first_prod:
                if a != EPSILON:
                    key = (nt, a)
                    if key in tabla:
                        conflictos.append({
                            'tipo': 'FIRST/FIRST',
                            'nt': nt,
                            'terminal': a,
                            'prod1': tabla[key],
                            'prod2': prod
                        })
                    tabla[key] = prod
            
            if EPSILON in first_prod:
                for b in follow[nt]:
                    key = (nt, b)
                    if key in tabla:
                        conflictos.append({
                            'tipo': 'FIRST/FOLLOW',
                            'nt': nt,
                            'terminal': b,
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
