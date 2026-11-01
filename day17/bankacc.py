# TASK 17 - MENU-DRIVEN BANK ACCOUNT SIMULATOR


def create_account(account_holder, initial_balance):
    return {
        "account_holder": account_holder,
        "balance": initial_balance,
        "transactions": []
    }


def get_balance(account):
    return account["balance"]


def deposit(account, amount):

    if amount <= 0:
        return False, "Deposit amount must be greater than zero."

    account["balance"] += amount

    account["transactions"].append({
        "type": "Deposit",
        "amount": amount,
        "balance": account["balance"]
    })

    return True, "Deposit successful."


def withdraw(account, amount):

    if amount <= 0:
        return False, "Withdrawal amount must be greater than zero."

    if amount > account["balance"]:
        return False, "Insufficient balance. Withdrawal rejected."

    account["balance"] -= amount

    account["transactions"].append({
        "type": "Withdrawal",
        "amount": amount,
        "balance": account["balance"]
    })

    return True, "Withdrawal successful."


def get_transaction_history(account):

    return account["transactions"]


if __name__ == "__main__":

    print("=" * 60)
    print("           BANK ACCOUNT SIMULATOR")
    print("=" * 60)

    name = input("Enter account holder name: ")

    while True:

        try:

            initial_balance = float(
                input("Enter initial deposit: ")
            )

            if initial_balance < 0:
                print(
                    "Initial balance cannot be negative."
                )
            else:
                break

        except ValueError:

            print(
                "Invalid amount. "
                "Please enter a valid number."
            )

    account = create_account(
        name,
        initial_balance
    )

    while True:

        print("\n")
        print("=" * 60)
        print("                 BANK MENU")
        print("=" * 60)

        print("1. Balance Inquiry")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Exit")

        choice = input(
            "Enter your choice: "
        )

        if choice == "1":

            print(
                f"\nCurrent Balance: "
                f"₹{get_balance(account):.2f}"
            )

        elif choice == "2":

            try:

                amount = float(
                    input("Enter deposit amount: ")
                )

                success, message = deposit(
                    account,
                    amount
                )

                print(message)

                if success:
                    print(
                        f"New Balance: "
                        f"₹{account['balance']:.2f}"
                    )

            except ValueError:

                print(
                    "Invalid amount."
                )

        elif choice == "3":

            try:

                amount = float(
                    input("Enter withdrawal amount: ")
                )

                success, message = withdraw(
                    account,
                    amount
                )

                print(message)

                if success:
                    print(
                        f"New Balance: "
                        f"₹{account['balance']:.2f}"
                    )

            except ValueError:

                print(
                    "Invalid amount."
                )

        elif choice == "4":

            transactions = get_transaction_history(
                account
            )

            if not transactions:

                print(
                    "\nNo transactions available."
                )

            else:

                print("\nTransaction History")
                print("-" * 60)

                for transaction in transactions:

                    print(
                        f"{transaction['type']:<15}"
                        f"₹{transaction['amount']:>12.2f}"
                        f"  Balance: "
                        f"₹{transaction['balance']:.2f}"
                    )

        elif choice == "5":

            print(
                "\nThank you for using "
                "Bank Account Simulator!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1 to 5."
            )