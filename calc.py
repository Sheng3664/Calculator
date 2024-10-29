import tkinter as tk
import math

LIGHT_GREY = "#D3D3D3"
LABEL_COLOR = "#001861"
WHITE = "#FFFFFF"
OFF_WHITE = '#F8FAFF'
LIGHT_BLUE = "#ADD8e6"

SMALL_FONT_STYLE = ("Times New Roman", 16)
LARGE_FONT_STYLE = ("Times New Roman", 40, "bold")
DIGITS_FONT_STYLE = ("Times New Roman", 24, "bold")
DEFAULT_FONT_STYLE = ("Times New Roman", 20)

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("365x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.total_exp = ""
        self.current_exp = ""

        self.display_frame = self.create_display_frame()
        self.total, self.current_value = self.create_display_labels()
        self.buttons_frame = self.create_buttons_frame()

        #number 7 in row 1, column 1
        self.digits = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            0:(4,2), ".":(4,1)
        }

        self.operators = {" / ": "\u00F7",
                          " x ": "\u00D7",
                          " - ": " - ",
                          " + ": " + ",
                          }
        
        #fill all buttons into the empty space
        self.buttons_frame.rowconfigure(0, weight = 1)
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x,weight =1)
            self.buttons_frame.columnconfigure(x, weight =1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def create_display_labels(self):
        total= tk.Label(self.display_frame, text=self.total_exp, anchor = tk.E, 
                        bg =LIGHT_GREY, fg=LABEL_COLOR, padx = 24, font = SMALL_FONT_STYLE)
        #anchor right, set background, set font color, style, add padding

        total.pack(expand=True, fill="both")

        #current label
        current_value= tk.Label(self.display_frame, text=self.current_exp, anchor = tk.E, 
                                bg =LIGHT_GREY, fg=LABEL_COLOR, padx = 24, font = LARGE_FONT_STYLE)
        
        current_value.pack(expand=True, fill="both")

        return total, current_value
    
    def add_to_expression(self,value):
        if self.current_exp.endswith("="):  # Check if the current expression ends with "="
            self.total_exp = self.current_exp.split('=')[0].strip()  # Take the previous expression
            self.current_exp = ""  # Reset current expression
            
        self.current_exp += str(value)  # Add the new digit to the current expression
        self.update_current_value()
        print(f'Current Expression: {self.current_exp}')
        print(f'Total Expression: {self.total_exp}')

    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg = WHITE,
                               fg = LABEL_COLOR, font = DIGITS_FONT_STYLE, borderwidth=0,
                               command = lambda x = digit: self.add_to_expression(x))
            
            #sticky = make everybutton sitck together in the grid
            button.grid(row=grid_value[0], column = grid_value[1], sticky=tk.NSEW)

    #add operators to the display
    def append_operator(self, operator):
        if operator == " \u00D7 ":
            operator = " x "  # Use "x" for display
        elif operator == " math.sqrt(":
            operator = " \u221a ("

        self.current_exp += operator
        self.total_exp += self.current_exp.replace("x", "*")  # Replace "x" with "*" for evaluation
        self.current_exp = ""

        self.update_total()
        self.update_current_value()
        print(f'Current Expression: {self.current_exp}')
        print(f'Total Expression: {self.total_exp}')


    def create_display_frame(self):
        frame = tk.Frame(self.window, height = 221, bg = LIGHT_GREY)
        frame.pack(expand = True, fill = "both")
        return frame
    
    def create_operator_buttons(self):
        i = 0 #operator buttons start a row above the numbers
        for operator,symbol in self.operators.items():
            buttons = tk.Button(self.buttons_frame, text = symbol, bg = OFF_WHITE, 
                                fg = LABEL_COLOR, font= DEFAULT_FONT_STYLE, borderwidth=0,
                                command = lambda x=operator: self.append_operator(x))
            buttons.grid(row = i, column=4,sticky =tk.NSEW)
            i += 1

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand = True, fill = "both")
        return frame

    def clear(self):
        self.current_exp = ""
        self.total_exp = ""
        self.update_current_value()
        self.update_total()

    def create_clear_button(self):
        buttons = tk.Button(self.buttons_frame, text = "C", bg = OFF_WHITE, 
                                fg = LABEL_COLOR, font= DEFAULT_FONT_STYLE, borderwidth=0
                                ,command= self.clear)
        buttons.grid(row = 0, column=1, sticky =tk.NSEW)

    def create_square_button(self):
        buttons = tk.Button(self.buttons_frame, text = "x\u00b2", bg = OFF_WHITE, 
                                fg = LABEL_COLOR, font= DEFAULT_FONT_STYLE, borderwidth=0,
                                command= self.sqaure)
        buttons.grid(row = 0, column=2, sticky =tk.NSEW)

    def sqaure(self):
        self.current_exp = f"{self.current_exp}\u00b2"
        self.update_current_value()

    def create_sqrt_button(self):
        buttons = tk.Button(self.buttons_frame, text = "\u221a", bg = OFF_WHITE, 
                                fg = LABEL_COLOR, font= DEFAULT_FONT_STYLE, borderwidth=0
                                ,command= self.sqrt)
        buttons.grid(row = 0, column=3, sticky =tk.NSEW)

    def sqrt(self):
        if self.current_exp:  # Check if there's a current number
            self.clear
            self.current_exp = f"\u221a({self.current_exp})"  
        self.update_current_value() 

    def prepare_expression(self, expression):
        expression = expression.replace("\u221a(", "math.sqrt(")
        expression = expression.replace("\u00b2", "**2")
        expression = expression.replace("x", "*")
        return expression

    def format_total_expression(self, expression):
        if "math.sqrt(" in expression:
            expression = expression.replace("math.sqrt(", "\u221a(")
        return f"{expression} ="
    
    def evaluate(self):
        #Entire Block of code is to continure calculating with the previous answer 
        # without clearing 
        new_expression = ""

        if "=" in self.total_exp:
            parts = self.total_exp.split('=')
            if len(parts) > 1:
                new_expression = parts[1].strip()
            self.total_exp = ""

        if not new_expression:
            new_expression = self.total_exp + self.current_exp
        else:
            new_expression = self.total_exp + new_expression + self.current_exp

        new_expression = self.prepare_expression(new_expression)
        print(new_expression)
        #end of block

        try:
            result = eval(new_expression)
        except Exception:
            self.current_exp = "Error"
            self.update_current_value()
            return

        self.total_exp = self.format_total_expression(new_expression)
        self.current_exp = str(result)

        print(f'Current Expression: {self.current_exp}')
        print(f'Total Expression: {self.total_exp}')
        
        self.update_current_value()
        self.update_total()

    def create_equals_button(self):
        buttons = tk.Button(self.buttons_frame, text = "=", bg = LIGHT_BLUE, 
                                fg = LABEL_COLOR, font= DEFAULT_FONT_STYLE, borderwidth=0,
                                command = self.evaluate)
        buttons.grid(row = 4, column=3, columnspan = 2, sticky =tk.NSEW)
    
    def create_delete_button(self):
        buttons = tk.Button(self.buttons_frame, text = "\u2190", bg = LIGHT_BLUE, 
                                fg = LABEL_COLOR, font= DEFAULT_FONT_STYLE, borderwidth=0,
                                command = self.evaluate)
        buttons.grid(row = 4, column=1, sticky =tk.NSEW)

    def delete(self):
        if self.current_exp:
            self.current_exp = self.current_exp[:-1]  # Remove the last character
        self.update_current_value()
        
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.delete())

        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        
        for key in self.operators:
            self.window.bind(str(key), lambda even, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_equals_button()
        self.create_clear_button()
        self.create_sqrt_button()
        self.create_square_button()
        self.create_delete_button()

    def update_total(self):
        expression = self.total_exp
        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f'{symbol}')
        self.total.config(text=self.total_exp.replace("*", "x"))

    def update_current_value(self):
        self.current_value.config(text=self.current_exp[:11])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()