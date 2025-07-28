print("Welcome to Basic Calculator")


# Take two values from user
val1 = float(input("Enter first value: "))
val2 = float(input("Enter second value: "))


# Arithmetic Operations
print("\nArithmetic Operations:")
print(f"Addition: {val1 + val2}")
print(f"Subtraction: {val1 - val2}")
print(f"Multiplication: {val1 * val2}")
if val2 != 0:
    print(f"Division: {val1 / val2}")
else:
    print("Division: Cannot divide by zero.")

# Assignment Operations
print("\nAssignment Operations:")
a = val1
b = val2
a += 5
b += 5
print(f"Value 1 after +=5: {a}")
print(f"Value 2 after +=5: {b}")


# Comparison Operations
print("\nComparison Operations:")
print(f"val1 > val2: {val1 > val2}")
print(f"val1 < val2: {val1 < val2}")
print(f"val1 == val2: {val1 == val2}")
print(f"val1 != val2: {val1 != val2}")


# Logical Operations
print("\nLogical Operations:")
print(f"val1 and val2: {bool(val1) and bool(val2)}")
print(f"val1 or val2: {bool(val1) or bool(val2)}")
print(f"not val1: {not bool(val1)}")
print(f"not val2: {not bool(val2)}")

