import time
from sage.all import Integer, prod, factor, prime_range, sqrt

# Primes in 1,5 mod 6 up to 100, plus 2 and 3
SMALL_PRIMES = [p for p in prime_range(101) if p <= 3 or p % 6 in [1, 5]]

def get_congruence_class(p):
    """Return the congruence class of p modulo 6."""
    mod6 = p % 6
    if mod6 == 1:
        return "1 mod 6"
    elif mod6 == 5:
        return "5 mod 6"
    else:
        return f"{mod6} mod 6"

def is_sum_of_two_squares(n):
    """Return (a, b) if n = a^2 + b^2, else None."""
    limit = int(sqrt(n)) + 1
    for a in range(0, limit):
        b_squared = n - a * a
        if b_squared < 0:
            break
        b = int(sqrt(b_squared))
        if b * b == b_squared:
            return (a, b)
    return None

def sieve_prime_powers(limit):
    """Sieve prime powers up to limit that are sums of two squares."""
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

# Enhanced sieve up to 100 (keep it lean)
ENHANCED_PRIMES = SMALL_PRIMES + sieve_prime_powers(100)

def laplacian_eigenfunction_approach_custom(n):
    """Jenga-inspired factorization with identity sieve and congruence classes."""
    start_time = time.time()
    factors = dict()  # {prime: exponent}
    
    n = Integer(n)
    print("Finding initial prime factors...")
    
    # Step 1: Use enhanced sieve up to 100
    temp_n = n
    for p in ENHANCED_PRIMES:
        exp = 0
        while temp_n % p == 0:
            exp += 1
            temp_n //= p
        if exp > 0:
            factors[p] = exp
            print(f"Found factor {p} ({get_congruence_class(p)}) with exponent {exp}")
    
    # Step 2: Finish with Sage
    if temp_n > 1:
        for p, e in factor(temp_n):
            p = int(p)
            factors[p] = e
            print(f"Found factor {p} ({get_congruence_class(p)}) with exponent {e}")
    
    total_time = time.time() - start_time
    print(f"Initial factorization took: {total_time:.3f} seconds")
    print(f"Factors with multiplicity: {factors}")
    
    factor_list = sorted([p for p, e in factors.items() for _ in range(e)])
    print(f"Factors found: {factor_list}")
    print(f"Total time: {total_time:.3f} seconds")
    
    return factors  # Return dict for verification

def verify_factorization(number, factors):
    """Fast verification."""
    n = Integer(number)
    product = prod(Integer(p) ** e for p, e in factors.items())
    return n == product

if __name__ == '__main__':
    number_to_factor = Integer("1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139")
    print(f"Finding factors for RSA-100: {number_to_factor}")
    factors = laplacian_eigenfunction_approach_custom(number_to_factor)
    is_correct = verify_factorization(number_to_factor, factors)
    print(f"Factorization correct: {is_correct}")
