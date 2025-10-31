from GUI.dashboards import Dashboard
from tkinter import *
from background.file_manager import FileManager
from tkinter import messagebox
from tkinter.ttk import Treeview
from background.check import Check
class EmployeeDashboard(Dashboard):
    def __init__(self, root,role="patients", main_theme="#13a83f", dashboard_name="Employee Dashboard", title="Employee Panel", message="Reception", home_page_title="Employee Panel"):        
        self.stats=[("Total Patients","patients","#42eef4"),("Appointments","appointments","#7d35ea")]
        super().__init__(root, main_theme, dashboard_name, title, message, home_page_title, self.stats,role="patients",name=(name.get("name") for name in FileManager.load_data("patients")))
        fields=[("🏠 Home",lambda:self.home_page(stats=self.stats)),
                      ("👥 Manage Patients ",self.manage_patients_ui),
                      ("Book Appointment",self.book_appointment_ui)]
        self.sidebar(fields=fields,background="#202124",button_bg="#3c4043", button_fg="#ffffff",)
    def manage_patients_ui(self):
        self.show_treeview("patient",self.delete_selected,("ID","Name","Phone","Gender"))
        self.patietns=FileManager.load_data("patinet")
        self.table.pack(fill=BOTH,side="left", expand=True, padx=6, pady=6)
        Label(self.home, text="Manage Patients", font=("Arial",16,"bold")).pack(pady=6)
        right = Frame(self.table)
        right.pack(side=RIGHT, fill=Y, padx=6)
        columns=("ID","Name","Phone","Gender")
        table = Treeview(self.table, columns=columns, show="headings")
        for c in columns:
            table.heading(c, text=c); table.column(c, width=140)
        patients = FileManager.load_data("patients")
        for patient in patients:
            table.insert("", "end", values=(patient.get("id"), patient.get("name"), patient.get("phone"), patient.get("active")))
        table.pack(fill=BOTH, expand=True)
        Label(right, text="Add Patient", font=("Arial",12,"bold")).pack(pady=6)
        self.entries = {}
        for  field in ["Name","Password","Phone","Gender"]:
            Label(right, text=field).pack()
            entry = Entry(right); entry.pack()
            self.entries[field.lower()] = entry
        def add_patient():
            name = self.entries["name"].get().strip()
            phone=self.entries["phone"].get().strip()
            gender=self.entries["gender"].get().strip()
            password=self.entries["password"].get().strip()
            check=Check.check_box(name,gender,password,phone)
            if check:
                if not Check.is_valid_password(password=password):
                    messagebox.showerror("Error","Password must be at least 6 chars and contain a number")
                    return
                if not Check.is_valid_phone(phone=phone):
                    messagebox.showerror("Error","Phone must be 9 digits")
                    return
                if gender.capitalize()!="Male" and gender.capitalize()!="Female":
                    messagebox.showerror("Error","Gender should be either 'Male' or 'Female'")
                    return
                new = {
                    "id": max([patient.get("id", 0) for patient in self.patietns] or [0]) + 1,
                    "name": name,
                    "password":password,
                    "role":"patient",
                    "phone":phone ,
                    "active": True
                }
                data = FileManager.load_data("patients")
                data.append(new)
                FileManager.save_data("patients", data)
                messagebox.showinfo("Saved","Patient added.")
                self.manage_patients_ui()
            else:
                messagebox.showwarning("Error","fill all the requirements please")
        Button(right, text="Add", bg="#4285f4", fg="white", command=add_patient).pack(pady=8)
    def book_appointment_ui(self):
        self.clear()
        Label(self.home, text="Book Appointment", font=("Arial", 20, "bold")).pack(pady=6)
        frame = Frame(self.home,width=150,padx=15,pady=15,relief="raised",bd=10)
        frame.place(relx=0.5,rely=0.5,anchor=CENTER)
        widgets={
                 "ID":"Patient ID",
                 "doctor_id":"Doctor ID",
                 "datetime":"DateTime (YYYY-MM-DD HH:MM)"
                 }
        index=0
        for key,value in widgets.items():
            Label(frame, text=value, font=("Arial", 15, "bold"),pady=20).grid(row=index, column=0, sticky=E)
            widgets[key] = Entry(frame,width=30,font=("courier",15,"bold"))
            widgets[key].grid(row=index, column=1,padx=10)
            index+=1
        def save_appt():
            patient_id = widgets["ID"].get().strip()
            doctor_id = widgets["doctor_id"].get().strip()
            dt_txt = widgets["datetime"].get().strip()
            if not Check.check_box(patient_id , doctor_id , dt_txt):
                messagebox.showwarning("Missing","Complete the required fields")
                return
            check_date=Check.is_valid_date(dt_txt=dt_txt)
            if check_date is not True:
                if check_date=="Missing":
                    messagebox.showwarning(title=check_date,message="Enter DateTime")
                else:
                    messagebox.showerror(check_date, "Use YYYY-MM-DD HH:MM")
                return
            from background.patients import Patient
            doctor=self.fetch(FileManager.load_data("doctors"),
                              compare_value=int(widgets["doctor_id"].get().strip()),
                              wanted_item="name")
            patient=self.fetch(FileManager.load_data("patients"),
                               compare_value=widgets["doctor_id"].get().strip(),
                               wanted_item="name")
            print(type(widgets["doctor_id"].get().strip()),widgets["doctor_id"].get().strip())
            Patient.add_patient(doctor=doctor,patient=patient,patient_id=int(patient_id),doctor_id=int(doctor_id),dt_txt=dt_txt)
            messagebox.showinfo("Saved","Appointment booked.")
            self.home_page(self.stats)
        Button(frame, text="Save Appointment", bg="#34a853", fg="white",font=("constantia",15,"italic"), command=save_appt).grid(row=4,column=0,columnspan=2,pady=8)
