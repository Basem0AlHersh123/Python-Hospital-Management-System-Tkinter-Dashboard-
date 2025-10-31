import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from background.file_manager import FileManager
from tkinter import *
from tkinter import messagebox,ttk
class Dashboard:
    def __init__(self,root,main_theme,dashboard_name,title,message,home_page_title,stats,role="",name=""):
        self.root=root
        self.title=Frame(self.root,bg=main_theme,height=60,pady=15,padx=10)
        self.title.pack(side="top",fill="x")
        Label(self.title,text=title,bg=main_theme,fg="white",font=("impact",30)).pack(side="top",anchor=CENTER)
        Button(self.title,bg="red",padx=10,pady=5,fg="white",text="Logout",font=("constantia",13,"bold"),command=self.logout).pack(side="left")
        Label(self.title,text=message,bg=main_theme,fg="white",font=("impact",20)).pack(side=RIGHT)
        self.root.title(dashboard_name)
        self.root.geometry("1024x640")
        self.home=Frame(self.root,bg="white")
        self.home.pack(side=RIGHT,pady=10,fill=BOTH,expand=True,padx=10)
        self.home_page_title=home_page_title
        self.stats=stats
        self.home_page(self.stats)
        self.role=role
        self.name=name
        Button(self.home, text="Manage Doctors", command=lambda: self.show_treeview(
            filename="doctor",
            function=self.delete_selected,
            columns=["id", "name", "specialization", "phone"],
            button=True
        )).pack(pady=5)

        Button(self.home, text="Manage Patients", command=lambda: self.show_treeview(
            filename="patient",
            function=self.delete_selected,
            columns=["id", "name", "age", "phone"],
            button=True
        )).pack(pady=5)

        Button(self.home, text="Appointments", command=lambda: self.show_treeview(
            filename="appointment",
            function=self.delete_selected,
            columns=["id", "doctor", "patient", "date"],
            button=True
        )).pack(pady=5)

        # self.sidebar(fields=fields,theme=sidebar_theme)
    def home_page(self,stats,title="Main Page"):
        self.clear()
        Label(self.home,text=title,font=("Arial",20,"bold")).pack(pady=20)
        self.sub_home=Frame(self.home,bg="white")
        self.sub_home.pack(pady=10)
        for index, (label,value,color) in enumerate(stats):
            self.sub_frame=Frame(self.sub_home,bg=color,width=200,height=150,relief="raised",bd=10)
            self.sub_frame.grid(row=index//2,column=index%2,padx=10,pady=20)
            self.sub_frame.pack_propagate(False)
            Label(self.sub_frame,text=label,fg="white",font=("Arial",20),bg=color).pack(pady=20)
            if "$"in value:
                Label(self.sub_frame,text=value,fg="white",font=("Impact",20),bg=color,relief="groove",padx=10).pack()
                
            else:
                # if self.role=="patients":
                    Label(self.sub_frame,text=len(FileManager.load_data(value)),fg="white",font=("Impact",20),bg=color,relief="groove",padx=10).pack()    

                # Label(sub_frame,text=len(FileManager.load_data(value)),fg="white",font=("Impact",20),bg=color,relief="groove",padx=10).pack()    
    def delete_selected(self, table, filename):
        selected = table.selection()
        if not selected:
            messagebox.showwarning(message="Select an item first to delete !!!")
            return

        item = table.item(selected[0])
        values = item['values']
        id_value = values[0]  
        if messagebox.askyesno(title='Warning', message="Are you sure you want to delete this item?"):
            data = FileManager.load_data(filename)
            if data and isinstance(data[0], dict):
                possible_keys = ["id", "doctor_id", "patient_id", "name"]
                for key in possible_keys:
                    if key in data[0]:
                        FileManager.delete_by_key(filename, key, id_value)
                        break
            table.delete(selected[0])
            messagebox.showinfo('success', 'The item has been successfully deleted')
    def show_treeview(self, filename, function, columns, button=False, button2=False):
        self.clear()
        filename1 = f"{filename}s"
        self.elements = FileManager.load_data(filename1)
        Label(self.home, text=filename1.capitalize(), font=("Arial", 20, "bold")).pack(pady=20)
        self.treeview = Frame(self.home, bg="white", width=650, height=300, bd=10)
        self.table = ttk.Treeview(self.treeview, columns=columns, show="headings")
        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=120, anchor=W)
        for index, element in enumerate(self.elements, start=1):
            first_column = columns[0]
            id_value = element.get("id", element.get("id", element.get(first_column.lower(), "")))
            row = [id_value]
            for column in columns[1:]:
                row.append(element.get(column.lower(), ""))
            self.table.insert(parent='', index="end", iid=index, values=row)
        self.table.pack(expand=True, fill=BOTH)
        self.treeview.pack(side="bottom", fill=BOTH, expand=True)
        if button:
            Button(self.treeview, text=f"Delete a {filename1[:-1]}",
                bg="red", font=("constantia", 20, "bold"),
                fg="white", command=lambda: function(self.table, filename=filename1)
                ).pack(side="bottom", pady=10)

            Button(self.treeview, text=f"Edit Selected {filename1[:-1]}",
                bg="orange", font=("constantia", 18, "bold"),
                fg="black", command=lambda: self.edit_selected(self.table, filename1)
                ).pack(side="bottom")

            if button2:
                list = {
                    "Add Doctor": lambda: self.open_add_form("doctor"),
                    "Add Patient": lambda: self.open_add_form("patient"),
                    "Add Appointment": lambda: self.open_add_form("appointment")
                }
                color = ["#7d35ea", "#fbbc05", "#42f4a1"]
                sub = Frame(self.home)
                for i, key in enumerate(list.keys()):
                    Button(sub, text=key, bg=color[i], fg="white",
                        command=list.get(key), padx=20, pady=5,
                        font=("constantia", 10, "italic")).pack(side="left")
                
                sub.pack(padx=5, pady=5, anchor=CENTER)


    def sidebar(self,fields,background,button_bg,button_fg):
        self.sidebar1=Frame(self.root,width=200,height=640,bg=background,padx=10,pady=10)
        self.sidebar1.pack(side="left",fill=BOTH)
        self.fields=fields
        self.entries={}
        for field,function in self.fields:
            Button(self.sidebar1,bg=button_bg, fg=button_fg,text=field,command=function,font=("Impact",12),width=20,padx=30,anchor=W,justify=LEFT,height=2,bd=0).pack(padx=10,pady=5,anchor=NW)
    def edit_selected(self, table, filename):
        selected = table.selection()
        if not selected:
            messagebox.showwarning(message="Select an item first to edit!")
            return

        item = table.item(selected[0])
        values = item['values']

        # Load existing data
        data = FileManager.load_data(filename)
        if not data:
            messagebox.showerror("Error", "No data found to edit.")
            return

        keys = list(data[0].keys())
        current = dict(zip(keys, values))

        win = Toplevel(self.home)
        win.title(f"Edit {filename[:-1]}")
        win.geometry("400x300")

        entries = {}
        for idx, key in enumerate(keys):
            Label(win, text=key.capitalize()).grid(row=idx, column=0, padx=10, pady=5)
            e = Entry(win)
            e.insert(0, str(current.get(key, "")))
            e.grid(row=idx, column=1, padx=10, pady=5)
            entries[key] = e

        def save():
            updated_item = {k: entries[k].get().strip() for k in keys}
            for i, row in enumerate(data):
                if row[keys[0]] == current[keys[0]]:
                    data[i] = updated_item
                    break
            FileManager.save_data(filename, data)
            messagebox.showinfo("Success", "Record updated successfully!")
            win.destroy()
            # refresh tree
            self.show_treeview(filename[:-1], self.delete_selected, [k.capitalize() for k in keys], button=True)

        Button(win, text="Save Changes", bg="blue", fg="white", command=save).grid(row=len(keys), column=0, columnspan=2, pady=10)

    def clear(self):        
        for widget in self.home.winfo_children():
            widget.destroy()
    def logout(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        from GUI.login_window import Loginwindow
        Loginwindow(self.root)

    @staticmethod
    def fetch(data_list, compare_value, wanted_item=None):
        for item in data_list:
            for key, value in item.items():
                if key == "password":
                    continue
                if str(value) == str(compare_value):
                    return item.get(wanted_item) if wanted_item else item
        return None

    def fetch_pro(self,wanted_item,compare_paramater):
        all_users=FileManager.load_data("appointments")
        data=FileManager.fetch(all_users,compare_paramater,wanted_item=wanted_item)
        FileManager.delete_by_key("doctors","id",3)
        return data