print("=" * 50)
print("           BMI CALCULATOR")
print("=" * 50)

try:
    weight = float(input("Enter your weight in kilograms: "))
    height = float(input("Enter your height in meters: "))

    if weight <= 0 or height <= 0:
        print("Weight and height must be greater than zero.")

    else:
        bmi = weight / (height ** 2)

        print("\nYour BMI is:", round(bmi, 2))

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        print("BMI Category:", category)

except ValueError:
    print("Invalid input. Please enter numbers only.")

print("\nThank you for using the BMI Calculator!")