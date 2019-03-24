import mongoengine

class Product(mongoengine.Document):
    productCode = mongoengine.IntField(required=True)
    productName = mongoengine.StringField()

    meta = {
        'db_alias': 'core',
        'collection': 'products'
    }
