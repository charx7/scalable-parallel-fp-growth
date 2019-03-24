import pandas as pd
import mongo_setup
import DBservices as svc

def main():
    # TODO: Setup mongoengine global values
    mongo_setup.global_init()
    df = pd.read_csv('VentasTienda.csv',sep=',',names=['TransactionID','ProductCode','ProductName'],header=None)
    listOfTransaction = []
    df = df.sort_values(by='TransactionID')
    df.head()
    df1 = df.groupby(['TransactionID']).groups.keys()
    for i in df1:
        subset=df[(df['TransactionID'] == i)]
        mongo_json = {"TransactionID": i, "ProductCode": subset['ProductCode'].tolist()}
        istOfTransaction.append(mongo_json)


if __name__ == '__main__':
    main()
