import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from matplotlib import style
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import os
import requests
from io import BytesIO

def create_database():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title('Stock Market Prediction AI')
        self.attributes('-fullscreen', True)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LoginPage, SecondPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        screen_width = self.controller.winfo_screenwidth()
        screen_height = self.controller.winfo_screenheight()

        image_relative_path = "landscape and add 2 textboxes (1).png"
            
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, image_relative_path)
            
            image_opening = Image.open(image_path)
            image_opening = image_opening.resize((screen_width, screen_height), Image.LANCZOS)
            self.photo_opening = ImageTk.PhotoImage(image_opening)
            
            canvas_opening = tk.Canvas(self, background='grey', width=screen_width, height=screen_height)
            canvas_opening.pack(fill='both', expand=True)
            canvas_opening.create_image(0, 0, anchor=tk.NW, image=self.photo_opening)
        except (FileNotFoundError, UnidentifiedImageError) as e:
            canvas_opening = tk.Canvas(self, background='grey', width=screen_width, height=screen_height)
            canvas_opening.pack(fill='both', expand=True)
            label_opening = ttk.Label(self, text=f"Could not load image from file. Error: {e}\nEnsure '{image_relative_path}' is in the same directory as the script.", font=("Arial", 16))
            label_opening.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
        title_label = ttk.Label(self, text="Stock Market Prediction AI", font=("Arial", 32, "bold"), background="#021171", foreground="White")
        title_label.place(relx=0.5, rely=0.044, anchor=tk.CENTER)
        
        start_button = ttk.Button(self, text="Start", command=lambda: controller.show_frame("LoginPage"))
        start_button.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        width1 = int(self.controller.winfo_screenwidth())
        height1 = int(self.controller.winfo_screenheight())
        width_image = int(width1 / 2 + 400)

        image_path_login = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Login Page Image.png")
        
        try:
            image_login = Image.open(image_path_login)
            image_login = image_login.resize((width_image, height1), Image.LANCZOS)
            self.photo_login = ImageTk.PhotoImage(image_login)

            canvas_login = tk.Canvas(self, width=width1 / 2 + 400, height=height1, background='black')
            canvas_login.pack(side='left')
            image_label_login = ttk.Label(canvas_login, image=self.photo_login)
            image_label_login.pack()
        except (FileNotFoundError, UnidentifiedImageError) as e:
            frame_warning = ttk.Frame(self)
            frame_warning.pack(side='left', expand=True, fill='both')
            label_warning = ttk.Label(frame_warning, text=f"Could not load login page image.\nError: {e}\nEnsure 'Login Page Image.png' is in the same directory as the script.", font=("Arial", 16))
            label_warning.pack(pady=200, padx=50)

        frame_login = ttk.Frame(self, width=width1 - width1 / 2 + 400, height=height1)
        frame_login.pack(side='left', expand=True, fill='both')
        
        label1 = ttk.Label(frame_login, text='Login Page', font=("Arial", 16))
        label1.pack(side='top', pady=100)
        
        username_label = ttk.Label(frame_login, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(frame_login, bg="white")
        self.username_entry.pack()

        password_label = ttk.Label(frame_login, text="Password:")
        password_label.pack(pady=10)
        self.password_entry = tk.Entry(frame_login, show="*", bg="white")
        self.password_entry.pack()

        button_frame = ttk.Frame(frame_login)
        button_frame.pack(pady=20)
        
        sign_in_button = ttk.Button(button_frame, text="Sign In", command=self.sign_in)
        sign_in_button.pack(side='left', padx=10)
        
        sign_up_button = ttk.Button(button_frame, text="Sign Up", command=self.sign_up)
        sign_up_button.pack(side='left', padx=10)

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.controller.show_frame("SecondPage")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username and password:
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Sign up successful!")
        else:
            messagebox.showerror("Error", "Both fields are required")

class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def show_message(title, message):
            message_box = tk.Toplevel(self.controller)
            message_box.title(title)
            message_box.geometry("400x150")
            
            label = ttk.Label(message_box, text=message, font=("Arial", 14), wraplength=380, justify=tk.CENTER)
            label.pack(pady=20, padx=10, fill="both", expand=True)

            close_button = ttk.Button(message_box, text="OK", command=message_box.destroy)
            close_button.pack(pady=10)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', font=("Arial", 14), background='#4a90e2', foreground='white', borderwidth=0, relief='flat')
        style.map('TButton', background=[('active', '#357abd')])
        style.configure('PageTitle.TLabel', background='#f0f0f0', foreground='#333333', anchor="center")

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

        go_back_button = ttk.Button(self, text="Go Back to Login", command=lambda: controller.show_frame("LoginPage"))
        go_back_button.place(relx=0.02, rely=0.02, anchor="nw")
    
    def model1(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            df = pd.read_csv(os.path.join(script_dir, 'portfolio_data.csv'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV from file: {e}")
            return 0.0, np.array([])
        
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        feature = 'AMZN'
        forecast_out = 30

        df['label'] = df[feature].shift(-forecast_out)
        
        df_forecast = df.copy()
        df_forecast.drop(['label'], axis=1, inplace=True)
        
        x_train_val = np.array(df.drop(['label', feature], axis=1))
        y = np.array(df['label'])
        
        x_lately = np.array(df_forecast.drop([feature], axis=1))[-forecast_out:]

        df.dropna(inplace=True)
        
        x_train_val = np.array(df.drop(['label', feature], axis=1))
        y = np.array(df['label'])
        
        scaler = StandardScaler()
        x_train_val_scaled = scaler.fit_transform(x_train_val)
        x_lately_scaled = scaler.transform(x_lately)

        x_train, x_test, y_train, y_test = train_test_split(x_train_val_scaled, y, test_size=0.2)
        
        clf = svm.SVR()
        clf.fit(x_train, y_train)

        accuracy = clf.score(x_test, y_test)
        
        forecast = clf.predict(x_lately_scaled)
        
        return accuracy, forecast

    def model2(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            df = pd.read_csv(os.path.join(script_dir, 'portfolio_data.csv'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV from file: {e}")
            return 0.0, np.array([])

        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        feature = 'AMZN'
        forecast_out = 30

        df['label'] = df[feature].shift(-forecast_out)
        
        df_forecast = df.copy()
        df_forecast.drop(['label'], axis=1, inplace=True)
        
        x_train_val = np.array(df.drop(['label', feature], axis=1))
        y = np.array(df['label'])
        
        x_lately = np.array(df_forecast.drop([feature], axis=1))[-forecast_out:]

        df.dropna(inplace=True)
        
        x_train_val = np.array(df.drop(['label', feature], axis=1))
        y = np.array(df['label'])
        
        scaler = StandardScaler()
        x_train_val_scaled = scaler.fit_transform(x_train_val)
        x_lately_scaled = scaler.transform(x_lately)

        x_train, x_test, y_train, y_test = train_test_split(x_train_val_scaled, y, test_size=0.2)

        model = RandomForestRegressor(n_estimators=100)
        model.fit(x_train, y_train)
        
        accuracy = model.score(x_test, y_test)
        forecast = model.predict(x_lately_scaled)

        return accuracy, forecast
    
    def model3(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            df = pd.read_csv(os.path.join(script_dir, 'portfolio_data.csv'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV from file: {e}")
            return 0.0, np.array([])

        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        feature = 'AMZN'
        forecast_out = 30

        df['label'] = df[feature].shift(-forecast_out)
        
        df_forecast = df.copy()
        df_forecast.drop(['label'], axis=1, inplace=True)
        
        x_train_val = np.array(df.drop(['label', feature], axis=1))
        y = np.array(df['label'])
        
        x_lately = np.array(df_forecast.drop([feature], axis=1))[-forecast_out:]

        df.dropna(inplace=True)
        
        x_train_val = np.array(df.drop(['label', feature], axis=1))
        y = np.array(df['label'])
        
        scaler = StandardScaler()
        x_train_val_scaled = scaler.fit_transform(x_train_val)
        x_lately_scaled = scaler.transform(x_lately)

        x_train, x_test, y_train, y_test = train_test_split(x_train_val_scaled, y, test_size=0.2, random_state=42)

        model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, activation='relu', solver='adam', random_state=42)
        model.fit(x_train, y_train)

        accuracy = model.score(x_test, y_test)
        forecast = model.predict(x_lately_scaled)

        return accuracy, forecast

    def show_output_and_graph(self, algo_name, model_func):
        try:
            accuracy, data = model_func()
            
            result_window = tk.Toplevel(self.controller)
            result_window.title(f"{algo_name} Result")
            
            accuracy_label = tk.Label(result_window, text=f"Accuracy: {accuracy:.2f}", font=("Arial", 14))
            accuracy_label.pack(pady=10)
            
            if data is not None and data.size > 0:
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(data, label="Forecasted Price", color="green")
                ax.set_title(f"Stock Price Forecast - {algo_name}")
                ax.set_xlabel('Time')
                ax.set_ylabel('Stock Price')
                ax.legend()
                
                canvas = FigureCanvasTkAgg(fig, master=result_window)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill=tk.BOTH, expand=True)
                canvas.draw()
            else:
                messagebox.showinfo("No Data", "No forecast data available for this algorithm.")

            # Center the window
            result_window.update_idletasks()
            window_width = result_window.winfo_width()
            window_height = result_window.winfo_height()
            screen_width = result_window.winfo_screenwidth()
            screen_height = result_window.winfo_screenheight()
            
            x = int((screen_width / 2) - (window_width / 2))
            y = int((screen_height / 2) - (window_height / 2))
            
            result_window.geometry(f"+{x}+{y}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

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
        start_button = ttk.Button(start_button_frame, text="START", command=lambda: controller.frames["SecondPage"].show_output_and_graph("SVR Model", controller.frames["SecondPage"].model1))
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

        title_label = ttk.Label(self, text="Random Forest", font=("Arial", 20, "bold"), style='PageTitle.TLabel')
        title_label.pack(pady=10)

        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Regression Image.png")
        self.create_bg_image(image_path)

        start_button_frame = ttk.Frame(self, relief='solid', borderwidth=2)
        start_button_frame.pack(side="bottom", pady=20, fill="x", padx=20)
        start_button = ttk.Button(start_button_frame, text="START", command=lambda: controller.frames["SecondPage"].show_output_and_graph("Random Forest Model", controller.frames["SecondPage"].model2))
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
        start_button = ttk.Button(start_button_frame, text="START", command=lambda: controller.frames["SecondPage"].show_output_and_graph("ANN Model", controller.frames["SecondPage"].model3))
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
    create_database()
    app = App()
    app.mainloop()
