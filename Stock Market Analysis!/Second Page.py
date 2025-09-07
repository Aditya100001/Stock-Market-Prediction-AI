import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import requests
from io import BytesIO
import os

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Stock Market AI")
        self.attributes('-fullscreen', True)
        
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', font=("Arial", 14), background='#4a90e2', foreground='white', borderwidth=0, relief='flat')
        style.map('TButton', background=[('active', '#357abd')])
        
        style.configure('PageTitle.TLabel', background='#f0f0f0', foreground='#333333', anchor="center")
        
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        page_name = MainPage.__name__
        frame = MainPage(parent=container, controller=self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()

        main_bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "App Background.jpeg")
        try:
            image_opening = Image.open(main_bg_path)
            image_opening = image_opening.resize((screen_width, screen_height), Image.LANCZOS)
            self.photo_opening = ImageTk.PhotoImage(image_opening)
            main_canvas = tk.Canvas(self, width=screen_width, height=screen_height, highlightthickness=0)
            main_canvas.pack(fill="both", expand=True)
            main_canvas.create_image(0, 0, image=self.photo_opening, anchor="nw")
        except (FileNotFoundError, UnidentifiedImageError) as e:
            main_canvas = tk.Canvas(self, width=screen_width, height=screen_height, bg="grey", highlightthickness=0)
            main_canvas.pack(fill="both", expand=True)
            label_opening = ttk.Label(main_canvas, text=f"Could not load main background image.\nError: {e}", font=("Arial", 16))
            main_canvas.create_window(screen_width/2, screen_height/2, window=label_opening)

        columns_frame = ttk.Frame(self, style='TFrame')
        columns_frame.place(relx=0.5, rely=0.5, anchor="center", width=screen_width * 0.8, height=screen_height * 0.8)
        columns_frame.grid_rowconfigure(0, weight=1)
        for i in range(3):
            columns_frame.grid_columnconfigure(i, weight=1, uniform="group1")

        SVRPage(columns_frame, controller).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        RegressionPage(columns_frame, controller).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ANNPage(columns_frame, controller).grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

class SVRPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style='TFrame', relief='solid', borderwidth=2)
        self.controller = controller

        title_label = ttk.Label(self, text="SVM", font=("Arial", 20, "bold"), style='PageTitle.TLabel')
        title_label.pack(pady=10)

        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SVM_margin.png")
        self.create_bg_image(image_path)

        start_button_frame = ttk.Frame(self, relief='solid', borderwidth=2)
        start_button_frame.pack(side="bottom", pady=20, fill="x", padx=20)
        start_button = ttk.Button(start_button_frame, text="START", command=lambda: messagebox.showinfo("SVM", "SVM Model started!"))
        start_button.pack(expand=True, fill="both", ipady=10)

    def create_bg_image(self, path):
        try:
            image = Image.open(path)
            image = image.resize((350, 450), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            canvas = tk.Canvas(self, width=350, height=450, highlightthickness=0)
            canvas.pack(expand=True, pady=10)
            canvas.create_image(0, 0, image=self.photo, anchor="nw")
        except (FileNotFoundError, UnidentifiedImageError) as e:
            label = ttk.Label(self, text=f"Could not load image.\nError: {e}", font=("Arial", 12), anchor="center")
            label.pack(expand=True, fill="both")

class RegressionPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style='TFrame', relief='solid', borderwidth=2)
        self.controller = controller

        title_label = ttk.Label(self, text="Regression", font=("Arial", 20, "bold"), style='PageTitle.TLabel')
        title_label.pack(pady=10)

        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regression Image.png")
        self.create_bg_image(image_path)

        start_button_frame = ttk.Frame(self, relief='solid', borderwidth=2)
        start_button_frame.pack(side="bottom", pady=20, fill="x", padx=20)
        start_button = ttk.Button(start_button_frame, text="START", command=lambda: messagebox.showinfo("Regression", "Regression Model started!"))
        start_button.pack(expand=True, fill="both", ipady=10)

    def create_bg_image(self, path):
        try:
            image = Image.open(path)
            image = image.resize((350, 450), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            canvas = tk.Canvas(self, width=350, height=450, highlightthickness=0)
            canvas.pack(expand=True, pady=10)
            canvas.create_image(0, 0, image=self.photo, anchor="nw")
        except (FileNotFoundError, UnidentifiedImageError) as e:
            label = ttk.Label(self, text=f"Could not load image.\nError: {e}", font=("Arial", 12), anchor="center")
            label.pack(expand=True, fill="both")

class ANNPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style='TFrame', relief='solid', borderwidth=2)
        self.controller = controller

        title_label = ttk.Label(self, text="ANN", font=("Arial", 20, "bold"), style='PageTitle.TLabel')
        title_label.pack(pady=10)

        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ANN Image.png")
        self.create_bg_image(image_path)

        start_button_frame = ttk.Frame(self, relief='solid', borderwidth=2)
        start_button_frame.pack(side="bottom", pady=20, fill="x", padx=20)
        start_button = ttk.Button(start_button_frame, text="START", command=lambda: messagebox.showinfo("ANN", "ANN Model started!"))
        start_button.pack(expand=True, fill="both", ipady=10)

    def create_bg_image(self, path):
        try:
            image = Image.open(path)
            image = image.resize((350, 450), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            canvas = tk.Canvas(self, width=350, height=450, highlightthickness=0)
            canvas.pack(expand=True, pady=10)
            canvas.create_image(0, 0, image=self.photo, anchor="nw")
        except (FileNotFoundError, UnidentifiedImageError) as e:
            label = ttk.Label(self, text=f"Could not load image.\nError: {e}", font=("Arial", 12), anchor="center")
            label.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()
