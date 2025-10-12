from tkinter import *
import math
from asteval import Interpreter

#FUNCTIONS AND OPERATIONS

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
    text = calc_operator[:-1]
    calc_operator = text
    text_input.set(text)

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
            calc_operator = ""
            text_input.set("error")
        else:
            temp = str(math.sqrt(num))
            calc_operator = temp
            text_input.set(temp)
    except:
        calc_operator = ""
        text_input.set("error")

def cube_root():
    global calc_operator
    try:
        num = float(calc_operator)
        temp = str(num ** (1/3))
        calc_operator = temp
        text_input.set(temp)
    except:
        text_input.set("error")

def sign_change():
    global calc_operator
    if calc_operator and calc_operator[0] == '-':
        temp = calc_operator[1:]
    else:
        temp = '-' + calc_operator
    calc_operator = temp
    text_input.set(temp)

def summation(expression, *args, **kwargs):
    if not args or len(args) % 3 != 0:
        raise ValueError("summation requires groups of (variable, start, end)")
    
    aeval.symtable.update(kwargs)
    var, start, end = args[0], args[1], args[2]
    total = 0
    for i in range(int(aeval.eval(str(start))), int(aeval.eval(str(end))) + 1):
        inner_aeval = Interpreter(symtable=aeval.symtable.copy())
        inner_aeval.symtable[var] = i
        if len(args) > 3:
            total += inner_aeval.eval(f"summation('{expression}', *{list(args[3:])}, **{kwargs})")
        else:
            total += inner_aeval.eval(expression)
    return total

def prod(expression, *args, **kwargs):
    if not args or len(args) % 3 != 0:
        raise ValueError("prod requires groups of (variable, start, end)")
    aeval.symtable.update(kwargs)
    var, start, end = args[0], args[1], args[2]
    total = 1
    start_val = int(aeval.eval(str(start)))
    end_val = int(aeval.eval(str(end)))
    if end_val < start_val:
        return 1
    for i in range(start_val, end_val + 1):
        inner_aeval = Interpreter(symtable=aeval.symtable.copy())
        inner_aeval.symtable[var] = i
        if len(args) > 3:
            val = inner_aeval.eval(f"prod('{expression}', *{list(args[3:])}, **{kwargs})")
        else:
            val = inner_aeval.eval(expression)
        if val is None:
            val = 1
        total *= val
    return total

