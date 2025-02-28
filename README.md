# RSA_Factorization
RSA_Factorization algortihm for SAGE Math

This code is a custom factorization algorithm with some number theory flavor (congruence classes, sums of two squares, and a "Laplacian eigenfunction" inspiration), 
applied to a large number (RSA-100). It uses Python with the SageMath library for mathematical heavy lifting. 

Here’s the explanation:

Imports
python

import time
from sage.all import Integer, prod, factor, prime_range, sqrt

    time: Measures how long the factorization takes.
    sage.all: Imports SageMath tools like Integer (for big numbers), prod (product of a sequence), factor (Sage’s factorization function), prime_range (list of primes up to a bound), and sqrt (square root).

Constants
python

SMALL_PRIMES = [p for p in prime_range(101) if p <= 3 or p % 6 in [1, 5]]

    This creates a list of prime numbers up to 100 that are either 2, 3, or congruent to 1 or 5 modulo 6 (e.g., 5, 7, 11, 13, 17, etc.).
    Why 1 or 5 mod 6? All primes greater than 3 fall into these classes because numbers congruent to 0, 2, 3, or 4 mod 6 are divisible by 2 or 3 (except 2 and 3 themselves).

Helper Function: get_congruence_class
python

def get_congruence_class(p):
    mod6 = p % 6
    if mod6 == 1:
        return "1 mod 6"
    elif mod6 == 5:
        return "5 mod 6"
    else:
        return f"{mod6} mod 6"

    Takes a prime p and returns its congruence class modulo 6 as a string (e.g., "1 mod 6" for 7, "5 mod 6" for 5, "2 mod 6" for 2).
    Used for printing informative output about the factors.

Helper Function: is_sum_of_two_squares
python

def is_sum_of_two_squares(n):
    limit = int(sqrt(n)) + 1
    for a in range(0, limit):
        b_squared = n - a * a
        if b_squared < 0:
            break
        b = int(sqrt(b_squared))
        if b * b == b_squared:
            return (a, b)
    return None

    Checks if a number n can be written as n = a² + b² (e.g., 5 = 1² + 2²).
    Returns a tuple (a, b) if true, or None if not.
    Uses a brute-force search up to sqrt(n), computing b = sqrt(n - a²) and checking if b is an integer.
    Fun fact: A number is a sum of two squares if, in its prime factorization, all primes congruent to 3 mod 4 (e.g., 3, 7, 11) have even exponents.

Helper Function: sieve_prime_powers
python

def sieve_prime_powers(limit):
    prime_powers = []
    for p in prime_range(5, limit + 1):
        if p % 6 not in [1, 5]:
            continue
        k = 1
        while p ** k <= limit:
            if is_sum_of_two_squares(p ** k):
                prime_powers.append(p ** k)
            k += 1
    return sorted(prime_powers)

    Builds a list of prime powers (e.g., 5¹, 5², 7¹, etc.) up to limit that are sums of two squares.
    Only considers primes congruent to 1 or 5 mod 6 (since primes like 3 or 7 mod 4 require even exponents, handled elsewhere).
    Example: For limit = 100, it might include 5, 13, 25 (5²), etc., if they pass the is_sum_of_two_squares test.

Enhanced Prime List
python

ENHANCED_PRIMES = SMALL_PRIMES + sieve_prime_powers(100)

    Combines SMALL_PRIMES (primes up to 100 that are 2, 3, or 1/5 mod 6) with prime powers up to 100 that are sums of two squares.
    This is a precomputed "sieve" used in the main factorization algorithm.

Main Function: laplacian_eigenfunction_approach_custom
python

def laplacian_eigenfunction_approach_custom(n):
    start_time = time.time()
    factors = dict()  # {prime: exponent}
    n = Integer(n)
    print("Finding initial prime factors...")

    The core factorization function. Takes a number n and returns its prime factors as a dictionary {prime: exponent}.
    Uses Integer from Sage to handle large numbers precisely.
    Tracks execution time with time.time().

