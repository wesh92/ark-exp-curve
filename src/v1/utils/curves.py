import math

MAX_XP = 255000000

def linear_curve(level: int, base_exp: int) -> int:
    return min(MAX_XP, base_exp * level)

def quadratic_curve(level: int, base_exp: int) -> int:
    return min(MAX_XP, base_exp * level**2)

def cubic_curve(level: int, base_exp: int) -> int:
    return min(MAX_XP, base_exp * level**3)

def exponential_curve(level: int, base_exp: int) -> int:
    return min(MAX_XP, int(base_exp * math.exp(level / 500)))  # Adjusted the denominator to ensure the values don't grow too quickly

def sqrt_curve(level: int, base_exp: int) -> int:
    return min(MAX_XP, int(base_exp * math.sqrt(level)))

def log_curve(level: int, base_exp: int) -> int:
    return min(MAX_XP, int(base_exp * math.log(level + 1)))

def fibonacci_curve(level: int, base_exp: int) -> int:
    if level == 1 or level == 2:
        return min(MAX_XP, level * base_exp)
    else:
        fib1, fib2 = base_exp, base_exp*2
        for _ in range(level - 2):
            fib1, fib2 = fib2, min(MAX_XP, fib1 + fib2)
        return fib2

def sigmoid_curve(level: int, base_exp: int) -> int:
    return min(MAX_XP, int(base_exp / (1 + math.exp(-level))))

def piecewise_curve(level: int, base_exp: int) -> int:
    if level < 3:
        return min(MAX_XP, level * base_exp)
    else:
        return min(MAX_XP, (level - 2) * (base_exp*2.5))
