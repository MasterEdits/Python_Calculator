import requests
import os

HISTORY_FILE = "calculator_history.txt"

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
        print("  ", item)
    print()

while True:
    try:
        first_input = input("Enter first number (or currency code like USD): ")
        operator = input("Enter operator (+ - * / ** % // currency): ")
        second_input = input("Enter second number (or currency code like EUR): ")

        if operator == "currency":
            url = f"https://api.exchangerate-api.com/v4/latest/{first_input.upper()}"
            response = requests.get(url)
            data = response.json()
            rate = data["rates"].get(second_input.upper())
            if rate:
                result = rate
                operator = f"{first_input.upper()} to {second_input.upper()}"
            else:
                result = "Invalid currency code!"
        else:
            first_number = float(first_input)
            second_number = float(second_input)

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

        history.append(str(first_input) + " " + operator + " " + str(second_input) + " = " + str(result))
        print("History:", history)
        save_history(history)

    except ValueError:
        print("Invalid input! Please enter numbers only.")
    except ZeroDivisionError:
        print("Cannot divide by zero!")
    except requests.exceptions.RequestException:
        print("Network error! Please check your connection.")
    except KeyError:
        print("Currency code not found. Please use valid codes like USD, EUR, CAD.")

    again = input("Do another calculation? (yes/no): ")
    if again == "no":
        break

print("Goodbye!")
input("Press Enter to exit...")
