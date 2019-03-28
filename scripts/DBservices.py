from Transaction import Transaction
from Product import Product


def insert_transaction(TransactionId: int, productCode: int):
    transaction = Transaction()
    transaction.transactionId = TransactionId
    transaction.productCode.append(productCode)

    transaction.save()


def find_transcation_by_id(TransactionId: int) -> Transaction:
    transaction = Transaction.objects().filter(transactionId=TransactionId).first()
    return transaction

def find_product_by_code(productCode: int) -> Product:
    product = Product.objects().filter(productCode=productCode).first()
    return product


def update_transaction(transaction: Transaction, productCode):
    transaction.productCode.append(productCode)
    transaction.save()
