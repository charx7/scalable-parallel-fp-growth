'''
    First define a class of Tree and TreeNode that will implement the graph
    structure of our data
    @nameArg:    The current name of the product on the nod
    @freqArg:    The frequency of the product
    @parentNode: The parent of the node for linking 
'''
# Define a node on the tree
class TreeNode:
    # Class constructor
    def __init__(self, item_value, frequency_value, parent_value):
        self._itemName      = item_value
        self._freq          = frequency_value
        self._parent        = parent_value
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

# This method will create the fp-tree
'''
    @data must be sorted and filtered by frequency count
'''
def CreateTree(data):
    # rootNode = TreeNode('root',1,None)
    # rootNode.children['something'] = TreeNode('something',3,None)
    # rootNode.display()

    # Create a root node object of type TreeNode
    root = TreeNode('root',0,None)

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
        if tree.children and len(previousItems)>0:
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
            newNode = TreeNode(item,1,tree._itemName)
            # Append it to the children dict
            tree.children[item] = newNode

if __name__ == "__main__":
    # to test the tree
    testData = [
        ['K','E','M','O','Y'],
        ['K','E','O','Y']
    ] 
    testData2 = [
        ['K','E','M'],
        ['K','M','Y'],
        ['K','E','O']
    ]
    testData3 = [
        ['K','E','O','Y'],
        ['E','O','M']
    ]
    #breakpoint()
    fpTree = CreateTree(testData)
    # to display
    fpTree.display()
    