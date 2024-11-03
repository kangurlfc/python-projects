import argparse
#import numpy (for arrays)
import sys
#print ints when ints and floats when floats

def main():

    parser = argparse.ArgumentParser(description='Perform math operations using command-line arguments')
    parser.add_argument('-a', help="Addition of provided command-line arguments. "
                                   "Sample input: '-a 5 3 6' output: 90", nargs='+', type=float)
    parser.add_argument('-d', help="Division of provided command-line arguments. "
                                   "Sample input: '-d 15 3 5' output: 1", nargs='+', type=float)
    parser.add_argument('-m', help="Multiplication of provided command-line arguments. "
                                   "Sample input: '-m 5 2 10' output: 100", nargs='+', type=float)
    parser.add_argument('-s', help="Subtraction of provided command-line arguments."
                                   "The first argument passed in is the minuend. Sample input: '-s 10 3 2' output: 5", nargs='+', type=float)
    parser.add_argument('-p', help="Power of provided command-line arguments."
                                   "The first argument of the notation should be base, the second -exponent. "
                                   "Sample input: '-p 3 2' output: 9", nargs='+', type=float)
    #-ta, ts, td, tm totals for previous results

    args = parser.parse_args()

    ops = {
        'a': add,
        'd': div,
        'm': multi,
        's': sub,
        'p': power
    }
    for key, func in ops.items():
        if getattr(args, key) is not None and key != 'p':
            result = func(*getattr(args, key))
            print(int(result) if result.is_integer() else result)
        if key == 'p':
            try:
                result = power(*args)
                print(int(result) if result.is_integer() else result)
            except TypeError:
                sys.exit('Two arguments required')

def add(*args: float) -> float:
    return sum(a for a in args)

def div(*args: float) -> float:
    result = args[0]

    try:
        for d in args[1:]:
            result /= d
        return result
    except ZeroDivisionError:
        sys.exit('Error. You cannot divide by 0')

def multi(*args: float) -> float:
    result = args[0]
    for m in args[1:]:
        result *= m
    return result

def sub(*args: float) -> float:
    result = args[0]
    for s in args[1:]:
        result -= s
    return result

def power(base: float, exponent: float) -> float:
    return pow(base, exponent)

if __name__ == "__main__":
    main()