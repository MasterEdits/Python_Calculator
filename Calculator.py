
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

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "C" and to_unit == "F":
        return (value * 9/5) + 32
    elif from_unit == "F" and to_unit == "C":
        return (value - 32) * 5/9
    elif from_unit == "C" and to_unit == "K":
        return value + 273.15
    elif from_unit == "K" and to_unit == "C":
        return value - 273.15
    else:
        return "Invalid conversion!"

def convert_length(value, from_unit, to_unit):
    if from_unit == "m" and to_unit == "ft":
        return value * 3.28084
    elif from_unit == "ft" and to_unit == "m":
        return value / 3.28084
    elif from_unit == "km" and to_unit == "mi":
        return value * 0.621371
    elif from_unit == "mi" and to_unit == "km":
        return value / 0.621371
    else:
        return "Invalid conversion!"

def convert_weight(value, from_unit, to_unit):
    if from_unit == "kg" and to_unit == "lb":
        return value * 2.20462
    elif from_unit == "lb" and to_unit == "kg":
        return value / 2.20462
    else:
        return "Invalid conversion!"

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

        elif operator == "convert":
            conversion_type = first
            from_unit = second
            to_unit = entry_second.get()
            value = float(entry_first.get())

            if conversion_type == "temp":
                result = convert_temperature(value, from_unit, to_unit)
            elif conversion_type == "length":
                result = convert_length(value, from_unit, to_unit)
            elif conversion_type == "weight":
                result = convert_weight(value, from_unit, to_unit)
            else:
                result = "Invalid conversion type!"

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
                result = "Invalid operator!"

        label_result.config(text=f"Result: {result}")
        history.append(f"{first} {operator} {second} = {result}")
        save_history(history)
        show_history()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")
    except ZeroDivisionError:
        messagebox.showerror("Error", "Cannot divide by zero!")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error! Check your connection.")
    except KeyError:
        messagebox.showerror("Error", "Currency code not found. Use USD, EUR, CAD, etc.")

def show_history():
    history_text = "\n".join(history[-5:])
    label_history.config(text=f"History:\n{history_text}")

root = tk.Tk()
root.title("Amirmahdi's Calculator")
root.geometry("450x650")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

title_font = ("Arial", 18, "bold")
label_font = ("Arial", 12)
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

tk.Label(root, text="Python Calculator", font=title_font, bg="#1e1e1e", fg="#00ff88").pack(pady=15)

tk.Label(root, text="First Number / Currency / Conversion Type:", font=label_font, bg="#1e1e1e", fg="white").pack(pady=5)
entry_first = tk.Entry(root, font=entry_font, width=30, bg="#2d2d2d", fg="white", insertbackground="white")
entry_first.pack(pady=5)

tk.Label(root, text="Operator (+ - * / ** % // currency convert):", font=label_font, bg="#1e1e1e", fg="white").pack(pady=5)
entry_operator = tk.Entry(root, font=entry_font, width=30, bg="#2d2d2d", fg="white", insertbackground="white")
entry_operator.pack(pady=5)

tk.Label(root, text="Second Number / Currency / From Unit:", font=label_font, bg="#1e1e1e", fg="white").pack(pady=5)
entry_second = tk.Entry(root, font=entry_font, width=30, bg="#2d2d2d", fg="white", insertbackground="white")
entry_second.pack(pady=5)

tk.Button(root, text="Calculate", command=calculate, font=button_font, bg="#00ff88", fg="#1e1e1e", width=20).pack(pady=15)

label_result = tk.Label(root, text="Result: ", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="#00ff88")
label_result.pack(pady=10)

label_history = tk.Label(root, text="History:\n", font=("Arial", 10), bg="#1e1e1e", fg="white", justify="left")
label_history.pack(pady=10)

show_history()
root.mainloop()