def pre_parse_expression(expr):
    """
    Translates custom ∑ and Π notation into standard function calls.
    Example: '∑∑ x+y (a=1, b=3, c=2, d=4)' -> "summation('x+y','x',1,3,'y',2,4)"
    """
    expr = expr.strip()
    # Support ∑(expr,var,start,end) and Π(expr,var,start,end)
    if expr.startswith('∑(') and expr.endswith(')'):
        inner = expr[2:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) == 4:
            return f"summation('{parts[0]}','{parts[1]}',{parts[2]},{parts[3]})"
    if expr.startswith('Π(') and expr.endswith(')'):
        inner = expr[2:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) == 4:
            return f"prod('{parts[0]}','{parts[1]}',{parts[2]},{parts[3]})"

    # Support alternate/nested format: ∑∑ x+y (a=1, b=3, c=2, d=4)
    import re
    match = re.match(r'([∑Π]+)\s*([\w\+\-\*/^ ]+)\s*\(([^)]+)\)', expr)
    if match:
        ops = match.group(1)
        math_expr = match.group(2).strip()
        vars_part = match.group(3).replace(' ', '')
        var_map = dict(item.split('=') for item in vars_part.split(','))
        loop_vars = ['x', 'y', 'z', 'w', 'u', 'v'][:len(ops)]
        range_defs = [('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'h'), ('i', 'j'), ('k', 'l')]
        args = [f"'{math_expr}'"]
        for i in range(len(ops)):
            var = loop_vars[i]
            start_var, end_var = range_defs[i]
            args.extend([f"'{var}'", var_map[start_var], var_map[end_var]])
        func_name = 'summation' if ops[0] == '∑' else 'prod'
        return f"{func_name}({', '.join(args)})"
    return expr

def button_equal():
    global calc_operator
    try:
        # Pre-parse for custom notation, then evaluate
        parsed_expr = pre_parse_expression(calc_operator)
        temp_op = str(aeval.eval(parsed_expr))
        text_input.set(temp_op)
        calc_operator = temp_op
    except Exception as e:
        text_input.set("Error")
        calc_operator = ""


#VARIABLES
aeval = Interpreter()
aeval.symtable['summation'] = summation
aeval.symtable['prod'] = prod
aeval.symtable['sin'] = math.sin
aeval.symtable['cos'] = math.cos
aeval.symtable['tan'] = math.tan
aeval.symtable['radians'] = math.radians
aeval.symtable['factorial'] = math.factorial
aeval.symtable['log'] = math.log10
aeval.symtable['ln'] = math.log
args = ['a', 'b', 'c', 'd', 'x', 'y']
e = math.exp
p = math.pi


#GUI SETUP
tk_calc = Tk()
tk_calc.configure(bg="#E75480", bd=10)
tk_calc.title('SCIENTIFIC CALCULATOR')

calc_operator = ""
text_input = StringVar()

text_display = Entry(tk_calc, font=('arial', 20, 'bold'), 
                     textvariable=text_input,
                     bd=7, insertwidth=7, bg="#D5C4D4",
                     justify='right').grid(columnspan=5, padx=10, pady=15)

button_params = {'bd': 5, 'fg':'#BBB', 'bg': '#4B0082', 'font': ('arial', 18, 'bold')} 
button_params_main = {'bd': 5, 'fg':'#BBB', 'bg': "#3B083B", 'font': ('arial', 18, 'bold')}

#BUTTONS 1ST ROW
floor_btn = Button(tk_calc, button_params, text='FLOOR',
                   command=floor_func).grid(
                       row=1, column=0, sticky="nsew")

ceil_btn = Button(tk_calc, button_params, text='CEIL',
                command=ceil_func).grid(
                    row=1, column=1, sticky="nsew")

int_btn = Button(tk_calc, button_params, text='INT',
                 command=int_func).grid(
                     row=1, column=2, sticky="nsew")

factorial_btn = Button(tk_calc, button_params, text='x!',
                       command=lambda:button_click('factorial(')).grid(
                           row=1, column=3, sticky="nsew")

power_btn = Button(tk_calc, button_params, text='x^y',
                    command=lambda:button_click('**')).grid(
                        row=1, column=4, sticky="nsew")

#2ND ROW BUTTONS
modulo = Button(tk_calc, button_params, text='mod',
                command=lambda:button_click('%')).grid(
                    row=2, column=0, sticky="nsew")

int_div = Button(tk_calc, button_params, text='//',
                 command=lambda:button_click('//')).grid(
                     row=2, column=1, sticky="nsew")

log = Button(tk_calc, button_params, text='log',
                   command=lambda:button_click('log(')).grid(
                       row=2, column=2, sticky="nsew")

ln_btn = Button(tk_calc, button_params, text='ln',
                   command=lambda:button_click('ln(')).grid(
                       row=2, column=3, sticky="nsew")

pi_num = Button(tk_calc, button_params, text='π',
                  command=lambda:button_click(str(math.pi))).grid(
                      row=2, column=4, sticky="nsew")

#3RD ROW BUTTONS
square_root_btn = Button(tk_calc, button_params, text='√',
                         command=square_root).grid(
                             row=3, column=0, sticky="nsew")

cube_root_btn = Button(tk_calc, button_params, text='∛',
                        command=cube_root).grid(
                            row=3, column=1, sticky="nsew")

eulers_num = Button(tk_calc, button_params, text='e',
                    command=lambda:button_click(str(math.e))).grid(
                        row=3, column=2, sticky="nsew")

sum_btn = Button(tk_calc, button_params, text='∑',
                   command=lambda:button_click('∑(')).grid(
                       row=3, column=3, sticky="nsew")

prod_btn = Button(tk_calc, button_params, text='Π',
                   command=lambda:button_click('Π(')).grid(
                       row=3, column=4, sticky="nsew")

#4TH ROW BUTTONS

a = Button(tk_calc, button_params, text='a',
                   command=lambda:button_click('a')).grid(
                       row=4, column=0, sticky="nsew")

b = Button(tk_calc, button_params, text='b',
                   command=lambda:button_click('b')).grid(
                       row=4, column=1, sticky="nsew")

c = Button(tk_calc, button_params, text='c',
                   command=lambda:button_click('c')).grid(
                       row=4, column=2, sticky="nsew")

d = Button(tk_calc, button_params, text='d',
                   command=lambda:button_click('d')).grid(
                       row=4, column=3, sticky="nsew")

x = Button(tk_calc, button_params, text='x',
                   command=lambda:button_click('x')).grid(
                       row=4, column=4, sticky="nsew")


#5TH ROW BUTTONS
left_par = Button(tk_calc, button_params_main, text='(',
                  command=lambda:button_click('(')).grid(
                      row=5, column=0, sticky="nsew")

right_par = Button(tk_calc, button_params_main, text=')',
                   command=lambda:button_click(')')).grid(
                       row=5, column=1, sticky="nsew")

comma_btn = Button(tk_calc, button_params_main, text=',',
               command=lambda:button_click(',')).grid(
                   row=5, column=2, sticky="nsew")

y = Button(tk_calc, button_params, text='y',
           command=lambda:button_click('y')).grid(
               row=5, column=3, sticky="nsew")

equal_btn_single = Button(tk_calc, button_params_main, text='=', command=button_equal, bg="#2D502D").grid(row=5, column=4, sticky="nsew")

#6TH ROW BUTTONS
button_7 = Button(tk_calc, button_params_main, text='7',
                 command=lambda:button_click('7')).grid(
                     row=6, column=0, sticky="nsew")

button_8 = Button(tk_calc, button_params_main, text='8',
                 command=lambda:button_click('8')).grid(
                     row=6, column=1, sticky="nsew")

button_9 = Button(tk_calc, button_params_main, text='9',
                    command=lambda:button_click('9')).grid(
                        row=6, column=2, sticky="nsew")

delete_one = Button(tk_calc, button_params_main, text='DEL',
                    command=button_delete, bg='#FF6347').grid(
                        row=6, column=3, sticky="nsew")

delete_all = Button(tk_calc, button_params_main, text='AC',
                    command=button_clear_all, bg='#FF6347').grid(
                        row=6, column=4, sticky="nsew")

#7TH ROW BUTTONS
button_4 = Button(tk_calc, button_params_main, text='4',
                 command=lambda:button_click('4')).grid(
                     row=7, column=0, sticky="nsew")

button_5 = Button(tk_calc, button_params_main, text='5',
                 command=lambda:button_click('5')).grid(
                     row=7, column=1, sticky="nsew")

button_6 = Button(tk_calc, button_params_main, text='6',
                 command=lambda:button_click('6')).grid(
                     row=7, column=2, sticky="nsew")

multiply = Button(tk_calc, button_params_main, text='×',
                  command=lambda:button_click('*')).grid(
                      row=7, column=3, sticky="nsew")

divide = Button(tk_calc, button_params_main, text='÷',
                command=lambda:button_click('/')).grid(
                    row=7, column=4, sticky="nsew")

#8TH ROW BUTTONS
button_1 = Button(tk_calc, button_params_main, text='1',
                 command=lambda:button_click('1')).grid(
                     row=8, column=0, sticky="nsew")

button_2 = Button(tk_calc, button_params_main, text='2',
                 command=lambda:button_click('2')).grid(
                     row=8, column=1, sticky="nsew")

button_3 = Button(tk_calc, button_params_main, text='3',
                 command=lambda:button_click('3')).grid(
                     row=8, column=2, sticky="nsew")

add = Button(tk_calc, button_params_main, text='+',
             command=lambda:button_click('+')).grid(
                 row=8, column=3, sticky="nsew")

subtract = Button(tk_calc, button_params_main, text='-',
                  command=lambda:button_click('-')).grid(
                      row=8, column=4, sticky="nsew")

#9TH ROW BUTTONS
button_0 = Button(tk_calc, button_params_main, text='0',
                 command=lambda:button_click('0')).grid(
                     row=9, column=0, sticky="nsew")

button_point = Button(tk_calc, button_params_main, text='.',
                 command=lambda:button_click('.')).grid(
                     row=9, column=1, sticky="nsew")

equal = Button(tk_calc, button_params_main, text='=',
                 command=button_equal, bg="#2D502D").grid(
                      row=9, column=2, sticky="nsew", columnspan=3)

tk_calc.mainloop()from tkinter import *
import math
from asteval import Interpreter

#FUNCTIONS AND OPERATIONS

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
    text = calc_operator[:-1]
    calc_operator = text
    text_input.set(text)

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
            calc_operator = ""
            text_input.set("error")
        else:
            temp = str(math.sqrt(num))
            calc_operator = temp
            text_input.set(temp)
    except:
        calc_operator = ""
        text_input.set("error")

def cube_root():
    global calc_operator
    try:
        num = float(calc_operator)
        temp = str(num ** (1/3))
        calc_operator = temp
        text_input.set(temp)
    except:
        text_input.set("error")

def sign_change():
    global calc_operator
    if calc_operator and calc_operator[0] == '-':
        temp = calc_operator[1:]
    else:
        temp = '-' + calc_operator
    calc_operator = temp
    text_input.set(temp)

def summation(expression, *args, **kwargs):
    if not args or len(args) % 3 != 0:
        raise ValueError("summation requires groups of (variable, start, end)")
    
    aeval.symtable.update(kwargs)
    var, start, end = args[0], args[1], args[2]
    total = 0
    for i in range(int(aeval.eval(str(start))), int(aeval.eval(str(end))) + 1):
        inner_aeval = Interpreter(symtable=aeval.symtable.copy())
        inner_aeval.symtable[var] = i
        if len(args) > 3:
            total += inner_aeval.eval(f"summation('{expression}', *{list(args[3:])}, **{kwargs})")
        else:
            total += inner_aeval.eval(expression)
    return total

def prod(expression, *args, **kwargs):
    if not args or len(args) % 3 != 0:
        raise ValueError("prod requires groups of (variable, start, end)")
    aeval.symtable.update(kwargs)
    var, start, end = args[0], args[1], args[2]
    total = 1
    start_val = int(aeval.eval(str(start)))
    end_val = int(aeval.eval(str(end)))
    if end_val < start_val:
        return 1
    for i in range(start_val, end_val + 1):
        inner_aeval = Interpreter(symtable=aeval.symtable.copy())
        inner_aeval.symtable[var] = i
        if len(args) > 3:
            val = inner_aeval.eval(f"prod('{expression}', *{list(args[3:])}, **{kwargs})")
        else:
            val = inner_aeval.eval(expression)
        if val is None:
            val = 1
        total *= val
    return total

def pre_parse_expression(expr):
    """
    Translates custom ∑ and Π notation into standard function calls.
    Example: '∑∑ x+y (a=1, b=3, c=2, d=4)' -> "summation('x+y','x',1,3,'y',2,4)"
    """
    expr = expr.strip()
    # Support ∑(expr,var,start,end) and Π(expr,var,start,end)
    if expr.startswith('∑(') and expr.endswith(')'):
        inner = expr[2:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) == 4:
            return f"summation('{parts[0]}','{parts[1]}',{parts[2]},{parts[3]})"
    if expr.startswith('Π(') and expr.endswith(')'):
        inner = expr[2:-1]
        parts = [p.strip() for p in inner.split(',')]
        if len(parts) == 4:
            return f"prod('{parts[0]}','{parts[1]}',{parts[2]},{parts[3]})"

    # Support alternate/nested format: ∑∑ x+y (a=1, b=3, c=2, d=4)
    import re
    match = re.match(r'([∑Π]+)\s*([\w\+\-\*/^ ]+)\s*\(([^)]+)\)', expr)
    if match:
        ops = match.group(1)
        math_expr = match.group(2).strip()
        vars_part = match.group(3).replace(' ', '')
        var_map = dict(item.split('=') for item in vars_part.split(','))
        loop_vars = ['x', 'y', 'z', 'w', 'u', 'v'][:len(ops)]
        range_defs = [('a', 'b'), ('c', 'd'), ('e', 'f'), ('g', 'h'), ('i', 'j'), ('k', 'l')]
        args = [f"'{math_expr}'"]
        for i in range(len(ops)):
            var = loop_vars[i]
            start_var, end_var = range_defs[i]
            args.extend([f"'{var}'", var_map[start_var], var_map[end_var]])
        func_name = 'summation' if ops[0] == '∑' else 'prod'
        return f"{func_name}({', '.join(args)})"
    return expr

def button_equal():
    global calc_operator
    try:
        # Pre-parse for custom notation, then evaluate
        parsed_expr = pre_parse_expression(calc_operator)
        temp_op = str(aeval.eval(parsed_expr))
        text_input.set(temp_op)
        calc_operator = temp_op
    except Exception as e:
        text_input.set("Error")
        calc_operator = ""


#VARIABLES
aeval = Interpreter()
aeval.symtable['summation'] = summation
aeval.symtable['prod'] = prod
aeval.symtable['sin'] = math.sin
aeval.symtable['cos'] = math.cos
aeval.symtable['tan'] = math.tan
aeval.symtable['radians'] = math.radians
aeval.symtable['factorial'] = math.factorial
aeval.symtable['log'] = math.log10
aeval.symtable['ln'] = math.log
args = ['a', 'b', 'c', 'd', 'x', 'y']
e = math.exp
p = math.pi


#GUI SETUP
tk_calc = Tk()
tk_calc.configure(bg="#E75480", bd=10)
tk_calc.title('SCIENTIFIC CALCULATOR')

calc_operator = ""
text_input = StringVar()

text_display = Entry(tk_calc, font=('arial', 20, 'bold'), 
                     textvariable=text_input,
                     bd=7, insertwidth=7, bg="#D5C4D4",
                     justify='right').grid(columnspan=5, padx=10, pady=15)

button_params = {'bd': 5, 'fg':'#BBB', 'bg': '#4B0082', 'font': ('arial', 18, 'bold')} 
button_params_main = {'bd': 5, 'fg':'#BBB', 'bg': "#3B083B", 'font': ('arial', 18, 'bold')}

#BUTTONS 1ST ROW
floor_btn = Button(tk_calc, button_params, text='FLOOR',
                   command=floor_func).grid(
                       row=1, column=0, sticky="nsew")

ceil_btn = Button(tk_calc, button_params, text='CEIL',
                command=ceil_func).grid(
                    row=1, column=1, sticky="nsew")

int_btn = Button(tk_calc, button_params, text='INT',
                 command=int_func).grid(
                     row=1, column=2, sticky="nsew")

factorial_btn = Button(tk_calc, button_params, text='x!',
                       command=lambda:button_click('factorial(')).grid(
                           row=1, column=3, sticky="nsew")

power_btn = Button(tk_calc, button_params, text='x^y',
                    command=lambda:button_click('**')).grid(
                        row=1, column=4, sticky="nsew")

#2ND ROW BUTTONS
modulo = Button(tk_calc, button_params, text='mod',
                command=lambda:button_click('%')).grid(
                    row=2, column=0, sticky="nsew")

int_div = Button(tk_calc, button_params, text='//',
                 command=lambda:button_click('//')).grid(
                     row=2, column=1, sticky="nsew")

log = Button(tk_calc, button_params, text='log',
                   command=lambda:button_click('log(')).grid(
                       row=2, column=2, sticky="nsew")

ln_btn = Button(tk_calc, button_params, text='ln',
                   command=lambda:button_click('ln(')).grid(
                       row=2, column=3, sticky="nsew")

pi_num = Button(tk_calc, button_params, text='π',
                  command=lambda:button_click(str(math.pi))).grid(
                      row=2, column=4, sticky="nsew")

#3RD ROW BUTTONS
square_root_btn = Button(tk_calc, button_params, text='√',
                         command=square_root).grid(
                             row=3, column=0, sticky="nsew")

cube_root_btn = Button(tk_calc, button_params, text='∛',
                        command=cube_root).grid(
                            row=3, column=1, sticky="nsew")

eulers_num = Button(tk_calc, button_params, text='e',
                    command=lambda:button_click(str(math.e))).grid(
                        row=3, column=2, sticky="nsew")

sum_btn = Button(tk_calc, button_params, text='∑',
                   command=lambda:button_click('∑(')).grid(
                       row=3, column=3, sticky="nsew")

prod_btn = Button(tk_calc, button_params, text='Π',
                   command=lambda:button_click('Π(')).grid(
                       row=3, column=4, sticky="nsew")

#4TH ROW BUTTONS

a = Button(tk_calc, button_params, text='a',
                   command=lambda:button_click('a')).grid(
                       row=4, column=0, sticky="nsew")

b = Button(tk_calc, button_params, text='b',
                   command=lambda:button_click('b')).grid(
                       row=4, column=1, sticky="nsew")

c = Button(tk_calc, button_params, text='c',
                   command=lambda:button_click('c')).grid(
                       row=4, column=2, sticky="nsew")

d = Button(tk_calc, button_params, text='d',
                   command=lambda:button_click('d')).grid(
                       row=4, column=3, sticky="nsew")

x = Button(tk_calc, button_params, text='x',
                   command=lambda:button_click('x')).grid(
                       row=4, column=4, sticky="nsew")


#5TH ROW BUTTONS
left_par = Button(tk_calc, button_params_main, text='(',
                  command=lambda:button_click('(')).grid(
                      row=5, column=0, sticky="nsew")

right_par = Button(tk_calc, button_params_main, text=')',
                   command=lambda:button_click(')')).grid(
                       row=5, column=1, sticky="nsew")

comma_btn = Button(tk_calc, button_params_main, text=',',
               command=lambda:button_click(',')).grid(
                   row=5, column=2, sticky="nsew")

y = Button(tk_calc, button_params, text='y',
           command=lambda:button_click('y')).grid(
               row=5, column=3, sticky="nsew")

equal_btn_single = Button(tk_calc, button_params_main, text='=', command=button_equal, bg="#2D502D").grid(row=5, column=4, sticky="nsew")

#6TH ROW BUTTONS
button_7 = Button(tk_calc, button_params_main, text='7',
                 command=lambda:button_click('7')).grid(
                     row=6, column=0, sticky="nsew")

button_8 = Button(tk_calc, button_params_main, text='8',
                 command=lambda:button_click('8')).grid(
                     row=6, column=1, sticky="nsew")

button_9 = Button(tk_calc, button_params_main, text='9',
                    command=lambda:button_click('9')).grid(
                        row=6, column=2, sticky="nsew")

delete_one = Button(tk_calc, button_params_main, text='DEL',
                    command=button_delete, bg='#FF6347').grid(
                        row=6, column=3, sticky="nsew")

delete_all = Button(tk_calc, button_params_main, text='AC',
                    command=button_clear_all, bg='#FF6347').grid(
                        row=6, column=4, sticky="nsew")

#7TH ROW BUTTONS
button_4 = Button(tk_calc, button_params_main, text='4',
                 command=lambda:button_click('4')).grid(
                     row=7, column=0, sticky="nsew")

button_5 = Button(tk_calc, button_params_main, text='5',
                 command=lambda:button_click('5')).grid(
                     row=7, column=1, sticky="nsew")

button_6 = Button(tk_calc, button_params_main, text='6',
                 command=lambda:button_click('6')).grid(
                     row=7, column=2, sticky="nsew")

multiply = Button(tk_calc, button_params_main, text='×',
                  command=lambda:button_click('*')).grid(
                      row=7, column=3, sticky="nsew")

divide = Button(tk_calc, button_params_main, text='÷',
                command=lambda:button_click('/')).grid(
                    row=7, column=4, sticky="nsew")

#8TH ROW BUTTONS
button_1 = Button(tk_calc, button_params_main, text='1',
                 command=lambda:button_click('1')).grid(
                     row=8, column=0, sticky="nsew")

button_2 = Button(tk_calc, button_params_main, text='2',
                 command=lambda:button_click('2')).grid(
                     row=8, column=1, sticky="nsew")

button_3 = Button(tk_calc, button_params_main, text='3',
                 command=lambda:button_click('3')).grid(
                     row=8, column=2, sticky="nsew")

add = Button(tk_calc, button_params_main, text='+',
             command=lambda:button_click('+')).grid(
                 row=8, column=3, sticky="nsew")

subtract = Button(tk_calc, button_params_main, text='-',
                  command=lambda:button_click('-')).grid(
                      row=8, column=4, sticky="nsew")

#9TH ROW BUTTONS
button_0 = Button(tk_calc, button_params_main, text='0',
                 command=lambda:button_click('0')).grid(
                     row=9, column=0, sticky="nsew")

button_point = Button(tk_calc, button_params_main, text='.',
                 command=lambda:button_click('.')).grid(
                     row=9, column=1, sticky="nsew")

equal = Button(tk_calc, button_params_main, text='=',
                 command=button_equal, bg="#2D502D").grid(
                      row=9, column=2, sticky="nsew", columnspan=3)

tk_calc.mainloop()
