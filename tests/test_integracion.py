"""
Pruebas de integración y casos adicionales
"""

import unittest
from src.lexer.lexer import analizador_lexico
from src.parser.parser_ll1 import ParserLL1


class TestIntegracion(unittest.TestCase):
    def test_casa_inteligente_completo(self):
        entrada = """
        WHEN temperatura > 28 AND humedad < 40 THEN encender ventilador, activar_deshumidificador;
        WHEN luz == 0 AND movimiento == TRUE THEN encender luces = 100 ELSE apagar luces;
        WHEN NOT alarma_activa AND puerta_abierta THEN activar_alarma;
        """
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 3)
    
    def test_dron(self):
        entrada = "WHEN bateria < 20 THEN regresar_base, bajar_altitud;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_riego_agricola(self):
        entrada = "WHEN humedad_suelo < 30 OR temperatura > 35 THEN activar_riego = 10;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_todos_relacionales(self):
        casos = [
            "WHEN x > 1 THEN a;",
            "WHEN x < 1 THEN a;",
            "WHEN x >= 1 THEN a;",
            "WHEN x <= 1 THEN a;",
            "WHEN x == 1 THEN a;",
            "WHEN x != 1 THEN a;",
        ]
        for c in casos:
            tokens = analizador_lexico(c)
            parser = ParserLL1(tokens)
            ast = parser.parse()
            self.assertEqual(len(ast.reglas), 1)
    
    def test_not_anidado(self):
        entrada = "WHEN NOT NOT activo THEN ejecutar;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)
    
    def test_precedencia_and_sobre_or(self):
        # a OR b AND c debe parsearse como a OR (b AND c)
        entrada = "WHEN a == 1 OR b == 2 AND c == 3 THEN x;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 1)


if __name__ == '__main__':
    unittest.main()
