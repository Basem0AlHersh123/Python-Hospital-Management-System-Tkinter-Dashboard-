from GUI.dashboards import Dashboard
from tkinter import *
from background.file_manager import FileManager
from tkinter import messagebox
from background.doctors import Doctor
class DoctorDashboard(Dashboard):
    def __init__(self, root,name):
        self.stats = [("Appointments", "appointments", "#ea4335"), ("Patients", "patients", "#4285f4")]
        super().__init__(root, main_theme="#fbbc05", dashboard_name="Doctor Dashboard", title="Doctor Panel", message=f"Welcome Dr. {name}", home_page_title="Doctor Panel", stats=self.stats, role="doctors", name=name)
        fields=[("🏠 Home Page",lambda:self.home_page(stats=self.stats)),
                    ("📅 My appointments ",self.show_appointments),
                    ("👥 My patients ",self.patients),
                    ("✍️ Add Diagnosis",self.add_diagnosis_ui)]
        self._appointments = FileManager.load_data("appointments")
        self.sidebar(fields=fields,background="#202124",button_bg="#3c4043", button_fg="#fbbc05")
        self._appointments = FileManager.load_data("appointments")
    def show_appointments(self):
        self.show_treeview(filename="appointment",function=self.delete_selected, columns= ("ID", "Doctor", "Date", "Diagnosis", "Treatement"),button=True)
    def patients(self):
        self.clear()
        Label(self.home, text="My Patients", font=("Arial",16,"bold")).pack(pady=8)
        self.show_treeview("patients",self.delete_selected,("ID","Name","Phone","Active"),button=True)
    def show_treeview(self, filename, function, columns, button=False):
        super().show_treeview(filename, function, columns, button)
        for row in self.table.get_children():
            self.table.delete(row)
        patients = FileManager.load_data("patients")
        doctors = FileManager.load_data("doctors")
        appointments = FileManager.load_data("appointments")
        doctor_id = self.fetch(data_list=doctors, compare_value=self.name, wanted_item="id")
        if filename == "patients":
            doctor_appts = [a for a in appointments if a.get("doctor_id") == doctor_id]
            patient_ids = {a.get("patient_id") for a in doctor_appts}
            for p in patients:
                if p.get("id") in patient_ids:
                    row = (p.get("id"), p.get("name"), p.get("phone"), p.get("active"))
                    self.table.insert("", "end", values=row)
        elif filename == "appointment":
            doctor_appts = [a for a in appointments if a.get("doctor_id") == doctor_id]
            for appointment in doctor_appts:
                patient_name = self.fetch(patients, compare_value=appointment.get("patient_id"), wanted_item="name")
                row = (
                    appointment.get("id"),
                    patient_name,
                    appointment.get("date"),
                    appointment.get("diagnosis") or "",
                    appointment.get("treatment") or ""
                )
                self.table.insert("", "end", values=row)
        self.table.pack(fill=BOTH, expand=True, padx=6, pady=6)
    def add_diagnosis_ui(self):
        self.clear()
        Label(self.home, text="Add Diagnosis to Appointment", font=("Arial", 20, "bold")).pack(pady=6)
        frame = Frame(self.home,width=150,padx=15,pady=15,relief="raised",bd=10)
        frame.place(relx=0.5,rely=0.5,anchor=CENTER)
        widgets={
                 "ID":"Appointment ID",
                 "diagnosis":"Diagnosis",
                 "treatment":"Treatment",
                 }
        index=0
        for key,value in widgets.items():
            
            Label(frame, text=value, font=("Arial", 15, "bold"),pady=20).grid(row=index, column=0, sticky=E)
            widgets[key] = Entry(frame,width=30,font=("courier",15,"bold"))
            widgets[key].grid(row=index, column=1,padx=10)
            index+=1
        def save_diag():
            appt_id = widgets["ID"].get().strip()
            for widget in ["ID","diagnosis","treatment"]:
                if not widgets[widget].get().strip():
                    messagebox.showwarning("Missing", f"Enter {widget}")
                    return
            self._appointments = FileManager.load_data("appointments")
            found = False
            for appointment in self._appointments:
                if str(appointment.get("id")) == str(appt_id):
                    appt_doc_id = appointment.get("doctor_id") 
                    doctors=FileManager.load_data("doctors")
                    test=self.fetch(doctors,compare_value=appointment.get("doctor_id"),wanted_item="id")
                    if str(appt_doc_id) != str(test):
                        continue
                    appointment["diagnosis"] = widgets["diagnosis"].get().strip()
                    appointment["treatment"] = widgets["treatment"].get().strip()
                    found = True
                    break
            if not found:
                messagebox.showerror("Not found", "Appointment not found or not assigned to you.")
                return
            patient_name=self.fetch(FileManager.load_data("patients"),compare_value=appointment.get("patient_id"),wanted_item="full_name")
            Doctor.add_diagnosis(appointment_id=appointment.get("id"),diagnosis=widgets["diagnosis"].get().strip(),treatment=widgets["treatment"].get().strip())
            messagebox.showinfo("Saved", "Diagnosis saved.")
            self.home_page(self.stats)
        Button(frame, text="Save", command=save_diag, bg="#34a853", fg="white",font=("impact",15),padx=20,pady=10).grid(row=3,column=0,columnspan=2,pady=8)
