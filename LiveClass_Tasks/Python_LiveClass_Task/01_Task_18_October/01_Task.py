
#Task 1:
# Take a 3 input from the user
# perform the sub, sub, mul and div on them
#------------------------------------------------------------

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
num3 = int(input("Enter third number: "))

# Performing calculations
sub_result = abs(num1) - abs(num2) - abs(num3)
add_result = abs(num1) + abs(num2) + abs(num3)
mul_result = abs(num1) * abs(num2) * abs(num3)
div_result = abs(num1) / abs(num2) / abs(num3)

# Printing the results
print("\n--- Results ---")
print(f"Subtraction ({num1} - {num2} - {num3}) = {sub_result}")
print(f"Addition ({num1} + {num2} + {num3}) = {add_result}")
print(f"Multiplication ({num1} * {num2} * {num3}) = {mul_result}")
print(f"Division ({num1} / {num2} / {num3}) = {div_result}")