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


if __name__ == '__main__':
    unittest.main()
