import math
from random import *
import time


start_time = time.time()

#
#   Finds a list of primes within the LIMIT
#   then returns a list of the last X primes
#
def primes_sieve(limit, x):
    limitn = limit+1

    not_prime = [False] * limitn
    primes = []

    for i in range(2, limitn):
        if not_prime[i]:
            continue
        for f in range(i*2, limitn, i):
            not_prime[f] = True

        primes.append(i)
        
    start = len(primes) - x

    return primes[start:limitn]


#
#   picks x amount of random values in a list
#
def pick_primes(primes, x):
    picks = []

    i = 0
    while i < x:
        picks.append(primes[randint(0, len(primes)-1)])
        i += 1

    return picks

#
#   picks one random value in a list
#
def pick_prime(primes):

    return primes[randint(0, len(primes)-1)]


def check_coprime(a,b):
    while b: #while b != 0
        a,b = b, a%b

    return a == 1

def find_e(totient):
    
    coprimes = []
    i = 2

    while i < totient:
        if(check_coprime(i,totient)):
            coprimes.append(i)
        
        i += 1

    return pick_prime(coprimes)

#
#   inverse modulus function, thx to Mart Bakhoff
#
# returns (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)
    
# x = mulinv(b) mod n, (x * b) % n == 1
def mod_inv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


    

def find_d(e, totient):

    return mod_inv(e,totient)
    '''
    d = 0
    while ((d * e) % totient) != 1:
        print((d * e) % totient)
        d += 1

    return d
    '''


##
## RSA
##
class GenerateRSA:

    # needs better arguments
    def __init__(self, prime_range, top_sift):
        self.prime_range = prime_range
        self.top_sift = top_sift

        print("Picking 2 primes between 1 and ", prime_range)
        print("Only chooses from the last ",top_sift, " prime numers in the range")

        self.d = None
        
        while self.d is None:
            # find these primes!
            self.primes =  primes_sieve(prime_range,top_sift)

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

        self.public = [self.e, self.n]
        self.private = [self.d, self.n]
    

    def encrypt_int(self,m):
        return pow(m, self.e) % self.n

    def decrypt_int(self,c):
        return pow(c, self.d) % self.n

    def encrypt_string(self, string):
        result = []
    
        for char in string:
            result.append(self.encrypt_int(ord(char)))

        return result
                          

    def decrypt_string(self, data):
        result = []

        for var in data:
            result.append(chr(self.decrypt_int(var)))

        return ''.join(result)

    

class RSA:
    
    def __init__(self, public, private):
        self.public = public
        self.private = private
    
    def en_int(self,message):
        return pow(message, self.public[0]) % self.public[1]

    def de_int(self,crypt):
        return pow(crypt, self.private[0]) % self.private[1]

    def encrypt(self, string):
        result = []
    
        for char in string:
            result.append(self.en_int(ord(char)))

        return result
                          

    def decrypt(self, data):
        result = []

        for var in data:
            result.append(chr(self.de_int(var)))

        return ''.join(result)


#
#   Finds a list of primes within the LIMIT
#   then returns a list of the last X primes
#

'''
key = GenerateRSA(1000,100)
print("Public Key =", key.public)
print("Private Key =", key.private)
secure = RSA(key.public, key.private)
print(secure.encrypt("ZIZY MACK"))
'''

secure = RSA(None,[423853, 850441])
print(secure.decrypt([769715, 236168, 769715, 498592, 520419, 184163, 380665, 288383, 329917]))

                          
'''
print(key.encrypt_int(encrypted))
print(key.decrypt_int(encrypted))

string = key.encrypt_string("This is a secure line bitch")
print(string)
print(key.decrypt_string(string))
'''



print("--- %s seconds ---" % (time.time() - start_time))




