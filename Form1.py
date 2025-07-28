print("Welcome To My Restaurant")
print("Please Enter Your Info")

# Ensure name is not numeric
while True:
    name = input("Enter your name: ")
    if not name.isnumeric() and name.strip() != "":
        break
    print("Name cannot be numeric. Please enter a valid name.")

# Ensure age is numeric
while True:
    age = input("Enter your age: ")
    if age.isdigit():
        break
    print("Age must be a number. Please enter a valid age.")

# Ensure address is not numeric
while True:
    address = input("Enter your address: ")
    if not address.isnumeric() and address.strip() != "":
        break
    print("Address cannot be numeric. Please enter a valid address.")

print(f"Your name is {name}, your age is {age}, your address is {address}")

print("Welcome to the BMI Calculator")

# Get valid weight (in kilograms)
while True:
    weight = input("Enter your weight in kilograms: ")
    try:
        weight = float(weight)
        if weight > 0:
            break
        else:
            print("Weight must be a positive number.")
    except ValueError:
        print("Please enter a valid number for weight.")

# Get valid height (in feet)
while True:
    height_ft = input("Enter your height in feet: ")
    try:
        height_ft = float(height_ft)
        if height_ft > 0:
            # Convert feet to meters (1 foot = 0.3048 meters)
            height = height_ft * 0.3048
            break
        else:
            print("Height must be a positive number.")
    except ValueError:
        print("Please enter a valid number for height.")

# Calculate BMI
bmi = weight / (height ** 2)
print(f"Your BMI is: {bmi:.2f}")

# Optional: Give a BMI category
if bmi < 18.5:
    print("You are underweight.")
elif 18.5 <= bmi < 25:
    print("You have a normal weight.")
elif 25 <= bmi < 30:
    print("You are overweight.")
else:
    print("You are obese.")

