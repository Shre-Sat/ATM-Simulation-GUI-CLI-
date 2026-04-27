import customtkinter as ctk
from . import logic
""" from . import sounds """  # Assuming you created sounds.py earlier

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ATMApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SHRESAT ATM SYSTEM")
        self.geometry("450x600")
        
        # Main container that holds everything
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_login_page()

    # --- PAGE 1: LOGIN ---
    def show_login_page(self):
        self.clear_screen()
        
        ctk.CTkLabel(self.main_container, text="WELCOME", font=("Orbitron", 30, "bold")).pack(pady=20)
        ctk.CTkLabel(self.main_container, text="Please Enter Account Number", font=("Arial", 14)).pack(pady=5)

        self.acc_entry = ctk.CTkEntry(self.main_container, placeholder_text="11-Digits", width=250, height=40, justify="center")
        self.acc_entry.pack(pady=10)

        login_btn = ctk.CTkButton(self.main_container, text="LOGIN", command=self.attempt_login, height=45, corner_radius=10)
        login_btn.pack(pady=20)

    def attempt_login(self):
        acc = self.acc_entry.get()
        if logic.validate_account_number(acc):
            # sounds.play_sound("welcome.mp3") 
            self.show_menu_page(acc)
        else:
            # sounds.play_sound("error.mp3")
            self.acc_entry.configure(border_color="red")
            print("Invalid Account")

    # --- PAGE 2: MAIN MENU ---
    def show_menu_page(self, acc):
        self.clear_screen()

        ctk.CTkLabel(self.main_container, text="SHRESAT BANK", font=("Arial", 16, "bold"), text_color="#3b8ed0").pack(pady=10)
        ctk.CTkLabel(self.main_container, text=f"Acc: {acc}", font=("Arial", 12)).pack()

        # Grid for Buttons (Keypad Style)
        menu_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        menu_frame.pack(pady=20, fill="both", expand=True)

        buttons = [
            ("Balance", self.display_balance),
            ("Deposit", self.display_deposit),
            ("Withdraw", self.display_withdraw),
            ("Statement", self.display_statement),
            ("Change PIN", self.display_change_pin),
            ("Logout", self.show_login_page)
        ]

        # Organizing buttons in 2 columns
        for i, (text, cmd) in enumerate(buttons):
            btn = ctk.CTkButton(menu_frame, text=text, command=cmd, height=50, width=160)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            
            # Make Logout Red
            if text == "Logout":
                btn.configure(fg_color="#a32a2a", hover_color="#822121")

    # --- FUNCTIONALITIES ---
    def display_balance(self):
        bal = logic.get_balance()
        self.show_popup("Current Balance", f"Your balance is:\n${bal:.2f}")

    def display_withdraw(self):
        # We will build a specific keypad for this in the next step
        amount = ctk.CTkInputDialog(text="Enter amount to withdraw:", title="Withdrawal").get_input()
        if amount:
            try:
                if logic.withdraw(float(amount)):
                    self.show_popup("Success", "Please collect your cash!")
                else:
                    self.show_popup("Error", "Insufficient funds or invalid amount.")
            except ValueError:
                self.show_popup("Error", "Please enter a valid number.")

    def display_deposit(self):
        amount = ctk.CTkInputDialog(text="Enter amount to deposit:", title="Deposit").get_input()
        if amount:
            try:
                if logic.deposit(float(amount)):
                    self.show_popup("Success", "Amount Deposited!")
                else:
                    self.show_popup("Error", "Invalid Amount.")
            except ValueError:
                self.show_popup("Error", "Please enter a valid number.")

    def display_statement(self):
        history = logic.get_statement()
        if not history:
            self.show_popup("Statement", "No transactions yet.")
            return
        
        # Format the history into a string
        report = ""
        for tx in history[-5:]: # Show last 5
            report += f"{tx['type']}: ${tx['amount']} ({tx['status']})\n"
        self.show_popup("Mini Statement", report)

    def display_change_pin(self):
        new_pin = ctk.CTkInputDialog(text="Enter new 4-digit PIN:", title="Change PIN").get_input()
        if logic.change_pin(new_pin):
            self.show_popup("Success", "PIN Changed! Please log in again.")
            self.show_login_page()
        else:
            self.show_popup("Error", "Invalid PIN Format (4 Digits).")

    # --- UTILS ---
    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_popup(self, title, message):
        # A simple alert window
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("300x150")
        popup.attributes("-topmost", True) # Keep on top
        
        ctk.CTkLabel(popup, text=message, pady=20).pack()
        ctk.CTkButton(popup, text="OK", command=popup.destroy).pack(pady=10)

if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()