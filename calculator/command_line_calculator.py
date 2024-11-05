import argparse
from math import log
from re import search
import sys


decimal_places = 6


def main():

    parser = argparse.ArgumentParser(
        description="Perform math operations using command-line arguments"
    )
    parser.add_argument(
        "-a",
        help="Addition of provided command-line arguments. "
        "Sample input: '-a 5 3 6' output: 14",
        nargs="+",
        type=float,
    )
    parser.add_argument(
        "-d",
        help="Division of provided command-line arguments. "
        "Sample input: '-d 15 3 5' output: 1",
        nargs="+",
        type=float,
    )
    parser.add_argument(
        "-m",
        help="Multiplication of provided command-line arguments. "
        "Sample input: '-m 5 2 10' output: 100",
        nargs="+",
        type=float,
    )
    parser.add_argument(
        "-n",
        help="N-th root of provided command-line arguments"
        "The first argument of the notation should be the radicand and the second - index. "
        "Sample input: '-n 9 2' output: 3",
        nargs="+",
        type=float,
    )
    parser.add_argument(
        "-p",
        help="Power of provided command-line argument."
        "The first argument of the notation should be base and the second - the exponent. "
        "Sample input: '-p 3 2' output: 9",
        nargs="+",
        type=float,
    )
    parser.add_argument(
        "-s",
        help="Subtraction of provided command-line arguments."
        "The first argument passed in is the minuend. "
        "Sample input: '-s 10 3 2' output: 5",
        nargs="+",
        type=float,
    )
    parser.add_argument(
        "-l",
        help="Logarithm of provided command-line arguments"
             "The first argument of the notation should be base and the second - the argument. "
             "Sample input: '-l 16 2' output: 4",
        nargs="+",
        type=float
    )

    args = parser.parse_args()

    ops = {"a": add, "d": div, "l": xlog, "m": multi, "n": nroot, "p": power, "s": sub}
    ordered_ops = [arg.replace('-', '') for arg in sys.argv if search(r"-{1,2}[a-zA-Z]", arg)]

    for key in ordered_ops:
        if getattr(args, key) and key not in ["l", "n", "p"]:
            result = ops[key](*getattr(args, key))
            print(int(result) if result.is_integer() else result)
        elif getattr(args, key) and key in ["l", "n", "p"]:
            if len(getattr(args, key)) != 2:
                raise TypeError("Error. Two arguments required")
            else:
                result = ops[key](*getattr(args, key))
                print(int(result) if result.is_integer() else result)


def add(*args: float) -> float:
    return round(sum(a for a in args), decimal_places)


def div(*args: float) -> float:
    result = args[0]
    for d in args[1:]:
        if d == 0:
            raise ZeroDivisionError("Error. You cannot divide by 0.")
        result /= d
    return round(result, decimal_places)


def multi(*args: float) -> float:
    result = args[0]
    for m in args[1:]:
        result *= m
    return round(result, decimal_places)


def sub(*args: float) -> float:
    result = args[0]
    for s in args[1:]:
        result -= s
    return round(result, decimal_places)


def power(base: float, exponent: float) -> float:
    return round(pow(base, exponent), decimal_places)


def nroot(radicand: float, index: float) -> float:
    if radicand < 0 and index % 2 != 0:
        result = -pow(abs(radicand), 1 / index)
    elif radicand < 0 < index and index % 2 == 0:
        raise TypeError("The root of a negative number must have an odd index")
    elif radicand > 0 > index and index % 2 == 0:
        raise TypeError("Negative root indicis must be an odd number")
    else:
        result = pow(radicand, 1 / index)
    return round(result, decimal_places)


def xlog(arg: float, base: float) -> float:
    if base <= 0 or base == 1:
        raise ValueError("The base needs to greater than 0 and different than 1.")
    if arg <= 0:
        raise ValueError("The argument needs to be greater than 0.")
    return round(log(arg, base), decimal_places)


if __name__ == "__main__":
    main()
