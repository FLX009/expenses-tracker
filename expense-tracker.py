import argparse
import json
import datetime

class ExpenseTracker:
    def __init__(self, expenses = []):
        self.expenses = expenses

    def get_date(self) -> str:
        x = datetime.datetime.now()
        y = x.strftime(("%m/%d/%Y"))
        return y
    
    def write_file(self) -> str:
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f, indent=2)
        return f"expense added. (ID:)"     

    def add_expense(self, desc: str, amount: int):
        if amount <= 0:
            return "invalid amount"
        expense = {
            "description": desc,
            "amount": amount,
            "date": self.get_date(),
        }
        self.expenses.append(expense)
        return self.write_file()

    def summary(self, month = None):
        x = 0
        if month:
            for e in self.expenses:
                x += e["amount"] if month == e["date"][0:2] else 0
        else:
            for e in self.expenses:
                x += e["amount"]

        return f"Total expenses: ${x}"
    
    def list_expenses(self) -> None:
        print(f"{'Description':<10}{'Date':^13}{'Amount':<10}")
        print(f"{'-' * 30}")
        for e in self.expenses:
            print(f"{e['description']:<10}{e['date']:^13}${e['amount']:<10}")
        print(f"{'-' * 30}")

def main():
    parser = argparse.ArgumentParser(prog="Expense Tracker")

    subparser = parser.add_subparsers(dest="command")

    add_parser = subparser.add_parser("add", help="add a expense to the tracker")
    add_parser.add_argument("-d", "--description", required=True, help="description of the expense")
    add_parser.add_argument("-a",  "--amount", required=True, type=int, help="amount of the expense")

    subparser.add_parser("list", help="list all expenses")

    summary_parser = subparser.add_parser("summary", help="summary of the expenses")
    summary_parser.add_argument("-m", "--month", choices=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], help="filter by month")

    args = parser.parse_args()

    try:
        with open("expenses.json", "r") as f:
            expenses = json.load(f)
        tracker = ExpenseTracker(expenses)
    except (FileNotFoundError, json.JSONDecodeError):
        tracker = ExpenseTracker()

    if args.command == "add":
        print(tracker.add_expense(args.description, args.amount))
    elif args.command == "list":
        tracker.list_expenses()
    elif args.command == "summary":
        if args.month:
            print(tracker.summary(args.month))
        else:
            print(tracker.summary())

if __name__ == "__main__":
    main()