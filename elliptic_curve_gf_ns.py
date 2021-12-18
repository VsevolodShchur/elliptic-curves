from point import Point
from polynomial import Polynomial
from utils import mod_inverse_gf


class EllipticCurveGF2NS:
    def __init__(self, a, b, c, p):
        self.a = a
        self.b = b
        self.c = c
        self.p = p

    def __contains__(self, p):
        if p == Point(Polynomial(0), Polynomial(0)):
            return True

        return ((p.y * p.y + self.a * p.x * p.y) - (p.x * p.x * p.x + self.b * p.x * p.x + self.c)) % self.p == 0
    
    def add(self, p1, p2):
        if p1 not in self or p2 not in self:
            return None

        if p1 == Point(Polynomial(0), Polynomial(0)):
            return p2
        if p2 == Point(Polynomial(0), Polynomial(0)):
            return p1

        if p1.x == p2.x and p1.y != p2.y:
            return Point(Polynomial(0), Polynomial(0))
        
        if p1.x != p2.x:
            k = ((p1.y + p2.y) * mod_inverse_gf(p1.x + p2.x, self.p)) % self.p
        else:
            k = ((self.a * p1.y + p1.x * p1.x) * (mod_inverse_gf(self.a * p1.x, self.p))) % self.p
       
        x3 = (k * k + k * self.a + self.b + p1.x + p2.x) % self.p
        y3 = (p1.y + k * (x3 + p1.x)) % self.p
        return Point(x3, (self.a * x3 + y3) % self.p)

    def mul(self, p, n):
        if n == 0:
           return Point(Polynomial(0), Polynomial(0))
        if n == 1:
           return p

        if n % 2 == 1:
           return self.add(p, self.mul(p, n - 1))
        else:
           return self.mul(self.add(p, p), n // 2)
