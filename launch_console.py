
import json
import os
import math
from datetime import datetime

FILE = "budget_data.json"


def load_data():
    if not os.path.exists(FILE):
        return {"transactions": [], "savings_goal": 0.0}

    try:
        with open(FILE, "r") as file:
            saved_data = json.load(file)

        if not isinstance(saved_data, dict):
            raise ValueError("Invalid data format.")

        transactions = saved_data.get("transactions", [])
        savings_goal = saved_data.get("savings_goal", 0)

        if not isinstance(transactions, list):
            raise ValueError("Invalid transactions data.")

        if isinstance(savings_goal, bool):
            raise ValueError("Invalid savings goal.")

        savings_goal = float(savings_goal)

        if not math.isfinite(savings_goal) or savings_goal < 0:
            raise ValueError("Invalid savings goal.")

        for t in transactions:
            if not isinstance(t, dict):
                raise ValueError("Invalid transaction.")

            if t.get("type") not in ["income", "expense"]:
                raise ValueError("Invalid transaction type.")

            if isinstance(t.get("amount"), bool):
                raise ValueError("Invalid transaction amount.")

            amount = float(t["amount"])

            if not math.isfinite(amount) or amount <= 0:
                raise ValueError("Invalid transaction amount.")

            if not isinstance(t.get("description"), str):
                raise ValueError("Invalid description.")

            if not isinstance(t.get("category"), str):
                raise ValueError("Invalid category.")

            if not isinstance(t.get("date"), str):
                raise ValueError("Invalid date.")

            t["amount"] = amount

        return {
            "transactions": transactions,
            "savings_goal": savings_goal
        }

    except (json.JSONDecodeError, ValueError, TypeError, KeyError) as e:
        raise SystemExit(
            f"\nERROR: Your budget_data.json file has invalid data: {e}\n"
            "Check or reset the JSON file before restarting BudgetBuddy."
        )


data = load_data()
transactions = data["transactions"]
savings_goal = data["savings_goal"]


def save_data():
    data = {
        "transactions": transactions,
        "savings_goal": savings_goal
    }

    temp_file = FILE + ".tmp"

    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)

    os.replace(temp_file, FILE)




def get_balance():
    balance = 0

    for t in transactions:
        if t["type"] == "income":
            balance += t["amount"]
        else:
            balance -= t["amount"]

    return balance


def show_balance():
    print("\n=== CURRENT BALANCE ===")
    print(f"Available money: ${get_balance():.2f}")




def add_transaction():
    print("\n1. Income")
    print("2. Expense")

    choice = input("Choose transaction type: ")

    if choice not in ["1", "2"]:
        print("Invalid choice.")
        return

    description = input("Description: ")
    category = input("Category (Food, Shopping, Allowance, etc.): ")

    try:
        amount = float(input("Amount: "))

        if not math.isfinite(amount) or amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    transaction_type = "income" if choice == "1" else "expense"

    transactions.append({
        "description": description,
        "category": category,
        "amount": amount,
        "type": transaction_type,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    save_data()
    print("Transaction added!")




def list_transactions():
    print("\n=== ALL TRANSACTIONS ===")

    if not transactions:
        print("No transactions yet.")
        return

    for t in transactions:
        sign = "+" if t["type"] == "income" else "-"

        print(
            f'{t["date"]} | {t["description"]} | '
            f'{t["category"]} | {sign}${t["amount"]:.2f}'
        )




def filter_category():
    category = input("Enter category: ").lower()

    found = False

    for t in transactions:
        if t["category"].lower() == category:
            sign = "+" if t["type"] == "income" else "-"

            print(
                f'{t["date"]} | {t["description"]} | '
                f'{sign}${t["amount"]:.2f}'
            )

            found = True

    if not found:
        print("No transactions found.")




def last_transaction():
    print("\n=== MOST RECENT TRANSACTION ===")

    if transactions:
        t = transactions[-1]
        sign = "+" if t["type"] == "income" else "-"

        print(
            f'{t["date"]} | {t["description"]} | '
            f'{t["category"]} | {sign}${t["amount"]:.2f}'
        )
    else:
        print("No transactions yet.")




def category_breakdown():
    print("\n=== CATEGORY BREAKDOWN ===")

    categories = {}

    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]

            categories[category] = (
                categories.get(category, 0) + t["amount"]
            )

    if not categories:
        print("No expenses recorded.")
        return

    for category, amount in categories.items():
        print(f"{category}: ${amount:.2f}")




def spending_summary():
    income = sum(
        t["amount"] for t in transactions
        if t["type"] == "income"
    )

    expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "expense"
    )

    print("\n=== SPENDING SUMMARY ===")
    print(f"Total income: ${income:.2f}")
    print(f"Total expenses: ${expenses:.2f}")
    print(f"Net balance: ${income - expenses:.2f}")




def set_savings_goal():
    global savings_goal

    print("\n=== SET SAVINGS GOAL ===")

    try:
        goal = float(input("Enter your savings goal: $"))

        if not math.isfinite(goal) or goal <= 0:
            print("Goal must be greater than zero.")
            return

        savings_goal = goal
        save_data()

        print(f"Savings goal set to ${savings_goal:.2f}!")

    except ValueError:
        print("Please enter a valid amount.")




def savings_calculator():
    print("\n SAVINGS CALCULATOR ")

    try:
        weekly_savings = float(
            input("How much will you save each week? $")
        )

        weeks = int(
            input("How many weeks do you want to save? ")
        )

        if not math.isfinite(weekly_savings) or weekly_savings < 0 or weeks <= 0:
            print("Enter a valid amount and number of weeks.")
            return

        total_savings = weekly_savings * weeks

        print("\n Final Result ")
        print(f" Total: ${total_savings:.2f}")

    except ValueError:
        print("Please enter valid numbers.")



def main():
    while True:
        print("\n====== BUDGET BUDDY ======")
        print("1) Show balance")
        print("2) List transactions")
        print("3) Add transaction")
        print("4) Filter by category")
        print("5) Show recent transaction")
        print("6) Category breakdown")
        print("7) Spending summary")
        print("8) Set savings goal")
        print("9) Savings calculator")
        print("0) Quit")

        choice = input("\nPick an option: ")

        if choice == "1":
            show_balance()

        elif choice == "2":
            list_transactions()

        elif choice == "3":
            add_transaction()

        elif choice == "4":
            filter_category()

        elif choice == "5":
            last_transaction()

        elif choice == "6":
            category_breakdown()

        elif choice == "7":
            spending_summary()

        elif choice == "8":
            set_savings_goal()

        elif choice == "9":
            savings_calculator()

        elif choice == "0":
            print("Thanks for using BudgetBuddy!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()

