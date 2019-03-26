def hashNum(hashTable, item):
    return hashTable[item]

def mapTransactions(int_header_table, transaction):
    header_table = {}
    for k in int_header_table.keys():
        header_table[str(k)] = int_header_table[k]
    #print('The header table is: ', header_table)
    #print('The transaction is: ', transaction)

    start = len(transaction) - 1
    stop = 0
    step = -1
    keyValuesToEmit = []
    for i in range(start, stop, step):
        currItem = transaction[i]
        currHash = hashNum(header_table, currItem)
        
        if currHash != None:
            # Delete currHash from the Hash table since it has already been processed
            if currHash in header_table.values():
                # Delete the current item 
                header_table.pop(currItem)
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
        'M', 'E', 'K'
    ]
    print('Processing the ordered and filtered transaction', sample_transaction)

    header_table = {
        'M': 0,
        'E': 1,
        'K': 2
    }

    # debug stuff
    #other_dict = {4157: 0, 15350: 2, 23356: 1, 28306: 5, 32981: 3, 36039: 4}
    #listKeys = [k  for  k in  header_table.keys()]
    #header_table_keys = list(header_table.keys())
    
    example = mapTransactions(header_table, sample_transaction)
    
    print('Executing reducer test...')
