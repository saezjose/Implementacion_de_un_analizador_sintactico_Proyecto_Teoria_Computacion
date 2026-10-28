"""
Cálculo de conjuntos FIRST y FOLLOW para la gramática SmartRule
"""

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
                
                # Procesar símbolos de la producción
                for i, sym in enumerate(prod):
                    if es_terminal(sym):
                        if not es_epsilon(sym) and sym not in first[nt]:
                            first[nt].add(sym)
                            changed = True
                        break
                    elif es_no_terminal(sym):
                        # Añadir FIRST(sym) - {ε}
                        before = len(first[nt])
                        for f in first[sym]:
                            if not es_epsilon(f):
                                first[nt].add(f)
                        if len(first[nt]) != before:
                            changed = True
                        # Si FIRST(sym) no contiene ε, parar
                        if EPSILON not in first[sym]:
                            break
                        # Si es el último símbolo y todos contienen ε
                        if i == len(prod) - 1:
                            if EPSILON not in first[nt]:
                                first[nt].add(EPSILON)
                                changed = True
                    elif es_epsilon(sym):
                        if EPSILON not in first[nt]:
                            first[nt].add(EPSILON)
                            changed = True
                        break
                    else:
                        # Símbolo desconocido
                        if sym not in first[nt]:
                            first[nt].add(sym)
                            changed = True
                        break
    return first


def calcular_follow(first=None):
    if first is None:
        first = calcular_first()
    
    follow = {nt: set() for nt in NO_TERMINALES}
    # Símbolo inicial
    follow[SIMBOLO_INICIAL].add('$')
    
    changed = True
    while changed:
        changed = False
        for nt, producciones in GRAMATICA.items():
            for prod in producciones:
                for i, sym in enumerate(prod):
                    if es_no_terminal(sym):
                        # Símbolos después de sym
                        rest = prod[i+1:]
                        if not rest:
                            # Añadir FOLLOW(nt) a FOLLOW(sym)
                            before = len(follow[sym])
                            follow[sym].update(follow[nt])
                            if len(follow[sym]) != before:
                                changed = True
                        else:
                            # Calcular si toda la cola puede derivar ε
                            cola_puede_eps = True
                            first_rest = set()
                            for s2 in rest:
                                if es_epsilon(s2):
                                    continue
                                if es_terminal(s2):
                                    first_rest.add(s2)
                                    cola_puede_eps = False
                                    break
                                elif es_no_terminal(s2):
                                    for f in first[s2]:
                                        if not es_epsilon(f):
                                            first_rest.add(f)
                                    if EPSILON not in first[s2]:
                                        cola_puede_eps = False
                                        break
                                else:
                                    first_rest.add(s2)
                                    cola_puede_eps = False
                                    break
                            # Añadir FIRST(rest) a FOLLOW(sym)
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


def mostrar_first_follow():
    first = calcular_first()
    follow = calcular_follow(first)
    
    print("=" * 60)
    print("CONJUNTOS FIRST")
    print("=" * 60)
    for nt in sorted(NO_TERMINALES):
        elems = sorted([e if e != EPSILON else 'epsilon' for e in first[nt]])
        print(f"FIRST({nt}) = {{ {', '.join(elems)} }}")
    
    print("\n" + "=" * 60)
    print("CONJUNTOS FOLLOW")
    print("=" * 60)
    for nt in sorted(NO_TERMINALES):
        elems = []
        for e in sorted(follow[nt]):
            if e == '$':
                elems.append('$')
            elif e == EPSILON:
                elems.append('epsilon')
            else:
                elems.append(e)
        print(f"FOLLOW({nt}) = {{ {', '.join(elems)} }}")
    
    return first, follow


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
            # Calcular FIRST de la producción
            first_prod = set()
            if not prod or prod == [EPSILON]:
                first_prod = {EPSILON}
            else:
                all_eps = True
                for sym in prod:
                    if sym in terminales:
                        if sym == EPSILON:
                            continue
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
                    elif sym == EPSILON:
                        continue
                    else:
                        first_prod.add(sym)
                        all_eps = False
                        break
                if all_eps:
                    first_prod.add(EPSILON)
            
            # Para cada terminal en FIRST(prod)
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
                        print(f"¡CONFLICTO LL(1)! En M[{nt}, {a}] - FIRST/FIRST: {tabla[key]} vs {prod}")
                    tabla[key] = prod
            
            # Si ε está en FIRST(prod), añadir para FOLLOW(nt)
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
                        print(f"¡CONFLICTO LL(1)! En M[{nt}, {b}] - FIRST/FOLLOW: {tabla[key]} vs {prod}")
                    tabla[key] = prod
    
    return tabla, first, follow, conflictos


if __name__ == '__main__':
    import sys
    mostrar_first_follow()
    print("\n" + "=" * 60)
    print("ANÁLISIS TABLA LL(1)")
    print("=" * 60)
    tabla, first, follow, conflictos = construir_tabla_ll1()
    print(f"Entradas en tabla LL(1): {len(tabla)}")
    if conflictos:
        print(f"¡{len(conflictos)} CONFLICTO(S) DETECTADO(S)!")
        sys.exit(1)
    else:
        print("Sin conflictos detectados.")
