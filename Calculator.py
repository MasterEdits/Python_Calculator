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

def convert_unit(value, from_unit, to_unit):
    # Length
    if from_unit == "km" and to_unit == "miles":
        return value * 0.621371
    elif from_unit == "miles" and to_unit == "km":
        return value / 0.621371
    elif from_unit == "m" and to_unit == "ft":
        return value * 3.28084
    elif from_unit == "ft" and to_unit == "m":
        return value / 3.28084
    elif from_unit == "cm" and to_unit == "inch":
        return value * 0.393701
    elif from_unit == "inch" and to_unit == "cm":
        return value / 0.393701
    elif from_unit == "mm" and to_unit == "cm":
        return value / 10
    elif from_unit == "cm" and to_unit == "mm":
        return value * 10

    # Weight
    elif from_unit == "kg" and to_unit == "lbs":
        return value * 2.20462
    elif from_unit == "lbs" and to_unit == "kg":
        return value / 2.20462
    elif from_unit == "g" and to_unit == "oz":
        return value * 0.035274
    elif from_unit == "oz" and to_unit == "g":
        return value / 0.035274
    elif from_unit == "ton" and to_unit == "kg":
        return value * 1000
    elif from_unit == "kg" and to_unit == "ton":
        return value / 1000

    # Volume
    elif from_unit == "l" and to_unit == "ml":
        return value * 1000
    elif from_unit == "ml" and to_unit == "l":
        return value / 1000
    elif from_unit == "l" and to_unit == "gallon":
        return value * 0.264172
    elif from_unit == "gallon" and to_unit == "l":
        return value / 0.264172

    # Temperature
    elif from_unit == "c" and to_unit == "f":
        return (value * 9/5) + 32
    elif from_unit == "f" and to_unit == "c":
        return (value - 32) * 5/9

    else:
        return "Invalid conversion type!"

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
                history_entry = f"{first.upper()} to {second.upper()} = {result}"
            else:
                result = "Invalid currency code!"
                history_entry = f"{first} {operator} {second} = {result}"

        elif operator == "convert":
            parts = first.split()
            value = float(parts[0])
            from_unit = parts[1].lower()
            to_unit = second.lower()
            result = convert_unit(value, from_unit, to_unit)
            history_entry = f"{value} {from_unit} convert to {to_unit} = {result}"

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

            history_entry = f"{first} {operator} {second} = {result}"

        label_result.config(text=f"Result: {result}", fg="#00ff00")
        history.append(history_entry)
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
    except IndexError:
        messagebox.showerror("Error", "For unit conversion, enter like: 100 km")

def show_history():
    history_text = "\n".join(history[-5:])
    label_history.config(text=f"History:\n{history_text}", fg="#00ff00")

root = tk.Tk()
root.title("Amirmahdi's Calculator")
root.geometry("400x550")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

tk.Label(root, text="Python Calculator", font=("Arial", 20, "bold"), fg="#00ff00", bg="#1e1e1e").pack(pady=10)

tk.Label(root, text="First Number / Currency / Value + Unit:", fg="white", bg="#1e1e1e").pack(pady=5)
entry_first = tk.Entry(root, bg="#2e2e2e", fg="white", insertbackground="white")
entry_first.pack(pady=5)

tk.Label(root, text="Operator (+ - * / ** % // currency convert):", fg="white", bg="#1e1e1e").pack(pady=5)
entry_operator = tk.Entry(root, bg="#2e2e2e", fg="white", insertbackground="white")
entry_operator.pack(pady=5)

tk.Label(root, text="Second Number / Currency / To Unit:", fg="white", bg="#1e1e1e").pack(pady=5)
entry_second = tk.Entry(root, bg="#2e2e2e", fg="white", insertbackground="white")
entry_second.pack(pady=5)

tk.Button(root, text="Calculate", command=calculate, bg="#00ff00", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

label_result = tk.Label(root, text="Result: ", font=("Arial", 14), fg="#00ff00", bg="#1e1e1e")
label_result.pack(pady=10)

label_history = tk.Label(root, text="History:\n", font=("Arial", 10), fg="#00ff00", bg="#1e1e1e", justify="left")
label_history.pack(pady=10)

show_history()
root.mainloop()