Step 1: Trial Division with Enhanced Sieve
python

    temp_n = n
    for p in ENHANCED_PRIMES:
        exp = 0
        while temp_n % p == 0:
            exp += 1
            temp_n //= p
        if exp > 0:
            factors[p] = exp
            print(f"Found factor {p} ({get_congruence_class(p)}) with exponent {exp}")

    Starts with temp_n = n and divides out all factors from ENHANCED_PRIMES (primes and prime powers up to 100).
    For each prime/power p, counts how many times it divides temp_n (the exponent) and updates the factors dictionary.
    Prints each factor found with its congruence class.

Step 2: Finish with Sage’s Factorization
python

    if temp_n > 1:
        for p, e in factor(temp_n):
            p = int(p)
            factors[p] = e
            print(f"Found factor {p} ({get_congruence_class(p)}) with exponent {e}")

    If temp_n isn’t fully factored (i.e., still > 1), uses Sage’s factor() function to finish the job.
    Adds remaining prime factors and their exponents to the factors dictionary.
    This ensures correctness for large numbers beyond the sieve’s reach.

Output and Return
python

    total_time = time.time() - start_time
    print(f"Initial factorization took: {total_time:.3f} seconds")
    print(f"Factors with multiplicity: {factors}")
    factor_list = sorted([p for p, e in factors.items() for _ in range(e)])
    print(f"Factors found: {factor_list}")
    print(f"Total time: {total_time:.3f} seconds")
    return factors

    Computes and prints the total time taken.
    Prints the factors dictionary (e.g., {2: 1, 3: 2} means 2¹ × 3²).
    Creates a flat list of factors (repeating primes according to their exponents) and prints it.
    Returns the factors dictionary.

Verification Function: verify_factorization
python

def verify_factorization(number, factors):
    n = Integer(number)
    product = prod(Integer(p) ** e for p, e in factors.items())
    return n == product

    Takes the original number and the factors dictionary.
    Computes the product of p^e for each prime-exponent pair.
    Returns True if the product equals the original number, confirming the factorization is correct.

Main Execution
python

if __name__ == '__main__':
    number_to_factor = Integer("1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139")
    print(f"Finding factors for RSA-100: {number_to_factor}")
    factors = laplacian_eigenfunction_approach_custom(number_to_factor)
    is_correct = verify_factorization(number_to_factor, factors)
    print(f"Factorization correct: {is_correct}")

    Runs the code with RSA-100, a 100-digit number from the RSA Factoring Challenge.
    RSA-100 is 1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139, known to be the product of two 50-digit primes.
    Calls the factorization function, verifies the result, and prints whether it’s correct.

What’s the “Laplacian Eigenfunction” Part?
The function name laplacian_eigenfunction_approach_custom is a hybrid factorization algorithm:

    Step 1: A custom trial division with a sieve enriched by primes and prime powers related to sums of two squares.
    Step 2: Falls back to Sage’s optimized factorization for efficiency.
    The “Jenga-inspired” imply iteratively pulling out small factors (like blocks) until the structure (number) collapses into its prime components.

Example Output for RSA-100
For RSA-100, the actual factors are:

    37975227936943673922808872755445627854565536638199
    40094690950920881030683735292761468389214899724061
    Your code would:

    Try small primes/powers from ENHANCED_PRIMES (none divide RSA-100 since its factors are huge).
    Use factor() to find the two large primes.
    Output something like:

    Finding initial prime factors...
    Found factor 37975227936943673922808872755445627854565536638199 (1 mod 6) with exponent 1
    Found factor 40094690950920881030683735292761468389214899724061 (1 mod 6) with exponent 1
    Initial factorization took: X.XXX seconds
    Factors with multiplicity: {379752...: 1, 400946...: 1}
    Factors found: [379752..., 400946...]
    Total time: X.XXX seconds
    Factorization correct: True

Summary
Your code is a two-stage factorization tool:

    Custom Sieve: Uses a precomputed list of small primes and prime powers (tied to sums of two squares) for initial factoring.
    Sage Backup: Leverages Sage’s factor() for the heavy lifting on large numbers like RSA-100.
    It’s efficient for small factors and falls back to a robust method for big ones, with added flair from congruence classes and timing stats. 
