# Simple Fahrenheit to Celsius converter
print("Welcome to the Temperature Converter!")
print("You can convert temperatures between Fahrenheit and Celsius.")
print("Please enter the temperature you want to convert.")

fahrenheit = float(input("Enter temperature in Fahrenheit: "))
celsius = (fahrenheit - 32) * 5 / 9
print(celsius)


celsius = float(input("Enter temperature in Celsius: "))
fahrenheit = (celsius * 9 / 5) + 32
print(fahrenheit)

print("Thank you for using the Temperature Converter!")
# End of the temperature conversion program