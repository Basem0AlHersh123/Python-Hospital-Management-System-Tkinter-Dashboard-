from tkinter import *
from tkinter import messagebox
from GUI.app import App_interface
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from background.user import User
class Loginwindow(App_interface):
    def __init__(self,root):
        self.root=root
        super().__init__(self.root)
        self.main_page()
    def main_page(self):
        self.main_page_button=Button(self.frame,font=("Arial",23,"bold"),text="Get started",width=15,fg="white",anchor=CENTER,bg="#0066cc",command=self.main_click)
        self.main_page_button.pack()    
    def main_click(self):
        self.frame.destroy()
        self.create_widgets()
    def create_widgets(self):
        self.frame=Frame(self.root,bd=3,bg="white",padx=40,pady=40,relief="raised",border=5)
        self.frame.place(relx=0.5,rely=0.5,anchor=CENTER)
        # Title
        self.fields=["name","password"]
        self.entries={}
        for index, field in enumerate(self.fields):
            Label(self.frame,text=f"{field}: ",font=("arial",12,"bold"),bg="white").grid(row=index+2,column=0,pady=10)
            show=""
            if field=="password":
                show="*"
            self.entries[field]=Entry(self.frame,relief="raised",bd=2,font=("arial",12),show=show)
            self.entries[field].grid(row=index+2,column=1,pady=10)
        Label(self.frame,bg="WHITE",text="City Medical Center\nPlease Enter your data to Login",font=("Arial",18,"bold"),fg="#0066cc").grid(row=0,column=0,columnspan=2, pady=10)
        # Logo
        Label(self.frame,font=("Arial",30),bg="white",text="🏥") .grid(row=1,column=0,columnspan=2,pady=10)
        self.button=Button(
            self.frame,
            font=("arial",14),
            bg="#1989f8",
            text="Login",
            fg="white",
            activebackground="Purple",
            activeforeground="yellow",
            width=10,
            command=self.login,
            cursor="hand2"
        )
        self.button.grid(row=5,column=0,columnspan=2,pady=20)
        self.button.bind("<Enter>",self.hover)
        self.button.bind("<Leave>",self.leave)
        self.button2 = Button(self.frame,
            font=("arial",14),
            bg="#78b0e7",
            text="Sign up",
            fg="white",
            activebackground="Purple",
            activeforeground="yellow",
            width=8,
            command=self.register,
            cursor="hand2")
        self.button2.grid(row=6,column=0,columnspan=2,pady=15)
    def login(self):
        username = self.entries['name'].get().strip()
        password = self.entries['password'].get().strip()
        users = User.load_user()
        check = User.authenticate(users, username, password)
        if check is True:
            user = next((usr for usr in users if usr['name'] == username), None)
            if user:  
                    role = user.get("role", "admin")
                    self.root.destroy()
                    from tkinter import Tk
                    new_root = Tk()
                    if role == "admin":
                        from GUI.admin_dashboard import AdminDashboard
                        AdminDashboard(new_root)
                    elif role == "doctor":
                        from GUI.doctors_dashboard import DoctorDashboard
                        DoctorDashboard(new_root,name=username)
                    elif role == "employee":
                        from GUI.employee_dashboard import EmployeeDashboard
                        EmployeeDashboard(new_root)
                    else:
                        from GUI.patients_dashboard import PatientDashboard
                        PatientDashboard(new_root,patient_name=username)
                    new_root.mainloop()
        else:
            messagebox.showerror(title="Error", message=check)

    def hover(self,e):
        self.button.config(bg="aqua",fg="red")
    def leave(self,e):
        self.button.config(bg="#1989f8",fg="white")
    def register(self):
        from GUI.register import Register
        Register(self.root).widgets()
    