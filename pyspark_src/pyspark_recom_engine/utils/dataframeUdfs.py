# the user defined function that will reorder items based on a list
def list_sorter(transaction, sorted_items_dict):
    print('\n')
    print(sorted_items_dict)
    
    # Get the list of sorted items from the dict
    sorted_items_list = list(sorted_items_dict.values())
    
    # Filtering out the items that do not appear in the sorted items list
    filtered_transaction = [item for item in transaction if item in sorted_items_list]
    print(filtered_transaction)

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
    sampleOrderedItemsDict = dict(zip(sampleOrderedItemsIndex, sampleOrderedItemsList))
    
    sampleTransaction = [
        2,
        9,
        7,
        5
    ]
    print('The sample transaction is: \n', sampleTransaction)
    list_sorter(sampleTransaction, sampleOrderedItemsDict)