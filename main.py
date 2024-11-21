def zero(*args):
    return 0


def successor(n):
    return n + 1


def id(*args):
    return ([args[0], args[1]])


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


def two(*args):
    return successor(successor(zero()))


def fifteen(*args):
    return successor(successor(successor(successor(successor(
        successor(successor(successor(successor(successor(successor(successor(successor(successor(zero()))))))))))))))


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
    return substitution(subtract_example, one,
                        substitution(is_zero, substitution(subtract_example, projection(2), projection(1))))(*args)


def is_ge(*args):
    return substitution(subtract_example, one, is_less)(*args)


def conditional(c, a, b, *args):
    return add_example(multiply_example(c, a), multiply_example(subtract_example(one(), c), b))


def g_mod_example(*args):
    return args[0]


def h_mod_example(*args):
    return substitution(conditional, substitution(is_ge, projection(2), projection(4)),
                        substitution(subtract_example, projection(2), projection(4)), projection(2))(*args)


def mod_example(*args):
    return substitution(primitive_recursion(g_mod_example, h_mod_example), projection(1), projection(1), projection(2))(
        *args)


def is_divisor(*args):
    return substitution(is_zero, mod_example)(*args)


def g_count_divisors_example(*args):
    return zero()


def h_count_divisors_example(*args):
    return substitution(add_example, projection(2),
                        substitution(is_divisor, projection(3), substitution(successor, projection(1))))(*args)


def count_divisors_example(*args):
    return substitution(primitive_recursion(g_count_divisors_example, h_count_divisors_example), projection(1),
                        projection(1))(*args)


def is_prime_example(*args):
    return substitution(is_zero, substitution(subtract_example, count_divisors_example, two))(*args)


def g_count_primes_up_to_example(*args):
    return zero()


def h_count_primes_up_to_example(y_minus_one, previous, *args):
    return add_example(previous, is_prime_example(successor(y_minus_one)))


def count_primes_up_to_example(*args):
    return substitution(primitive_recursion(g_count_primes_up_to_example, h_count_primes_up_to_example),
                        substitution(subtract_example, projection(1), one))(*args)


def g_n_th_prime(*args):
    return two()


def h_n_th_prime(*args):
    return substitution(conditional,
                        substitution(is_ge, substitution(count_primes_up_to_example, projection(2), projection(3)),
                                     projection(3)), projection(2), substitution(successor, projection(2)))(*args)


def n_th_prime_example(*args):
    return substitution(subtract_example, substitution(primitive_recursion(g_n_th_prime, h_n_th_prime),
                                                       substitution(multiply_example,
                                                                    substitution(add_example, projection(1), one),
                                                                    fifteen), projection(1)), one)(*args)


if __name__ == "__main__":
    print("\nТест функции n_prime:")
    print(f"1 = {n_th_prime_example(1)}")
    print(f"2 = {n_th_prime_example(2)}")
    print(f"3 = {n_th_prime_example(3)}")
    print(f"4 = {n_th_prime_example(4)}")
    print(f"5 = {n_th_prime_example(5)}")
    print(f"6 = {n_th_prime_example(6)}")
