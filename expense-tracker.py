import argparse
import datetime
import json


class ExpenseTracker:
    def __init__(self, expenses=None):
        self.expenses = expenses if expenses else []

    def get_date(self) -> str:
        x = datetime.datetime.now(tz=datetime.timezone.utc)
        y = x.strftime("%m/%d/%Y")
        return y

    def get_id(self):
        if not self.expenses:
            return 1
        else:
            return max(e["ID"] for e in self.expenses) + 1

    def write_file(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f, indent=2)

    def add_expense(self, desc: str, amount: int):
        if amount <= 0:
            return "invalid amount"
        expense = {
            "description": desc,
            "amount": amount,
            "date": self.get_date(),
            "ID": self.get_id(),
        }
        self.expenses.append(expense)
        self.write_file()
        return f"expense added. (ID:{expense['ID']})"

    def summary(self, month=None):
        x = 0
        if month:
            for e in self.expenses:
                x += (
                    e["amount"]
                    if month == e["date"][0:2]
                    and e["date"][6:]
                    == str(datetime.datetime.now(tz=datetime.timezone.utc).year)
                    else 0
                )
        else:
            for e in self.expenses:
                x += e["amount"]

        return f"Total expenses: ${x}"

    def del_expense(self, e_id):
        for e in self.expenses:
            if e["ID"] == e_id:
                self.expenses.remove(e)
                break
        else:
            return "expense not found"
        self.write_file()
        return "expense deleted"

    def edit_expense(self, e_id, e_desc=None, e_amount=None):
        if not e_desc and not e_amount:
            return "not enough arguments"
        for e in self.expenses:
            if e["ID"] == e_id:
                if e_desc:
                    e["description"] = e_desc
                if e_amount:
                    e["amount"] = e_amount
                self.write_file()
                return "expense edited"
        return "expense not found"

    def list_expenses(self) -> None:
        print(f"{'ID':<10}{'Description':<10}{'Date':^13}{'Amount':<10}")
        print(f"{'-' * 45}")
        for e in self.expenses:
            print(
                f"{e['ID']:<10}{e['description']:<10}{e['date']:^13}${e['amount']:<10}"
            )
        print(f"{'-' * 45}")


def main():
    parser = argparse.ArgumentParser(prog="expense-tracker")

    subparser = parser.add_subparsers(dest="command")

    add_parser = subparser.add_parser("add", help="add a expense to the tracker")
    add_parser.add_argument(
        "-d", "--description", required=True, help="description of the expense"
    )
    add_parser.add_argument(
        "-a", "--amount", required=True, type=int, help="amount of the expense"
    )

    delete_parser = subparser.add_parser("delete", help="deletes a task")
    delete_parser.add_argument(
        "ID", type=int, help="ID of the expense you want to deleted"
    )

    edit_parser = subparser.add_parser("edit", help="edit a expense")
    edit_parser.add_argument("ID", type=int, help="ID of expense you want to edit")
    edit_parser.add_argument("-d", "--description", help="new description")
    edit_parser.add_argument("-a", "--amount", type=int, help="new amount")

    subparser.add_parser("list", help="list all expenses")

    summary_parser = subparser.add_parser("summary", help="summary of the expenses")
    summary_parser.add_argument(
        "-m",
        "--month",
        choices=[f"{i:02d}" for i in range(1, 13)],
        help="filter by month",
    )

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
    elif args.command == "delete":
        print(tracker.del_expense(args.ID))
    elif args.command == "edit":
        print(tracker.edit_expense(args.ID, args.description, args.amount))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
