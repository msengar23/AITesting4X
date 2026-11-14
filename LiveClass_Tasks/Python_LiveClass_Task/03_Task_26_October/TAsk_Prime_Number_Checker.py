import math

def is_prime(num):
    # Numbers less than or equal to 1 are not prime
    if num <= 1:
        return False
    
    # Loop from 2 up to the square root of num
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
            
    return True

# Read the input number
num = int(input())

# Print YES or NO based on the primality check

if is_prime(num):
    print("YES")
else:
    print("NO")