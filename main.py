iport tkinter as tk
import ast
import operator
import math

root = tk.Tk()
root.title("Modern Calculator")
root.geometry("360x540")
root.resizable(False, False)
root.configure(bg="#F4F7FB")

expression = tk.StringVar()

display = tk.Entry(
    root,
    textvariable=expression,
    font=("Arial", 25),
    justify="right",
    bg="white",
    fg="#1769AA",
    bd=0,
    relief="flat"
)
display.pack(fill="x", padx=15, pady=25, ipady=18)

def calculate():
    try:
        tree = ast.parse(expression.get(), mode="eval")

        def safe_eval(node):
            if isinstance(node, ast.Expression):
                return safe_eval(node.body)

            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value

            if isinstance(node, ast.BinOp):
                operations = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.Pow: operator.pow,
                }
                op = operations.get(type(node.op))
                if op:
                    return op(
                        safe_eval(node.left),
                        safe_eval(node.right)
                    )

            if isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -safe_eval(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return safe_eval(node.operand)

            raise ValueError("Invalid expression")

        result = safe_eval(tree)
        if not math.isfinite(result):
            raise ValueError()

        expression.set(str(result))

    except Exception:
        expression.set("Error")

def press(value):
    expression.set(expression.get() + value)

def clear():
    expression.set("")

def square_root():
    try:
        value = float(expression.get())
        if value < 0:
            raise ValueError()
        expression.set(str(math.sqrt(value)))
    except Exception:
        expression.set("Error")

buttons = [
    ["C", "(", ")", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["√", "0", ".", "="],
    ["%"]
]

blue = "#1769AA"
red = "#E85D65"
white = "#FFFFFF"

frame = tk.Frame(root, bg="#F4F7FB")
frame.pack(expand=True, fill="both", padx=12, pady=10)

for r, row in enumerate(buttons):
    frame.rowconfigure(r, weight=1)
    for c, value in enumerate(row):
        frame.columnconfigure(c, weight=1)

        color = blue
        if value == "C":
            color = red
        elif value in ["÷", "×", "-", "+", "=", "√", "%"]:
            color = "#E8F1FA"

        fg = white if color in [blue, red] else blue

        def action(v=value):
            if v == "C":
                clear()
            elif v == "=":
                calculate()
            elif v == "√":
                square_root()
            elif v == "%":
                press("/100")
            elif v == "÷":
                press("/")
            elif v == "×":
                press("*")
            else:
                press(v)

        btn = tk.Button(
            frame,
            text=value,
            font=("Arial", 18, "bold"),
            bg=color,
            fg=fg,
            activebackground="#D5E7F7",
            bd=0,
            relief="flat",
            command=action
        )

        if len(row) == 1:
            btn.grid(row=r, column=0, columnspan=4,
                     sticky="nsew", padx=4, pady=4)
        else:
            btn.grid(row=r, column=c,
                     sticky="nsew", padx=4, pady=4)

root.mainloop()
  
