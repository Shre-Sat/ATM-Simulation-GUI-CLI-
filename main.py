from atm_package.interface import start_menu
from atm_package.gui_interface import ATMApp

start = int(input("Which interface you want? Press 1 for CLI, Press 2 for GUI: "))

if start == 1:
    if __name__ == "__main__":
        try:
            start_menu()
        except KeyboardInterrupt:
            print("\n\nATM System forced to shut down. Goodbye!")
        except Exception as e:
            print(f"\n[CRITICAL ERROR]: {e}")

elif start == 2:
    if __name__ == "__main__":
        app = ATMApp()
        app.mainloop()  

else:
    print("Invalid Input")