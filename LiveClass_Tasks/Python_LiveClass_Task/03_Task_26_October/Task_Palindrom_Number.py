# Read the input from the user
user_input = input("Enter a string or number: ")

# Remove spaces and convert to lowercase to ensure the check is case-insensitive
cleaned_input = user_input.replace(" ", "").lower()

# Check if the cleaned string is equal to its reverse
if cleaned_input == cleaned_input[::-1]:
    print(f"'{user_input}' is a palindrome.")
else:
    print(f"'{user_input}' is not a palindrome.")