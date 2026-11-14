#Task 2:
# Take a 2 input from the user
# Print the Quotient and Remainder
# Example: 
# 15 ->  num1
# 2 -> num2
# Quotient -> 7
# Remainder -> 1


num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

quotient = num1 // num2
remainder = num1 % num2

print(f"Quotient: {quotient}")
print(f"Remainder: {remainder}")

