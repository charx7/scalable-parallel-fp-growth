import json
import itertools
from operator import itemgetter

### It will create a list of dictionaries for all the possible path for a particular item
### The key in the dictionary is path and value is the frequency.
def find_values(id, json_repr):
    results = []
    finalResult = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)  # Return value ignored.
    
    for i in results:
        
        elementToAppend = {str(tuple(i["parentTree"])):i["freq"]}
        finalResult.append(json.dumps(elementToAppend))
        
    return finalResult

def generatePowerset(item, conditional_patterns, threshold):
   print('The item is: ', item)
   print('The cond patterns are: ', conditional_patterns)
   listofPatterns = []
   finalList=[]
   print('Parsed cond patterns is: ',list(json.loads(conditional_patterns)))
   #conditional_patterns = json.loads(conditional_patterns) # String parse into dict
   for path in list(json.loads(conditional_patterns)):
       print('the path is: ', path)
       #path = json.loads(path)
       # print(list(path.keys()))
       for key,value in (path.items()):
           #print(key)
           #print(value)
           listOfPowerset = (powerset(list(eval(key))))
           #print(listOfPowerset)
           for sets in listOfPowerset:
               #tup = tuple(item)
               tup = (item, )
               print('The sets object is: ',sets)
               print('The type of sets is: ',type(sets))
               print('The tuple of sets object is: ', (sets,))
               if not isinstance(sets, tuple):
                   sets = (sets,)

               tupleToAppend = sets + tup
               stringToAppend = str(tupleToAppend)
               print('The string to append is: ', stringToAppend)
               dictToAppend = {
                   "ConditionalPatternSets": stringToAppend,
                   "freq": value
               }
               listofPatterns.append(dictToAppend)
   listofPatterns.sort(key=itemgetter("ConditionalPatternSets"))
   for key, group in itertools.groupby(listofPatterns, lambda item: item["ConditionalPatternSets"]):
       #print(key, sum([item["freq"] for item in group]))
       #finalList.append({"ConditionalPatternSets":key, "freq":sum([item["freq"] for item in group])})
       mydict = {"ConditionalPatternSets":key, "freq":sum([item["freq"] for item in group])}
       if (mydict["freq"] >= threshold):
           finalList.append(mydict)

   return finalList

### It will call the find_values function for all the items in the itemSupportTable
# It will store all the possible patterns in the data frame for a particular item.
def generateConditionalPatternBase(itemSupportTable,treeString):
    conditionalPatternBaseTable = pd.DataFrame(columns=['item','ConditionalPattern'])
    for itemset in itemSupportTable['item']:
        path = find_values(itemset,treeString)
        conditionalPatternBaseTable = conditionalPatternBaseTable.append({'item': itemset, 'ConditionalPattern': path},ignore_index=True)
        
    return conditionalPatternBaseTable


#### This is generic function which I had written for generating Powerset to test ['K','E','M','O','Y']
### Will write the function to generate the powersets and group it as we discussed for FP-Growth.
def powerset(iterable):
    if len(iterable) == 1:
        return iterable
    listOfPowerSets=[]
    for L in range(1, len(iterable)+1):
        for subset in itertools.combinations(iterable, L):
            listOfPowerSets.append(subset)
    
    return listOfPowerSets

def mergeList(finalPatternList,itemSupportList):
   mergedList=[]
   for singleItemSupport in itemSupportList:
       #item = tuple(set(item))
       singleItemSupport = eval(singleItemSupport)
       #print(type(singleItemSupport[1]),type(singleItemSupport[0]))
       mydict = {"ConditionalPatternSets": (singleItemSupport[0],),"freq":singleItemSupport[1]}
       mergedList.append(mydict)
   for item in finalPatternList:
       mydict = {"ConditionalPatternSets": eval(item["ConditionalPatternSets"]),"freq":int(item["freq"])}
       mergedList.append(mydict)
   return mergedList

def generate_association_rules(finalPatternList, itemSupportList, confidence_threshold):
   #rules = pd.DataFrame(columns=['boughtItem','suggestedItem','confidence'])
   RulesList = []

   mergedList = mergeList(finalPatternList,itemSupportList)
   patterns = {}
   for item in mergedList:
       patterns[item["ConditionalPatternSets"]] = item["freq"]

   for itemset in mergedList:
       union_support = itemset["freq"]

       for i in range(1, len(itemset["ConditionalPatternSets"])):
           for boughtItem in itertools.combinations(itemset["ConditionalPatternSets"], i):
               boughtItem = tuple(sorted(boughtItem))
               suggestedItem = tuple(sorted(set(itemset["ConditionalPatternSets"]) - set(boughtItem)))

               #if (d['ConditionalPatternSets'] == boughtItem for d in mergedList):
               if boughtItem in patterns.keys():
                   support = patterns[boughtItem]
                   confidence = float(union_support) / support

                   if confidence >= confidence_threshold:
                       RulesList.append({'boughtItem':boughtItem,'suggestedItem':suggestedItem,'confidence':confidence})
                      # rules['boughtItem','suggestedItem','confidence'] = [boughtItem,suggestedItem,confidence]


   return RulesList

def main():

    treeString = '{"root": {"children": [{"K": {"children": [{"E": {"children": [{"M": {"children": [{"O": {"children": [{"Y": {"children": [{}], "depth": 5, "parentTree": ["root", "K", "E", "M", "O"], "freq": 1}}], "depth": 4, "parentTree": ["root", "K", "E", "M"], "freq": 1}}], "depth": 3, "parentTree": ["root", "K", "E"], "freq": 1}}, {"O": {"children": [{"Y": {"children": [{}], "depth": 4, "parentTree": ["root", "K", "E", "O"], "freq": 1}}], "depth": 3, "parentTree": ["root", "K", "E"], "freq": 1}}], "depth": 2, "parentTree": ["root", "K"], "freq": 2}}], "depth": 1, "parentTree": ["root"], "freq": 2}}], "depth": 0, "parentTree": [], "freq": 0}}'
    items = [ ('Y', 5) ,('E', 4)]
    #items = [('K',2)]
    itemSupportTable = pd.DataFrame(items,columns=['item','support']) 

    conditionalPatternBaseTable = generateConditionalPatternBase(itemSupportTable,treeString)

    print(conditionalPatternBaseTable)

    lists = ['K','E','M','O','Y']

    powersets = powerset(lists)
    print(conditionalPatternBaseTable.iloc[1]['ConditionalPattern'])
    #print(powersets)
    

if __name__ == '__main__':
    main()
