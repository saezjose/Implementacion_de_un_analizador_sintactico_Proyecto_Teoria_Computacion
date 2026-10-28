import unittest
from src.lexer.lexer import analizador_lexico, LexerError
from src.parser.parser_ll1 import ParserLL1, ParserError


class TestCasosInforme(unittest.TestCase):
    def test_v1(self):
        entrada = "WHEN temperatura > 28 AND humedad < 40 THEN encender ventilador;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v2(self):
        entrada = "WHEN luz == 0 OR movimiento == TRUE THEN encender luces, alarma = 1 ELSE apagar luces;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v3(self):
        entrada = "WHEN NOT puerta_abierta THEN activar_alarma;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v4(self):
        entrada = "WHEN nivel_agua >= 80 THEN bomba = 1, notificar_app;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v5(self):
        entrada = "WHEN presion < 10 AND NOT emergencia THEN abrir_valvula;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v6(self):
        entrada = "WHEN humedad <= 30 THEN encender riego = 100;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v7(self):
        entrada = "WHEN movimiento == TRUE THEN activar alarma; WHEN luz < 5 THEN encender luces;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v8(self):
        entrada = "WHEN a == 1 OR b == 2 AND c != 3 THEN x = 1 ELSE x = 0;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v9(self):
        entrada = "WHEN NOT NOT NOT x THEN a;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_v10(self):
        entrada = "WHEN bateria < 20 THEN volver_base, aterrizar, notificar operador;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_i1(self):
        entrada = "WHEN temperatura > THEN encender ventilador;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba un factor", msg)
        self.assertIn("'THEN'", msg)

    def test_i2(self):
        entrada = "temperatura > 28 THEN encender luces;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba la palabra reservada WHEN o el fin de la entrada", msg)
        self.assertIn("'temperatura'", msg)

    def test_i3(self):
        entrada = "WHEN temperatura > 28 encender luces;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba THEN", msg)

    def test_i4(self):
        entrada = "WHEN AND humedad < 40 THEN encender ventilador;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba un factor", msg)
        self.assertIn("'AND'", msg)

    def test_i5(self):
        entrada = "WHEN temperatura > 28 THEN ;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba", msg)

    def test_i6(self):
        entrada = "WHEN temperatura > 28 THEN accion1,, accion2;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba una acción", msg)

    def test_i7(self):
        entrada = "WHEN temperatura > 28 THEN encender ventilador"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba ';' al final de la regla", msg)
        self.assertIn("fin de la entrada", msg)

    def test_i8(self):
        entrada = "WHEN temperatura > 28 > 30 THEN encender ventilador;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba THEN", msg)

    def test_i9(self):
        entrada = "WHEN luz == 0 THEN encender luces ELSE ;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertTrue("se esperaba" in msg)

    def test_i10(self):
        entrada = "WHEN luz == 0 THEN encender luces, ;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertTrue("se esperaba" in msg)

    def test_l1(self):
        entrada = ""
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.reglas), 0)

    def test_l2(self):
        entrada = "WHEN x THEN a;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_l3(self):
        entrada = "WHEN NOT NOT NOT x THEN a;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast = parser.parse()
        self.assertIsNotNone(ast)

    def test_l4(self):
        entrada = "WHEN x THEN a; WHEN"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse()
        msg = str(ctx.exception)
        self.assertIn("se esperaba un factor", msg)

    def test_l5(self):
        entrada = "WHEN x # 3 THEN a;"
        with self.assertRaises(LexerError) as ctx:
            analizador_lexico(entrada)
        msg = str(ctx.exception)
        self.assertIn("símbolo no reconocido", msg)
        self.assertIn("#", msg)


if __name__ == '__main__':
    unittest.main()
