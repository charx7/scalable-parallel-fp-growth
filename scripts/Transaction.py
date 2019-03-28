import mongoengine

class Transaction(mongoengine.Document):
    transactionId = mongoengine.IntField(required=True)
    productCode = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'transactions'
    }
