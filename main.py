from tkinter import messagebox
from background.user import User
from GUI.login_window import Loginwindow
from tkinter.ttk import Progressbar
from time import sleep
from tkinter import *

def check(username, password):
    users = User.load_user()
    result = User.authenticate(users, username, password)
    if result is True:
        messagebox.showinfo("Success", "Logged in Successfully")
        return True
    else:
        messagebox.showerror("Error", result)
        return False
def click_progress_bar(window,bar,text,label):
    begin,end,step=0,100,1
    while begin<=end:
        sleep(0.01)
        text.set(f"{int((begin/end)*100)}%")
        bar["value"]+=step
        begin+=step
        window.update_idletasks()
    bar.destroy()
    label.destroy()         
    Loginwindow(window)
def main():
    if __name__=="__main__":
        window=Tk()
        bar= Progressbar(window,orient=HORIZONTAL,length=300)
        bar.pack(pady=10)
        text=StringVar()
        label=Label(window,textvariable=text,font=("Impact",25))
        label.pack()
        bar.pack(padx=20)    
        click_progress_bar(window,bar,text,label)
        window.mainloop()
main()