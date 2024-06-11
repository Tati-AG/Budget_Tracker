import json
from expenses import Expense

class Expenses_Manager:

  def __init__(self):
    self.expenses = []
  
  def add_expense(self, expense):
    self.expenses.append(expense)

  def edit_expense(self, index, description = None, amount = None, category = None, date = None):
    if 0 <= index < len(self.expenses):
      self.expenses[index].edit_expense(description, amount, category, date)
    else:
      raise IndexError("Expense index out of range")
  
  def remove_expense(self, index):
    if 0 <= index < len(self.expenses):
      del self.expenses[index]
    else:
      raise IndexError("Expense index out of range")
  
  def list_expenses(self):
    for expense in self.expenses:
      print(expense)
  
  def summarize_by_category(self):
    summary = {}
    for expense in self.expenses:
      if expense.category in summary:
        summary[expense.category] += expense.amount
      else:
        summary[expense.category] = expense.amount
    return summary
  
  def save_to_file(self, filename):
    with open(filename, 'w') as f:
      json.dump([expense.to_dict() for expense in self.expenses], f, indent = 2)
  
  def load_from_file(self, filename):
    with open(filename, 'r') as f:
      expenses_data = json.load(f)
      self.expenses = [Expense(**data) for data in expenses_data]