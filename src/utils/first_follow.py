"""
Cálculo de conjuntos FIRST y FOLLOW para la gramática SmartRule
"""

from src.gramatica import GRAMATICA, TERMINALES, NO_TERMINALES, SIMBOLO_INICIAL


def calcular_first():
    first = {nt: set() for nt in NO_TERMINALES}
    
    changed = True
    while changed:
        changed = False
        for nt, producciones in GRAMATICA.items():
            for prod in producciones:
                if not prod or prod == ['ε']:
                    if 'ε' not in first[nt]:
                        first[nt].add('ε')
                        changed = True
                    continue
                
                # Procesar símbolos de la producción
                for i, sym in enumerate(prod):
                    if sym in TERMINALES:
                        if sym != 'ε' and sym not in first[nt]:
                            first[nt].add(sym)
                            changed = True
                        break
                    elif sym in NO_TERMINALES:
                        # Añadir FIRST(sym) - {ε}
                        before = len(first[nt])
                        for f in first[sym]:
                            if f != 'ε':
                                first[nt].add(f)
                        if len(first[nt]) != before:
                            changed = True
                        # Si FIRST(sym) no contiene ε, parar
                        if 'ε' not in first[sym]:
                            break
                        # Si es el último símbolo y todos contienen ε
                        if i == len(prod) - 1:
                            if 'ε' not in first[nt]:
                                first[nt].add('ε')
                                changed = True
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
    follow['Prog'].add('$')
    
    changed = True
    while changed:
        changed = False
        for nt, producciones in GRAMATICA.items():
            for prod in producciones:
                for i, sym in enumerate(prod):
                    if sym in NO_TERMINALES:
                        # Símbolos después de sym
                        rest = prod[i+1:]
                        if not rest:
                            # Añadir FOLLOW(nt) a FOLLOW(sym)
                            before = len(follow[sym])
                            follow[sym].update(follow[nt])
                            if len(follow[sym]) != before:
                                changed = True
                        else:
                            # Calcular FIRST(rest)
                            first_rest = set()
                            all_eps = True
                            for s2 in rest:
                                if s2 in TERMINALES:
                                    if s2 != 'ε':
                                        first_rest.add(s2)
                                    all_eps = (s2 == 'ε')
                                    break
                                elif s2 in NO_TERMINALES:
                                    for f in first[s2]:
                                        if f != 'ε':
                                            first_rest.add(f)
                                    if 'ε' not in first[s2]:
                                        all_eps = False
                                        break
                                else:
                                    first_rest.add(s2)
                                    all_eps = False
                                    break
                            # Añadir FIRST(rest) a FOLLOW(sym)
                            before = len(follow[sym])
                            follow[sym].update(first_rest)
                            if len(follow[sym]) != before:
                                changed = True
                            # Si todos pueden derivar ε
                            if all_eps and 'ε' in ''.join(str(x) for x in rest) if False else True:
                                # Verificar si toda la cola puede generar ε
                                cola_puede_eps = True
                                for s2 in rest:
                                    if s2 in TERMINALES and s2 != 'ε':
                                        cola_puede_eps = False
                                        break
                                    elif s2 in NO_TERMINALES and 'ε' not in first[s2]:
                                        cola_puede_eps = False
                                        break
                                    elif s2 not in TERMINALES and s2 not in NO_TERMINALES:
                                        cola_puede_eps = False
                                        break
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
        elems = sorted([e if e != 'ε' else 'epsilon' for e in first[nt]])
        print(f"FIRST({nt}) = {{ {', '.join(elems)} }}")
    
    print("\n" + "=" * 60)
    print("CONJUNTOS FOLLOW")
    print("=" * 60)
    for nt in sorted(NO_TERMINALES):
        elems = sorted([e if e != 'ε' else 'epsilon' for e in follow[nt]])
        print(f"FOLLOW({nt}) = {{ {', '.join(elems)} }}")
    
    return first, follow


def construir_tabla_ll1():
    first = calcular_first()
    follow = calcular_follow(first)
    
    tabla = {}
    conflictos = []
    
    for nt, producciones in GRAMATICA.items():
        for i, prod in enumerate(producciones):
            # Calcular FIRST de la producción
            first_prod = set()
            if not prod or prod == ['ε']:
                first_prod = {'ε'}
            else:
                all_eps = True
                for sym in prod:
                    if sym in TERMINALES:
                        if sym == 'ε':
                            continue
                        first_prod.add(sym)
                        all_eps = False
                        break
                    elif sym in NO_TERMINALES:
                        for f in first[sym]:
                            if f != 'ε':
                                first_prod.add(f)
                        if 'ε' not in first[sym]:
                            all_eps = False
                            break
                    else:
                        first_prod.add(sym)
                        all_eps = False
                        break
                if all_eps:
                    first_prod.add('ε')
            
            # Para cada terminal en FIRST(prod)
            for a in first_prod:
                if a != 'ε':
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
            if 'ε' in first_prod:
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
