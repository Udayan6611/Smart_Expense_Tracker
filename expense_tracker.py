import json
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

class Transaction:
    FILE_NAME = "transactions.json"  # File where transactions will be stored

    def __init__(self, date, category, amount, description=""):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not value:
            raise ValueError("Date cannot be empty.")
        self._date = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value:
            raise ValueError("Category cannot be empty.")
        self._category = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Amount should be a positive number.")
        self._amount = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @staticmethod
    def load_from_file():
        """Loads and displays transactions from the file."""
        try:
            with open(Transaction.FILE_NAME, "r") as file:
                transactions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ No transactions found.")
            return []

        if not transactions:
            print("⚠️ No transactions to display.")
            return []

        print("\n📜 **Transaction History:**")
        for i, transaction in enumerate(transactions, start=1):
            print(f"{i}. {transaction['date']} - {transaction['category']} - ₹{transaction['amount']}")

        return transactions

    @staticmethod
    def add_transaction(date=None, category=None, amount=None, description=None):
        """Adds a new transaction and saves it to the file."""
        if date is None:
            date = input("📅 Enter transaction date (YYYY-MM-DD): ").strip()
        if category is None:
            category = input("🛒 Enter transaction category: ").strip()
        if amount is None:
            amount = input("💰 Enter transaction amount: ").strip()

        try:
            amount = float(amount)
        except ValueError:
            print("❌ Invalid amount. Please enter a valid number.")
            return

        if description is None:
            description = input("📝 Enter description (optional): ").strip()
        
        if not description:
            description = "No description"

        new_transaction = {
            "date": date,
            "category": category,
            "amount": amount,
            "description": description
        }

        try:
            with open(Transaction.FILE_NAME, "r") as file:
                transactions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            transactions = []

        transactions.append(new_transaction)

        with open(Transaction.FILE_NAME, "w") as file:
            json.dump(transactions, file, indent=4)

        print("✅ Transaction added successfully!")

    @staticmethod
    def delete_transaction(index=None):
        """Deletes a transaction from the list."""
        transactions = Transaction.load_from_file()

        if not transactions:
            return

        if index is None:
            try:
                index = int(input("Enter the transaction number to delete: ")) - 1
            except ValueError:
                print("❌ Invalid input. Please enter a valid number.")
                return

        if index < 0 or index >= len(transactions):
            print("❌ Invalid transaction number.")
            return

        del transactions[index]

        with open(Transaction.FILE_NAME, "w") as file:
            json.dump(transactions, file, indent=4)

        print("✅ Transaction deleted successfully!")

    @staticmethod
    def show_summary():
        """Shows total spending per category and generates pie chart."""
        try:
            with open(Transaction.FILE_NAME, "r") as file:
                transactions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ No transactions found.")
            return "⚠️ No transactions found."

        if not transactions:
            print("⚠️ No transactions to summarize.")
            return "⚠️ No transactions to summarize."

        category_totals = defaultdict(float)
        total_spent = 0

        for transaction in transactions:
            category = transaction['category']
            amount = float(transaction['amount'])

            category_totals[category] += amount
            total_spent += amount

        summary_str = "\n📊 **Expense Summary:**\n"
        for category, total in category_totals.items():
            summary_str += f"🛒 {category}: ₹{total:.2f}\n"

        summary_str += f"\n💰 **Total Spent:** ₹{total_spent:.2f}\n"
        print(summary_str)

        # Pie chart for category breakdown
        labels = category_totals.keys()
        sizes = category_totals.values()

        plt.figure(figsize=(7, 7))
        plt.rcParams['font.family'] = 'Segoe UI'  # Works better on Windows
        plt.rcParams['axes.unicode_minus'] = False  # Ensure symbols display correctly
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(" Expense Category Breakdown")
        plt.axis('equal')
        plt.show()


        return summary_str

    @staticmethod
    def monthly_analysis():
        """Analyzes transactions by month and generates bar chart."""
        try:
            with open(Transaction.FILE_NAME, "r") as file:
                transactions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ No transactions found.")
            return

        monthly_data = defaultdict(list)

        for transaction in transactions:
            date = transaction["date"]
            month = date[:7]  # Extract YYYY-MM
            monthly_data[month].append(transaction)

        print("\n📊 Monthly Expense Summary:")

        months = []
        totals = []

        for month, transactions in monthly_data.items():
            total = sum(t["amount"] for t in transactions)
            months.append(month)
            totals.append(total)

        for month, total in zip(months, totals):
            print(f"\n📅 {month}: Total Spent = ₹{total:.2f}")

        plt.figure(figsize=(10, 5))
        plt.rcParams['font.family'] = 'Segoe UI'  # Works better on Windows
        plt.rcParams['axes.unicode_minus'] = False  # Ensure symbols display correctly
        plt.bar(months, totals, color='skyblue')
        plt.xlabel('Month')
        plt.ylabel('Total Spending (₹)')
        plt.title('Monthly Spending Analysis')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def export_to_csv():
        """Exports transactions to a CSV file."""
        try:
            with open(Transaction.FILE_NAME, "r") as file:
                transactions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️ No transactions found.")
            return

        with open("transactions.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

            for transaction in transactions:
                writer.writerow([
                    transaction["date"],
                    transaction["category"],
                    transaction["amount"],
                    transaction.get("description", "No description")  # Fix KeyError
                ])

        print("✅ Transactions exported to transactions.csv")


def menu():
    """Displays the menu and handles user input."""
    while True:
        print("\n=== Expense Tracker ===")
        print("1️⃣ Add Transaction")
        print("2️⃣ View Transactions")
        print("3️⃣ Delete Transaction")
        print("4️⃣ Show Expense Summary")
        print("5️⃣ Monthly Analysis")
        print("6️⃣ Export to CSV")
        print("7️⃣ Exit")

        choice = input("Choose an option (1/2/3/4/5/6/7): ").strip()

        if choice == "1":
            Transaction.add_transaction()
        elif choice == "2":
            Transaction.load_from_file()
        elif choice == "3":
            Transaction.delete_transaction()
        elif choice == "4":
            Transaction.show_summary()
        elif choice == "5":
            Transaction.monthly_analysis()
        elif choice == "6":
            Transaction.export_to_csv()
        elif choice == "7":
            print("👋 Exiting. Have a great day!")
            break
        else:
            print("❌ Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    menu()
