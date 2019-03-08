
from collections import Counter
import pandas as pd


## Will generate the support count table for all the items present in all the transaction

def getSupportCount(listOfTransaction):
    itemSupportTable = pd.DataFrame(columns=['item', 'support'])
    listofAllItems = []
    for item in listOfTransaction:
        for i in item:
            listofAllItems.append(i)

    itemSupportTable['item'] = Counter(listofAllItems).keys()
    itemSupportTable['support'] = Counter(listofAllItems).values()

    itemSupportTable = itemSupportTable.sort_values(by='support', ascending=False)

    return itemSupportTable


## Will only keep the items which have count greater than or equal to a threshold value.

def thresholdSupport(itemSupportTable, thresholdValue, finalSupportTable):
    count = len(itemSupportTable)
    if itemSupportTable['support'].iloc[count - 1] == thresholdValue:
        finalSupportTable = pd.concat([finalSupportTable, itemSupportTable])
        return finalSupportTable
    if itemSupportTable['support'].iloc[count // 2] >= thresholdValue:
        finalSupportTable = pd.concat([finalSupportTable, itemSupportTable[:count // 2]])
        return thresholdSupport(itemSupportTable[count // 2:], thresholdValue, finalSupportTable)
    if itemSupportTable['support'].iloc[round(count // 2)] < thresholdValue:
        return thresholdSupport(itemSupportTable[:round(count // 2)], thresholdValue, finalSupportTable)


## Will create the Ordered Item set in the same order as the frequent pattern list

def listingOrderedItem(listOfTransaction, finalSupportTable):
    orderedItemLists = []
    for item in listOfTransaction:
        orderedItemList = []
        for row in finalSupportTable.itertuples():
            if row[1] in item:
                orderedItemList.append(row[1])
                if (len(item) == len(orderedItemList)):
                    break
        orderedItemLists.append(orderedItemList)



def main():

## Reads the data from csv and store it in the data frame
    df = pd.read_csv('VentasTienda.csv', sep=',', names=['TransactionID', 'ProductCode', 'ProductName'], header=None)

## It will contain all the lists of all the items bought together in a transactions (Lists of list)
    listOfTransaction = []

## Sorting the value by transactionID
    df = df.sort_values(by='TransactionID')

## A dictionary which contains all the transaction ID which will help in creating a list of items bought in a transaction.
    df1 = df.groupby(['TransactionID']).groups.keys()

## It creates a list of items bought in a transactions and stores it in listOfTransaction list.
    for i in df1:
        subset = df[(df['TransactionID'] == i)]
        listOfTransaction.append(subset['ProductCode'].tolist())

## It will get all the items with support count in the data frame
    itemSupportTable = getSupportCount(listOfTransaction)

## A data frame to store the items which are above the threshold value
    finalSupportTable = pd.DataFrame(columns=['item', 'support'])

### Set the threshold value which you want to set and pass it in the function instead of thresholdValue
#    finalSupportTable = thresholdSupport(itemSupportTable,thresholdValue,finalSupportTable)

if __name__ == '__main__':
    main()

