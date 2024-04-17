import functions
import time
import pandas as pd


print("WELCOME TO EXPENSE TRACKER V11")
print("\nPLEASE LOGIN")


user_data = functions.load()

usernames = []
hashed_passwords = []
logged_in_user = []
if not user_data.empty:
  usernames = user_data['Usernames'].tolist()
  hashed_passwords = user_data['HashedPasswords'].tolist()

while True:
  store = input("\nDo you want to create a new account? (y/n): ")
  if store.lower() == "y":
    username_input = input("\nEnter Username: ")
    if username_input not in usernames:
      valid_password = False 
      while not valid_password:
        nonhashed_input = input("\nEnter Password: ")
        if functions.is_password_valid(nonhashed_input):
          valid_password = True 
          password_input = functions.get_hash(nonhashed_input)
          usernames.append(username_input)
          hashed_passwords.append(password_input)
          functions.save(usernames, hashed_passwords)
          print("\nAccount created successfully.\n")
          functions.sleep(1)
          functions.clear_term()
          logged_in_user.append(username_input)
        else:
          print("""\nPassword Not Valid Try Again, Password Must Contain:
          8 or More Characters
          An Uppercase and Lowercase Letter
          A Special Character""")
    else:
      print("\nUsername already exists. Please log in.\n")

  else:
    username_input = input("\nEnter Username: ")
    password_input = functions.get_hash(input("\nEnter Password: "))
    if username_input in usernames and hashed_passwords[usernames.index(username_input)] == password_input:
      print("\nLogged in successfully.\n")
      logged_in_user.append(username_input)
      functions.sleep(1)
      functions.clear_term()

      income = functions.load_data(f'CSVs/user-{logged_in_user[0]}-income.csv')
      expense = functions.load_data(f'CSVs/user-{logged_in_user[0]}-expenses.csv')

      #Admin
      if logged_in_user[0] == "Admin":
        print("\nWelcome System Administrator")
        while True:
          admin_choice = input(f"\nWhat would you like to do?:\n\n1.View Users 2.Delete Users 3.Create Sample CSV 4.View User Income/Expense 5.Drop To User: ").strip() 
          if admin_choice == "1":
            print("\n")
            for username in usernames:  
              print(f"{username}")
            print("\n")
          elif admin_choice == "2":
            username_input = input("\nEnter Username to remove: ")
            if username_input in usernames:
              index = usernames.index(username_input)
              usernames.pop(index)
              hashed_passwords.pop(index)
              functions.save(usernames, hashed_passwords)
              print("\nAccount removed successfully.\n")
              functions.sleep(1)
              functions.clear_term()
            else:
              print("\nUsername does not exist.\n")
          elif admin_choice == "3":
            name_choice = input("\nWhich User do you want to create data for?: ").strip()
            type_choice = input("\nIncome or Expense or Both?: ").strip().lower()
            if type_choice == "both":
              income_csvs = functions.generate_income_csvs()
              income_csvs[0].to_csv(f"CSVs/user-{name_choice}-income.csv", index=False)
              expense_csvs = functions.generate_expense_csvs()
              expense_csvs[0].to_csv(f"CSVs/user-{name_choice}-expenses.csv", index=False)
            elif type_choice == "income":
              income_csvs = functions.generate_income_csvs()
              income_csvs[0].to_csv(f"CSVs/user-{name_choice}-income.csv", index=False)
            elif type_choice == "expense":
              expense_csvs = functions.generate_expense_csvs()
              expense_csvs[0].to_csv(f"CSVs/user-{name_choice}-expenses.csv", index=False)
            else:
              print("Choice Not Valid Try Again")
          elif admin_choice == "4":
            print_user_choice = input("\nWould you like to view the users first? (y/n): ").strip().lower()
            if print_user_choice == "y":
              for username in usernames:
                print(f"{username}")
              print("\n")
              continue
            else:
              user_choice = input("\nWhich users data would you like to view?: ")
              if user_choice in usernames:
                admin_income = functions.load_data(f'CSVs/user-{user_choice}-income.csv')
                admin_expense = functions.load_data(f'CSVs/user-{user_choice}-expenses.csv')
                user_choice_type = input(f"\nWould you like to view {user_choice}'s income or expenses?: ").strip().lower()
                if user_choice_type == "expenses":
                  print(admin_expense)
                  print("\n")
                else:
                  print(admin_income)
                  print("\n")
          elif admin_choice == "5":
            break

          else:
            print("\nInvalid Choice Please Try Again")

      #User
      while True:
        choice1 = input(
            "\nChoose an option:(1.Log Expense, 2.Log Income, 3.View, 4.Remove Log, 5.Graphing, 6.Report 7.Exit): "
        ).strip()

        if choice1 == "1":
          amount = float(input("\nEnter the amount of the expense: ").strip())
          date = input(
              "\nEnter the date of the expense (e.g., YYYY-MM-DD): ").strip()
          category = input("\nEnter the category (e.g., Groceries): ")
          expense = functions.log_entry(expense, amount, date, category)
          functions.save_data(expense, f'CSVs/user-{logged_in_user[0]}-expenses.csv')

        elif choice1 == "2":
          amount = float(input("\nEnter the amount of the income: ").strip())
          date = input(
              "\nEnter the date of the income (e.g., YYYY-MM-DD): ").strip()
          category = input("\nEnter the category (e.g., Paycheck): ")
          income = functions.log_entry(income, amount, date, category)
          functions.save_data(income, f'CSVs/user-{logged_in_user[0]}-income.csv')

        elif choice1 == "3":
          choice2 = input(
              "\nWhat would you like to view (1.Income, 2.Expenses, 3.Finance Sorting): "
          ).strip()

          if choice2 == "1":
            print(income)
          elif choice2 == "2":
            print(expense)
          elif choice2 == "3":
            choice3 = input(
                "\n(1.Monthly Spending, 2.Monthly Income, 3.Yearly Income, 4.Category Based Spending): "
            )

            if choice3 == "1":
              functions.monthly_speding_sort(expense)
            elif choice3 == "2":
              functions.monthly_income_sort(income)
            elif choice3 == "3":
              functions.yearly_income_sort(income)
            elif choice3 == "4":
              functions.category_based_spending_sort(expense)
            else:
              print("Invalid Choice Please Try Again")

        elif choice1 == "4":
          choice3 = input(
              "\nWhat would you like to delete (1.Income, 2.Expense): ").strip(
              )
          if choice3 in ["1", "2"]:
            amount = float(input("\nEnter the amount: ").strip())
            date = input("\nEnter the date (e.g., YYYY-MM-DD): ").strip()
            category = input("\nEnter the category: ")
            if choice3 == "1":
              income = functions.delete_log(income, category, date, amount)
              functions.save_data(income, f'CSVs/user-{logged_in_user[0]}-income.csv')
            elif choice3 == "2":
              expense = functions.delete_log(expense, category, date, amount)
              functions.save_data(expense, f'CSVs/user-{logged_in_user[0]}-expenses.csv')

        elif choice1 == "5":
          choice5 = input(
              "\nWhat data would you like to plot (1.Expense, 2.Income)?: "
          ).strip()
          if choice5 == "1":
            functions.plot_spending_by_date(expense)
          elif choice5 == "2":
            functions.plot_income_by_date(income)
          else:
            print("Invalid choice for plotting.")

        elif choice1 == "6":
            current_time = time.localtime()
            report_date = time.strftime("%Y-%m-%d", current_time)
            report = pd.concat([income, expense], ignore_index=True)
            report["Net Income"] = income["Amount"] - expense["Amount"]
            report.to_csv(f"Reports/user-{logged_in_user[0]}-report-{report_date}.csv", index=False)
            print(f"\nReport Generated for {logged_in_user[0]} on {report_date}")
            functions.sleep(2)
            choice9 = input("\nWould you like to view this report now? (y/n): ")
            if choice9.lower() == "y":
              choice10 = input("\nWhat's the report date?: (YYYY-MM-DD): ")
              report_loaded = functions.load_data(f'Reports/user-{logged_in_user[0]}-report-{choice10}.csv')
              print(f"\n{report_loaded}")
            else:
              continue


        elif choice1 == "7":
          functions.save_data(income, f'CSVs/user-{logged_in_user[0]}-income.csv')
          functions.save_data(expense, f'CSVs/user-{logged_in_user[0]}-expenses.csv')
          print("\nData saved. Exiting...")
          break

        else:
          print("Invalid Choice, Try Again")
      break
    else:
      print("Login Incorrect, please try again!")
