'''
    First define a class of Tree and TreeNode that will implement the graph
    structure of our data
    @nameArg:    The current name of the product on the nod
    @freqArg:    The frequency of the product
    @parentNode: The parent of the node for linking
'''
import json
# Define a node on the tree

class TreeNode:
    # Class constructor
    def __init__(self, item_value, frequency_value, parent_value):
        self._itemName = item_value
        self._freq = frequency_value
        self._parent = parent_value
        # A dictionary that contains a list of the children of this leaf
        self.children = {}

    # Method that increments the frequency of an item
    def incrementFreq(self):
        self._freq += 1

    # Method that will display the tree
    def display(self, ind=1):
        print(' '*ind, self._itemName, ' ', self._freq)
        # Iteration over the dictionary of children to display them
        for child in self.children.values():
            child.display(ind+1)

    def makeDictionary(self, depth=0, parentList=[]):
       # parentList2 = []
        # print(self._parent, depth, self._itemName, parentList)
        if self._parent is not None and self._parent != 'root':
            parentList = parentList + [self._parent]

        if len(self.children) == 0:
            return {
                self._itemName: {
                    'children': [{}],
                    'depth': depth,
                    'parentTree': parentList,
                    'freq': self._freq
                }
            }
        childrenList = list(self.children.keys())
        childrenTrees = []
        for child in childrenList:
            childrenTrees += [self.children[child]
                              .makeDictionary(depth + 1, parentList)]

        return {
            self._itemName: {
                'children': childrenTrees,
                'depth': depth,
                'parentTree': parentList,
                'freq': self._freq
            }
        }

def CreateLocalTree(tupledData):
    root = TreeNode('root', 0, None)
    
    for transaction in tupledData:
        # For each item on the current transaction
        previousItemsList = []
        
        for item in transaction:
            # Have to clone the object because the pop() method is messing outside of scope
            previousItemsArgument = previousItemsList.copy()
            updateTree(item, previousItemsArgument, root)
            # Save a reference to the previous item
            previousItemsList.append(item)
    # Return with the grown tree
    return root
'''
    @data must be sorted and filtered by frequency count
'''
def CreateTree(data):
    # Create a root node object of type TreeNode
    root = TreeNode('root', 0, None)
    
    # Recursively grow the fp-tree
    for transaction in data:
        # For each item on the current transaction
        previousItemsList = []
        for item in transaction:
            # Have to clone the object because the pop() method is messing outside of scope
            previousItemsArgument = previousItemsList.copy()
            updateTree(item, previousItemsArgument, root)
            # Save a reference to the previous item
            previousItemsList.append(item)
    # Return with the grown tree
    return root

def updateTree(item, previousItems, tree):
    if item in tree.children:
        # increment the frequency for that item
        tree.children[item].incrementFreq()
    # If not we create a child
    else:
        # Check if the node has children so we go 1 level deeper
        # Weird condition in and TODO check it :P
        if tree.children and len(previousItems) > 0:
            # Traverse the previous items list untill it is empty
            # Not sure if this while is necessary since we check up for length of prev items
            while(len(previousItems) > 0):
                currentKey = previousItems[0]
                # pop from the stack ie, child has been visited
                previousItems.pop(0)
                # Recursively grow the tree
                updateTree(item, previousItems, tree.children[currentKey])
        else:
            # Create a new node that has parent tree
            newNode = TreeNode(item, 1, tree._itemName)
            # Append it to the children dict
            tree.children[item] = newNode

def mergeTree(tree1, tree2, baseTree, depth=0):
    currentNodeName = baseTree._itemName
    childrenList1 = list(tree1.children.keys())
    childrenList2 = list(tree2.children.keys())
    childrenToBeMerged = list(set(childrenList1) & set(childrenList2))

    for node in childrenToBeMerged:
        freqsSum = tree1.children[node]._freq + tree2.children[node]._freq
        baseTree.children[node] = TreeNode(node, freqsSum, currentNodeName)

        mergeTree(
            tree1.children[node],
            tree2.children[node],
            baseTree.children[node],
            depth+1)

    childrenToAppend1 = [
        x for x in childrenList1 if x not in childrenToBeMerged]
    childrenToAppend2 = [
        x for x in childrenList2 if x not in childrenToBeMerged]

    for node in childrenToAppend1:
        baseTree.children[node] = tree1.children[node]
    for node in childrenToAppend2:
        baseTree.children[node] = tree2.children[node]
    return baseTree


def mainMerge(tree1, tree2):
    """
    Executes a merge of two trees.
    Takes parsed JSONs as input.
    """
    # parse the string into a json
    #parsedTree1 = json.loads(fpTree1)
    #parsedTree2 = json.loads(fpTree2)
    baseTree = TreeNode('root', 0, None)
    finalTree = mergeTree(tree1, tree2, baseTree)

    return finalTree

# Main func
def main():
    test2()

def test2():
    print('Executing local tree creation test...')
    # Note assume that a key is 2
    data = [('44871', ), ('22396', '44871', '22088', '44865')] 
    localTree = CreateLocalTree(data)
    localTree.display()

# Test of the global tree
def test1():
    # to test the tree
    testData = [
        ['K', 'E', 'M', 'O', 'Y'],
        ['K', 'E', 'O', 'Y']
    ]
    testData2 = [
        ['K', 'E', 'M'],
        ['K', 'M', 'Y'],
        ['K', 'E', 'O']
    ]
    testData3 = [
        ['K', 'E', 'O', 'Y'],
        ['E', 'O', 'M']
    ]
    
    # breakpoint()
    fpTree1 = CreateTree(testData)
    fpTree2 = CreateTree(testData2)

    # Display test
    print('the non root tree is: ')
    fpTree1.display()

    mergedTree = mainMerge(fpTree1, fpTree2)
    print(type(mergedTree))
    print(mergedTree.display())

if __name__ == "__main__":
    main()  
  