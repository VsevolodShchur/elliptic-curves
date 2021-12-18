from point import Point
from polynomial import Polynomial
from elliptic_curve_zp import EllipticCurveZp
from elliptic_curve_gf_ns import EllipticCurveGF2NS
import unittest

class TestZpCurves(unittest.TestCase):
    def test_simple_addition(self):
        curve = EllipticCurveZp(-1, 3, 19)
        self.assertEqual(curve.add(Point(2, 3), Point(2, 3)), Point(2, 16))
        self.assertEqual(curve.add(Point(4, 5), Point(4, 5)), Point(12, 3))
        self.assertEqual(curve.add(Point(4, 5), Point(12, 3)), Point(9, 1))
        self.assertEqual(curve.add(Point(6, 2), Point(16, 6)), Point(4, 14))

    def test_simple_multiplication(self):
        curve = EllipticCurveZp(-1, 3, 19)
        self.assertEqual(curve.mul(Point(6, 2), 2), Point(16, 6))

    def test_complex_multiplication(self):
        curve = EllipticCurveZp(-3, 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1, 6277101735386680763835789423207666416083908700390324961279)
        point = Point(0x188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012, 0x07192B95FFC8DA78631011ED6B24CDD573F977A11E794811)
        self.assertEqual(curve.mul(point, 1), point)
        self.assertEqual(curve.mul(point, 2), 
                         Point(0xDAFEBF5828783F2AD35534631588A3F629A70FB16982A888, 0xDD6BDA0D993DA0FA46B27BBC141B868F59331AFA5C7E93AB))
        self.assertEqual(curve.mul(point, 3), 
                         Point(0x76E32A2557599E6EDCD283201FB2B9AADFD0D359CBB263DA, 0x782C37E372BA4520AA62E0FED121D49EF3B543660CFD05FD))
        self.assertEqual(curve.mul(point, 6), 
                         Point(0xA37ABC6C431F9AC398BF5BD1AA6678320ACE8ECB93D23F2A, 0x851B3CAEC99908DBFED7040A1BBDA90E081F7C5710BC68F0))
        self.assertEqual(curve.mul(point, 1484605055214526729816930749766694384906446681761906688), 
                         Point(0x0C40230F9C4B8C0FD91F2C604FCBA9B87C2DFA153F010B4F, 0x5FC4F5771F467971B2C82752413833A68CE00F4A9A692B02))


class TestGF2NSCurves(unittest.TestCase):
    def test_simple_addition(self):
        curve = EllipticCurveGF2NS(Polynomial(1), Polynomial(1), Polynomial(1), Polynomial.get_irreducible(4))
        self.assertEqual(curve.add(Point(Polynomial(0b1000), Polynomial(0b0010)),
                                   Point(Polynomial(0b1000), Polynomial(0b0010))), 
                         Point(Polynomial(0b110), Polynomial(0b111)))
        self.assertEqual(curve.add(Point(Polynomial(0b1000), Polynomial(0b0010)), 
                                   Point(Polynomial(0b110), Polynomial(0b111))),
                         Point(Polynomial(0b1010), Polynomial(0b101)))

    def test_simple_multiplication(self):
        curve = EllipticCurveGF2NS(Polynomial(1), Polynomial(1), Polynomial(1), Polynomial.get_irreducible(4))
        self.assertEqual(curve.mul(Point(Polynomial(0b1000), Polynomial(0b0010)), 1), 
                         Point(Polynomial(0b1000), Polynomial(0b0010)))
        self.assertEqual(curve.mul(Point(Polynomial(0b1000), Polynomial(0b0010)), 2), 
                         Point(Polynomial(0b1), Polynomial(0b0)),
                        f'result {curve.mul(Point(Polynomial(0b1000), Polynomial(0b0010)), 2)} != expected {Point(Polynomial(0b1), Polynomial(0b0))}')
        self.assertEqual(curve.mul(Point(Polynomial(0b1000), Polynomial(0b0010)), 8), 
                         Point(Polynomial(0b0), Polynomial(0b0)))
        self.assertEqual(curve.mul(Point(Polynomial(0b1000), Polynomial(0b0010)), 0b101), 
                         Point(Polynomial(0b1100), Polynomial(0b1000)))

    def test_complex_addition(self):
        curve = EllipticCurveGF2NS(Polynomial(1), Polynomial(1), Polynomial(1), Polynomial.get_irreducible(163))
        point = Point(Polynomial(0x2fe13c0537bbc11acaa07d793de4e6d5e5c94eee8),
                      Polynomial(0x289070fb05d38ff58321f2e800536d538ccdaa3d9))

        self.assertEqual(curve.add(point, point),
                         Point(Polynomial(0xcb5ca2738fe300aacfb00b42a77b828d8a5c41eb),
                               Polynomial(0x229c79e9ab85f90acd3d5fa3a696664515efefa6b)))

    def test_complex_multiplication(self):
        curve = EllipticCurveGF2NS(Polynomial(1), Polynomial(1), Polynomial(1), Polynomial.get_irreducible(163))
        point = Point(Polynomial(0x2fe13c0537bbc11acaa07d793de4e6d5e5c94eee8),
                      Polynomial(0x289070fb05d38ff58321f2e800536d538ccdaa3d9))
        self.assertEqual(curve.mul(point, 2),
                         Point(Polynomial(0xcb5ca2738fe300aacfb00b42a77b828d8a5c41eb),
                               Polynomial(0x229c79e9ab85f90acd3d5fa3a696664515efefa6b)))

        self.assertEqual(curve.mul(point, 3),
                         Point(Polynomial(0x02ACFCFCC9A2AF8E3F2828024F820033DB20F69520),
                               Polynomial(0x05729C47F915BADC7B4C17DF14E5804109FFECDFE4)))

        self.assertEqual(curve.mul(point, 6),
                         Point(Polynomial(0x0765470BC65E9AB8C40B297C983B1000BCF021426E),
                               Polynomial(0x00A58BA7C589659F870A0CB121F76D61122D8741B6)))

        self.assertEqual(curve.mul(point, 112233445566778899),
                         Point(Polynomial(0x025E375998A309D04E13D0DEDCCB41C4092E10AA09),
                               Polynomial(0x0294931E03634C0372A5FD6CA8B5FC8653F05F3BA9)))

        self.assertEqual(curve.mul(point, 5846006549323611672814741753598448348329118574063), Point(Polynomial(0), Polynomial(0)))


if __name__ == '__main__':
    unittest.main()
