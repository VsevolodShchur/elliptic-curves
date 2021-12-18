from polynomial import Polynomial


def mod_inverse_zp(num, p):
    s, old_s = 0, 1
    r, old_r = p, num

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    return old_s % p

def mod_inverse_gf(polynomal, p):
    s, old_s = Polynomial(0), Polynomial(1)
    r, old_r = p, polynomal

    while r != 0:
        quotient = old_r / r
        old_r, r = r, old_r + quotient * r
        old_s, s = s, old_s + quotient * s

    return old_s % p
