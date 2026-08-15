# Expense-Tracker
A CLI application that tracks your expenses.

Expenses are written in a JSON file.

## -Usage-
### Add new expenses:
```bash
# specify the description and the amount of the expense
python expense-tracker.py add -d 'Groceries' -a 100
```

### Summary expenses:
```bash
# you can specify which month of the current year to summary
python expense-tracker.py summary -m 08

# example output:
Total expenses: $300
```
### List expenses:
```bash
# it lists all your expenses
python expense-tracker.py list

# example output:
ID        Description    Date        Amount
---------------------------------------------
1         Groceries      08/14/2026  $100
2         Rent           08/14/2026  $200
```
### Edit expenses:
```bash
# specify the ID of the expense and add the changes.         
python expense-tracker.py edit 2 -d 'Rent' -a 200
``` 

### Delete expenses:
```bash
# specify the id of the expense you want to delete
python expense-tracker.py delete 1
```

## -How to install-

```bash
# clone the repo into your machine
git clone https://github.com/FLX009/expenses-tracker.git

# open the directory
cd expenses-tracker

# check all commands
python expense-tracker.py --help
```
Requires Python 3.7+
