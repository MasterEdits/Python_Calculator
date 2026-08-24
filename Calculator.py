
history = []

while True:
    try:
        first_number = float(input("Enter first number: "))
        operator = input("Enter operator (+ - * / ** % //): ")
        second_number = float(input("Enter second number: "))

        if operator == "+":
            result = first_number + second_number
        elif operator == "-":
            result = first_number - second_number
        elif operator == "*":
            result = first_number * second_number
        elif operator == "/":
            result = first_number / second_number
        elif operator == "**":
            result = first_number ** second_number
        elif operator == "%":
            result = first_number % second_number
        elif operator == "//":
            result = first_number // second_number
        else:
            result = "invalid operator!"

        print("Result:", result)

        history.append(str(first_number) + " " + operator + " " + str(second_number) + " = " + str(result))
        print("History:", history)

    except ValueError:
        print("Invalid input! Please enter numbers only.")
    except ZeroDivisionError:
        print("Cannot divide by zero!")

    again = input("Do another calculation? (yes/no): ")
    if again == "no":
        break

print("Goodbye!")
input("Press Enter to exit...")
