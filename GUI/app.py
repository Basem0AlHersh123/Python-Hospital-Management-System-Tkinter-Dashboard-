from tkinter import *
from background.utils import resource_path   # <-- ADD THIS IMPORT

class App_interface:
    def __init__(self, root):
        self.root = root
        self.root.title("City Medical Center - Main page")
        self.root.geometry("720x720")
        self.root.resizable(FALSE, FALSE)

        image_path = resource_path("requirements/hosital (1).png")
        self.photo = PhotoImage(file=image_path)

        self.section = ""
        self.root.iconphoto(True, self.photo)

          
        self.canvas = Canvas(self.root, height=720, width=720)
        self.image = self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.canvas.pack()
        self.frame = Frame(self.root, height=360, width=360, padx=10, pady=10)
        self.frame.place(relx=0.5, rely=0.6, anchor=CENTER)
