import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Single Window Application")
        self.geometry("600x400")

        # Configure rows and columns to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize two frames (screens)
        self.main_frame = MainFrame(self)
        self.menu_frame = MenuFrame(self)

        # Show the main frame by default
        self.show_frame(self.main_frame)

    def show_frame(self, frame):
        # Hide all frames
        self.main_frame.grid_forget()
        self.menu_frame.grid_forget()

        # Show the selected frame
        frame.grid(row=0, column=0, sticky="nsew")

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Main screen content
        label = ctk.CTkLabel(self, text="Main Screen", font=("Arial", 24))
        label.grid(row=0, column=0, padx=20, pady=20)

        # Button to navigate to the menu screen
        menu_button = ctk.CTkButton(self, text="Go to Menu", command=lambda: master.show_frame(master.menu_frame))
        menu_button.grid(row=1, column=0, padx=20, pady=20)

class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Menu screen content
        label = ctk.CTkLabel(self, text="Menu Screen", font=("Arial", 24))
        label.grid(row=0, column=0, padx=20, pady=20)

        # Button to navigate back to the main screen
        back_button = ctk.CTkButton(self, text="Back to Main", command=lambda: master.show_frame(master.main_frame))
        back_button.grid(row=1, column=0, padx=20, pady=20)

# Run the application
if __name__ == "__main__":
    app = App()
    app.mainloop()