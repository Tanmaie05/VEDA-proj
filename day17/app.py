from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from bankacc import (
    create_account,
    get_balance,
    deposit,
    withdraw,
    get_transaction_history
)


app = Flask(__name__)

# Secret key required for Flask session
app.secret_key = "day17-bank-account-secret-key"


def get_account():

    if "account" not in session:
        return None

    return session["account"]


def save_account(account):

    session["account"] = account
    session.modified = True


@app.route("/", methods=["GET", "POST"])
def home():

    account = get_account()

    error = None
    message = None

    if request.method == "POST":

        action = request.form.get("action")

        # Create account
        if action == "create_account":

            account_holder = request.form.get(
                "account_holder",
                ""
            ).strip()

            initial_balance = request.form.get(
                "initial_balance",
                ""
            ).strip()

            if not account_holder:

                error = (
                    "Account holder name "
                    "cannot be empty."
                )

            else:

                try:

                    initial_balance = float(
                        initial_balance
                    )

                    if initial_balance < 0:

                        error = (
                            "Initial balance "
                            "cannot be negative."
                        )

                    else:

                        account = create_account(
                            account_holder,
                            initial_balance
                        )

                        save_account(account)

                        message = (
                            "Account created successfully!"
                        )

                except ValueError:

                    error = (
                        "Please enter a valid "
                        "initial balance."
                    )

        # Deposit
        elif action == "deposit":

            if account is None:

                error = (
                    "Please create an account first."
                )

            else:

                amount = request.form.get(
                    "amount",
                    ""
                ).strip()

                try:

                    amount = float(amount)

                    account = get_account()

                    success, result = deposit(
                        account,
                        amount
                    )

                    if success:

                        save_account(account)

                        message = result

                    else:

                        error = result

                except ValueError:

                    error = (
                        "Please enter a valid "
                        "deposit amount."
                    )

        # Withdraw
        elif action == "withdraw":

            if account is None:

                error = (
                    "Please create an account first."
                )

            else:

                amount = request.form.get(
                    "amount",
                    ""
                ).strip()

                try:

                    amount = float(amount)

                    account = get_account()

                    success, result = withdraw(
                        account,
                        amount
                    )

                    if success:

                        save_account(account)

                        message = result

                    else:

                        error = result

                except ValueError:

                    error = (
                        "Please enter a valid "
                        "withdrawal amount."
                    )

        # Reset account
        elif action == "reset":

            session.clear()

            account = None

            message = (
                "Account has been reset successfully."
            )

    account = get_account()

    transactions = []

    if account:

        transactions = get_transaction_history(
            account
        )

    return render_template(
        "index.html",
        account=account,
        transactions=transactions,
        error=error,
        message=message
    )


if __name__ == "__main__":

    app.run(debug=True)