import datetime

class Expense:

  def __init__(self, description, amount, category, date = None):
    self.description = description
    self.amount = amount
    self.category = category
    self.date = self.validate_date(date) if date else datetime.date.today()

  def __str__(self):
    return f'Date: {self.date.strftime("%d/%m/%Y")}\tDescription: {self.description}\tAmount: ${self.amount:.2f}\tCategory: {self.category}'

  def __eq__(self, other):
    if self.description != other.description:
      return False
    if self.amount != other.amount:
      return False
    if self.category != other.category:
      return False
    if self.date != other.date:
      return False
    return True

  def edit_expense(self, description = None, amount = None, category = None, date = None):
    if description != None:
      self.description = description
    if amount != None:
      self.amount = self.validate_amount(amount)
    if category != None:
      self.category = category
    if date != None:
      self.date = self.validate_date(date)

  def to_dict(self):
    return { 'description': self.description, 'amount': self.amount, 'category': self.category, 'date': self.date.strftime('%d/%m/%Y') }
    
  @staticmethod
  def validate_amount(amount):
    if not isinstance(amount, (int, float)):
      raise TypeError('Amount must be of numeric type')
    if amount < 0:
      raise ValueError('Amount must be positive')
    return amount

  @staticmethod
  def validate_date(date):
    try:
      return datetime.datetime.strptime(date, '%d/%m/%Y').date()
    except ValueError:
      raise ValueError('Date must be in the format DD/MM/YYYY')