from tkinter import *
import math

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

def factorial(n):
    if n < 0:
        return "error"
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)
    
def fact_func():
    global calc_operator
    try:
        result = factorial(int(calc_operator))
        if result == "error":
            calc_operator = ""
            text_input.set("error")
        else:
            calc_operator = str(result)
            text_input.set(calc_operator)
    except:
        calc_operator = ""
        text_input.set("error")

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

def button_equal():
    global calc_operator
    try:
        # Replace custom operators with Python equivalents
        expression = calc_operator.replace('log(', 'log10(')
        temp_op = str(eval(expression))
        text_input.set(temp_op)
        calc_operator = temp_op
    except:
        text_input.set("error")
        calc_operator = ""

#VARIABLES
log10 = math.log10
ln = math.log
e = math.e
pi = math.pi



#GUI SETUP
tk_calc = Tk()
tk_calc.configure(bg="#E75480", bd=10)
tk_calc.title("GEN-Z Calculator - Coding Olympics 2023")

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
                       command=fact_func).grid(
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

log_base10 = Button(tk_calc, button_params, text='log',
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
                   command=lambda:button_click('sum(')).grid(
                       row=3, column=3, sticky="nsew")

prod_btn = Button(tk_calc, button_params, text='Π',
                   command=lambda:button_click('prod(')).grid(
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

signs = Button(tk_calc, button_params_main, text='±',
               command=sign_change).grid(
                   row=5, column=3, sticky="nsew")

x_var = Button(tk_calc, button_params_main, text='x',
           command=lambda:button_click('x')).grid(
               row=5, column=4, sticky="nsew")

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
