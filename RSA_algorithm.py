import math
from random import *
import time

#   /   /   /   /   /   /   /   /   /   /   
#
#   Finds a list of primes within the LIMIT
#   then returns a list of the last X primes
#
#   Thanks to Glenn Maynard
def primes_sieve(limit, x):
    limitn = limit+1

    not_prime = [False] * limitn
    primes = []

    for i in range(2, limitn):
        if not_prime[i]:
            continue
        for f in range(i*i, limitn, i):
            not_prime[f] = True

        primes.append(i)
        
    start = len(primes) - x

    return primes[start:limitn]

#   /   /   /   /   /   /   /   /   /   /   /
#
#   picks x amount of random values in a list
def pick_primes(primes, x):
    picks = []

    i = 0
    while i < x:
        picks.append(primes[randint(0, len(primes)-1)])
        i += 1

    return picks

#   /   /   /   /   /   /   /   /   /
#
#   picks one random value in a list
def pick_prime(primes):
    return primes[randint(0, len(primes)-1)]


#   /   /   /   /   /   /   /   /   /   
#
#   checks if two numbers are coprime
def check_coprime(a,b):
    while b: #while b != 0
        a,b = b, a%b

    return a == 1


#   /   /   /   /   /   /   /   /   /   
#
#   finds the 1st private key value, e
def find_e(totient):
    
    coprimes = []
    i = 2
    
    # makes a list of coprimes between 1 and the totient
    while i < totient:
        if(check_coprime(i,totient)):
            coprimes.append(i)
        
        i += 1
    
    # return a randomly selected coprime
    return pick_prime(coprimes)

#   /   /   /   /   /   /   /   /   /   /   /   /     
#
#   inverse modulus function, thx to Mart Bakhoff
#   returns (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)
    
# x = mod_inv(b) mod n, (x * b) % n == 1
def mod_inv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

    
#   /   /   /   /   /   /   /   /   /   /
#
#   finds the 1st private key value, d
#	by calculating d = mod_inv(e) mod totient(n)
def find_d(e, totient):

    return mod_inv(e,totient)


##  /  /   /   /   /   /   /   /   /   /   /   /   /   /
##
##  CLASS: GenerateKey
##
##  generates an RSA key by selecting two random primes, p and q, from the
## 	range, "prime_range," while only considering the last "last_primes."
##	Then, n is calculated by multiplying them together. Next, a totient(n) is 	
##	calculated from: (p-1)*(q-1). Now, e is found by chosing a number that
##	satisfies 1 < e < totient(n) AND is also coprime to n. Finally, d is found 
##	by solving (d * e) % totient(n) = 1
##
##	the public key consists of e,n
##	the private key consists of d,n
class GenerateKey:

    def __init__(self, prime_range, last_primes):
        self.prime_range = prime_range
        self.last_primes = last_primes

        print("Picking 2 primes between 1 and ", prime_range)
        print("Only chooses from the last ",last_primes, " prime numers in the range")

        self.d = None
        
        while self.d is None:
            # find those primes!
            self.primes =  primes_sieve(prime_range,last_primes)
			
			# calculates p,q,b,totient(n),e, and d
            self.p = pick_prime(self.primes)
            self.q = pick_prime(self.primes)
            self.n = self.p * self.q
            self.totient = (self.p-1)*(self.q-1)
            self.e = find_e(self.totient)
            #uses Extended Euclidean algorithm
            self.d = find_d(self.e, self.totient)

        #
        print ("p = ", self.p)
        print ("q = ", self.q)
        print ("n = ", self.n)
        print("totient = ", self.totient)
        print("e = ", self.e)
        print("d = ", self.d)
        #
		
		# assigns the private and public key pairs
        self.public = [self.e, self.n]
        self.private = [self.d, self.n]

        
##  /  /   /   /   /   /   /   /   /   /   /   /   /   /
##
##  CLASS: RSA
##
##  encrypt and decrypt functions with private/public key
class RSA:
    
	# gets the public and private variables 
	# which are each stored as a pair of integers
	# in an array
	#
	# public[0]  = e | public[1]  = n
	# private[0] = d | private[1] = n
	#
    def __init__(self, public, private):

        self.public = public
		# uses the python naming convention for a private variable
        self.__private = private
    
    # encrypt an integer
	# (x ^ e) % n
    def en_int(self,message):
        return pow(message, self.public[0]) % self.public[1]
    
    # decrypt an integer
	# (x ^ d) % n
    def de_int(self,crypt):
        return pow(crypt, self.__private[0]) % self.__private[1]
    
    # encrypt a string
    def encrypt(self, string):
        result = []

    	# turns each character into its ascii value,
		# then uses en_int() to encrypt it and appends
		# it to result
        for char in string:
            result.append(self.en_int(ord(char)))

        return result
           
	# decrypt a string             
    def decrypt(self, data):
        result = []

		# takes in an array of integers that was encrypted,
		# decrypts them with de_int, turns it into a char and
		# appends it to result
        for var in data:
            result.append(chr(self.de_int(var)))

        return ''.join(result)


#
# MAIN PROCESS
#
# Generates a key pair using two random primes from 900 - 1000
# then prints the encrypted message -> "This is a secure message"
# Next, decrypts the message and prints it to the console

# START THE CLOCK!
start_time = time.time()

# the larger the range for the primes, the longer this whole
# process will take, however, the encryption will be stronger
key = GenerateKey(1000,100)
print("Public Key =", key.public)
print("Private Key =", key.private, "\n")
secure = RSA(key.public, key.private)
crypt = secure.encrypt("This is a secure message")
print ("The encrypted message:")
print (crypt, "\n")
print ("The decrypted message:")
print (secure.decrypt(crypt), "\n")

# How long did this take?
print("--- This took %s seconds ---" % (time.time() - start_time))
