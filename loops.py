# Get input from the user
number = int(input("Enter a number: "))

# Print the multiplication table from 1 to 10
print(f"Multiplication table for {number}:")
for i in range(1, 11):
    print(f"{number} x {i} = {number * i}")