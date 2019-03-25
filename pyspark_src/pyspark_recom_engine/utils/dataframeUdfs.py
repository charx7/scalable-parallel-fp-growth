# the user defined function that will reorder items based on a list
def list_sorter(transaction, sorted_items_dict):
    # Get the list of sorted items from the dict
    sorted_items_list = list(sorted_items_dict.keys())
    
    # Filtering out the items that do not appear in the sorted items list
    filtered_transaction = [item for item in transaction if item in sorted_items_list]
    
    # Order a transaction by the sorted items dict
    ordered_transaction_list = []
    for row in sorted_items_dict.keys():
        if row in filtered_transaction:
            ordered_transaction_list.append(row)
    
    if len(ordered_transaction_list) == 0:
        return None

    return ordered_transaction_list

if __name__ == '__main__':
    print('Executing test...')
    sampleOrderedItemsList = [
        5,
        7,
        2,
        1
    ]
    
    # Make indices
    sampleOrderedItemsIndex = [item for item in range(len(sampleOrderedItemsList))]
    
    # Make a dictionary using zip
    sampleOrderedItemsDict = dict(zip(sampleOrderedItemsList, sampleOrderedItemsIndex))
    
    sampleTransaction = [
        2,
        9,
        7,
        5
    ]
    singleItemTest = [
        2
    ]
    print('The sample transaction is: \n', singleItemTest)
    sorted = list_sorter(singleItemTest, sampleOrderedItemsDict)
    print(sorted)