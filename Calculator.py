
import tkinter as tk
from tkinter import messagebox
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

def calculate():
    try:
        first = entry_first.get()
        operator = entry_operator.get()
        second = entry_second.get()

        if operator == "currency":
            url = f"https://api.exchangerate-api.com/v4/latest/{first.upper()}"
            response = requests.get(url)
            data = response.json()
            rate = data["rates"].get(second.upper())
            if rate:
                result = rate
                operator = f"{first.upper()} to {second.upper()}"
            else:
                result = "Invalid currency code!"
        else:
            first_number = float(first)
            second_number = float(second)

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

        label_result.config(text=f"Result: {result}")
        history.append(str(first) + " " + operator + " " + str(second) + " = " + str(result))
        save_history(history)
        show_history()

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter numbers only.")
    except ZeroDivisionError:
        messagebox.showerror("Error", "Cannot divide by zero!")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error! Please check your connection.")
    except KeyError:
        messagebox.showerror("Error", "Currency code not found. Use USD, EUR, CAD, etc.")

def show_history():
    history_text = "\n".join(history[-5:])  # show last 5
    label_history.config(text=f"History:\n{history_text}")

# GUI Setup
root = tk.Tk()
root.title("Python Calculator")
root.geometry("400x500")
root.resizable(False, False)

tk.Label(root, text="First Number / Currency:").pack(pady=5)
entry_first = tk.Entry(root)
entry_first.pack(pady=5)

tk.Label(root, text="Operator (+ - * / ** % // currency):").pack(pady=5)
entry_operator = tk.Entry(root)
entry_operator.pack(pady=5)

tk.Label(root, text="Second Number / Currency:").pack(pady=5)
entry_second = tk.Entry(root)
entry_second.pack(pady=5)

tk.Button(root, text="Calculate", command=calculate).pack(pady=10)

label_result = tk.Label(root, text="Result: ", font=("Arial", 14))
label_result.pack(pady=10)

label_history = tk.Label(root, text="History:\n", font=("Arial", 10), justify="left")
label_history.pack(pady=10)

show_history()
root.mainloop()
