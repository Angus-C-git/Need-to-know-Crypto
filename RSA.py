from random import randrange, getrandbits


def check_primality(candidate, test_cycles=128):
    # Check for basic primes (We don't want these since they will produce a key which is to easy to reverse
    if candidate == 2 or candidate == 3:
        return False

    # Check if the candidate is a smaller number than one or even (even numbers cannot be prime)
    if candidate <= 1 or candidate % 2 == 0:
        return False

    # Use Miller-Rabin's test to determine primality
    count = 0
    r = candidate - 1
    while r & 1 == 0:
        count += 1
        r //= 2

    # begin test_cycles
    for _ in range(test_cycles):
        a = randrange(2, candidate - 1)
        x = pow(a, r, candidate)
        if x != 1 and x != candidate - 1:
            j = 1
            while j < count and x != candidate - 1:
                x = pow(x, 2, candidate)
                if x == 1:
                    return False
                j += 1
            if x != candidate - 1:
                return False
    return True


def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1

    return p


def find_co_prime(cp, n):
    if n == 0:
        return cp
    else:
        return find_co_prime(n, cp % n)


def derive_keys(length=8):  # Default key len is low for testing
    p = 4  # arbitrary non primes
    q = 4

    while not check_primality(p):
        p = generate_prime_candidate(length)
    while not check_primality(q):
        q = generate_prime_candidate(length)

    # Check they are not the same
    if p == q:
        derive_keys(length)
    print("p:", p)
    print("q:", q)
    # generate n variable for further calculations
    n = p * q

    # Assign a variable equal to the p,q function input into euler's totient function
    euler_totient = (p - 1) * (q - 1)  # compute euler's totient
    # print(euler_totient)
    # ---- Generate a number between 1 and euler's totient, which is not co-prime of the totient value ----

    public_key = 0
    # Generate factors of euler's totient
    for number in range(randrange(2, 1000), euler_totient):  # Picks a random number to try for co-primality
        # Check if the candidate number is a factor
        if find_co_prime(number, euler_totient) == 1:  # If its not a factor
            public_key = number  # Assign the public key value to be this valid candidate
            break

    # Find a multiple of the public key which obtains a remainder of 1 when modulated with euler's totient
    # private_key = int((euler_totient + 1) // public_key)  # derive PK
    private_key = 0
    for num in range(1, 1000):
        pk_candidate = 1 + (num * euler_totient)
        if pk_candidate % public_key == 0:
            private_key = int(pk_candidate / public_key)

    return public_key, private_key, n


def decrypt(cipher_text, private_key, n):
    print("The recipient (public key owner) can then use the formula cipher_text^private_key % n, to produce the "
          "plaintext")
    print("\nIn this case the owners private key is", private_key)
    decrypted_plain_text = []
    for char in cipher_text:
        decrypted_plain_text.append(pow(char, private_key) % n)
    decrypted_plain_text = ''.join(chr(c) for c in decrypted_plain_text)
    print("Decrypted plaintext:", decrypted_plain_text)


def encrypt(plain_text):
    print("\nConvert the plain text to a integer value (string of ASCII values)")
    ascii_val_array = [ord(c) for c in plain_text]
    print("Giving us the integer representation of the plaintext as", ascii_val_array)
    keys = derive_keys()

    print("We can then encrypt the text with our recipients public key", keys[0])
    print("We use the formula plaintext^public_key % n, where n in our two large primes p & q (see 1.)\n")
    cipher_text = []

    for char in ascii_val_array:
        cipher_text.append(pow(char, keys[0]) % keys[2])
    print("This gives us the cipher txt", ''.join(chr(c) for c in cipher_text), '\n')

    print("We send this to the owner of the public key, that is the person we wish to communicate with securely")
    decrypt(cipher_text, keys[1], keys[2])


def main():
    print(" --- Welcome to the Interactive RSA calculator --\n")
    print("~The RSA algorithm is used to help generate shared secrets securely for further communications\n\n")

    print("1. Generate a key pair")
    print("2. Learn how to encrypt & decrypt a message with RSA")

    choice = input("Enter a number listed above to begin ~> ")
    if choice == "1":
        derive_keys()
    if choice == "2":
        plain_text = str(input("Enter a msg to be encrypted: "))
        encrypt(plain_text)


main()

"""


The goal of Miller-Rabin is to find a nontrivial square roots of 1 modulo n.

Take back the Fermat’s little theorem: a^(n-1) = 1 (mod n).

For Miller-Rabin, we need to find r and s such that (n-1) = r*(2^s), with r odd.

Then, we pick a, an integer in the range [1, n-1].

    If a^r != 1 (mod n) and a^((2^j)r) != -1 (mod n) for all j such that 0 ≤ j ≤ s-1, then n is not prime and a is 
    called a strong witness to composites for n. 
    
    In the other hand, if a^r = 1 (mod n) or a^((2^j)r) = -1 (mod n) 
    for some j such as 0 ≤ j ≤ s-1, then n is said to be a strong pseudo-prime to the base a, and a is called a 
    strong liar to primality for n. 

"""
