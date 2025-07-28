score = int(input("Enter your score :"))
grade= None
if (score>= 90):
    grade = "A"

if (score >=75 and score <= 89):
    grade = "B"

if (score >=65 and score <= 74):
    grade = "C"

print(f"Your Grade is: {grade}")