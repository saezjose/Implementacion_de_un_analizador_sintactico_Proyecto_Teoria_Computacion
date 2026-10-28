"""
Exporta tablas FIRST, FOLLOW y LL(1) a LaTeX
"""

import os
from src.utils.first_follow import calcular_first, calcular_follow, construir_tabla_ll1
from src.gramatica import GRAMATICA, EPSILON, TERMINALES


def terminal_a_latex(t):
    if t == '$':
        return r'\$'
    if t == 'PUNTO_COMA':
        return r';'
    if t == 'OP_REL':
        return r'OP\_REL'
    if t == 'IGUAL':
        return r'='
    if t == 'COMA':
        return r','
    return t


def no_terminal_a_latex(nt):
    return nt


def prod_a_latex(prod):
    if not prod or prod == [EPSILON]:
        return r'$\epsilon$'
    parts = []
    for s in prod:
        if s == EPSILON:
            continue
        if s == '$':
            parts.append(r'\$')
        elif s == 'PUNTO_COMA':
            parts.append(r';')
        elif s == 'OP_REL':
            parts.append(r'OP\_REL')
        elif s == 'IGUAL':
            parts.append(r'=')
        elif s == 'COMA':
            parts.append(r',')
        else:
            parts.append(s)
    return ' '.join(parts)


def exportar_tablas(outdir=None):
    if outdir is None:
        outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs', 'informe_latex')
    os.makedirs(outdir, exist_ok=True)
    
    first = calcular_first()
    follow = calcular_follow(first)
    tabla, first2, follow2, conflictos = construir_tabla_ll1()
    
    # tabla_first.tex
    with open(os.path.join(outdir, 'tabla_first.tex'), 'w', encoding='utf-8') as f:
        f.write(r'\begin{table}[H]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\begin{tabular}{|l|l|}' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\textbf{No Terminal} & \textbf{FIRST} \\ ' + '\n')
        f.write(r'\hline' + '\n')
        for nt in sorted(GRAMATICA.keys()):
            elems = []
            for e in sorted(first[nt]):
                if e == EPSILON:
                    elems.append(r'$\epsilon$')
                elif e == '$':
                    elems.append(r'\$')
                elif e == 'OP_REL':
                    elems.append(r'OP\_REL')
                else:
                    elems.append(e)
            f.write(f'\\texttt{{{nt}}} & {{ {", ".join(elems)} }} \\\\ \n')
            f.write(r'\hline' + '\n')
        f.write(r'\end{tabular}' + '\n')
        f.write(r'\caption{Conjuntos FIRST}' + '\n')
        f.write(r'\label{tab:first}' + '\n')
        f.write(r'\end{table}' + '\n')
    
    # tabla_follow.tex
    with open(os.path.join(outdir, 'tabla_follow.tex'), 'w', encoding='utf-8') as f:
        f.write(r'\begin{table}[H]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\begin{tabular}{|l|l|}' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\textbf{No Terminal} & \textbf{FOLLOW} \\ ' + '\n')
        f.write(r'\hline' + '\n')
        for nt in sorted(GRAMATICA.keys()):
            elems = []
            for e in sorted(follow[nt]):
                if e == EPSILON:
                    elems.append(r'$\epsilon$')
                elif e == '$':
                    elems.append(r'\$')
                elif e == 'OP_REL':
                    elems.append(r'OP\_REL')
                else:
                    elems.append(e)
            f.write(f'\\texttt{{{nt}}} & {{ {", ".join(elems)} }} \\\\ \n')
            f.write(r'\hline' + '\n')
        f.write(r'\end{tabular}' + '\n')
        f.write(r'\caption{Conjuntos FOLLOW}' + '\n')
        f.write(r'\label{tab:follow}' + '\n')
        f.write(r'\end{table}' + '\n')
    
    # tabla_ll1.tex
    terminales_list = sorted([t for t in TERMINALES if t != 'EOF'])
    no_terminales_list = sorted(GRAMATICA.keys())
    
    with open(os.path.join(outdir, 'tabla_ll1.tex'), 'w', encoding='utf-8') as f:
        f.write(r'\begin{landscape}' + '\n')
        f.write(r'\begin{longtable}{|l|' + '|'.join(['l'] * len(terminales_list)) + '|}' + '\n')
        f.write(r'\hline' + '\n')
        header = r'\textbf{}'
        for t in terminales_list:
            header += ' & \\textbf{' + terminal_a_latex(t) + '}'
        header += r' \\ ' + '\n'
        f.write(header)
        f.write(r'\hline' + '\n')
        f.write(r'\endfirsthead' + '\n')
        f.write(r'\hline' + '\n')
        f.write(header)
        f.write(r'\hline' + '\n')
        f.write(r'\endhead' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\endfoot' + '\n')
        for nt in no_terminales_list:
            row = f'\\texttt{{{nt}}}'
            for t in terminales_list:
                key = (nt, t)
                if key in tabla:
                    row += ' & ' + prod_a_latex(tabla[key])
                else:
                    row += ' & '
            row += r' \\ ' + '\n'
            f.write(row)
            f.write(r'\hline' + '\n')
        f.write(r'\end{longtable}' + '\n')
        f.write(r'\caption{Tabla LL(1)}' + '\n')
        f.write(r'\label{tab:ll1}' + '\n')
        f.write(r'\end{landscape}' + '\n')
    
    return {'first': outdir + '/tabla_first.tex', 'follow': outdir + '/tabla_follow.tex', 'll1': outdir + '/tabla_ll1.tex', 'conflictos': len(conflictos)}


if __name__ == '__main__':
    res = exportar_tablas()
    print(res)
