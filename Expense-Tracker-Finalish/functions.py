import hashlib
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import numpy as np
from datetime import datetime, timedelta
import re



def clear_term():
  os.system("clear")


def sleep(entered_time):
  time.sleep(entered_time)


def get_hash(password):
  hash_object = hashlib.sha256(password.encode())
  return hash_object.hexdigest()


def load():
  try:
    load_hashes = pd.read_csv("Usernames&HashedPasswords.csv")
    if 'Usernames' not in load_hashes.columns or 'HashedPasswords' not in load_hashes.columns:
      return pd.DataFrame(columns=["Usernames", "HashedPasswords"])
    return load_hashes
  except FileNotFoundError:
    return pd.DataFrame(columns=["Usernames", "HashedPasswords"])
  except pd.errors.EmptyDataError:
    return pd.DataFrame(columns=["Usernames", "HashedPasswords"])


def save(usernames, hashed_passwords):
  df = pd.DataFrame({
      'Usernames': usernames,
      'HashedPasswords': hashed_passwords
  })
  df.to_csv("Usernames&HashedPasswords.csv", index=False)


def log_entry(df, amount, date, category):
  print(f"\nLogging entry: Amount={amount}, Date={date}, Category={category}")
  date_obj = pd.to_datetime(date)
  dateF = date_obj.strftime('%Y-%m-%d')
  new_entry = pd.DataFrame({
      'Date': [dateF],
      'Amount': [amount],
      'Category': [category]
  })
  updated_df = pd.concat([df, new_entry], ignore_index=True)
  return updated_df


def delete_log(df, category, date, amount):
  condition = (df['Category']
               == category) & (df['Date'] == date) & (df['Amount'] == amount)
  if condition.any():
    modified_df = df.drop(df[condition].index)
    return modified_df
  print("delete_log: No row was dropped, returning original DataFrame")
  return df


def save_data(df, filename):
  df.to_csv(filename, index=False)


def load_data(filename):
  try:
    df = pd.read_csv(filename)
    return df
  except FileNotFoundError:
    print(f"{filename} not found or empty, starting fresh.")
    return pd.DataFrame(columns=['Date', 'Amount', 'Category'])


def monthly_speding_sort(expense):
  expense['Date'] = pd.to_datetime(expense['Date'])
  expense['Year-Month'] = expense['Date'].dt.to_period('M')
  monthly_expense = expense.groupby('Year-Month')['Amount'].sum()
  print("\nPrinting Monthly Expenses\n")
  print(monthly_expense)


def monthly_income_sort(income):
  income['Date'] = pd.to_datetime(income['Date'])
  income['Year-Month'] = income['Date'].dt.to_period('M')
  monthly_income = income.groupby('Year-Month')['Amount'].sum()
  print("\nPrinting Monthly Income\n")
  print(monthly_income)


def yearly_income_sort(income):
  income['Date'] = pd.to_datetime(income['Date'])
  income['Year'] = income['Date'].dt.to_period('Y')
  yearly_income = income.groupby('Year')['Amount'].sum()
  print("\nPrinting Yearly Income\n")
  print(yearly_income)


def category_based_spending_sort(expense):
  category_spending = expense.groupby('Category')['Amount'].sum()
  print("\nPrinting Category Based Spending\n")
  print(category_spending)


def plot_spending_by_date(expense):
  expense['Date'] = pd.to_datetime(expense["Date"])
  plt.figure(figsize=(8, 6))
  plt.scatter(expense['Date'],
              expense['Amount'],
              color='red',
              marker='o',
              linestyle="-")
  plt.title('Spending by Date')
  plt.xlabel('Date')
  plt.ylabel('Amount Spent')
  plt.xticks(rotation=45)
  plt.grid(True)
  plt.savefig('Spending by Date.png', dpi=300)
  plt.show()
  print("\nFile Saved")


def plot_income_by_date(income):
  income['Date'] = pd.to_datetime(income['Date'])
  plt.figure(figsize=(8, 6))
  plt.scatter(income['Date'],
              income['Amount'],
              color='green',
              marker='o',
              linestyle='-')
  plt.title('Income by Date')
  plt.xlabel('Date')
  plt.ylabel('Amount Earned')
  plt.xticks(rotation=45)
  plt.grid(True)
  plt.savefig('Income_by_Date.png', dpi=300)
  plt.show()
  print("\nFile Saved")

def generate_dates(start_date, end_date, n):
  start = datetime.strptime(start_date, "%Y-%m-%d")
  end = datetime.strptime(end_date, "%Y-%m-%d")
  date_generated = [start + timedelta(days=x) for x in np.linspace(0, (end-start).days, n)]
  return [date.strftime("%Y-%m-%d") for date in date_generated]


def generate_income_csvs(n_csvs=10, entries_per_csv=50):
  categories = ["Paycheck", "Bonus", "Freelance"]
  csvs = []
  for _ in range(n_csvs):
      dates = generate_dates("2024-01-01", "2024-12-31", entries_per_csv)
      amounts = np.random.uniform(100, 5000, size=entries_per_csv).round(2)
      category_choices = np.random.choice(categories, size=entries_per_csv)
      df = pd.DataFrame({"Date": dates, "Amount": amounts, "Category": category_choices})
      csvs.append(df)
  return csvs

def generate_expense_csvs(n_csvs=10, entries_per_csv=50):
  categories = ["Groceries", "Utilities", "Rent", "Entertainment", "Healthcare", "Snacks"]
  csvs = []
  for _ in range(n_csvs):
      dates = generate_dates("2024-01-01", "2024-12-31", entries_per_csv)
      amounts = np.random.uniform(10, 300, size=entries_per_csv).round(2)
      category_choices = np.random.choice(categories, size=entries_per_csv)
      df = pd.DataFrame({"Date": dates, "Amount": amounts, "Category": category_choices})
      csvs.append(df)
  return csvs


def is_password_valid(password):

  if len(password) < 8:
      return False
  
  if not re.search("[A-Z]", password):
      return False
  
  if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
      return False
  
  return True