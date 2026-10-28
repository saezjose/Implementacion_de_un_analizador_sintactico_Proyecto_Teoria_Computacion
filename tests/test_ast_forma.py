import unittest
from src.lexer.lexer import analizador_lexico
from src.parser.parser_ll1 import ParserLL1
from src.ast.nodos import Programa, Regla, BinOp, UnOp, Identificador, Literal, ListaAcciones, LlamadaAccion


class TestASTForma(unittest.TestCase):
    def test_ast_forma_precedencia_not_and_or(self):
        entrada = "WHEN a > 1 AND NOT b THEN x;\n"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse(modo_panic=False)
        self.assertIsInstance(ast, Programa)
        self.assertEqual(len(ast.reglas), 1)
        regla = ast.reglas[0]
        self.assertIsInstance(regla, Regla)
        # Condición debe ser BinOp AND con NOT teniendo mayor precedencia
        self.assertIsInstance(regla.condicion, BinOp)
        self.assertEqual(regla.condicion.op, 'AND')
        # Izquierda: a > 1
        self.assertIsInstance(regla.condicion.izq, BinOp)
        self.assertEqual(regla.condicion.izq.op, '>')
        self.assertIsInstance(regla.condicion.izq.izq, Identificador)
        self.assertEqual(regla.condicion.izq.izq.nombre, 'a')
        # Derecha: NOT b (UnOp tiene mayor precedencia que AND)
        self.assertIsInstance(regla.condicion.der, UnOp)
        self.assertEqual(regla.condicion.der.op, 'NOT')
        self.assertIsInstance(regla.condicion.der.expr, Identificador)
        self.assertEqual(regla.condicion.der.expr.nombre, 'b')
        # Acciones
        self.assertIsInstance(regla.acciones_then, ListaAcciones)
        self.assertEqual(len(regla.acciones_then.acciones), 1)
        self.assertIsInstance(regla.acciones_then.acciones[0], LlamadaAccion)
        self.assertEqual(regla.acciones_then.acciones[0].nombre, 'x')


if __name__ == '__main__':
    unittest.main()
