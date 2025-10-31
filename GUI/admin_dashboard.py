from tkinter import messagebox
from GUI.dashboards import Dashboard
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GUI.calculator import Calculator   
from background.file_manager import FileManager
from tkinter import *
class AdminDashboard(Dashboard):
    def __init__(self,root):
        self.stats=[("Patients","patients","#ea4335"),
                     ("Doctors","doctors","#fbbc05"),
                     ("Appointments","appointments","#4285f4"),
                     ("Funds","5000$","#34a853")]
        super().__init__(root=root,main_theme="#1a73e8",dashboard_name="Hospital",title="Admin Dashboard",message="Hello Manager",home_page_title="Main Page",stats=self.stats)
        # self.root.config(background="white",)
        fields=[("🏠 Home Page",lambda:self.home_page(title="Main Page",stats=self.stats)),
                     ("😷 Doctors dashboard ",self.manage_doctors),
                     ("💼 Employees dashboard",self.manage_employees),
                     ("👥 Patients dashboard",self.manage_patients),
                     ("📊 Reports",self.reports),
                     ("🧮 Calculator",self.calculator)]
        self.sidebar(fields=fields,background="#202124",button_bg="#3c4043",button_fg="#0DDCF7",)   
        self.active=Button(self.title,bg="blue",padx=10,pady=5,fg="white",text="Activate/Deactivate",font=("constantia",13,"bold"))
        self.active.pack(side="left")
    def reports(self):
        Button(self.home, text="View Reports", bg="purple", fg="white",
       command=self.show_reports).pack(pady=5)
        self.clear()
        doctors_data=FileManager.load_data("doctors")
        patients_data=FileManager.load_data("patients")
        Label(self.home, text="Reports", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        report_text = f"""
        📊 Hospital Reports
        ----------------------------
        Patients: {len(patients_data)}
        Doctors staff: {len(doctors_data)}
        Doctors' specilizations:
        """
        for doc in doctors_data:
            report_text += f"\n  - {doc['name']} ({doc['specialization']})"
        report_text += "\n\n Created successfully."
        text_area = Text(self.home, font=("Arial", 12), bg="#f8f9fa", fg="#333")
        text_area.pack(fill="both", expand=True, padx=20, pady=10)
        text_area.insert("1.0", report_text)
        text_area.config(state="disabled") 
    def show_reports(self):
        doctors = FileManager.load_data("doctors")
        patients = FileManager.load_data("patients")
        appointments = FileManager.load_data("appointments")
        report = (
            f"📊 System Report\n\n"
            f"👨‍⚕️ Total Doctors: {len(doctors)}\n"
            f"🧑‍🤝‍🧑 Total Patients: {len(patients)}\n"
            f"📅 Total Appointments: {len(appointments)}\n"
        )
        messagebox.showinfo("Reports", report)
    def open_add_form(self, entity):
        win = Toplevel(self.root)
        win.title(f"Add {entity.capitalize()}")
        win.geometry("400x300")
        fields = []
        if entity == "doctor":
            fields = ["id", "name", "specialization", "phone"]
        elif entity == "patient":
            fields = ["id", "name", "age", "phone"]
        elif entity == "appointment":
            fields = ["id", "doctor", "patient", "date"]
        entries = {}
        for index, field in enumerate(fields):
            Label(win, text=field.capitalize(),padx=10,pady=10,font=("constantia",15,"italic")).grid(row=index, column=0, padx=10, pady=5, sticky="w")
            entry = Entry(win,width=20)
            entry.grid(row=index, column=1, padx=10, pady=5,)
            entries[field] = entry

            def save():
                data = FileManager.load_data(entity + "s")
                new_item = {field: entries[field].get().strip() for field in fields}
                if not all(new_item.values()):
                    from tkinter import messagebox
                    messagebox.showerror("Error", "All fields are required!")
                    return
                if any(str(item.get("id")) == new_item["id"] for item in data):
                    from tkinter import messagebox
                    messagebox.showerror("Error", "ID already exists!")
                    return
                data.append(new_item)
                FileManager.save_data(entity + "s", data)
                from tkinter import messagebox
                messagebox.showinfo("Success", f"New {entity} added.")
                win.destroy()
            Button(win, text="Save", bg="blue", fg="white",relief=RAISED, command=save,padx=10,pady=10,font=("constantia",15,"italic")).grid(row=len(fields), column=1, columnspan=2, pady=5,padx=20)
    def manage_patients(self,):
        self.show_treeview("patient",self.delete_selected,("ID","name","phone","active"),button=True,button2=True)
        self.active.config(command=lambda:self.activate_deactivate("patients"))
    def manage_doctors(self):
        self.show_treeview("doctor",self.delete_selected,("ID","Name","Phone","Specialization","license_number","Active"),button=True,button2=True)
        self.active.config(command=lambda:self.activate_deactivate("doctors"))
    def manage_employees(self):
        self.show_treeview("employee",self.delete_selected,columns=("ID","name","phone","age","gender","active"),button=True,button2=True)
        self.active.config(command=lambda:self.activate_deactivate("employees"))
    def calculator(self):
        Calculator(Toplevel(self.root))
    def activate_deactivate(self, filename):
        # Make sure a tree/table is present and still exists
        if not hasattr(self, "table") or not getattr(self, "table"):
            messagebox.showwarning("Error", "Open the list first (click Manage …) then select a row.")
            return
        try:
            if not self.table.winfo_exists():
                messagebox.showwarning("Error", "Table widget was closed — reopen the list and try again.")
                return
        except Exception:
            messagebox.showwarning("Error", "Table not available.")
            return
        selection = self.table.selection()
        if not selection:
            messagebox.showwarning("Wrong", "Select a row first")
            return
        item = self.table.item(selection[0])
        values = item.get("values", [])
        if not values:
            messagebox.showwarning("Wrong", "Selected row has no data")
            return
        id_value = values[0]
        phone= values[2]
        print(phone)
        patients = FileManager.load_data(filename)
        users = FileManager.load_data("users")
        def save_data(filename,elements,id_value,phone):
            for index,element in enumerate(elements):
                if str(element.get("id", element.get("id", ""))) == str(id_value) and str(element.get("phone"))==str(phone):
                    current = element.get("active", False)
                    print(current)
                    if current:
                        if messagebox.askyesno("Confirm", "Do you really want to deactivate this?"):
                            elements[index]["active"] = False
                    else:
                        if messagebox.askyesno("Confirm", "Do you really want to activate this?"):
                            elements[index]["active"] = True
                    FileManager.save_data(filename, elements)
                    if filename=="users":
                        return
                    messagebox.showinfo("Done", "Status updated.")
                    self.show_treeview(filename[:-1], self.delete_selected,tuple(column for column in tuple(map(str.capitalize, element.keys()))),button=True,button2=True)
                    return
                continue
            messagebox.showerror("Not found", "Selected item not found in data.")
            return
        save_data(filename="users",elements=users,id_value=id_value,phone=phone)
        save_data(filename=filename,elements=patients,id_value=id_value,phone=phone)
        return