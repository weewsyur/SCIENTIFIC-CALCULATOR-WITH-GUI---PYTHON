from tkinter import *
import math
from asteval import Interpreter

# ────────── FUNCTIONS AND OPERATIONS ──────────

def button_click(char):
    global calc_operator
    calc_operator += str(char)
    text_input.set(calc_operator)

def button_clear_all():
    global calc_operator
    calc_operator = ""
    text_input.set("")

def button_delete():
    global calc_operator
    calc_operator = calc_operator[:-1]
    text_input.set(calc_operator)

def floor_func():
    global calc_operator
    try:
        result = str(math.floor(float(calc_operator)))
        calc_operator = result
        text_input.set(result)
    except:
        text_input.set("error")

def ceil_func():
    global calc_operator
    try:
        result = str(math.ceil(float(calc_operator)))
        calc_operator = result
        text_input.set(result)
    except:
        text_input.set("error")

def int_func():
    global calc_operator
    try:
        result = str(int(float(calc_operator)))
        calc_operator = result
        text_input.set(result)
    except:
        text_input.set("error")

def square_root():
    global calc_operator
    try:
        num = float(calc_operator)
        if num < 0:
            raise ValueError
        result = str(math.sqrt(num))
        calc_operator = result
        text_input.set(result)
    except:
        text_input.set("error")

def cube_root():
    global calc_operator
    try:
        num = float(calc_operator)
        result = str(num ** (1/3))
        calc_operator = result
        text_input.set(result)
    except:
        text_input.set("error")

def sign_change():
    global calc_operator
    if calc_operator.startswith('-'):
        calc_operator = calc_operator[1:]
    else:
        calc_operator = '-' + calc_operator
    text_input.set(calc_operator)

# ────────── FIXED SUMMATION AND PRODUCT ──────────

def summation(expr, var, start, end):
    total = 0
    s = int(start)
    e = int(end)
    for i in range(s, e+1):
        e_str = expr.replace(var, str(i)).replace('^','**')
        val = Interpreter().eval(e_str, {})
        total += val
    return total

def prod(expr, var, start, end):
    result = 1
    s = int(start)
    e = int(end)
    for i in range(s, e+1):
        e_str = expr.replace(var, str(i)).replace('^','**')
        val = Interpreter().eval(e_str, {})
        result *= val
    return result

# ────────── PARSER FOR ∑ AND Π NOTATION ──────────

def pre_parse_expression(e):
    e = e.strip()
    if e.startswith('∑(') and e.endswith(')'):
        parts = []
        level = 0
        buf = ''
        for ch in e[2:-1]:
            if ch == '(':
                level += 1
            elif ch == ')':
                level -= 1
            if ch == ',' and level == 0:
                parts.append(buf.strip())
                buf = ''
            else:
                buf += ch
        parts.append(buf.strip())
        if len(parts) == 4:
            return f"summation('{parts[0]}','{parts[1]}',{parts[2]},{parts[3]})"
    if e.startswith('Π(') and e.endswith(')'):
        parts = []
        level = 0
        buf = ''
        for ch in e[2:-1]:
            if ch == '(':
                level += 1
            elif ch == ')':
                level -= 1
            if ch == ',' and level == 0:
                parts.append(buf.strip())
                buf = ''
            else:
                buf += ch
        parts.append(buf.strip())
        if len(parts) == 4:
            return f"prod('{parts[0]}','{parts[1]}',{parts[2]},{parts[3]})"
    return e

def button_equal():
    global calc_operator
    try:
        parsed = pre_parse_expression(calc_operator)
        result = str(aeval.eval(parsed))
        calc_operator = result
        text_input.set(result)
    except:
        calc_operator = ""
        text_input.set("Error")

# ──────────  EVALUATOR SETUP ──────────

aeval = Interpreter()
aeval.symtable['summation'] = summation
aeval.symtable['prod'] = prod
aeval.symtable.update({
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'radians': math.radians,
    'factorial': math.factorial,
    'log': math.log10, 'ln': math.log,
    'sqrt': math.sqrt, 'pi': math.pi, 'e': math.e
})
for v in ['a','b','c','d','x','y','z']:
    aeval.symtable[v] = 0

# ────────── GUI SETUP ──────────

tk_calc = Tk()
tk_calc.configure(bg="#E75480", bd=10)
tk_calc.title('SCIENTIFIC CALCULATOR')
calc_operator = ""
text_input = StringVar()

Entry(tk_calc, font=('arial',20,'bold'), textvariable=text_input,
      bd=7, insertwidth=7, bg="#D5C4D4", justify='right')\
