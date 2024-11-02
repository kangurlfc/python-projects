import argparse
#import numpy (for arrays)
#print ints when ints and floats when floats

def main():

    parser = argparse.ArgumentParser(description='Perform math operations using command-line arguments')
    parser.add_argument('-a', help="Addition of provided command-line arguments. "
                                   "Sample input: '-a 5 3 6' output: 90", nargs='+', type = float)
    parser.add_argument('-d', help="Division of provided command-line arguments. "
                                   "Sample input: '-d 15 3 5' output: 1", nargs='+', type=float)
    parser.add_argument('-m', help="Multiplication of provided command-line arguments. "
                                   "Sample input: '-m 5 2 10' output: 100", nargs='+', type = float)

    #-ta, ts, td, tm totals for previous results

    args = parser.parse_args()

    if args.a:
        print(add(*args.a))

    if args.m:
        print(multi(*args.m))

    if args.d:
        print(multi(*args.d))

def add(*args: float) -> float:
    return sum(a for a in args)

def div(*args: float) -> float:
    result = args[0]
    for m in args[1:]:
        result *= m
    return result

def multi(*args: float) -> float:
    result = args[0]
    for m in args[1:]:
        result *= m
    return result



if __name__ == "__main__":
    main()