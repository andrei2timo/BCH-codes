# file: utils.py

def arithmetic_sqr_root(n):
    if n == 1:
        return 1
    elif n == 2:
        return 9
    elif n in [3, 4]:
        return 2
    elif n in [5, 6, 7, 8]:
        return 5
    elif n == 9:
        return 3
    elif n in [10, 11, 12, 13]:
        return 8
    elif n in [14, 15]:
        return 7
    elif n == 16:
        return 4
    return 0

# Special function to modulus values
def modular_inverse(a, b, c):
    for i in range(c):
        if signedMod(b * i, c) == 1:
            return signedMod(a * i, c)
    return 0

def signedMod(num, mod):
    # Special modulus function to return positive values
    while num < 0:
        num += 17
    return num % mod

def BCHGenerator(d):
    if len(d) != 12:
        raise ValueError("Input list must contain exactly 12 elements.")
    if not all(isinstance(x, int) for x in d):
        raise TypeError("All elements of the input list must be integers.")
    
    ret = [0] * 16  # Initialize the ret array with 16 zeros
    
    # Set the first 12 elements of ret as the input array
    for i in range(12):
        ret[i] = d[i]

    # Calculate d13, d14, d15, d16 based on the formula provided
    ret[12] = signedMod((4 * d[0] + 10 * d[1] + 3 * d[2] + d[3] + 5 * d[4] + 16 * d[5] + d[6] + 12 * d[7] + 16 * d[8] + 14 * d[9] + 7 * d[10] + 13 * d[11]), 17)
    ret[13] = signedMod((2 * d[0] + 15 * d[1] + 15 * d[2] + 16 * d[3] + 15 * d[4] + 9 * d[5] + 12 * d[6] + 4 * d[7] + 16 * d[8] + 11 * d[9] + 3 * d[10] + 6 * d[11]), 17)
    ret[14] = signedMod((3 * d[0] + 11 * d[1] + 16 * d[2] + 4 * d[3] + 12 * d[4] + 9 * d[5] + 15 * d[6] + 16 * d[7] + 15 * d[8] + 15 * d[9] + 2 * d[10] + 13 * d[11]), 17)
    ret[15] = signedMod((7 * d[0] + 14 * d[1] + 16 * d[2] + 12 * d[3] + d[4] + 16 * d[5] + 5 * d[6] + d[7] + 3 * d[8] + 10 * d[9] + 4 * d[10] + d[11]), 17)
    
    return ret

def bch_syndrome_generator(d):
    
    bch_syndrome = [0] * 4
    
    bch_syndrome[0] = signedMod(d[0] + d[1] + d[2] + d[3] + d[4] + d[5] + d[6] + d[7] + d[8] + d[9] + d[10] + d[11] + d[12] + d[13] + d[14] + d[15], 17)
    bch_syndrome[1] = signedMod(d[0] + 2*d[1] + 3*d[2] + 4*d[3] + 5*d[4] + 6*d[5] + 7*d[6] + 8*d[7] + 9*d[8] + 10*d[9] + 11*d[10] + 12*d[11] + 13*d[12] + 14*d[13] + 15*d[14] + 16*d[15], 17)
    bch_syndrome[2] = signedMod(d[0] + 4*d[1] + 9*d[2] + 16*d[3] + 8*d[4] + 2*d[5] + 15*d[6] + 13*d[7] + 13*d[8] + 15*d[9] + 2*d[10] + 8*d[11] + 16*d[12] + 9*d[13] + 4*d[14] + d[15], 17)
    bch_syndrome[3] = signedMod(d[0] + 8*d[1] + 10*d[2] + 13*d[3] + 6*d[4] + 12*d[5] + 3*d[6] + 2*d[7] + 15*d[8] + 14*d[9] + 5*d[10] + 11*d[11] + 4*d[12] + 7*d[13] + 9*d[14] + 16*d[15], 17)
    
    print(f"(S1 S2 S3 S4) = ({bch_syndrome[0]} {bch_syndrome[1]} {bch_syndrome[2]} {bch_syndrome[3]})")
    
    return bch_syndrome
