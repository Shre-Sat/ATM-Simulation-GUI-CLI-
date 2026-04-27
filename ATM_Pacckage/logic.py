import re

# --- Data Storage ---
balance = 1000.0
transactions = []
SECRET_PIN = "1234"  # Default PIN

def get_balance():
    # current balance
    return balance

def validate_account_number(acc_num):
    # acc no. check
    return bool(re.match(r"^\d{11}$", str(acc_num)))

def validate_pin_format(pin):
    # pin check
    return bool(re.match(r"^\d{4}$", str(pin)))

def verify_pin(entered_pin):
    # pin verification
    return str(entered_pin) == SECRET_PIN

def deposit(amount):
    # Deposit
    global balance
    if amount > 0:
        balance += amount
        _log_transaction("Deposit", amount, "Success")
        return True
    _log_transaction("Deposit", amount, "Failed (Invalid Amount)")
    return False

def withdraw(amount):
    # Withdrawl
    global balance
    if 0 < amount <= balance:
        balance -= amount
        _log_transaction("Withdrawal", amount, "Success")
        return True
    
    if amount > balance:
        reason = "Insufficient Funds"
        _log_transaction("Withdrawal", amount, f"Failed ({reason})")
        return False
    else:
        reason = "Invalid Amount"
        _log_transaction("Withdrawal", amount, f"Failed ({reason})")
        return False

def get_statement():
    # list of transactions
    return transactions

def _log_transaction(t_type, amt, status):
    entry = {
        "type": t_type,
        "amount": amt,
        "status": status
    }
    transactions.append(entry)

def change_pin(pin):
    global SECRET_PIN
    if bool(re.match(r"^\d{4}$", str(pin))):
        SECRET_PIN = str(pin)
        return True
    return False