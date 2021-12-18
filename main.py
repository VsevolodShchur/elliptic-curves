from elliptic_curve_gf_ns import EllipticCurveGF2NS
from elliptic_curve_gf_nn import EllipticCurveGF2NN
from elliptic_curve_zp import EllipticCurveZp
from polynomial import Polynomial
from point import Point
import os

def to_int(s):
    if len(s) < 2:
        return int(s)
    if s[1] == 'x':
        return int(s, 16)
    if s[1] == 'b':
        return int(s, 2)
    return int(s)

def create_zp_curve(curve_args):
    a = to_int(curve_args[0])
    b = to_int(curve_args[1])
    p = to_int(curve_args[2])
    return EllipticCurveZp(a, b, p)

def create_gf2ns_curve(curve_args):
    a = to_int(curve_args[0])
    b = to_int(curve_args[1])
    c = to_int(curve_args[2])
    p = to_int(curve_args[3])
    return EllipticCurveGF2NS(Polynomial(a), Polynomial(b), Polynomial(c), Polynomial.get_irreducible(p))

def create_gf2nn_curve(curve_args):
    a = to_int(curve_args[0])
    b = to_int(curve_args[1])
    c = to_int(curve_args[2])
    p = to_int(curve_args[3])
    return EllipticCurveGF2NN(Polynomial(a), Polynomial(b), Polynomial(c), Polynomial.get_irreducible(p))


def parse_curve(curve_type, curve_args):
    if curve_type == 'zp':
        return create_zp_curve(curve_args)
    elif curve_type == 'gf2ns':
        return create_gf2ns_curve(curve_args)
    elif curve_type == 'gf2nn':
        return create_gf2nn_curve(curve_args)
    else:
        print(f'Неизвестный тип кривой: {curve_type}')
        return

def parse_point(curve_type, x_str, y_str):
    if curve_type == 'zp':
        return Point(to_int(x_str), to_int(y_str))
    if curve_type in ['gf2ns', 'gf2nn']:
        return Point(Polynomial(to_int(x_str)), Polynomial(to_int(y_str)))

def solve_task(curve_type, curve, args):
    operation = args[0]
    if operation == 'ADD':
        p1 = parse_point(curve_type, args[1], args[2])
        p2 = parse_point(curve_type, args[3], args[4])
        return curve.add(p1, p2)
    
    elif operation == 'MUL':
        p = parse_point(curve_type, args[1], args[2])
        n = to_int(args[3])
        return curve.mul(p, n)
    else:
        return f'Неизвестный тип операции: {operation}'

def main():
    mypath = os.path.abspath(os.getcwd())
    in_dir = os.path.join(mypath, 'inputs')
    out_dir = os.path.join(mypath, 'outputs')
    try:
        os.mkdir(out_dir)
    except FileExistsError:
        pass
    
    for in_file_name in os.listdir(in_dir):
        name, ext = os.path.splitext(in_file_name)
        if ext != '.txt':
            continue
        in_file =  os.path.join(in_dir, in_file_name)
        out_file = os.path.join(out_dir, f'{name}_result{ext}')
        if not os.path.exists(out_file):
            open(out_file, 'w').close()    
        
        with open(in_file, 'r') as f_in, open(out_file, 'w') as f_out:
            lines = list(map(str.strip, f_in.readlines()))
            if len(lines) < 2:
                print(f'Слишком мало строк в файле {in_file_name}. Пропуск')
                continue
            curve_type = lines[0]
            curve_args = lines[1].split()
            curve = parse_curve(curve_type, curve_args)
            if curve is None:
                print(f'Не удалось создать кривую из файла {in_file_name}. Пропуск')
                continue
            
            for task in lines[2:]:
                res = solve_task(curve_type, curve, task.split())
                f_out.write(str(res)+'\n')


if __name__ == '__main__':
    main()
