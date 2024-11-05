## ***Command-line argument calculator***

### Overview

This program allows the user to execute the following math operations:
- addition
- subtraction
- multiplication
- division
- n-th roots
- exponentiation
- logarithms for given base

### Usage

Each operation can be executed in the command-line with the following flags:
- -a - addition of provided command-line arguments. 
  -     Sample input: '-a 5 3 6' output: 14,
- -d - division of provided command-line arguments. The first argument is the dividend, every other: divisors. 
  -     Sample input: '-d 15 3 5' output: 1,
- -l - logarithm of provided command-line arguments. The first argument of the notation should be base and the second - the argument.
  -     Sample input: '-l 16 2' output: 4,
- -m - multiplication of provided command-line arguments. 
  -     Sample input: '-m 5 2 10' output: 100
- -n - n-th root of provided command-line arguments
        The first argument of the notation should be the radicand and the second - index. 
  -     Sample input: '-n 9 2' output: 3,
- -p - power of provided command-line argument.
        The first argument of the notation should be base and the second - the exponent.
  -     Sample input: '-p 3 2' output: 9,
- -s - subtraction of provided command-line arguments. The first argument passed in is the minuend. 
  -     Sample input: '-s 10 3 2' output: 5,

Notes:

- arguments (integers and floats only) must be separated with a space
- multiple flags may be used in the same command-line,
- -l, -n and -p flags require exactly two arguments, while other flags do not have a specific limit on the number of arguments they accept.
- the program outputs results in the order of flags passed in to the command-line
- due to the precision of representing floating-point numbers, every output is rounded up to 6 decimal places
