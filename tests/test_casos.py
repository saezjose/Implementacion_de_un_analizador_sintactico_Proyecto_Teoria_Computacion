import unittest
from src.lexer.lexer import analizador_lexico, LexerError
from src.parser.parser_ll1 import ParserLL1, ParserError
from tests.casos import CASOS


class TestCasos(unittest.TestCase):
    def test_todos_los_casos(self):
        for caso in CASOS:
            with self.subTest(id=caso["id"], descripcion=caso["descripcion"]):
                entrada = caso["entrada"]
                esperado = caso["esperado"]
                try:
                    tokens = analizador_lexico(entrada)
                    parser = ParserLL1(tokens)
                    ast = parser.parse(modo_panic=False)
                    obtenido = "ACEPTA"
                except LexerError:
                    obtenido = "RECHAZA"
                except ParserError:
                    obtenido = "RECHAZA"
                except Exception:
                    obtenido = "RECHAZA"
                self.assertEqual(obtenido, esperado, 
                    f"Caso {caso['id']}: {caso['descripcion']} - Esperado {esperado}, Obtenido {obtenido}. Entrada: {repr(entrada)}")


if __name__ == '__main__':
    unittest.main()
