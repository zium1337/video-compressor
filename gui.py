import tkinter
from tkinter import Tk
import customtkinter
from tkinter.filedialog import askopenfilename
import converter
import pathlib


class sidebar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.file = ""
        self.filesize = int
        self.state = tkinter.IntVar()
        self.title = customtkinter.CTkLabel(self, text="Configuration", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, columns=2, padx=10, pady=10, sticky="nwes")
        self.pathtitle = customtkinter.CTkLabel(self, text="Path:")
        self.pathtitle.grid(row=1, column=0, padx=10, pady=0)
        self.path = customtkinter.CTkTextbox(self, height=20, wrap="none", activate_scrollbars=False)
        self.path.grid(row=2, column=0, padx=10, pady=(0, 10))
        self.pathbutton = customtkinter.CTkButton(self, text="File", height=30, width=30, command=self.choosefile)
        self.pathbutton.grid(row=2, column=1, padx=10, pady=(0, 10))
        self.radiobutton1 = customtkinter.CTkRadioButton(self, text="10MB", value=10, variable=self.state, command=self.radiocheck)
        self.radiobutton2 = customtkinter.CTkRadioButton(self, text="25MB", value=20, variable=self.state, command=self.radiocheck)
        self.radiobutton3 = customtkinter.CTkRadioButton(self, text="50MB", value=50, variable=self.state, command=self.radiocheck)
        self.radiobutton4 = customtkinter.CTkRadioButton(self, text="Custom", value=0, variable=self.state, command=self.radiocheck)
        self.radiobutton1.grid(row=3, columns=2, padx=10, pady=(0, 10), sticky="nwes")
        self.radiobutton2.grid(row=4, columns=2, padx=10, pady=(0, 10), sticky="nwes")
        self.radiobutton3.grid(row=5, columns=2, padx=10, pady=(0, 10), sticky="nwes")
        self.radiobutton4.grid(row=6, columns=2, padx=10, pady=(0, 10), sticky="nwes")
        self.filesizetitle = customtkinter.CTkLabel(self, text="Custom file size (in MB):")
        self.filesizetext = customtkinter.CTkEntry(self, height=20)
        self.filesizetitle.grid(row=7, columns=2, padx=10, pady=0, sticky="nwes")
        self.filesizetext.grid(row=8, columns=2, padx=10, pady=(0, 10), sticky="nwes")
        self.convertbutton = customtkinter.CTkButton(self, text="Convert", command=self.compress_video)
        self.convertbutton.grid(row=9, columns=2, padx=10, pady=(0, 10), sticky="nwes")

    def choosefile(self):
        Tk().withdraw()
        filename = askopenfilename(title="Select video",
                                   filetypes=(("Movie Files", ".mp4 .avi .mkv"), ("", "")))
        self.file = filename
        self.path.configure(state="normal")
        self.path.delete("0.0", f"{len(filename)}.{len(filename)}")
        self.path.insert("0.0", f"\"{filename}\"")
        self.path.configure(state="disable")

    def radiocheck(self):
        state = int(self.state.get())
        if state == 0:
            self.filesizetext.configure(state="normal")
        else:
            self.filesize = state
            self.filesizetext.configure(state="disabled")

    def compress_video(self):
        ext = pathlib.Path(self.file).suffix
        output = "output" + ext
        if int(self.state.get()) == 0:
            fs = int(self.filesizetext.get())
            try:
                converter.compress_video(self.file, fs, output)
            except:
                print("Something is wrong!")
        else:
            fs = int(self.filesize)
            try:
                converter.compress_video(self.file, fs, output)
            except:
                print("Something is wrong!")


class gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video compressor by zium1337")
        self.theme = customtkinter.set_default_color_theme("green")
        self.geometry("400x400")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.sidebar = sidebar(self)
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="")


gui = gui()
gui.mainloop()
