"""
Pruebas del analizador léxico
"""

import unittest
from src.lexer.lexer import analizador_lexico, LexerError


class TestLexer(unittest.TestCase):
    def test_tokens_basicos(self):
        entrada = "WHEN temperatura > 28 AND humedad < 40 THEN encender ventilador;"
        tokens = analizador_lexico(entrada)
        tipos = [t[0] for t in tokens if t[0] != 'EOF']
        self.assertIn('WHEN', tipos)
        self.assertIn('ID', tipos)
        self.assertIn('OP_REL', tipos)
        self.assertIn('NUM', tipos)
        self.assertIn('AND', tipos)
        self.assertIn('THEN', tipos)
        self.assertIn('PUNTO_COMA', tipos)
    
    def test_palabras_reservadas(self):
        entrada = "WHEN THEN ELSE AND OR NOT TRUE FALSE"
        tokens = analizador_lexico(entrada)
        tipos = [t[0] for t in tokens if t[0] != 'EOF']
        esperados = ['WHEN', 'THEN', 'ELSE', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE']
        self.assertEqual(tipos, esperados)
    
    def test_operadores_relacionales(self):
        for op in ['>=', '<=', '==', '!=', '>', '<']:
            tokens = analizador_lexico(f"x {op} 1;")
            self.assertEqual(tokens[1][0], 'OP_REL')
            self.assertEqual(tokens[1][1], op)
    
    def test_igual_coma(self):
        entrada = "x = 5, y = 10"
        tokens = analizador_lexico(entrada)
        tipos = [t[0] for t in tokens if t[0] != 'EOF']
        self.assertIn('IGUAL', tipos)
        self.assertIn('COMA', tipos)
    
    def test_error_lexico(self):
        with self.assertRaises(LexerError):
            analizador_lexico("WHEN x > 5 THEN accion@;")

    def test_parentesis_no_reconocidos(self):
        for entrada in ("WHEN (x) THEN a;", "WHEN x ) THEN a;"):
            with self.assertRaises(LexerError) as ctx:
                analizador_lexico(entrada)
            self.assertIn("símbolo no reconocido", str(ctx.exception))
        # formato exacto: línea y columna
        with self.assertRaises(LexerError) as ctx:
            analizador_lexico("WHEN (x) THEN a;")
        self.assertEqual(str(ctx.exception),
                         "Error léxico (línea 1, columna 6): símbolo no reconocido '('")

    def test_formato_error_lexico_multilinea(self):
        with self.assertRaises(LexerError) as ctx:
            analizador_lexico("WHEN x THEN a;\nWHEN y # 1 THEN b;")
        self.assertEqual(str(ctx.exception),
                         "Error léxico (línea 2, columna 8): símbolo no reconocido '#'")


if __name__ == '__main__':
    unittest.main()
