import decimal
import time
def pi():
    decimal.getcontext().prec += 2  # extra digits for intermediate steps
    three = decimal.Decimal(3) # substitute "three=3.0" for regular floats
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    decimal.getcontext().prec -= 2
    return +s # unary plus applies the new precision

decimal.getcontext().prec = 50000
t1 = time.time()
pi = pi()
t2 = time.time()
print(pi)
print("~"*30)
print(t2-t1)
