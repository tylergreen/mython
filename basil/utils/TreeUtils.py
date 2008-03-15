#! /usr/bin/env python
# ______________________________________________________________________
"""Module TreeUtils.py

Defines several utility functions for manipulating and traversing nested
tuple/list tree structures (where node = (nodeData, [childNode,...]).)

Jonathan Riehl

$Id: TreeUtils.py,v 1.1 2003/07/10 18:27:05 jriehl Exp $
"""
# ______________________________________________________________________
# No imports.

# ______________________________________________________________________

def prefix_tree_iter (treeTuple):
    """prefix_tree_iter()
    """
    node_queue = [treeTuple]
    while node_queue:
        crnt_node = node_queue[0]
        yield crnt_node[0]
        node_queue = crnt_node[1] + node_queue[1:]

# ______________________________________________________________________

def postfix_tree_iter (treeTuple):
    """postfix_tree_iter()
    Rewriting the nodes like this smells of just adding a visit tag to
    stuff.  One wonders if there is a simpler way to do this."""
    node_queue = treeTuple[1] + [(treeTuple[0], [])]
    while node_queue:
        crnt_node = node_queue[0]
        if len(crnt_node[1]) == 0:
            yield crnt_node[0]
            del node_queue[0]
        else:
            node_queue = crnt_node[1] + [(treeTuple[0], [])] + node_queue[1:]

# ______________________________________________________________________

def _flattenTree (treeTuple, treeList):
    treeList.append(treeTuple)
    for child in treeTuple[1]:
	_flattenTree(child, treeList)

def flattenTree (treeTuple):
    if treeTuple == None:
	return []
    treeList = []
    _flattenTree(treeTuple, treeList)
    return treeList

# ______________________________________________________________________

def _flattenTreeLevels (treeTuple, level, levelList):
    levelList.append(level)
    for child in treeTuple[1]:
	_flattenTreeLevels(child, level + 1, levelList)

def flattenTreeLevels (treeTuple):
    if treeTuple == None:
	return []
    levelList = []
    _flattenTreeLevels(treeTuple, 0, levelList)
    return levelList

# ______________________________________________________________________

def _flattenTreeParents (treeTuple, parentIndex, parentList):
    myIndex = len(parentList)
    parentList.append(parentIndex)
    for child in treeTuple[1]:
	_flattenTreeParents(child, myIndex, parentList)

def flattenTreeParents (treeTuple):
    if treeTuple == None:
	return []
    parentList = []
    _flattenTreeParents(treeTuple, None, parentList)
    return parentList

# ______________________________________________________________________

def _flattenSubordinateCount (treeList, subCountList, treeNode):
    myIndex = len(subCountList)
    subCountList.append(0)
    sum = 0
    for child in treeNode[1]:
	sum = _flattenSubordinateCount(treeList, subCountList, child) + sum
    subCountList[myIndex] = sum
    return sum + 1

def flattenSubordinateCount (treeList):
    subCountList = []
    if treeList:
	_flattenSubordinateCount(treeList, subCountList, treeList[0])
    return subCountList

# ______________________________________________________________________

def _makeTestTree (depth, bredth, parentStr):
    childList = []
    if depth > 0:
	i = 1
	while i <= bredth:
	    myStr = "%s.%d" % (parentStr, i)
	    myTuple = (myStr, _makeTestTree(depth - 1, bredth, myStr))
	    childList.append(myTuple)
	    i = i + 1
    return childList

def makeTestTree (depth, bredth):
    return ("0", _makeTestTree(depth, bredth, "0"))

# ______________________________________________________________________

class TreeTestNode:
    # ____________________________________________________________
    def __init__ (self, parent = None, index = None):
	if (parent == None) or (index == None):
	    self.id = "0"
	else:
	    self.id = "%s.%d" % (parent.id, index)

    # ____________________________________________________________
    def __str__ (self):
	return self.id

# ______________________________________________________________________

def _makeTestObjTree (depth, bredth, parentObj):
    childList = []
    if depth > 0:
	i = 1
	while i <= bredth:
	    myObj = TreeTestNode(parentObj, i)
	    myTuple = (myObj, _makeTestObjTree(depth - 1, bredth, myObj))
	    childList.append(myTuple)
	    i = i + 1
    return childList

def makeTestObjTree (depth, bredth):
    root = TreeTestNode()
    return (root, _makeTestObjTree(depth, bredth, root))

# ______________________________________________________________________

def depthTraverse (tree, preFunction = None, postFunction = None, depth = 0):
    if preFunction:
	preFunction(tree, depth)
    for subTree in tree[1]:
	depthTraverse(subTree, preFunction, postFunction, depth + 1)
    if postFunction:
	postFunction(tree, depth)

# ______________________________________________________________________

def bredthTraverse (tree, function):
    function(tree, 0)
    levelNr = 1
    currentLevel = tree[1]
    while len(currentLevel) > 0:
	nextLevel = []
	for subTree in currentLevel:
	    function(subTree, levelNr)
	    nextLevel = nextLevel + subTree[1]
	currentLevel = nextLevel

# ______________________________________________________________________

def depthSearch (tree, searchFn):
    if searchFn(tree):
        return tree
    for subTree in tree[1]:
        subResult = depthSearch(subTree, searchFn)
        if subResult != None:
            return subResult
    return None

# ______________________________________________________________________

def bredthSearch (tree, searchFn):
    if searchFn(tree):
        return tree
    currentLevel = tree[1]
    while len(currentLevel) > 0:
        nextLevel = []
        for subTree in currentLevel:
            if searchFn(subTree):
                return subTree
            nextLevel = nextLevel + subTree[1]
        currentLevel = nextLevel
    return None

# ______________________________________________________________________

def main ():
    import pprint
    testTree = makeTestTree(2,3)
    pprint.pprint(testTree)
    print "_" * 60
    flatTree = flattenTree(testTree)
    pprint.pprint(flatTree)
    print "_" * 60
    flatLevels = flattenTreeLevels(testTree)
    print flatLevels
    print "_" * 60
    flatParents = flattenTreeParents(testTree)
    print flatParents
    print "_" * 60
    flatSubs = flattenSubordinateCount(flatTree)
    print flatSubs

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of TreeUtils.py
