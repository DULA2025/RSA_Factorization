from sympy import factorint, isprime
import sys
import time
from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np

def laplacian_eigenfunction_approach(args):
    """
    Simplified version to avoid issues in multiprocessing.
    This function now focuses on polynomial factorization in finite fields.
    Args:
        args: Tuple of (p, k, n, verbose) where:
            p: The prime number (as int)
            k: The power to raise p to (as int)
            n: The number to factorize (as int)
            verbose: Boolean to control whether to print detailed steps
    Returns:
        A list of factors found.
    """
    p, k, n, verbose = args
    factors = set()
    q = p ** k
    
    try:
        if q > 10**12:  # Arbitrary limit to avoid huge fields
            if verbose:
                print(f"Field GF({q}) too large, skipping")
            return list(factors)
        
        from sympy.polys.domains import GF
        from sympy import Poly, symbols
        
        x = symbols('x')
        
        if k == 1:
            domain = GF(p)
        else:
            if verbose:
                print(f"Extension fields for k={k} not fully implemented. Skipping.")
            return list(factors)
        
        for m in range(3, p + 1):
            if verbose:
                print(f" Over GF({q}), m = {m}:")
            
            try:
                poly = Poly(x**m - 1, domain=domain)
                factorization = poly.factor_list()[1]  # List of (poly, multiplicity)
                
                for fact_tuple in factorization:
                    factor_poly, multiplicity = fact_tuple
                    try:
                        coeffs = factor_poly.all_coeffs()  # Highest degree first
                        factor_value = 0
                        for i, c in enumerate(reversed(coeffs)):
                            factor_value += int(c) * (p ** i)
                        
                        if factor_value != 0 and n % factor_value == 0:
                            if factor_value not in factors:
                                if verbose:
                                    print(f" Found new factor: {factor_value}")
                                factors.add(factor_value)
                    except Exception as e:
                        if verbose:
                            print(f" Error processing factor {factor_poly}: {e}")
                        continue
            except Exception as e:
                if verbose:
                    print(f" Error factoring polynomial for m={m}: {e}")
                continue
            
            if m == p or q % m == 1:
                break
    except Exception as e:
        if verbose:
            print(f" Error creating field GF({q}): {e}")
    
    return list(factors)

def find_factors_using_finite_fields(n, max_power_list=[2, 3], verbose=True):
    """
    Attempts to find factors of a large number n using finite fields with specific max_power values.
    Modified to properly handle multiprocessing and incorporate Laplacian eigenfunction approach.
    Args:
        n: The number to factorize (as string or integer)
        max_power_list: List of specific max_power values to check
        verbose: Boolean to control whether to print detailed steps
    Returns:
        A sorted list of factors found.
    """
    start_time = time.time()
    factors = set()
    # Convert to int
    n = int(n)
    
    # Find initial prime factors
    if verbose:
        print("Finding initial prime factors...")
    
    try:
        if isprime(n):
            factors.add(n)
        else:
            for p, e in factorint(n).items():
                for _ in range(e):
                    factors.add(p)
    except MemoryError:
        print("Memory error during initial factorization.")
        return sorted(list(factors))
    
    if verbose:
        print(f"Initial factors: {factors}")
    
    # Filter prime factors
    prime_factors = [p for p in factors if isprime(p) and p % 6 in [1, 5]]
    
    # Prepare arguments for parallel processing
    args_list = []
    for p in prime_factors:
        for k in max_power_list:
            args_list.append((p, k, n, False))
    
    # Use multiprocessing Pool
    num_processes = min(cpu_count(), len(args_list))
    if verbose:
        print(f"Using {num_processes} processes for {len(args_list)} tasks...")
    
    if args_list:  # Only create pool if there are tasks
        with Pool(processes=num_processes) as pool:
            results = pool.map(laplacian_eigenfunction_approach, args_list)
        # Combine results
        for result in results:
            factors.update(result)
    
    end_time = time.time()
    if verbose:
        print(f"\nTime taken: {end_time - start_time:.2f} seconds")
    
    return sorted(list(factors))

def verify_factorization(number, factors):
    """
    Verifies that the product of found factors equals the original number.
    
    Args:
        number: Original number to factor (as string or integer)
        factors: List of factors found
        
    Returns:
        bool: True if factorization is correct
    """
    number = int(number)
    product = 1
    for factor in factors:
        product *= factor
    return product == number

if __name__ == '__main__':
    # Test number
    number_to_factor = "28948022309329048855892746252171976963322203655954433126947083963168578338817"
    max_power_list = [2, 3]
    print(f"Finding factors for {number_to_factor}")
    found_factors = find_factors_using_finite_fields(number_to_factor, max_power_list, verbose=True)
    print(f"\nFactors found: {found_factors}")
    # Verify factorization
    is_correct = verify_factorization(number_to_factor, found_factors)
    print(f"\nFactorization verification: {is_correct}")
