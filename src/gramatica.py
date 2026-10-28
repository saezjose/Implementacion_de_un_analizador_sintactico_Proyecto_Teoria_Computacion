"""
Gramática única fuente de verdad para SmartRule
"""

GRAMATICA = {
    'Prog': [['Regla', 'Prog'], ['ε']],
    'Regla': [['WHEN', 'Cond', 'THEN', 'ListaAcciones', 'ElsePart', 'PUNTO_COMA']],
    'ElsePart': [['ELSE', 'ListaAcciones'], ['ε']],
    'Cond': [['OrExpr']],
    'OrExpr': [['AndExpr', 'OrTail']],
    'OrTail': [['OR', 'AndExpr', 'OrTail'], ['ε']],
    'AndExpr': [['NotExpr', 'AndTail']],
    'AndTail': [['AND', 'NotExpr', 'AndTail'], ['ε']],
    'NotExpr': [['NOT', 'NotExpr'], ['RelExpr']],
    'RelExpr': [['Factor', 'RelExprTail']],
    'RelExprTail': [['OP_REL', 'Factor'], ['ε']],
    'Factor': [['NUM'], ['ID'], ['TRUE'], ['FALSE']],
    'ListaAcciones': [['Accion', 'AccionTail']],
    'AccionTail': [['COMA', 'Accion', 'AccionTail'], ['ε']],
    'Accion': [['ID', 'AccionResto']],
    'AccionResto': [['IGUAL', 'Factor'], ['ID', 'ArgResto'], ['NUM'], ['TRUE'], ['FALSE'], ['ε']],
    'ArgResto': [['IGUAL', 'Factor'], ['ε']],
}

TERMINALES = {
    'WHEN', 'THEN', 'ELSE', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE',
    'NUM', 'ID', 'OP_REL', 'IGUAL', 'COMA', 'PUNTO_COMA',
    'PARENT_IZQ', 'PARENT_DER', 'EOF', 'ε'
}

NO_TERMINALES = set(GRAMATICA.keys())
SIMBOLO_INICIAL = 'Prog'
