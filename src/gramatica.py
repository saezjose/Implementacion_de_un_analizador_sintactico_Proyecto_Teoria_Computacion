"""
Gramática única fuente de verdad para SmartRule
"""

EPSILON = 'ε'

GRAMATICA = {
    'Prog': [['Regla', 'Prog'], [EPSILON]],
    'Regla': [['WHEN', 'Cond', 'THEN', 'ListaAcciones', 'ElsePart', 'PUNTO_COMA']],
    'ElsePart': [['ELSE', 'ListaAcciones'], [EPSILON]],
    'Cond': [['OrExpr']],
    'OrExpr': [['AndExpr', 'OrTail']],
    'OrTail': [['OR', 'AndExpr', 'OrTail'], [EPSILON]],
    'AndExpr': [['NotExpr', 'AndTail']],
    'AndTail': [['AND', 'NotExpr', 'AndTail'], [EPSILON]],
    'NotExpr': [['NOT', 'NotExpr'], ['RelExpr']],
    'RelExpr': [['Factor', 'RelExprTail']],
    'RelExprTail': [['OP_REL', 'Factor'], [EPSILON]],
    'Factor': [['NUM'], ['ID'], ['TRUE'], ['FALSE']],
    'ListaAcciones': [['Accion', 'AccionTail']],
    'AccionTail': [['COMA', 'Accion', 'AccionTail'], [EPSILON]],
    'Accion': [['ID', 'AccionResto']],
    'AccionResto': [['IGUAL', 'Factor'], ['ID', 'ArgResto'], ['NUM'], ['TRUE'], ['FALSE'], [EPSILON]],
    'ArgResto': [['IGUAL', 'Factor'], [EPSILON]],
}

TERMINALES = {
    'WHEN', 'THEN', 'ELSE', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE',
    'NUM', 'ID', 'OP_REL', 'IGUAL', 'COMA', 'PUNTO_COMA',
    'EOF'
}

NO_TERMINALES = set(GRAMATICA.keys())
SIMBOLO_INICIAL = 'Prog'
