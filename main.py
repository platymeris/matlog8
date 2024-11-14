def zero(*args):
    return 0


def successor(n):
    return n + 1


def one(*args):
    return successor(zero())


def projection(i):
    def proj(args):
        return args[i - 1]

    return proj


def compose(f, *gs):
    def composed(*args):
        return f(*[g(*args) for g in gs])

    return composed


def primitive_recursion(g, h):
    def f(y, args):
        if y == 0:
            return g(args)
        else:
            previous = f(y - 1, args)
            return h(y - 1, previous, args)

    return f


def pred(args):
    g = zero

    def h(y_minus_1, previous, args):
        return y_minus_1

    pred_rec = primitive_recursion(g, h)

    return pred_rec(args[0], args)


def is_zero(args):
    def g(args):
        return one()

    def h(y_minus_1, previous, args):
        return zero()

    is_zero_rec = primitive_recursion(g, h)
    return is_zero_rec(args[0], args)


def is_less(args):
    n, m = args[0], args[1]

    sub_mn = subtract_example([m, n])

    is_zero_val = is_zero([sub_mn])

    one = successor(zero(args))
    is_less_val = subtract_example([one, is_zero_val])
    return is_less_val


def is_ge(args):
    is_less_val = is_less(args)
    one = successor(zero(args))
    is_ge_val = subtract_example([one, is_less_val])
    return is_ge_val


def conditional(c, a, b, args):
    part1 = multiply_example([c, a])
    one = successor(zero(args))
    one_minus_c = subtract_example([one, c])
    part2 = multiply_example([one_minus_c, b])
    new_val = add_example([part1, part2])
    return new_val


def mod_example(args):
    n, m = args[0], args[1]

    def g(args):
        return n

    def h(y_minus_1, previous, args):
        c = is_ge([previous, m])
        temp = subtract_example([previous, m])
        new_remainder = conditional(c, temp, previous, args)
        return new_remainder

    mod_rec = primitive_recursion(g, h)
    return mod_rec(n, args)


def subtract_example(in_args):
    g = projection(1)

    def h(m_minus_1, previous, args):
        return pred([previous])

    sub = primitive_recursion(g, h)

    return sub(in_args[1], in_args)


def add_example(in_args):
    g = projection(1)

    def h(m_minus_1, previous, args):
        return successor(previous)

    add_f = primitive_recursion(g, h)
    return add_f(in_args[1], in_args)


def multiply_example(in_args):
    g = zero

    def h(m_minus_1, previous, args):
        return add_example([projection(1)(args), previous])

    mult_f = primitive_recursion(g, h)
    return mult_f(in_args[1], in_args)


def is_divisor(args):
    n, k = args[0], args[1]
    mod = mod_example([n, k])
    return is_zero([mod])


def count_divisors_example(args):
    n = args[0]

    def g(args):
        return 0

    def h(y_minus_1, previous, args):
        y = successor(y_minus_1)
        c = is_divisor([n, y])
        return add_example([previous, c])

    count_div_rec = primitive_recursion(g, h)
    return count_div_rec(n, [n])


def is_prime_example(args):
    n = args[0]

    count = count_divisors_example([n])

    def two(args):
        return successor(successor(zero(args)))

    count_minus_two = subtract_example([count, two([n])])

    is_prime = is_zero([count_minus_two])

    return is_prime


def count_primes_up_to_example(args):
    y_max, n = args[0], args[1]

    def g(args):
        return 0

    def h(y_minus_1, previous, args):
        y = successor(y_minus_1)
        is_prime = is_prime_example([y])
        return add_example([previous, is_prime])

    count_primes_rec = primitive_recursion(g, h)
    return count_primes_rec(y_max - 1, [y_max, n])


def n_th_prime_example(args):
    n = add_example([args[0], one()])

    y_max_initial = 2

    y_max_limit = multiply_example([n, 15])

    def y_max_iteration(y_max, args):
        count = count_primes_up_to_example([y_max, n])

        c = is_ge([count, n])

        y_max_plus_one = successor(y_max)

        return conditional(c, y_max, y_max_plus_one, [y_max, n])

    def find_nth_prime(y_max, args):
        def g(args):
            return y_max_initial

        def h(y_minus_1, previous, args):
            return y_max_iteration(previous, args)

        find_prime_rec = primitive_recursion(g, h)
        return find_prime_rec(y_max_limit - y_max_initial, [y_max_limit, n])

    y_max_found = find_nth_prime(y_max_limit, [n])

    y_max_prime = subtract_example([y_max_found, one()])

    return y_max_prime


if __name__ == "__main__":
    print("\nТест функции n_prime:")
    print(f"1 = {n_th_prime_example([1])}")
    print(f"2 = {n_th_prime_example([2])}")
    print(f"3 = {n_th_prime_example([3])}")
    print(f"4 = {n_th_prime_example([4])}")
    print(f"5 = {n_th_prime_example([5])}")
    print(f"6 = {n_th_prime_example([6])}")
