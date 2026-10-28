import unittest
from src.lexer.lexer import analizador_lexico
from src.parser.parser_ll1 import ParserLL1, ParserError


class TestErroresTarea4(unittest.TestCase):
    def test_multiples_errores_panic_mode(self):
        entrada = "WHEN temperatura > THEN encender ventilador;\ntemperatura > 28 THEN encender luces;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast, errores = parser.parse(modo_panic=True)
        self.assertGreaterEqual(len(errores), 2)
    
    def test_errores_multilinea_linea_columna(self):
        entrada = "WHEN a > THEN b;\nWHEN c > 1 THEN ;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        ast, errores = parser.parse(modo_panic=True)
        self.assertEqual(len(errores), 2)
        # Verificar que tienen línea y columna
        self.assertTrue(hasattr(errores[0].token, 'linea'))
        self.assertTrue(hasattr(errores[0].token, 'columna'))
        self.assertEqual(errores[0].token.linea, 1)
        self.assertEqual(errores[1].token.linea, 2)
    
    def test_mensaje_op_rel(self):
        entrada = "WHEN x > THEN y;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse(modo_panic=False)
        self.assertIn("se esperaba un valor", str(ctx.exception))
        self.assertIn("operador", str(ctx.exception))
    
    def test_mensaje_falta_then(self):
        entrada = "WHEN x > 1 encender;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse(modo_panic=False)
        self.assertIn("THEN", str(ctx.exception))
    
    def test_mensaje_falta_punto_coma(self):
        entrada = "WHEN x > 1 THEN encender"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse(modo_panic=False)
        self.assertIn(";", str(ctx.exception))
    
    def test_mensaje_coma_sobrante(self):
        entrada = "WHEN x > 1 THEN a,, b;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse(modo_panic=False)
        self.assertIn("después de ','", str(ctx.exception))
    
    def test_mensaje_lista_vacia(self):
        entrada = "WHEN x > 1 THEN ;"
        tokens = analizador_lexico(entrada)
        parser = ParserLL1(tokens)
        with self.assertRaises(ParserError) as ctx:
            parser.parse(modo_panic=False)
        self.assertIn("al menos una acción", str(ctx.exception))


if __name__ == '__main__':
    unittest.main()