.grid(columnspan=5, padx=10, pady=15)

# Button styling dictionaries
params = {'bd':5,'fg':'#BBB','bg':'#4B0082','font':('arial',18,'bold')}
main   = {'bd':5,'fg':'#BBB','bg':"#3B083B",'font':('arial',18,'bold')}

# Row 1
Button(tk_calc, params, text='FLOOR',  command=floor_func) \
    .grid(row=1, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='CEIL',   command=ceil_func) \
    .grid(row=1, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='INT',    command=int_func) \
    .grid(row=1, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='x!',     command=lambda:button_click('factorial(')) \
    .grid(row=1, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='x^y',    command=lambda:button_click('**')) \
    .grid(row=1, column=4, columnspan=1, sticky="nsew")

# Row 2
Button(tk_calc, params, text='mod',    command=lambda:button_click('%')) \
    .grid(row=2, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='//',     command=lambda:button_click('//')) \
    .grid(row=2, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='log',    command=lambda:button_click('log(')) \
    .grid(row=2, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='ln',     command=lambda:button_click('ln(')) \
    .grid(row=2, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='π',      command=lambda:button_click('π')) \
    .grid(row=2, column=4, columnspan=1, sticky="nsew")

# Row 3
Button(tk_calc, params, text='√', command=square_root) \
    .grid(row=3, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='∛',command=cube_root) \
    .grid(row=3, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='e', command=lambda:button_click('e')) \
    .grid(row=3, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='∑', command=lambda:button_click('∑(')) \
    .grid(row=3, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='Π', command=lambda:button_click('Π(')) \
    .grid(row=3, column=4, columnspan=1, sticky="nsew")

# Row 4
Button(tk_calc, params, text='a', command=lambda:button_click('a')) \
    .grid(row=4, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='b', command=lambda:button_click('b')) \
    .grid(row=4, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='c', command=lambda:button_click('c')) \
    .grid(row=4, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='d', command=lambda:button_click('d')) \
    .grid(row=4, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, params, text='x', command=lambda:button_click('x')) \
    .grid(row=4, column=4, columnspan=1, sticky="nsew")

# Row 5
Button(tk_calc, main, text='(',  command=lambda:button_click('(')) \
    .grid(row=5, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, main, text=')',  command=lambda:button_click(')')) \
    .grid(row=5, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, main, text=',',  command=lambda:button_click(',')) \
    .grid(row=5, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='±',  command=sign_change) \
    .grid(row=5, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='=', command=button_equal, bg="#2D502D") \
    .grid(row=5, column=4, columnspan=1, sticky="nsew")

# Row 6
Button(tk_calc, main, text='7', command=lambda:button_click('7')) \
    .grid(row=6, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='8', command=lambda:button_click('8')) \
    .grid(row=6, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='9', command=lambda:button_click('9')) \
    .grid(row=6, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='DEL', command=button_delete, bg='#FF6347') \
    .grid(row=6, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='AC',  command=button_clear_all, bg='#FF6347') \
    .grid(row=6, column=4, columnspan=1, sticky="nsew")

# Row 7
Button(tk_calc, main, text='4', command=lambda:button_click('4')) \
    .grid(row=7, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='5', command=lambda:button_click('5')) \
    .grid(row=7, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='6', command=lambda:button_click('6')) \
    .grid(row=7, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='×', command=lambda:button_click('*')) \
    .grid(row=7, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='÷', command=lambda:button_click('/')) \
    .grid(row=7, column=4, columnspan=1, sticky="nsew")

# Row 8
Button(tk_calc, main, text='1', command=lambda:button_click('1')) \
    .grid(row=8, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='2', command=lambda:button_click('2')) \
    .grid(row=8, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='3', command=lambda:button_click('3')) \
    .grid(row=8, column=2, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='+', command=lambda:button_click('+')) \
    .grid(row=8, column=3, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='-', command=lambda:button_click('-')) \
    .grid(row=8, column=4, columnspan=1, sticky="nsew")

# Row 9
Button(tk_calc, main, text='0', command=lambda:button_click('0')) \
    .grid(row=9, column=0, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='.', command=lambda:button_click('.')) \
    .grid(row=9, column=1, columnspan=1, sticky="nsew")
Button(tk_calc, main, text='=', command=button_equal, bg="#2D502D") \
    .grid(row=9, column=2, columnspan=3, sticky="nsew")

# Make grid cells expand equally
for i in range(10):
    tk_calc.grid_rowconfigure(i, weight=1)
for i in range(5):
    tk_calc.grid_columnconfigure(i, weight=1)

tk_calc.mainloop()
