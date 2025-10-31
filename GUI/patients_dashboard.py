import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from background.file_manager import FileManager
from tkinter import *
from tkinter import messagebox, ttk
from GUI.dashboards import Dashboard
class PatientDashboard(Dashboard):
    def __init__(self, root,patient_name):
        self.appointments=FileManager.load_data("appointments")
        self.patients=FileManager.load_data("patients")
        self.patient_id=self.fetch(self.patients,compare_value=patient_name,wanted_item="id")
        self.name=patient_name
        self.stats=[("Name",self.name,"#68ea35"),("Phone",self.fetch(self.patients,compare_value=patient_name,wanted_item="phone"),"#e242f4")]
        super().__init__(root, main_theme="#ea4335", dashboard_name="Patients Dashboard", title="Patient Panel", message="Patient Home", home_page_title="Main Page", stats=self.stats,role="patients",name=patient_name)
        fields=[("🏠 Home",lambda:self.home_page(stats=self.stats)),
                      ("📅 My Appointments ",self.show_appointments),
                      ("📝 Request appointment ",self.request_appointment_ui),]
        self.sidebar(fields=fields,background="#202124",button_bg="#3c4043", button_fg="#ea4335")
    def home_page(self, stats, title="Main Page"):
        self.clear()
        Label(self.home,text=title,font=("Arial",20,"bold")).pack(pady=20)
        self.sub_home=Frame(self.home,bg="white")
        self.sub_home.pack(pady=10)
        self.sub_home=Frame(self.home,bg="white")
        self.sub_home.pack(pady=10)
        for index, (label,value,color) in enumerate(stats):
            self.sub_frame=Frame(self.sub_home,bg=color,width=200,height=150,relief="raised",bd=10)
            self.sub_frame.grid(row=index//2,column=index%2,padx=10,pady=20)
            self.sub_frame.pack_propagate(False)
            Label(self.sub_frame,text=label,fg="white",font=("Arial",20),bg=color).pack(pady=20)
            Label(self.sub_frame,text=value,fg="white",font=("Impact",20),bg=color,relief="groove",padx=10).pack()
    def show_appointments(self):
        self.show_treeview("appointment",self.delete_selected,("ID", "Doctor", "Date", "Diagnosis"),button=True)
        self.table.pack(fill=BOTH, expand=True, padx=6, pady=6)
    def show_treeview(self, filename, function, columns, button=False):
        super().show_treeview(filename, function, columns, button)
        self.table.destroy()
        self.table = ttk.Treeview(self.treeview, columns=columns, show="headings")
        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=120, anchor=W)
        appointments_ids = [appointment.get("id") for appointment in  self.appointments if appointment.get("patient_id")==self.fetch(self.patients,compare_value=self.name,wanted_item="id")]
        doctors=FileManager.load_data("doctors")
        for appointment in self.appointments:                
            if appointment.get("id") in appointments_ids:
                doctor_name=self.fetch(doctors,compare_value=appointment.get("doctor_id"),wanted_item="name")
                self.table.insert("", "end", values=(appointment.get("id"), doctor_name, appointment.get("date"), appointment.get("diagnosis")))
        self.table.pack(fill=BOTH, expand=True, padx=6, pady=6)


    def request_appointment_ui(self):
        self.clear()
        Label(self.home, text="Request New Appointment", font=("Arial", 20, "bold")).pack(pady=6)
        frame = Frame(self.home,width=150,padx=15,pady=15,relief="raised",bd=10)
        frame.place(relx=0.5,rely=0.5,anchor=CENTER)
        widgets={
                 "doc_id":"Doctor ID (optional)",
                 "datetime":"DateTime (YYYY-MM-DD HH:MM)"
                 }
        index=0
        for key,value in widgets.items():
            
            Label(frame, text=value, font=("Arial", 15, "bold"),pady=20).grid(row=index, column=0, sticky=E)
            widgets[key] = Entry(frame,width=30,font=("courier",15,"bold"))
            widgets[key].grid(row=index, column=1,padx=10)
            index+=1
        def send_request():
            dt_txt = widgets["datetime"].get().strip()
            from background.check import Check
            check_date=Check.is_valid_date(dt_txt=dt_txt)
            if check_date is not True:
                if check_date=="Missing":
                    messagebox.showwarning(title=check_date,message="Enter DateTime")
                else:
                    messagebox.showerror(check_date, "Use YYYY-MM-DD HH:MM")
                return
            doctors=FileManager.load_data("doctors")
            new = {
                "id": max([patient.get("id", 0) for patient in self.appointments] or [0]) + 1,
                "doctor":self.fetch(doctors,compare_value=int(widgets["doc_id"].get().strip()),wanted_item="name") or None,
                "patient":self.name,
                "date": dt_txt,
                "diagnosis": None,
                "treatment": None,
                "patient_id":self.patient_id,
                "doctor_id": int(widgets["doc_id"].get().strip()) or None,
                
            }
            self.appointments.append(new)
            FileManager.save_data("appointments", self.appointments)
            messagebox.showinfo("Requested", "Appointment request submitted.")
            self.home_page(self.stats)
        Button(frame, text="Request", bg="#4285f4", fg="white", command=send_request,padx=20,pady=20,font=("Courier",18,"bold")).grid(row=3, column=0, columnspan=2, pady=8)
