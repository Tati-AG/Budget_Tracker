import pytest
import datetime
import json
from expenses import Expense
from expenses_manager import Expenses_Manager

def test_edit_expense_object():
  exp = Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024')
  exp.edit_expense(amount = 55.2)
  assert exp.amount == pytest.approx(55.2)

def test_object_to_dict():
  exp = Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024')
  expense_dict = exp.to_dict()
  assert expense_dict == {'description': 'Weekly grocery shopping', 'amount': 52.7, 'category': 'Groceries', 'date': '09/06/2024'}

def test_amount_validation_type_exception():
  with pytest.raises(TypeError, match = 'Amount must be of numeric type'):
    Expense.validate_amount('1,00')

def test_amount_validation_value_exception():
  with pytest.raises(ValueError, match = 'Amount must be positive'):
    Expense.validate_amount(-1)

def test_amount_validation_int():
  assert 10 == Expense.validate_amount(10)

def test_amount_validation_float():
  assert pytest.approx(20.50) == Expense.validate_amount(20.50)

def test_date_validation_value_exception():
  with pytest.raises(ValueError, match = 'Date must be in the format DD/MM/YYYY'):
    Expense.validate_date('2000-11-09')

def test_amount_validation_int():
  assert datetime.date(2000,11,9) == Expense.validate_date('09/11/2000')

def test_add_expense():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024'))
  assert len(budget.expenses) == 1
  assert budget.expenses[0].description == 'Weekly grocery shopping'
  assert budget.expenses[0].amount == pytest.approx(52.7)
  assert budget.expenses[0].category == 'Groceries'
  assert budget.expenses[0].date == datetime.date(2024,6,9)

def test_add_expense_without_data():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Bus fare', 4.5, 'Transport'))
  assert budget.expenses[0].date == datetime.date.today()

def test_edit_invalid_index():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024'))
  with pytest.raises(IndexError, match = 'Expense index out of range'):
    budget.edit_expense(-1, description = 'Weekly groceries')

def test_edit_expense_by_manager():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024'))
  budget.add_expense(Expense('Bus fare', 4.5, 'Transport'))
  budget.edit_expense(1, amount = 5)
  assert budget.expenses[1].amount == 5

def test_remove_invalid_index():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024'))
  with pytest.raises(IndexError, match = 'Expense index out of range'):
    budget.remove_expense(1)

def test_remove_expense():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024'))
  budget.remove_expense(0)
  assert len(budget.expenses) == 0

def test_list_empty_list(capsys):
  budget = Expenses_Manager()
  budget.list_expenses()
  out, _ = capsys.readouterr()
  assert out == ''

def test_list_single_expense(capsys):
  budget = Expenses_Manager()
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024'))
  budget.list_expenses()
  out, _ = capsys.readouterr()
  assert out == 'Date: 09/06/2024\tDescription: Weekly grocery shopping\tAmount: $52.70\tCategory: Groceries\n'

def test_list_multiple_expenses(capsys):
  budget = Expenses_Manager()
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '09/06/2024'))
  budget.add_expense(Expense('Bus fare', 4.5, 'Transport'))
  budget.add_expense(Expense('Lunch at cafe', 28.9, 'Dining'))
  budget.list_expenses()
  out, _ = capsys.readouterr()
  assert out == 'Date: 09/06/2024\tDescription: Weekly grocery shopping\tAmount: $52.70\tCategory: Groceries\nDate: 11/06/2024\tDescription: Bus fare\tAmount: $4.50\tCategory: Transport\nDate: 11/06/2024\tDescription: Lunch at cafe\tAmount: $28.90\tCategory: Dining\n'

def test_category_summary():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Monthly metro pass', 45.0, 'Transport', '01/06/2024'))
  budget.add_expense(Expense('Monthly bulk buy', 165.15, 'Groceries', '02/06/2024'))
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '06/06/2024'))
  budget.add_expense(Expense('Bus fare', 4.5, 'Transport', '07/06/2024'))
  budget.add_expense(Expense('Vegetables and fruits', 26.95, 'Groceries', '08/06/2024'))
  budget.add_expense(Expense('Movie ticket', 12.5, 'Entertainment', '09/06/2024'))
  budget.add_expense(Expense('Dinner at restaurant', 60.0, 'Dining', '10/06/2024'))
  budget.add_expense(Expense('Taxi fare', 12.57, 'Transport'))
  budget.add_expense(Expense('Concert ticket', 120.0, 'Entertainment'))
  budget.add_expense(Expense('Lunch at cafe', 28.99, 'Dining'))
  assert budget.summarize_by_category() == { 'Transport': 62.07, 'Groceries': 244.8, 'Entertainment': 132.5, 'Dining': 88.99 }

def test_save_to_file():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Monthly metro pass', 45.0, 'Transport', '01/06/2024'))
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '06/06/2024'))
  budget.add_expense(Expense('Taxi fare', 12.57, 'Transport'))
  budget.save_to_file('my_budget')
  with open('my_budget', 'r') as f:
    expenses_data = json.load(f)
    assert expenses_data == [{'description': 'Monthly metro pass', 'amount': 45.0, 'category': 'Transport', 'date': '01/06/2024'},
                            {'description': 'Weekly grocery shopping', 'amount': 52.7, 'category': 'Groceries', 'date': '06/06/2024'},
                            {'description': 'Taxi fare', 'amount': 12.57, 'category': 'Transport', 'date': '11/06/2024'}]
  
def test_read_from_file():
  budget = Expenses_Manager()
  budget.add_expense(Expense('Monthly metro pass', 45.0, 'Transport', '01/06/2024'))
  budget.add_expense(Expense('Weekly grocery shopping', 52.7, 'Groceries', '06/06/2024'))
  budget.add_expense(Expense('Taxi fare', 12.57, 'Transport'))
  file_budget = Expenses_Manager()
  file_budget.load_from_file('my_budget')
  assert budget.expenses == file_budget.expenses