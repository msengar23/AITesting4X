  
n = int(input())
# Print n! using a recursive function

def factorial(n):
    # Base case: factorial of 0 or 1 is 1
    if n == 0 or n == 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)



# Calculate and print the result
print(factorial(n))
