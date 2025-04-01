import unittest
import json
from expense_tracker import Transaction

class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        """Prepare test data before each test."""
        self.sample_transactions = [
            {"date": "2025-04-01", "category": "Food", "amount": 500, "description": "Lunch"},
            {"date": "2025-04-02", "category": "Transport", "amount": 150, "description": "Bus fare"}
        ]
        with open(Transaction.FILE_NAME, "w") as file:
            json.dump(self.sample_transactions, file)

    def tearDown(self):
        """Clean up test data after each test."""
        open(Transaction.FILE_NAME, "w").close()

    def test_add_transaction(self):
        """Test adding a transaction"""
        Transaction.add_transaction("2025-04-03", "Shopping", 1200, "New clothes")
        with open(Transaction.FILE_NAME, "r") as file:
            data = json.load(file)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[-1]["category"], "Shopping")

    def test_delete_transaction(self):
        """Test deleting a transaction"""
        Transaction.delete_transaction(1)
        with open(Transaction.FILE_NAME, "r") as file:
            data = json.load(file)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "Food")

    def test_summary(self):
        """Test expense summary"""
        summary = Transaction.show_summary()
        self.assertIn("Food", summary)
        self.assertIn("Transport", summary)

if __name__ == "__main__":
    unittest.main()
