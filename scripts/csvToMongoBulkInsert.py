#from builtins import len

import pandas as pd

import pymongo

import numpy as np

def unique(list1):
    x = np.array(list1)
    return np.unique(x)


def main():
    client = pymongo.MongoClient()
    db = client['AwesomeRecommendationEngine']
    collection = db['transactions']
    print("Created DB Connection")

    df = pd.read_csv('Ventas de Tienda.csv', sep=',', names=['TransactionID', 'ProductCode', 'ProductName','Brand'], header=None)
    listOfTransaction = []
    df = df.sort_values(by='TransactionID')
    df1 = df.groupby(['TransactionID']).groups.keys()
    print("Created List of Unique Transaction IDs")
    for i in df1:
        subset = df[(df['TransactionID'] == i)]
        ProductCode = subset['ProductCode'].tolist()
        uniqueProductCode = unique(ProductCode).tolist()
        mongo_json = {"TransactionID": i, "ProductCode": uniqueProductCode}
        listOfTransaction.append(mongo_json)
        if ((len(listOfTransaction)%100000) == 0):
            print(len(listOfTransaction))
            collection.insert_many(listOfTransaction)
            listOfTransaction.clear()
            print (len(listOfTransaction))


    collection.insert_many(listOfTransaction)
    print("Inserted all records in DB")


if __name__ == '__main__':
    main()


