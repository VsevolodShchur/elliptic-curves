class Polynomial:
    def __init__(self, bits):
        self.bits = bits
    
    def __str__(self):
        return bin(self.bits)

    def clone(self):
        return Polynomial(self.bits)
    
    def __len__(self):
        return self.bits.bit_length()

    def __eq__(self, other):
        if type(other) is int:
            return self.bits == other
        return self.bits == other.bits

    def __add__(self, other):
        return Polynomial(self.bits ^ other.bits)

    def __sub__(self, other):
        return self + other

    def __mul__(self, other):
        res = Polynomial(0)
        p = self.clone()
        other_bits = other.bits

        while other_bits:
            if other_bits & 1:
                res += p
            p.bits <<= 1
            other_bits >>= 1
        return res

    def div(self, other):
        q = Polynomial(0)
        r = self.clone()
        while len(r) >= len(other):
            product = Polynomial(1 << (len(r) - len(other)))
            q += product
            r += product * other

        return q, r

    def __truediv__ (self, other):
        q, _ = self.div(other)
        return q

    def __mod__(self, other):
        _, r = self.div(other)
        return r

    __irreducible_polynoms = {
        2:   7,  # x^2+x+1
        3:   11,  # x^3+x+1
        4:   19,  # x^4+x+1
        5:   37,  # x^5+x^2+1
        6:   66,  # x^6+x+1
        7:   131,  # x^7+x+1
        8:   283,  # x^8+x^4+x^3+x+1
        9:   529,  # x^9+x^4+1
        10:  1033,  # x^10+x^3+1
        11:  2053,  # x^11+x^2+1
        12:  4178,  # x^12+x^6+x^4+x+1
        13:  8219,  # x^13+x^4+x^3+x+1
        14:  17475,  # x^14+x^10+x^6+x+1
        15:  32771,  # x^15+x+1
        16:  69643,  # x^16+x^12+x^3+x+1
        17:  131081,  # x^17+x^3+1
        18:  262273,  # x^18+x^7+1
        19:  524327,  # x^19+x^5+x^2+x+1
        20:  1048585,  # x^20+x^3+1
        21:  2097157,  # x^21+x^2+1
        22:  4194307,  # x^22+x+1
        23:  8388641,  # x^23+x^5+1
        24:  16777351,  # x^24+x^7+x^2+x+1
        25:  33554441,  # x^25+x^3+1
        26:  67108935,  # x^26+x^6+x^2+x+1
        27:  134217767,  # x^27+x^5+x^2+x+1
        28:  268435465,  # x^28+x^3+1
        29:  536870917,  # x^29+x^2+1
        30:  1082130439,  # x^30+x^23+x^2+x+1
        31:  2147483657,  # x^31+x^3+1
        32:  4299161607,  # x^32+x^22+x^2+x+1
        36:  68719478785,  # x^36+x^11+1
        40:  1099511628299,  # x^40+x^9+x^3+x+1
        48:  281475245146123,  # x^48+x^28+x^3+x+1
        56:  72061992084439047,  # x^56+x^42+x^2+x+1
        64:  18446814442453729299,  # x^64+x^46+x^4+x+1
        72:  4726978168888072601613,  # x^72+x^62+x^3+x^2+1
        80:  1208925837629027684188167,  # x^80+x^54+x^2+x+1
        96:  79228162514264337595691434003,  # x^96+x^31+x^4+x+1
        128: 340282366920938463463374607431768211591,  # x^128+x^7+x^2+x+1
        160: 1461501637330902918203684832716283019655933067283,  # x^160+x^19+x^4+x+1
        163: 11692013098647223345629478661730264157247460344009,  # x^163+x^7+x^6+x^3+1
        192: 6277101735386680763835789585466943245315718836042044801043,  # x^192+x^107+x^4+x+1
        256: 115792089237316195423570985008687907853269984665640564039457584007913129705483,  # x^256+x^16+x^3+x+1
    }


    @staticmethod
    def get_irreducible(p):
        result = Polynomial.__irreducible_polynoms[p]
        if result is None:
           return None

        return Polynomial(result)
