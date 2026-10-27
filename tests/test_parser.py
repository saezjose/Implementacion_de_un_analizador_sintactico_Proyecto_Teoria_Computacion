"""
Pruebas del analizador sintáctico LL(1)
"""

import unittest
from src.lexer.lexer import analizador_lexico
from src.parser.parser_ll1 import ParserLL1, ParserError


class TestParser(unittest.TestCase):
    def test_regla_simple(self):
        entrada = "WHEN temperatura > 28 THEN encender ventilador;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_regla_con_and_or(self):
        entrada = "WHEN a > 1 AND b < 2 OR c == 3 THEN x;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_regla_con_not(self):
        entrada = "WHEN NOT puerta THEN cerrar;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_regla_con_else(self):
        entrada = "WHEN x > 0 THEN encender ELSE apagar;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast.reglas[0].acciones_else)
    
    def test_multiples_acciones(self):
        entrada = "WHEN x == 1 THEN a = 1, b = 2, encender;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas[0].acciones_then.acciones), 3)
    
    def test_asignacion(self):
        entrada = "WHEN x > 0 THEN y = 5;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_accion_sin_argumento(self):
        entrada = "WHEN x > 0 THEN reset;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_multiples_reglas(self):
        entrada = "WHEN a > 1 THEN x; WHEN b < 2 THEN y;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 2)
    
    def test_condicion_sin_relacional(self):
        entrada = "WHEN activo THEN encender;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_true_false(self):
        entrada = "WHEN sistema == TRUE THEN iniciar;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    # Errores sintácticos
    def test_error_falta_then(self):
        entrada = "WHEN x > 1 encender;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError):
            parser.parse()
    
    def test_error_falta_condicion(self):
        entrada = "WHEN THEN encender;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError):
            parser.parse()
    
    def test_error_falta_punto_coma(self):
        entrada = "WHEN x > 1 THEN encender"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError):
            parser.parse()
    
    def test_error_falta_when(self):
        entrada = "x > 1 THEN encender;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError):
            parser.parse()
    
    def test_error_coma_extra(self):
        entrada = "WHEN x > 1 THEN a,, b;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError):
            parser.parse()


if __name__ == '__main__':
    unittest.main()
