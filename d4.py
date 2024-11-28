import sys

sys.setrecursionlimit(5000)


def zero(*args):
    return 0


def successor(n):
    return n + 1


def one(*args):
    return successor(zero())


def projection(i):
    def proj(*args):
        return args[i - 1]

    return proj


def compose(f, *gs):
    def composed(*args):
        return f(*[g(*args) for g in gs])

    return composed


def substitution(g, *gs):
    def substituted(*args):
        results = [f(*args) for f in gs]
        return g(*results)

    return substituted


def primitive_recursion(g, h):
    def rec(y, *args):
        if y == 0:
            return g(*args)
        else:
            previous = rec(y - 1, *args)
            return h(y - 1, previous, *args)

    return rec


def g_pred(*args):
    return zero()


def h_pred(y_minus_1, previous, *args):
    return y_minus_1


def pred(*args):
    return substitution(primitive_recursion(g_pred, h_pred), projection(1))(*args)


def g_is_zero(*args):
    return one()


def h_is_zero(y_minus_1, previous, *args):
    return zero()


def is_zero(*args):
    return substitution(primitive_recursion(g_is_zero, h_is_zero), projection(1))(*args)


def g_subtract_example(*args):
    return projection(1)(*args)


def h_subtract_example(y_minus_one, previous, *args):
    return pred(previous, *args)


def subtract_example(*args):
    return substitution(primitive_recursion(g_subtract_example, h_subtract_example), projection(2), projection(1))(
        *args)


def g_add_example(*args):
    return projection(1)(*args)


def h_add_example(y_minus_1, previous, *args):
    return successor(previous)


def add_example(*args):
    return substitution(primitive_recursion(g_add_example, h_add_example), projection(2), projection(1))(*args)


def g_multiply_example(*args):
    return zero()


def h_multiply_example(*args):
    return substitution(add_example, projection(3), projection(2))(*args)


def multiply_example(*args):
    return substitution(primitive_recursion(g_multiply_example, h_multiply_example), projection(2), projection(1))(
        *args)


def is_less(*args):
    return substitution(is_zero, substitution(subtract_example, projection(1), projection(2)))(*args)


def is_ge(*args):
    return substitution(subtract_example, one, is_less)(*args)


def conditional(c, a, b, *args):
    return add_example(multiply_example_optimized(c, a), multiply_example_optimized(subtract_example(one(), c), b))


def g_mod_example(*args):
    return args[0]


def h_mod_example(*args):
    return substitution(conditional, substitution(is_ge, projection(2), projection(4)),
                        substitution(subtract_example, projection(2), projection(4)), projection(2))(*args)


def mod_example(*args):
    return substitution(primitive_recursion(g_mod_example, h_mod_example), projection(1), projection(1), projection(2))(
        *args)


def is_divisor(*args):
    return substitution(is_zero, mod_example_optimized)(*args)


def multiply_example_optimized(x, y):
    return x * y


def g_exp_example(*args):
    return one()


def h_exp_example(*args):
    return substitution(multiply_example_optimized, projection(3), projection(2))(*args)


def exp_example(*args):
    return substitution(primitive_recursion(g_exp_example, h_exp_example), projection(2), projection(1))(*args)


def mod_example_optimized(k, n):
    return k % n


def int_log_optimized(n, k):
    if k < n:
        return 0
    else:
        return 1 + int_log_optimized(n, k // n)


def g_int_log(*args):
    return zero()


def is_less_optimized(*args):
    return args[0] < args[1]


def h_int_log(*args):
    return substitution(conditional, substitution(is_less_optimized, projection(4),
                                                  substitution(exp_example, projection(3),
                                                               substitution(successor, projection(1)))), projection(2),
                        substitution(successor, projection(1)))(*args)


def int_log_example(*args):
    return substitution(primitive_recursion(g_int_log, h_int_log), projection(2), projection(1), projection(2))(*args)


def g_plog_n_example(n, k):
    return zero()


def is_divisor_optimized(k, n):
    return 1 if k % n == 0 else 0


def h_plog_n_example(*args):
    return substitution(conditional, substitution(is_ge, substitution(exp_example, projection(3),
                                                                      substitution(successor, projection(1))),
                                                  substitution(successor, projection(4))), projection(2),
                        substitution(conditional, substitution(is_divisor, projection(4),
                                                               substitution(exp_example, projection(3),
                                                                            substitution(successor, projection(1)))),
                                     substitution(successor, projection(1)), projection(2)))(*args)


def plog_n_example(*args):
    return substitution(primitive_recursion(g_plog_n_example, h_plog_n_example),
                        compose(successor, substitution(int_log_optimized, projection(1), projection(2))),
                        projection(1), projection(2))(*args)


def main():
    print("\nTesting int_log_example:")
    examples_int_log = [(2, 16, 4), (3, 81, 4), (5, 625, 4), (2, 31, 4), (7, 343, 3)]
    for n, k, expected in examples_int_log:
        result = int_log_example(n, k)
        print(f"int_log_{n}({k}) = {result} (Expected: {expected})")

    print("\nTesting plog_n_example:")
    examples_plog = [(2, 96, 5), (3, 81, 4), (5, 1000, 3), (2, 31, 0), (7, 343, 3)]
    for n, k, expected in examples_plog:
        result = plog_n_example(n, k)
        print(f"plog_{n}({k}) = {result} (Expected: {expected})")


if __name__ == "__main__":
    main()
