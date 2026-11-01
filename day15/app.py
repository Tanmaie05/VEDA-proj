from flask import Flask, render_template, request

app = Flask(__name__)


def calculate_subtotal(products):
    subtotal = 0

    for product in products:
        subtotal += product["quantity"] * product["price"]

    return subtotal


def calculate_discount(subtotal):
    if subtotal >= 5000:
        return subtotal * 0.10
    elif subtotal >= 2000:
        return subtotal * 0.05
    else:
        return 0


def calculate_tax(amount_after_discount):
    return amount_after_discount * 0.05


def calculate_total(subtotal, discount, tax):
    return subtotal - discount + tax


@app.route("/", methods=["GET", "POST"])
def home():

    products = []
    subtotal = 0
    discount = 0
    tax = 0
    final_amount = 0
    error = None

    if request.method == "POST":

        names = request.form.getlist("name")
        quantities = request.form.getlist("quantity")
        prices = request.form.getlist("price")

        try:
            for name, quantity, price in zip(names, quantities, prices):

                name = name.strip()

                if not name:
                    raise ValueError("Product name cannot be empty.")

                quantity = int(quantity)

                if quantity <= 0:
                    raise ValueError(
                        "Quantity must be greater than zero."
                    )

                price = float(price)

                if price < 0:
                    raise ValueError(
                        "Price cannot be negative."
                    )

                product = {
                    "name": name,
                    "quantity": quantity,
                    "price": price
                }

                products.append(product)

            if not products:
                raise ValueError("Please add at least one product.")

            subtotal = calculate_subtotal(products)

            discount = calculate_discount(subtotal)

            amount_after_discount = subtotal - discount

            tax = calculate_tax(amount_after_discount)

            final_amount = calculate_total(
                subtotal,
                discount,
                tax
            )

        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        products=products,
        subtotal=subtotal,
        discount=discount,
        tax=tax,
        final_amount=final_amount,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)