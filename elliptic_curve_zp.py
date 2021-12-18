from point import Point
from utils import mod_inverse_zp


class EllipticCurveZp:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def __contains__(self, p):
        if p == Point(0, 0):
            return True

        return ((p.y * p.y) - (pow(p.x, 3, self.p) + self.a * p.x + self.b)) % self.p == 0

    def add(self, p1, p2):
        if p1 not in self or p2 not in self:
            return

        if p1 == Point(0, 0):
            return p2
        if p2 == Point(0, 0):
            return p1
        if p1.x == p2.x and p1.y != p2.y:
            return Point(0, 0)

        if p1.x != p2.x:
            k = ((p2.y - p1.y) * mod_inverse_zp(p2.x - p1.x, self.p)) % self.p
        else:
            k = ((3 * p1.x * p1.x + self.a) * mod_inverse_zp(2 * p1.y, self.p)) % self.p
        
        x3 = (k * k - p1.x - p2.x) % self.p
        y3 = (p1.y + k * (x3 - p1.x)) % self.p
        return Point(x3, -y3 % self.p)

    def mul(self, p, n):
        if n == 0:
            return Point(0, 0)
        if n == 1:
            return p

        if n % 2 == 1:
            return self.add(p, self.mul(p, n - 1))
        else:
            return self.mul(self.add(p, p), n // 2)
