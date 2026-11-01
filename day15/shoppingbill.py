# TASK 15 - SHOPPING BILL GENERATOR


def calculate_subtotal(products):
    subtotal = 0

    for product in products:
        subtotal += product["quantity"] * product["price"]

    return subtotal


def calculate_discount(subtotal):

    if subtotal >= 5000:
        discount_rate = 0.10

    elif subtotal >= 2000:
        discount_rate = 0.05

    else:
        discount_rate = 0

    return subtotal * discount_rate


def calculate_tax(amount_after_discount):

    tax_rate = 0.05

    return amount_after_discount * tax_rate


def calculate_total(subtotal, discount, tax):

    return subtotal - discount + tax


def get_valid_quantity():

    while True:

        try:

            quantity = int(input("Enter quantity: "))

            if quantity <= 0:

                print(
                    "Invalid quantity! "
                    "Quantity must be greater than 0."
                )

            else:

                return quantity

        except ValueError:

            print(
                "Invalid quantity! "
                "Please enter a whole number."
            )


def main():

    products = []

    print("=" * 60)
    print("             SHOPPING BILL GENERATOR")
    print("=" * 60)

    try:

        number_of_products = int(
            input("Enter number of products: ")
        )

        if number_of_products <= 0:

            print(
                "Number of products must be greater than 0."
            )

            return

    except ValueError:

        print("Please enter a valid number.")

        return

    for i in range(number_of_products):

        print(f"\nProduct {i + 1}")

        name = input("Enter product name: ").strip()

        while not name:

            print("Product name cannot be empty.")

            name = input(
                "Enter product name: "
            ).strip()

        quantity = get_valid_quantity()

        while True:

            try:

                price = float(
                    input("Enter price: ")
                )

                if price < 0:

                    print(
                        "Price cannot be negative."
                    )

                else:

                    break

            except ValueError:

                print(
                    "Please enter a valid price."
                )

        product = {
            "name": name,
            "quantity": quantity,
            "price": price
        }

        products.append(product)

    subtotal = calculate_subtotal(products)

    discount = calculate_discount(subtotal)

    amount_after_discount = subtotal - discount

    tax = calculate_tax(amount_after_discount)

    final_amount = calculate_total(
        subtotal,
        discount,
        tax
    )

    print("\n")
    print("=" * 70)
    print("                       SHOPPING BILL")
    print("=" * 70)

    print(
        f"{'Product':<20}"
        f"{'Qty':>8}"
        f"{'Price':>15}"
        f"{'Amount':>15}"
    )

    print("-" * 70)

    for product in products:

        amount = (
            product["quantity"]
            * product["price"]
        )

        print(
            f"{product['name']:<20}"
            f"{product['quantity']:>8}"
            f"₹{product['price']:>13.2f}"
            f"₹{amount:>13.2f}"
        )

    print("-" * 70)

    print(
        f"{'Subtotal':<50}"
        f"₹{subtotal:>13.2f}"
    )

    print(
        f"{'Discount':<50}"
        f"₹{discount:>13.2f}"
    )

    print(
        f"{'Tax (5%)':<50}"
        f"₹{tax:>13.2f}"
    )

    print("-" * 70)

    print(
        f"{'FINAL AMOUNT':<50}"
        f"₹{final_amount:>13.2f}"
    )

    print("=" * 70)
    print("                 Thank you for shopping!")
    print("=" * 70)


if __name__ == "__main__":
    main()