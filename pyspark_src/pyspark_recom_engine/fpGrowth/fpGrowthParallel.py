import collections

def getConditionalItems(ConditionalDatabase, threshold):
   fpTreeDict={}
   allConditionalItems = list(ConditionalDatabase[1])
   counter=collections.Counter(allConditionalItems)
   itemsDict = (dict(counter))
   for k,v in itemsDict.items():
       if v >= threshold:
           fpTreeDict[k]= v
   groupId = ConditionalDatabase[0]
   return (groupId,fpTreeDict)

def hashNum(hashTable, item):
    return hashTable[item]

def mapTransactions(header_table, transaction):
    header_table_copy = header_table.copy()

    start = len(transaction) - 1
    stop = 0
    step = -1
    keyValuesToEmit = []
    for i in range(start, stop, step):
        currItem = transaction[i]
        currHash = hashNum(header_table_copy, currItem)
        
        if currHash != None:
            # Delete currHash from the Hash table since it has already been processed
            if currHash in header_table_copy.values():
                # Delete the current item 
                header_table_copy.pop(currItem)
                #print('the current keys on the ht are: ')
                #print(header_table.keys())

        # Emit the current k,v pair
        currValue = transaction[0:i]
        currKey   = currHash
        tupleToEmit = (currKey, tuple(currValue))
        keyValuesToEmit.append(tupleToEmit)
        #print('\nTo emit as value: ',currValue)
        #print('To emit as key: ', currHash)
        print('Tuple to emit: ', tupleToEmit)
    
    # Return value
    return keyValuesToEmit
                        

if __name__ == "__main__":
    print('Executing test...')

    sample_transaction = [
        '23', '24', '77'
    ]
    print('Processing the ordered and filtered transaction', sample_transaction)

    header_table = {
        '23': 0,
        '24': 1,
        '77': 2
    }

    # debug stuff
    #other_dict = {4157: 0, 15350: 2, 23356: 1, 28306: 5, 32981: 3, 36039: 4}
    #listKeys = [k  for  k in  header_table.keys()]
    #header_table_keys = list(header_table.keys())
    
    example = mapTransactions(header_table, sample_transaction)
    
    print('Executing reducer test...')
