from . import logic

def start_menu():
    while True:
        print("\n" + "="*40)
        print("      WELCOME TO THE SHRESAT ATM")
        print("="*40)
        
        # PHASE 1: ACCOUNT LOGIN
        while True:
            acc_num = input("Please enter your 11-digit Account Number (or 'q' to quit): ")
            
            if acc_num.lower() == 'q':
                print("Shutting down ATM...")
                return # Exits

            if logic.validate_account_number(acc_num):
                print(f">> Account [{acc_num}] verified.")
                break # Moves to Phase 2
            else:
                print(">> [ERROR]: Invalid Account Number. Must be exactly 11 digits.")

        # PHASE 2: MAIN MENU
        while True:
            print("\n" + "-"*30)
            print("          ATM MENU")
            print("-"*30)
            print("1. Display Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Mini Statement")
            print("5. Change PIN")
            print("6. Logout/Exit")
            print("-"*30)

            choice = input("Select an option (1-6): ")

            if choice == '1':
                print(f"\n[CURRENT BALANCE]: ${logic.get_balance():.2f}")

            elif choice == '2':
                try:
                    amt = float(input("Enter amount to deposit: "))
                    if logic.deposit(amt):
                        print(">> Deposit Successful!")
                    else:
                        print(">> [ERROR]: Invalid deposit amount.")
                except ValueError:
                    print(">> [ERROR]: Please enter numbers only.")

            elif choice == '3':
                pin = input("Enter 4-digit PIN to authorize: ")
                if logic.verify_pin(pin):
                    try:
                        amt = float(input("Verified. Enter withdrawal amount: "))
                        if logic.withdraw(amt):
                            print(">> Success! Please collect your cash.")
                        else:
                            print(">> [ERROR]: Withdrawal failed (Check balance/amount).")
                    except ValueError:
                        print(">> [ERROR]: Invalid input.")
                else:
                    print(">> [DENIED]: Incorrect PIN.")

            elif choice == '4':
                pin = input("Enter PIN to view records: ")
                if logic.verify_pin(pin):
                    history = logic.get_statement()
                    print("\n--- TRANSACTION HISTORY ---")
                    if not history:
                        print("No transactions yet.")
                    else:
                        for tx in history:
                            print(f"Type: {tx['type']:<10} | Amt: ${tx['amount']:>8.2f} | Status: {tx['status']}")
                else:
                    print(">> [DENIED]: Access denied.")

            elif choice == '5':
                old_pin = input("Enter current PIN: ")
                if logic.verify_pin(old_pin):
                    new_pin = input("Enter NEW 4-digit PIN: ")
                    confirm_pin = input("Confirm NEW 4-digit PIN: ")
                    
                    if new_pin == confirm_pin:
                        if logic.change_pin(new_pin):
                            print(">> PIN changed successfully! Please log in again.")
                            break # Back to Login
                        else:
                            print(">> [ERROR]: PIN must be 4 digits.")
                    else:
                        print(">> [ERROR]: PINs do not match.")
                else:
                    print(">> [DENIED]: Incorrect current PIN.")

            elif choice == '6':
                print("\nLogging out... Thank you!")
                break # Back to Login

            else:
                print(">> Invalid choice. Please select 1-6.")