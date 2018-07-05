from unittest import TestCase, TestSuite, TestLoader, TextTestRunner

import Exceptions as ex
import Fx_booleanos as fb
import Fx_conjunto_datos as fc
import Fx_valor_numerico as fv
import RQL_dic
import basicos_y_otros as bo
import interprete as i
import numpy as np


class TestConjuntosDatos(TestCase):
    def test_filtrar(self):
        self.assertEquals(fc.filtrar([x for x in range(1, 20)], '<', 10), [n for n in range(1, 10)])

    def test_evaluar(self):
        # Para este test, vamos a testearlo dos veces, una con valores que ya conozco el resultado por el ejemplo que nos dieron, y otra vez con una funcion inventada por mi.
        valor = round(i.interprete(['VAR', ['evaluar', ['crear_funcion', 'normal', 0, 0.5], -3, 5, 0.1]]), 3)
        self.assertEquals(valor, 0.055)

    def test_evaluar1(self):
        def funcion(x):
            f = 2 * x
            return f

        self.assertEquals(fc.evaluar(funcion, 1, 5, 1), [2, 4, 6, 8, 10])


class TestComandosBasicos(TestCase):
    def test_asignar(self):
        bo.asignar('x', 'probando')
        self.assertEquals(RQL_dic.diccionario['x'], 'probando')


class TestBooleanos(TestCase):
    def test_comparar_columna(self):
        self.assertTrue(fb.comparar_columna([x for x in range(1, 100)], '>', 'PROM', [x for x in range(1, 50)]))

    def test_comparar(self):
        self.assertEquals(fb.comparar(1, '>', 2), False)


class TestDCompuestos(TestCase):
    def test_do_if(self):
        self.assertEquals(bo.do_if('Bien', 'True', 'Malo'), 'Bien')


class TestValoresNumericos(TestCase):
    def test_PROM(self):
        self.assertEqual(fv.PROM([x for x in range(1, 100)]), np.mean([x for x in range(1, 100)]))

    def test_DESV(self):
        self.assertEqual(fv.DESV([x for x in range(1, 100)]), np.std([x for x in range(1, 100)], ddof=1))

    def test_MEDIAN(self):
        self.assertEqual(fv.MEDIAN([x for x in range(1, 100)]), np.median([x for x in range(1, 100)]))

    def test_VAR(self):
        self.assertEqual(fv.VAR([x for x in range(1, 100)]), np.var([x for x in range(1, 100)], ddof=1))


class TestErrores(TestCase):
    def test_argumento_invalido(self):
        with self.assertRaises(ex.ArgumentoInvalido) as exc:
            i.interprete(['PROM', [1, 2, 3], [10]])
            self.assertTrue('Argumento Invalido' == exc.nombre)

    def test_referencia_invalida(self):
        with self.assertRaises(ex.ReferenciaInvalida) as exc:
            i.interprete(['operar', 'x', '/', 2])
            self.assertTrue('Error Matematico' == exc.nombre)

    def test_error_de_tipo(self):
        with self.assertRaises(ex.ErrorDeTipo) as exc:
            i.interprete(['operar', [1, 2, 3, 4], '/', 'a'])
            self.assertTrue('Error de tipo' == exc.nombre)

    def test_error_matematico(self):
        with self.assertRaises(ex.ErrorMatematico) as exc:
            i.interprete(['operar', [1, 2, 3, 4, 5, 6], '/', 0])
            self.assertTrue('Error Matematico' == exc.nombre)

    def test_imposible_procesar(self):
        with self.assertRaises(ex.ImposibleProcesar) as exc:
            i.interprete(['graficar', [m for m in range(1, 20)], [m for m in range(1, 19)]])
            self.assertTrue('Imposible procesar' == exc.nombre)


Tsuite = TestSuite()

Tsuite.addTest(TestLoader().loadTestsFromTestCase(TestBooleanos))
Tsuite.addTest(TestLoader().loadTestsFromTestCase(TestConjuntosDatos))
Tsuite.addTest(TestLoader().loadTestsFromTestCase(TestComandosBasicos))
Tsuite.addTest(TestLoader().loadTestsFromTestCase(TestValoresNumericos))
Tsuite.addTest(TestLoader().loadTestsFromTestCase(TestDCompuestos))
Tsuite.addTest(TestLoader().loadTestsFromTestCase(TestErrores))

TextTestRunner().run(Tsuite)
