from models.customer import Customer
from models.account import BankAccount
from models.bank import Bank
from services.transaction_service import TransactionService


# 1. Create the bank
bank1 = Bank(
    bank_id=1,
    bank_name="Montcrest Bank"
)


# 2. Create a customer
customer1 = Customer(
    customer_id=101,
    first_name="Aryan",
    last_name="Srivastava",
    date_of_birth="2003-05-15",
    email="aryan@example.com",
    phone_number="9876543210",
    address="Gorakhpur, Uttar Pradesh"
)


# 3. Add the customer to the bank
bank1.add_customer(customer1)


# 4. Create a bank account for the customer
account1 = BankAccount(
    account_number=1000001,
    customer=customer1,
    balance=50000,
    account_type="Savings",
    status="ACTIVE",
    created_at="2026-08-15"
)


# 5. Add the account to the bank
bank1.add_account(account1)


# 6. Create TransactionService
transaction_service = TransactionService(bank1)


# 7. Find the customer through the bank
found_customer = bank1.find_customer(101)

if found_customer:
    print("Customer Found:")
    print(found_customer.get_customer_info())


# 8. Find the account through the bank
found_account = bank1.find_account(1000001)

if found_account:
    print("\nAccount Found:")
    print(found_account.get_account_info())


# 9. Process deposit
deposit_result = transaction_service.process_deposit(
    account1,
    10000
)

print("\nDeposit Successful:", deposit_result)
print("After Deposit:")
print(account1.get_account_info())


# 10. Process withdrawal
withdrawal_result = transaction_service.process_withdrawal(
    account1,
    5000
)

print("\nWithdrawal Successful:", withdrawal_result)
print("After Withdrawal:")
print(account1.get_account_info())


# 11. Display final balance
print("\nFinal Balance:", account1.get_balance())


# 12. Display transaction history
print("\nTransaction History:")

for transaction in bank1.transactions:
    print(transaction.get_transaction_info())

