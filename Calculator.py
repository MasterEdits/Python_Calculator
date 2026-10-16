import tkinter as tk
from tkinter import messagebox
import requests
import os
import math

HISTORY_FILE = "calculator_history.txt"
memory = 0

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
    if from_unit == "km" and to_unit == "miles":
        return value * 0.621371
    elif from_unit == "miles" and to_unit == "km":
        return value / 0.621371
    elif from_unit == "m" and to_unit == "ft":
        return value * 3.28084
    elif from_unit == "ft" and to_unit == "m":
        return value / 3.28084
    elif from_unit == "kg" and to_unit == "lbs":
        return value * 2.20462
    elif from_unit == "lbs" and to_unit == "kg":
        return value / 2.20462
    elif from_unit == "c" and to_unit == "f":
        return (value * 9/5) + 32
    elif from_unit == "f" and to_unit == "c":
        return (value - 32) * 5/9
    else:
        return "Invalid conversion type!"

def button_click(char):
    current = entry_display.get()
    entry_display.delete(0, tk.END)
    entry_display.insert(0, current + str(char))

def clear_display():
    entry_display.delete(0, tk.END)

def calculate():
    try:
        expression = entry_display.get()
        expression = expression.replace("sqrt", "math.sqrt")
        expression = expression.replace("sin", "math.sin")
        expression = expression.replace("cos", "math.cos")
        expression = expression.replace("tan", "math.tan")
        expression = expression.replace("log", "math.log")
        result = eval(expression)
        entry_display.delete(0, tk.END)
        entry_display.insert(0, str(result))
        history.append(f"{expression} = {result}")
        save_history(history)
        show_history()
    except ZeroDivisionError:
        entry_display.delete(0, tk.END)
        entry_display.insert(0, "Cannot divide by zero!")
    except Exception:
        entry_display.delete(0, tk.END)
        entry_display.insert(0, "Invalid input!")

def memory_add():
    global memory
    try:
        memory += float(entry_display.get())
    except:
        pass

def memory_subtract():
    global memory
    try:
        memory -= float(entry_display.get())
    except:
        pass

def memory_recall():
    entry_display.delete(0, tk.END)
    entry_display.insert(0, str(memory))

def memory_clear():
    global memory
    memory = 0

def currency_convert():
    try:
        parts = entry_display.get().split()
        first = parts[0].upper()
        second = parts[1].upper()
        url = f"https://api.exchangerate-api.com/v4/latest/{first}"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"].get(second)
        if rate:
            entry_display.delete(0, tk.END)
            entry_display.insert(0, str(rate))
            history.append(f"{first} to {second} = {rate}")
            save_history(history)
            show_history()
        else:
            entry_display.delete(0, tk.END)
            entry_display.insert(0, "Invalid currency code!")
    except Exception:
        entry_display.delete(0, tk.END)
        entry_display.insert(0, "Error!")

def unit_convert():
    try:
        parts = entry_display.get().split()
        value = float(parts[0])
        from_unit = parts[1].lower()
        to_unit = parts[2].lower()
        result = convert_unit(value, from_unit, to_unit)
        entry_display.delete(0, tk.END)
        entry_display.insert(0, str(result))
        history.append(f"{value} {from_unit} to {to_unit} = {result}")
        save_history(history)
        show_history()
    except Exception:
        entry_display.delete(0, tk.END)
        entry_display.insert(0, "Invalid conversion!")

def show_history():
    history_text = "\n".join(history[-5:])
    label_history.config(text=f"History:\n{history_text}")

root = tk.Tk()
root.title("Amirmahdi's Calculator")
root.geometry("450x700")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

entry_display = tk.Entry(root, font=("Arial", 20), bg="#2e2e2e", fg="#00ff00", insertbackground="white", justify="right")
entry_display.grid(row=0, column=0, columnspan=5, padx=10, pady=20, ipadx=8, ipady=10)

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sqrt', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('**', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('%', 3, 4),
    ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3), ('//', 4, 4),
    ('(', 5, 0), (')', 5, 1), ('C', 5, 2), ('sin', 5, 3), ('cos', 5, 4),
    ('tan', 6, 0), ('log', 6, 1), ('M+', 6, 2), ('M-', 6, 3), ('MR', 6, 4),
]

for (text, row, col) in buttons:
    if text == "=":
        btn = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#00ff00", fg="black", command=calculate)
    elif text == "C":
        btn = tk.Button(root, text=text, font=("Arial", 16, "bold"), bg="#ff4444", fg="white", command=clear_display)
    elif text == "M+":
        btn = tk.Button(root, text=text, font=("Arial", 14), bg="#4444ff", fg="white", command=memory_add)
    elif text == "M-":
        btn = tk.Button(root, text=text, font=("Arial", 14), bg="#4444ff", fg="white", command=memory_subtract)
    elif text == "MR":
        btn = tk.Button(root, text=text, font=("Arial", 14), bg="#4444ff", fg="white", command=memory_recall)
    else:
        btn = tk.Button(root, text=text, font=("Arial", 14), bg="#2e2e2e", fg="white", command=lambda t=text: button_click(t))
    btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew", ipadx=5, ipady=8)

tk.Button(root, text="Currency (USD EUR)", command=currency_convert, bg="#00ff00", fg="black").grid(row=7, column=0, columnspan=2, pady=5, sticky="nsew")
tk.Button(root, text="Convert (100 km miles)", command=unit_convert, bg="#00ff00", fg="black").grid(row=7, column=2, columnspan=3, pady=5, sticky="nsew")

label_history = tk.Label(root, text="History:\n", font=("Arial", 10), fg="#00ff00", bg="#1e1e1e", justify="left")
label_history.grid(row=8, column=0, columnspan=5, pady=10)

show_history()
root.mainloop()
