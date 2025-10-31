# You stopped at backslash function when you could not erase the last digit espacially when there's a symbol
from tkinter import *
class Calculator:
    def __init__(self,root):
        self.root=root
        self.equation_text=StringVar()
        self.text=""
        self.widgets()
    def widgets(self):
        self.label=Label(self.root,textvariable=self.equation_text,font=("Impact",40),width=20,bd=4,relief=GROOVE)
        self.label.pack()
        self.buttons=[[1,2,3,'+'],[4,5,6,'-'],[7,8,9,'/'],[0,'(',')','=']]
        self.buttons_frame= Frame ( self.root )
        for row in range(4):
            for column in range(4):
                number=self.buttons[row][column]
                if number=="=":
                    cmd=self.equal
                else:
                    cmd= lambda num=number:self.press_button(num)
                Button(self.buttons_frame,text=number,font=("consolas",12,"bold"),height=4,width=9,command=cmd,bd=4).grid(row=row,column=column)
        Button(self.buttons_frame,text="Clear",font=("Arial",12,"bold"),height=4,width=20,command=lambda:self.clear(),anchor=CENTER,bd=4).grid(row=4,column=0,columnspan=2)
        Button(self.buttons_frame,text="<backslash",font=("Arial",12,"bold"),height=4,width=20,command=lambda:self.backslash(),anchor=CENTER,bd=4).grid(row=4,column=2,columnspan=2)
        self.buttons_frame.pack()
    def press_button(self,num):
        self.text= self.text + str(num)
        self.equation_text.set(self.text)
    def equal(self):
        # self.equation_text,self.text
        try:
                
            total=str(eval(self.text))

            self.equation_text.set(total)
        except SyntaxError:
            self.equation_text.set("Invalid syntax")
        except ZeroDivisionError:
            self.equation_text.set("❌division by zero❌")
    def clear(self):
        self.text=""
        self.equation_text.set("")
    def backslash(self):
        self.text=self.text[:-1]
        self.equation_text.set(self.text)
