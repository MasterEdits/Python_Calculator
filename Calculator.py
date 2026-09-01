import os

HISTORY_FILE = "Calculator_history.txt"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return file.read().splitlines()
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        for item in history:
            file.write(item + "\n")

history = load_history()

if history:
    print("Previous History:")
    for item in history:
        print(" ", item)
    print()

while True:
    try:
        first_number = float(input("Enter first number: "))
        operator = input("Enter operator (+ - * / // ** %): ")
        second_number = float(input("Enter second number: "))

        if operator == "+":
            result = first_number + second_number
        elif operator == "-":
            result = first_number - second_number
        elif operator == "*":
            result = first_number * second_number
        elif operator == "/":
            result = first_number / second_number
        elif operator == "//":
            result = first_number // second_number
        elif operator == "**":
            result = first_number ** second_number
        elif operator == "%":
            result = first_number % second_number
        else:
            result = "Invalid operator!"

        print("Result:", result)

        history.append(str(first_number) + " " + operator + " " + str(second_number) + " = " + str(result))
        print("History:", history)

        save_history(history)

    except ValueError:
        print("Invalid input! Please enter numbers only.")
    except ZeroDivisionError:
        print("Cannot divide by zero!")

    again = input("Do another Calculation? (yes/no): ")
    if again == "no":
        break

print("Goodbye!")
input("Press Enter to exit...")
