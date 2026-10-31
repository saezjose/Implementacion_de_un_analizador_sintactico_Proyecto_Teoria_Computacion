import unittest
from src.utils.first_follow import calcular_first, calcular_follow, construir_tabla_ll1, GRAMATICA, TERMINALES, NO_TERMINALES


class TestGramaticaLL1(unittest.TestCase):
    def test_gramatica_real_sin_conflictos(self):
        tabla, first, follow, conflictos = construir_tabla_ll1()
        self.assertEqual(len(conflictos), 0, f"Se detectaron conflictos: {conflictos}")
        self.assertGreater(len(tabla), 0)
    
    def test_conflicto_con_gramatica_juguete(self):
        # Gramática con conflicto FIRST/FIRST conocido
        gramatica_juguete = {
            'S': [['a', 'b'], ['a', 'c']]
        }
        terminales_juguete = {'a', 'b', 'c'}
        no_terminales_juguete = {'S'}
        first = {nt: set() for nt in no_terminales_juguete}
        first['S'] = {'a'}
        follow = {nt: set() for nt in no_terminales_juguete}
        follow['S'] = {'$'}
        tabla, f, fl, conflictos = construir_tabla_ll1(gramatica_juguete, terminales_juguete, no_terminales_juguete)
        self.assertGreater(len(conflictos), 0, "Debe detectar conflicto FIRST/FIRST en gramática de juguete")
    
    def test_first_follow_accion(self):
        first = calcular_first()
        follow = calcular_follow(first)
        self.assertIn('ID', first['Accion'])
        asig = first['AsigOrCall']
        self.assertIn('IGUAL', asig)
        self.assertIn('ID', asig)
        self.assertTrue('epsilon' in asig or '\u03b5' in asig)
        self.assertIn('COMA', follow['Accion'])
        self.assertIn('ELSE', follow['Accion'])
        self.assertIn('PUNTO_COMA', follow['Accion'])
        asig_f = follow['AsigOrCall']
        self.assertIn('COMA', asig_f)
        self.assertIn('ELSE', asig_f)
        self.assertIn('PUNTO_COMA', asig_f)
    
    def test_follow_notexpr_relexpr(self):
        first = calcular_first()
        follow = calcular_follow(first)
        # NotExpr, RelExpr y RelExprTail deben incluir AND según requerimiento
        self.assertIn('AND', follow['NotExpr'])
        self.assertIn('AND', follow['RelExpr'])
        self.assertIn('AND', follow['RelExprTail'])


if __name__ == '__main__':
    unittest.main()
