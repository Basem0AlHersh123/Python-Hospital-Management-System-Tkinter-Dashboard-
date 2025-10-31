from GUI.app import App_interface


from tkinter import *
from tkinter import messagebox
class Register(App_interface):
    def __init__(self, root):
        self.root=root
        super().__init__(root)
        self.widgets()        
    def register(self):
        from background.file_manager import FileManager
        from background.check import Check
        username=self.entries["name"].get().strip()
        password=self.entries["password"].get().strip()
        phone=self.entries["phone"].get().strip()
        data=FileManager.load_data("users")
        message=Check.is_valid_username(username=username,data=data)
        check_boxes=Check.check_box(username,password,phone)
        if not check_boxes:
            messagebox.showerror(title="Error",message="You need to fill all the boxes")
            return
        if  Check.is_valid_username(username=username,data=data):
            messagebox.showerror(title="Error",message=message)
            return
        if not Check.is_valid_password(password):
            # if User.get("password") == User.hash_password(password):
            messagebox.showerror("Error", "Password must be at least 6 chars and contain a number")
            return
        patients=FileManager.load_data("patients")
        if not Check.is_valid_phone(phone):
            messagebox.showerror("Error", "Phone must be 9 digits")
            return
        next_id = max([patient.get("id", 0) for patient in patients] or [0]) + 1
        new_patient = {
            "id": next_id,
            "name": username,
            "password": password,
            "role": "patient",
            "phone": phone,
            "active": True
        }
        messagebox.showinfo("Successful","Successfully registers")
        data.append(new_patient)
        patients.append(new_patient)
        FileManager.save_data("users",data)
        FileManager.save_data("patients",data)
        self.root.destroy()
        from GUI.patients_dashboard import PatientDashboard
        new_root=Tk()       
        PatientDashboard(new_root,patient_name=username)
        new_root.mainloop()
    def widgets(self):
        self.frame=Frame(self.root,bd=3,bg="white",padx=40,pady=40,relief="raised",border=5)
        self.frame.place(relx=0.5,rely=0.5,anchor=CENTER)
        Label(self.frame,bg="WHITE",text="City Medical Center\nPlease Enter your data to register",font=("Arial",18,"bold"),fg="#0066cc").grid(row=0,column=0,columnspan=2, pady=10)        
        self.fields=["name","password","phone"]
        self.entries={}
        for index, field in enumerate(self.fields):
            Label(self.frame,text=f"{field}: ",font=("arial",12,"bold"),bg="white").grid(row=index+2,column=0,pady=10)
            show=""
            if field=="password":
                show="*"
            self.entries[field]=Entry(self.frame,relief="raised",bd=2,font=("arial",12),show=show)
            self.entries[field].grid(row=index+2,column=1,pady=10)
        Label(self.frame,font=("Arial",30),bg="white",text="🏥") .grid(row=1,column=0,columnspan=2,pady=10)
        self.button=Button(
            self.frame,
            font=("arial",14),
            bg="#1989f8",
            text="Register",
            fg="white",
            activebackground="Purple",
            activeforeground="yellow",
            width=10,
            command=self.register,
            cursor="hand2"
        )
        self.button.grid(row=7,column=0,columnspan=2,pady=20)
        self.button.bind("<Enter>",self.hover)
        self.button.bind("<Leave>",self.leave)
        self.button2 = Button(self.frame,
            font=("arial",14),
            bg="#78b0e7",
            text="Login",
            fg="white",
            activebackground="Purple",
            activeforeground="yellow",
            width=8,
            command=self.login,
            cursor="hand2")
        self.button2.grid(row=8,column=0,columnspan=2,pady=15)
    def hover(self,e):
        self.button.config(bg="aqua",fg="red")
    def leave(self,e):
        self.button.config(bg="#1989f8",fg="white")
    def login(self):
        from GUI.login_window import Loginwindow
        Loginwindow(self.root).create_widgets()
    