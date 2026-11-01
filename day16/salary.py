# TASK 16 - EMPLOYEE SALARY CALCULATOR


# Configurable salary rules
SALARY_RULES = {
    "hra_rate": 0.20,
    "da_rate": 0.10,
    "special_allowance_rate": 0.05,
    "pf_rate": 0.12,
    "professional_tax": 200
}


def calculate_hra(basic_salary):
    return basic_salary * SALARY_RULES["hra_rate"]


def calculate_da(basic_salary):
    return basic_salary * SALARY_RULES["da_rate"]


def calculate_special_allowance(basic_salary):
    return basic_salary * SALARY_RULES["special_allowance_rate"]


def calculate_gross_salary(basic_salary):
    hra = calculate_hra(basic_salary)
    da = calculate_da(basic_salary)
    special_allowance = calculate_special_allowance(basic_salary)

    return basic_salary + hra + da + special_allowance


def calculate_pf(basic_salary):
    return basic_salary * SALARY_RULES["pf_rate"]


def calculate_income_tax(gross_salary):

    if gross_salary <= 25000:
        tax = 0

    elif gross_salary <= 50000:
        tax = gross_salary * 0.05

    else:
        tax = gross_salary * 0.10

    return tax


def calculate_deductions(basic_salary, gross_salary):

    pf = calculate_pf(basic_salary)

    income_tax = calculate_income_tax(gross_salary)

    professional_tax = SALARY_RULES["professional_tax"]

    total_deductions = (
        pf
        + income_tax
        + professional_tax
    )

    return {
        "pf": pf,
        "income_tax": income_tax,
        "professional_tax": professional_tax,
        "total_deductions": total_deductions
    }


def calculate_net_salary(gross_salary, total_deductions):

    return gross_salary - total_deductions


def calculate_salary(basic_salary):

    hra = calculate_hra(basic_salary)

    da = calculate_da(basic_salary)

    special_allowance = calculate_special_allowance(
        basic_salary
    )

    gross_salary = calculate_gross_salary(
        basic_salary
    )

    deductions = calculate_deductions(
        basic_salary,
        gross_salary
    )

    net_salary = calculate_net_salary(
        gross_salary,
        deductions["total_deductions"]
    )

    return {
        "basic_salary": basic_salary,
        "hra": hra,
        "da": da,
        "special_allowance": special_allowance,
        "gross_salary": gross_salary,
        "pf": deductions["pf"],
        "income_tax": deductions["income_tax"],
        "professional_tax": deductions["professional_tax"],
        "total_deductions": deductions["total_deductions"],
        "net_salary": net_salary
    }


if __name__ == "__main__":

    print("=" * 60)
    print("           EMPLOYEE SALARY CALCULATOR")
    print("=" * 60)

    employee_name = input("Enter employee name: ")

    while True:

        try:

            basic_salary = float(
                input("Enter basic salary: ")
            )

            if basic_salary <= 0:

                print(
                    "Salary must be greater than zero."
                )

            else:

                break

        except ValueError:

            print(
                "Invalid input! "
                "Please enter a valid salary."
            )

    salary = calculate_salary(basic_salary)

    print("\n")
    print("=" * 60)
    print("              SALARY BREAKDOWN")
    print("=" * 60)

    print(f"Employee: {employee_name}")

    print("-" * 60)

    print(
        f"Basic Salary:        "
        f"₹{salary['basic_salary']:.2f}"
    )

    print(
        f"HRA:                 "
        f"₹{salary['hra']:.2f}"
    )

    print(
        f"DA:                  "
        f"₹{salary['da']:.2f}"
    )

    print(
        f"Special Allowance:   "
        f"₹{salary['special_allowance']:.2f}"
    )

    print("-" * 60)

    print(
        f"Gross Salary:        "
        f"₹{salary['gross_salary']:.2f}"
    )

    print("-" * 60)

    print(
        f"PF Deduction:        "
        f"₹{salary['pf']:.2f}"
    )

    print(
        f"Income Tax:          "
        f"₹{salary['income_tax']:.2f}"
    )

    print(
        f"Professional Tax:    "
        f"₹{salary['professional_tax']:.2f}"
    )

    print("-" * 60)

    print(
        f"Total Deductions:    "
        f"₹{salary['total_deductions']:.2f}"
    )

    print("-" * 60)

    print(
        f"NET SALARY:          "
        f"₹{salary['net_salary']:.2f}"
    )

    print("=" * 60)