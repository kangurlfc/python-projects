import unittest
from command_line_calculator import add, div, xlog, multi, nroot, power, sub


class MyTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(10, 5), 15)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(10, 5, 5), 20)
        self.assertEqual(add(1.4, 2.6), 4)
        self.assertEqual(add(1.1, 1.8), 2.9)
        self.assertEqual(add(1.1, 1.8, 0.002), 2.902)

    def test_div(self):
        self.assertEqual(div(10, 5), 2)
        self.assertEqual(div(2, 2, 2), 0.5)
        self.assertEqual(div(6, 3, 2), 1)
        self.assertEqual(div(10, -5), -2)
        self.assertEqual(div(0, 1), 0)

        with self.assertRaises(ZeroDivisionError):
            div(1, 0)

    def test_multi(self):
        self.assertEqual(multi(10, 5), 50)
        self.assertEqual(multi(-1, 1), -1)
        self.assertEqual(multi(10, 5, 5), 250)
        self.assertEqual(multi(1.4, 2.6), 3.64)
        self.assertEqual(multi(1.1, 1.8, 0.002), 0.00396)

    def test_xlog(self):
        self.assertEqual(xlog(16, 2), 4)
        self.assertEqual(xlog(32, 2), 5)
        self.assertEqual(xlog(9, 3), 2)
        self.assertEqual(xlog(1.4, 0.2), -0.209062)

        with self.assertRaises(ValueError):
            xlog(16, 0)
            xlog(16, 1)
            xlog(0, 2)
            xlog(-16, 1)
            xlog(16, -1)
            xlog(16, 0, 2)

    def test_nroot(self):
        self.assertEqual(nroot(16, 2), 4)
        self.assertEqual(nroot(9, 2), 3)
        self.assertEqual(nroot(8, 3), 2)
        self.assertEqual(nroot(-8, 3), -2)
        self.assertEqual(nroot(8, -3), 0.5)

        with self.assertRaises(TypeError):
            nroot(4, -2)
            nroot(-4, 2)
            nroot(4, 2, 2)

    def test_power(self):
        self.assertEqual(power(2, 2), 4)
        self.assertEqual(power(4, 2), 16)
        self.assertEqual(power(-8, 3), -512)
        self.assertEqual(power(8, -3), 0.001953)

        with self.assertRaises(TypeError):
            power(4, 2, 2)

    def test_sub(self):
        self.assertEqual(sub(10, 5), 5)
        self.assertEqual(sub(1, 2, 3), -4)
        self.assertEqual(sub(-5, 5), -10)
        self.assertEqual(sub(0, -5), 5)


if __name__ == '__main__':
    unittest.main()
