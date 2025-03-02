from sage.all import GF, PolynomialRing, factor, is_prime, Integer, sqrt, prime_range, log, cyclotomic_polynomial
import time
import numpy as np

def generate_special_primes(max_value):
    """
    Efficiently generate primes in congruence classes 1 and 5 modulo 6,
    plus include prime 3.
    
    Args:
        max_value: Upper limit for prime generation
        
    Returns:
        List of precomputed primes following the pattern
    """
    start_time = time.time()
    print(f"Generating special primes up to {max_value}...")

    # Start with prime 3, then generate primes ≡ 1 or 5 (mod 6)
    special_primes = [3]
    
    # Use sieve of Eratosthenes optimization for classes 1 and 5 mod 6
    # Only track positions to save memory for large ranges
    max_idx_1 = (max_value - 1) // 6
    max_idx_5 = (max_value - 5) // 6
    
    # Create bit arrays for both residue classes (much more memory efficient)
    sieve_1 = np.ones(max_idx_1 + 1, dtype=bool)  # For numbers of form 6k + 1
    sieve_5 = np.ones(max_idx_5 + 1, dtype=bool)  # For numbers of form 6k + 5
    
    # Sieve out composites
    for i in range(1, int(sqrt(max_value)) // 6 + 1):
        # Check numbers of form 6i + 1
        if sieve_1[i]:
            p = 6*i + 1
            # Mark multiples in 6k+1 sieve
            for j in range(i + p, max_idx_1 + 1, p):
                sieve_1[j] = False
            # Mark multiples in 6k+5 sieve
            start = (p*5 - 5) // 6
            if start > 0:
                for j in range(start, max_idx_5 + 1, p):
                    sieve_5[j] = False
                    
        # Check numbers of form 6i + 5
        if i <= max_idx_5 and sieve_5[i]:
            p = 6*i + 5
            # Mark multiples in 6k+1 sieve
            start = (p*1 - 1) // 6
            if start > 0:
                for j in range(start, max_idx_1 + 1, p):
                    sieve_1[j] = False
            # Mark multiples in 6k+5 sieve
            start = (p*5 - 5) // 6
            if start > 0:
                for j in range(start, max_idx_5 + 1, p):
                    sieve_5[j] = False
    
    # Convert back to prime numbers
    for i in range(1, max_idx_1 + 1):
        if sieve_1[i]:
            special_primes.append(6*i + 1)
    
    for i in range(1, max_idx_5 + 1):
        if sieve_5[i]:
            special_primes.append(6*i + 5)
    
    # Sort the list
    special_primes.sort()
    print(f"Generated {len(special_primes)} special primes in {time.time() - start_time:.2f} seconds")
    return special_primes

def factor_large_semiprime(n, max_prime=10000, max_attempts=3, use_parallel=False):
    """
    Specialized function to factor a single, known large semiprime.
    Optimized specifically for congruence classes 1 and 5 modulo 6.
    
    Args:
        n: The specific large semiprime to factor
        max_prime: Upper bound for prime search
        max_attempts: Maximum number of power attempts per prime
        use_parallel: Whether to use parallel processing
        
    Returns:
        List of prime factors found
    """
    # Convert to Integer for SageMath compatibility
    n = Integer(n)
    
    total_start_time = time.time()
    print(f"Attempting to factor large semiprime:\n{n}")
    
    # Stage 1: Direct factorization
    direct_start_time = time.time()
    try:
        factors = factor(n)
        direct_time = time.time() - direct_start_time
        print(f"Factors found via direct factorization in {direct_time:.2f} seconds: {factors}")
        total_time = time.time() - total_start_time
        print(f"Total factorization time: {total_time:.2f} seconds")
        return [Integer(p) for p, _ in factors]
    except Exception as e:
        direct_time = time.time() - direct_start_time
        print(f"Direct factorization failed in {direct_time:.2f} seconds: {e}")
    
    # Stage 2: Check small primes
    small_start_time = time.time()
    print(f"Checking small primes...")
    small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]
    for p in small_primes:
        if n % p == 0:
            other = n // p
            small_time = time.time() - small_start_time
            print(f"Found factor via small primes in {small_time:.2f} seconds: {p}")
            if is_prime(other):
                total_time = time.time() - total_start_time
                print(f"Other factor is prime: {other}")
                print(f"Factorization completed in {total_time:.2f} seconds")
                return [p, other]
            else:
                # Try to factor the other part
                sub_factors = factor(other)
                total_time = time.time() - total_start_time
                print(f"Subfactors in {small_time:.2f} seconds: {sub_factors}")
                result = [p]
                for f, _ in sub_factors:
                    result.append(f)
                print(f"Factorization completed in {total_time:.2f} seconds")
                return sorted(result)
    small_time = time.time() - small_start_time
    print(f"No factors found with small primes in {small_time:.2f} seconds")
    
    # Stage 3: Special primes trial division
    trial_start_time = time.time()
    print(f"Generating special primes up to {min(int(n.sqrt()) + 1, max_prime)}")
    special_primes = generate_special_primes(min(int(n.sqrt()) + 1, max_prime))
    print(f"Trial division with special primes...")
    
    # Batch processing for efficiency
    batch_size = 1000
    total_batches = (len(special_primes) + batch_size - 1) // batch_size
    
    for batch_idx in range(total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, len(special_primes))
        current_batch = special_primes[start_idx:end_idx]
        
        print(f"Processing batch {batch_idx+1}/{total_batches} ({start_idx}-{end_idx})")
        batch_start_time = time.time()
        
        # Direct trial division on each batch
        for p in current_batch:
            if n % p == 0:
                other = n // p
                batch_time = time.time() - batch_start_time
                print(f"Found factor via trial division in batch {batch_idx+1} in {batch_time:.2f} seconds: {p}")
                if is_prime(other):
                    total_time = time.time() - total_start_time
                    print(f"Other factor is prime: {other}")
                    print(f"Factorization completed in {total_time:.2f} seconds")
                    return [p, other]
                else:
                    # If other factor isn't prime, attempt to further factor it
                    sub_factors = factor(other)
                    total_time = time.time() - total_start_time
                    print(f"Subfactors in {batch_time:.2f} seconds: {sub_factors}")
                    result = [p]
                    for f, _ in sub_factors:
                        result.append(f)
                    print(f"Complete factorization: {sorted(result)}")
                    print(f"Factorization completed in {total_time:.2f} seconds")
                    return sorted(result)
        
        batch_time = time.time() - batch_start_time
        print(f"Batch {batch_idx+1} completed in {batch_time:.2f} seconds")
    
    trial_time = time.time() - trial_start_time
    print(f"No factors found with trial division in {trial_time:.2f} seconds")
    
    # Stage 4: Finite field and cyclotomic approach (limited for large n)
    finite_start_time = time.time()
    print(f"Attempting finite field and cyclotomic approach...")
    
    # Only try finite field approaches for selected primes to save time
    selected_primes = special_primes[::10]  # Take every 10th prime to reduce computation
    
    for p in selected_primes:
        for k in range(1, max_attempts + 1):
            try:
                q = p**k
                if q > 10**6:  # Skip if field is too large to be practical
                    break
                    
                Fq = GF(q, 'a')
                Rf = PolynomialRing(Fq, 'x')
                
                # Try cyclotomic approach with limited values of m
                for m in range(3, 7):  # Limited range to save time
                    try:
                        cyclotomic = cyclotomic_polynomial(m, var='x').change_ring(Fq)
                        eval_value = cyclotomic(Integer(n % p))
                        if eval_value == 0 and n % p == 0:
                            other = n // p
                            finite_time = time.time() - finite_start_time
                            print(f"Found factor via cyclotomic in {finite_time:.2f} seconds: {p}")
                            if is_prime(other):
                                total_time = time.time() - total_start_time
                                print(f"Other factor is prime: {other}")
                                print(f"Factorization completed in {total_time:.2f} seconds")
                                return [p, other]
                            else:
                                sub_factors = factor(other)
                                total_time = time.time() - total_start_time
                                print(f"Subfactors in {finite_time:.2f} seconds: {sub_factors}")
                                result = [p]
                                for f, _ in sub_factors:
                                    result.append(f)
                                print(f"Complete factorization: {sorted(result)}")
                                print(f"Factorization completed in {total_time:.2f} seconds")
                                return sorted(result)
                    except Exception:
                        pass
            except Exception:
                break
    
    finite_time = time.time() - finite_start_time
    print(f"No factors found with finite field/cyclotomic approach in {finite_time:.2f} seconds")
    
    total_time = time.time() - total_start_time
    print(f"No factors found in {total_time:.2f} seconds")
    return []

# Run for the specific large semiprime
if __name__ == "__main__":
    # The large semiprime number from the problem
    large_semiprime = Integer("1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139")
    
    # Run the factorization
    factors = factor_large_semiprime(large_semiprime, max_prime=10000, max_attempts=2)
    
    # Display results
    print("\nRESULTS:")
    if factors:
        print(f"Factors of the large semiprime: {factors}")
        if len(factors) == 2:
            p, q = factors
            product = p * q
            print(f"Verification: {p} * {q} = {product}")
            print(f"Original number: {large_semiprime}")
            print(f"Correct factorization: {product == large_semiprime}")
    else:
        print("No factors found. Try increasing max_prime or using more advanced methods.")
