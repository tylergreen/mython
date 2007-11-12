#! /usr/bin/env python
# ______________________________________________________________________
"""Module TreeBox.py

This module implements a tree control in Tkinter.  It was inspired by and
borrows from code written by Arpad Kiss (arpadk@geometria.hu)
However, this code uses a tree structure formed by tuples and lists.

NOTE ABOUT TREE DATA:
It is important that all nodes in the input data structure must be
unique, i.e. when compared to all nodes but their self, they must indicate
inequality.

Jonathan Riehl

$Id: TreeBox.py,v 1.3 2003/07/17 18:24:55 jriehl Exp $
"""
# ______________________________________________________________________
# Module constants.

__DEBUG__ = 0

# ______________________________________________________________________
# Module imports.

import Tkinter
import ScrolledCanvas

# ______________________________________________________________________
# TreeBox class.

class TreeBox (ScrolledCanvas.ScrolledCanvas):
    """Class TreeBox
    """
    # ____________________________________________________________
    # Static configuration items.  These may be set by child constructors.
    # ____________________________________________________________
    # color of the box around the current selection.
    selectionFill = "gray90"

    # Color of the plus/minus boxes and item text.
    foreground = "black"

    # Color of the connective lines between nodes.
    lineColor = "gray40"

    # ____________________________________________________________
    # Selected item related methods.
    # ____________________________________________________________
    def belowItem (self, currentItem = None):
	"""TreeBox.belowItem()
	"""
	if currentItem == None:
	    currentItem = self.currentItem
	if currentItem != None:
	    i = currentItem + 1
	    while i < len(self.treeList):
		if self.widgetList[i] != None:
		    return i
		i = i + 1
	return None

    # ____________________________________________________________
    def aboveItem (self, currentItem = None):
	"""TreeBox.aboveItem()
	"""
	if currentItem == None:
	    currentItem = self.currentItem
	if currentItem != None:
	    i = currentItem - 1
	    while i >= 0:
		if self.widgetList[i] != None:
		    return i
		i = i - 1
	return None

    # ____________________________________________________________
    def getCurrentItem (self):
	"""TreeBox.getCurrentItem()

	Returns the currently selected item.
	"""
	return self.currentItem

    # ____________________________________________________________
    def setCurrentItem (self, index):
	"""TreeBox.setCurrentItem()
	"""
	wIDs = self.find_withtag("selector")
	for wID in wIDs:
	    if self.widgetMap.has_key(wID):
		del self.widgetMap[wID]
	    self.delete(wID)
	self.currentItem = index
	if index != None:
	    if self.widgetList[index] == None: return
	    textWidget = self.widgetList[index][0]
	    x1, y1, x2, y2 = self.bbox(textWidget)
	    wID = self.create_rectangle(x1, y1, x2 + 1, y2,
					fill = self.selectionFill,
					tags = ("selector",))
	    self.widgetMap[wID] = index
	    self.tkraise(textWidget, wID)
	    # ________________________________________
	    # scroll to this item
	    allBBox = self.bbox(Tkinter.ALL)
	    up, vy = self.yview()
	    height = float(allBBox[3]) + self.scrollSize
	    if self.scrollX.place_info():
		ps = self.scrollSize + 1
	    else:
		ps = 0
	    ypos = y1 / height
	    if up > ypos:
		self.yview("moveto", ypos)
	    elif (self.winfo_height() < (y2 - (height * up) +
					 (2 * int(self['borderwidth']))+3+ps)):
		self.yview("moveto",
			   float(y2 - self.winfo_height() +
				 (2*int(self['borderwidth']))+3+ps) / height)
	    left, vx = self.xview()
	    width = float(allBBox[2]) + self.scrollSize
	    xpos = x1 / width
	    if left > xpos:
		self.xview("moveto", xpos)
	    elif vx < (float(x2 + int(self.scrollSize) - width * left) /
		       (width - width * left)):
		self.xview("moveto", xpos)

    # ____________________________________________________________
    def updateCurrentItem (self):
	"""TreeBox.updateCurrentItem()
	"""
	self.setCurrentItem(self.getCurrentItem())

    # ____________________________________________________________
    # Node collapse/expand methods.
    # ____________________________________________________________
    def toggleNode (self, index):
	"""TreeBox.toggleNode()
	"""
	if self.subordinateList[index] > 0:
	    if self.expandedList[index] == 1:
		self.collapseNode(index)
	    else:
		self.expandNode(index)
	    self.updatePlusMinus(index)

    # ____________________________________________________________
    def updateParentalVLines (self, index, space):
	"""TreeBox.updateParentalVLines()

	Traverses the parental chain upwards, adjusting their connective
	subordinate lines based on the loss or gain of the given amount
	of space.  Connective subordinate lines are the vertical lines
	extending from the bottom of a node's plus/minus box.  The space
	parameter should be the amount of pixels gained or lost.
	"""
	prevIndex = index
	crntIndex = self.parentList[index]
	while crntIndex != None:
	    wID = self.widgetList[crntIndex][1]
	    lastElement = (id(self.treeList[crntIndex][1][-1]) ==
			   id(self.treeList[prevIndex]))
	    if (not lastElement) and wID != None:
		x1, y1, x2, y2 = self.coords(wID)
		if y1 > y2: y1, y2 = y2, y1
		scale = (y2 - y1 + space) / (y2 - y1)
		self.scale(wID, x2, y2, 1, scale)
	    prevIndex = crntIndex
	    crntIndex = self.parentList[crntIndex]

    # ____________________________________________________________
    def updatePlusMinus (self, index):
	"""TreeBox.updatePlusMinus()

	Erases and redraws the plus/minus symbol inside a given node's
	plus/minus box.
	"""
	dx = self.dx
	hdx = dx / 2
	qdx = dx / 4
	tqdx = qdx * 3
	x = self.levelList[index] * dx
	y = self.bbox(self.widgetList[index][0])[1]
	# __________________________________________________
	self.addtag_overlapping("deleteMe", x + 1, y + 1,
				x + hdx - 1, y + hdx - 1)
	wIDs = self.find_withtag("deleteMe")
	for wID in wIDs:
	    del self.widgetMap[wID]
	self.delete("deleteMe")
	# __________________________________________________
	if self.subordinateList[index] > 0:
	    wID = self.create_polygon(x, y, x + hdx, y,
				      x + hdx, y + hdx, x, y + hdx,
				      outline = self.foreground, fill = '')
	    self.widgetMap[wID] = index
	    wID = self.create_line(x + 2, y + qdx, x + hdx - 1, y + qdx,
				   fill = self.foreground)
	    self.widgetMap[wID] = index
	    if not self.expandedList[index]:
		wID = self.create_line(x + qdx, y + 2, x + qdx, y + hdx - 1,
				       fill = self.foreground)
		self.widgetMap[wID] = index

    # ____________________________________________________________
    def getNodeText (self, nodeObject):
	"""TreeBox.getNodeText()

	Returns a text string for the given Python object passed in.  Used when
	drawing nodes to get the node's text.  May be overloaded by child
	classes to change how the TreeBox behaves.
	"""
	return str(nodeObject)

    # ____________________________________________________________
    def drawNode (self, index, y):
	"""TreeBox.drawNode()
	"""
	dx = self.dx
	hdx = dx / 2
	qdx = dx / 4
	tqdx = qdx * 3
	x = self.levelList[index] * dx
	if self.subordinateList[index] > 0:
	    wID = self.create_polygon(x, y, x + hdx, y,
				      x + hdx, y + hdx, x, y + hdx,
				      outline = self.foreground, fill = '')
	    self.widgetMap[wID] = index
	    wID = self.create_line(x + 2, y + qdx,
				   x + hdx - 1, y + qdx,
				   fill = self.foreground)
	    self.widgetMap[wID] = index
	    if not self.expandedList[index]:
		wID = self.create_line(x + qdx, y + 2,
				       x + qdx, y + hdx - 1,
				       fill = self.foreground)
		self.widgetMap[wID] = index
	    lineOfs = 0
	else:
	    lineOfs = hdx
	wID = self.create_text(x + tqdx, y, text =
			       self.getNodeText(self.treeList[index][0]),
			       anchor = Tkinter.NW,
			       fill = self.foreground, tags = ("primary",))
	self.widgetList[index] = [wID, None]
	self.widgetMap[wID] = index
	if index != 0:
	    self.create_line(x - tqdx, y + qdx, x + lineOfs, y + qdx,
			     fill = self.lineColor)

    # ____________________________________________________________
    def expandNode (self, index):
	"""TreeBox.expandNode()

	Expands a node at the specified index.
	"""
	oldCursor = self['cursor']
	self['cursor'] = 'watch'
	self.update()
	self.expandedList[index] = 1
	# __________________________________________________
	# Determine how much space is needed.
        space = 0
        i = index + 1
        stoppingPoint = i + self.subordinateList[index]
        while i < stoppingPoint:
            parentIndex = self.parentList[i]
            expandParent = self.expandedList[parentIndex]
            if (self.widgetList[parentIndex] != None and expandParent):
                self.widgetList[i] = -1
                space = space + self.dy
            if expandParent:
                i = i + 1
            else:
                i = i + self.subordinateList[i] + 1
	# __________________________________________________
	# Select all widgets below the current widget.
	wID = self.widgetList[index][0]
	assert wID != None
	elemBox = self.bbox(wID)
	allBox = self.bbox(Tkinter.ALL)
	self.addtag_overlapping("moveMe", allBox[0], elemBox[3], allBox[2],
				allBox[3])
	# __________________________________________________
	# Move them down.
	self.move("moveMe", 0, space)
	self.dtag("moveMe")
	self.updateParentalVLines(index, space)
	# __________________________________________________
	# Draw the subordinates.
	dx = self.dx
	hdx = dx / 2
	qdx = dx / 4
	tqdx = qdx * 3
	i = index + 1
	yStack = [(elemBox[1], index)]
	minLevel = self.levelList[index]
	nextLevel = minLevel + 1
	y = elemBox[1] + self.dy
	while i < stoppingPoint:
	    drawFlag = self.widgetList[i] != None
	    parentIndex = self.parentList[i]
	    if drawFlag:
		self.drawNode(i, y)
	    # ________________________________________
	    oldIndex = i
	    if drawFlag and self.expandedList[i]:
		i = i + 1
	    else:
		i = i + self.subordinateList[i] + 1
	    # ________________________________________
	    crntLevel = nextLevel
	    if i < stoppingPoint:
		nextLevel = self.levelList[i]
	    else:
		nextLevel = minLevel
	    # ________________________________________
	    if nextLevel > crntLevel:
		yStack.append((y, oldIndex))
	    elif nextLevel < crntLevel:
		crntY = y
		while nextLevel < crntLevel:
		    x = (crntLevel * dx) - tqdx
		    oldY, oldIndex = yStack[-1]
		    if self.widgetList[parentIndex] != None:
			wID = self.create_line(x, oldY + hdx + 1, x,
					       crntY + qdx,
					       fill = self.lineColor)
			self.widgetList[oldIndex][1] = wID
		    del yStack[-1]
		    crntY = oldY
		    crntLevel = crntLevel - 1
	    # ________________________________________
	    if drawFlag:
		y = y + self.dy
	# __________________________________________________
	# Clean up.
	self.updateScroll()
	self.updateCurrentItem()
	self['cursor'] = oldCursor

    # ____________________________________________________________
    def collapseNode (self, index):
	"""TreeBox.collapseNode()

	Collapses a node at the specified index.
	"""
	oldCursor = self['cursor']
	self['cursor'] = 'watch'
	self.update()
	self.expandedList[index] = 0
	# __________________________________________________
	# Select all widgets subordinate to the current widget.
	count = 0
	i = index + 1
	stoppingPoint = i + self.subordinateList[index]
	while i < stoppingPoint:
	    if self.widgetList[i] != None:
		count = count + 1
		self.widgetList[i] = None
	    if self.expandedList[i]:
		i = i + 1
	    else:
		i = i + self.subordinateList[i] + 1
	space = count * self.dy
	# __________________________________________________
	self.updateParentalVLines(index, -space)
	wID = self.widgetList[index][0]
	assert wID != None
	elemBox = self.bbox(wID)
	allBox = self.bbox(Tkinter.ALL)
	self.addtag_overlapping("removeMe", elemBox[0] - self.dx,
				elemBox[3], allBox[2], elemBox[3] + space)
	# __________________________________________________
	# Remove them.
	wIDs = self.find_withtag("removeMe")
	for wID in wIDs:
	    if self.widgetMap.has_key(wID):
		del self.widgetMap[wID]
	self.delete("removeMe")
	# __________________________________________________
	# Move all widgets below the current widget up.
	self.addtag_overlapping("moveMe", allBox[0], elemBox[3],
				allBox[2], allBox[3])
	self.move("moveMe", 0, -space)
	self.dtag("moveMe")
	# __________________________________________________
	# Clean up.
	self.updateScroll()
	self.updateCurrentItem()
	self['cursor'] = oldCursor

    # ____________________________________________________________
    # Master tree update method.
    # ____________________________________________________________
    def updateTree (self, index = 0):
	"""TreeBox.updateTree()

	Used to redraw entire tree.
	"""
	self.delete(Tkinter.ALL)
	if self.tree == None: return
	self.focus_set()
	oldCursor = self['cursor']
	self['cursor'] = 'watch'
	self.widgetMap = {}
	self.widgetList = [None] * len(self.treeList)
	dx = self.dx
	dy = self.dy
	y = 0
	i = index
	stoppingPoint = index + self.subordinateList[index] + 1
	if __DEBUG__:
	    print i, "to", (stoppingPoint - 1), "of", len(self.treeList)
	hdx = dx / 2 # Half dx
	qdx = dx / 4 # Quarter dx
	tqdx = 3 * qdx # Three quarters of dx
	yStack = []
	nextLevel = 0
	drawList = [0] * len(self.treeList)
	while i < stoppingPoint:
	    parentIndex = self.parentList[i]
	    expandNode = self.expandedList[i]
	    if i != 0:
		drawCrnt = ((self.widgetList[parentIndex] != None) and
			    self.expandedList[parentIndex])
	    else:
		drawCrnt = 1
	    crntLevel = nextLevel
	    # ________________________________________
	    if drawCrnt:
		self.drawNode(i, y)
	    # ________________________________________
	    oldIndex = i
	    if drawCrnt and expandNode:
		i = i + 1
	    else:
		i = i + self.subordinateList[i] + 1
	    # ________________________________________
	    if i < len(self.treeList):
		nextLevel = self.levelList[i]
	    else:
		nextLevel = 0
	    # ________________________________________
	    if nextLevel > crntLevel:
		yStack.append((y, oldIndex))
	    elif nextLevel < crntLevel:
		crntY = y
		while nextLevel < crntLevel:
		    x = (crntLevel * dx) - tqdx
		    oldY, oldIndex = yStack[-1]
		    if self.widgetList[parentIndex] != None:
			wID = self.create_line(x, oldY + hdx + 1, x,
					       crntY + qdx,
					       fill = self.lineColor)
			self.widgetList[oldIndex][1] = wID
		    del yStack[-1]
		    crntY = oldY
		    crntLevel = crntLevel - 1
	    # ________________________________________
	    if drawCrnt:
		y = y + dy
	self.updateScroll()
	self['cursor'] = oldCursor

    # ____________________________________________________________
    # Node removal/insertion methods.
    # ____________________________________________________________
    def getDisplayedSubs (self, parentIndex):
	"""TreeBox.getDisplayedSubs()

	Returns a list of subordinate indicies for all subordinates contained
	by the given parent node.

	(Currently not used by any other methods.  Kept for reference
	purposes.)
	"""
	displayedSubs = []
	i = parentIndex + 1
	stoppingPoint = self.subordinateList[parentIndex] + parentIndex + 1
	while i < stoppingPoint:
	    parentIndex = self.parentList[i]
	    expandParent = self.expandedList[parentIndex]
	    if (self.widgetList[parentIndex] != None and expandParent):
		displayedSubs.append(i)
	    if expandParent:
		i = i + 1
	    else:
		i = i + self.subordinateList[i] + 1
	return displayedSubs

    # ____________________________________________________________
    def invalidateParents (self, index):
	"""TreeBox.invalidateParents()

	Causes the given node, and all its parents to be erased and redrawn.
	"""
	while index != None:
	    self.invalidateNode(index)
	    index = self.parentList[index]

    # ____________________________________________________________
    def invalidateChildren (self, index):
	"""TreeBox.invalidateChildren()

	Causes the given node, and all its subordinates to be erased and
	redrawn.
	"""
	if index == None: return
	stoppingPoint = self.subordinateList[index] + index + 1
	while index < stoppingPoint:
	    self.invalidateNode(index)
	    if self.expandedList[index]:
		index = index + 1
	    else:
		index = index + self.subordinateList[index] + 1

    # ____________________________________________________________
    def invalidateNode (self, index):
	"""TreeBox.invalidateNode()

	If the given node is displayed, the widgets for the node are erased
	and then redrawn based on current model data.  Returns 1 if the node
	was redrawn, 0 otherwise.
	"""
	# If the given node is visible, then redraw it, otherwise, forget it.
	widgets = self.widgetList[index]
	if widgets:
	    # Erase the node.
	    wID = widgets[0]
	    elemBox = self.bbox(wID)
	    y = elemBox[1]
	    self.addtag_overlapping("removeMe", elemBox[0] - self.dx + 1, y,
				    elemBox[2], elemBox[1] + self.dy - 1)
	    wIDs = self.find_withtag("removeMe")
	    for wID in wIDs:
		if self.widgetMap.has_key(wID):
		    del self.widgetMap[wID]
	    self.delete("removeMe")
	    # Redraw it, and its vertical connector, if necessary.
	    self.drawNode(index, y)
	    if self.expandedList[index] and (self.subordinateList[index] > 0):
		lastChildNode = self.treeList[index][1][-1]
		lastChildIndex = self.treeList.index(lastChildNode)
		lastChildWidgets = self.widgetList[lastChildIndex]
		if lastChildWidgets:
		    dx = self.dx
		    hdx = dx / 2
		    qdx = dx / 4
		    tqdx = qdx * 3
		    x = ((self.levelList[index] + 1) * dx) - tqdx
		    lastChildY = self.bbox(lastChildWidgets[0])[1]
		    wID = self.create_line(x, y + hdx + 1, x, lastChildY + qdx,
					   fill = self.lineColor)
		    self.widgetList[index][1] = wID
	    return 1
	return 0

    # ____________________________________________________________
    def removeNode (self, index):
	"""TreeBox.removeNode()

	Removes the node and its subordinates at the specified index.
	Returns the actual tree node.
	"""
	# __________________________________________________
	# Update the GUI.
	i = index
	count = 0
	subCount = self.subordinateList[index] + 1
	branchEnd = index + subCount
	while i < branchEnd:
	    if self.widgetList[i] != None:
		count = count + 1
	    if self.expandedList[i]:
		i = i + 1
	    else:
		i = i + self.subordinateList[i] + 1
	space = count * self.dy
	wID = self.widgetList[index][0]
	elemBox = self.bbox(wID)
	allBox = self.bbox(Tkinter.ALL)
	self.addtag_overlapping("removeMe", allBox[0], elemBox[1],
				allBox[2], elemBox[1] + space - 1)
	wIDs = self.find_withtag("removeMe")
	for wID in wIDs:
	    if self.widgetMap.has_key(wID):
		del self.widgetMap[wID]
	self.delete("removeMe")
	self.addtag_overlapping("moveMe", allBox[0], elemBox[1], allBox[2],
				allBox[3])
	wIDs = self.find_withtag("moveMe")
	for wID in wIDs:
	    if self.widgetMap.has_key(wID):
		self.widgetMap[wID] = self.widgetMap[wID] - subCount
	self.move("moveMe", 0, -space)
	self.dtag("moveMe")
	parentIndex = self.parentList[index]
	# __________________________________________________
	# Remove the data.
	node = self.treeList[index]
	i = parentIndex
	if i != None:
	    parentNode = self.treeList[i]
	    parentNode[1].remove(node)
	    while i != None:
		self.subordinateList[i] = self.subordinateList[i] - subCount
		i = self.parentList[i]
	else:
	    self.tree = None
	del self.treeList[index:branchEnd]
	del self.levelList[index:branchEnd]
	del self.parentList[index:branchEnd]
	del self.subordinateList[index:branchEnd]
	del self.expandedList[index:branchEnd]
	del self.widgetList[index:branchEnd]
	i = index
	while i < len(self.treeList):
	    parentLoc = self.parentList[i]
	    if parentLoc >= branchEnd:
		self.parentList[i] = parentLoc - subCount
	    i = i + 1
	# __________________________________________________
	# Update the current position.
	self.invalidateParents(parentIndex)
	if self.currentItem != None and self.currentItem >= index:
	    if self.currentItem >= branchEnd:
		self.setCurrentItem(self.currentItem - subCount)
	    else:
		self.setCurrentItem(None)
	self.updateScroll()
	return node

    # ____________________________________________________________
    def appendNode (self, parentIndex, node):
	"""TreeBox.appendNode()

	Appends the node to the end of the given parent index.
	Returns the index where the node was inserted in the flattened
	tree list.
	"""
	parentNode = self.treeList[parentIndex]
	parentNode[1].append(node)
	nodeIndex = parentIndex + self.subordinateList[parentIndex] + 1
	self._insertNode(parentIndex, node, nodeIndex)
	return nodeIndex

    # ____________________________________________________________
    def insertNode (self, parentIndex, node, atIndex):
	"""TreeBox.insertNode()

	Inserts the node into the given parent (specified by index) at the
	specified location (mirrors Python list insert semantics.)  Returns
	the index where the node was inserted in the flattened tree list.
	"""
	parentNode = self.treeList[parentIndex]
	# Mirror Python list insertion semantics.
	if atIndex >= len(parentNode[1]):
	    return self.appendNode(parentIndex, node)
	elif atIndex < 0:
	    atIndex = 0
	# Determine the index to insert at.
	nodeIndex = self.treeList.index(parentNode[1][atIndex])
	parentNode[1].insert(atIndex, node)
	self._insertNode(parentIndex, node, nodeIndex)
	return nodeIndex

    # ____________________________________________________________
    def _insertNode (self, parentIndex, node, location):
	"""TreeBox._insertNode()
	"""
	# __________________________________________________
	# Generate flattened data for the branch.
	saveLists = (self.treeList, self.levelList, self.parentList,
		     self.subordinateList)
	self.flattenTree(node)
	appendBranch = self.treeList
	appendBranchLevels = self.levelList
	appendBranchParents = self.parentList
	appendBranchSubs = self.subordinateList
	(self.treeList,
	 self.levelList,
	 self.parentList,
	 self.subordinateList) = saveLists
	count = len(appendBranch)
	appendBranchExpand = [0] * count
	# __________________________________________________
	# Straighten out the branch data.
	i = 0
	parentLevel = self.levelList[parentIndex]
	while i < count:
	    appendBranchLevels[i] = appendBranchLevels[i] + parentLevel + 1
	    if i == 0:
		appendBranchParents[i] = parentIndex
	    else:
		appendBranchParents[i] = appendBranchParents[i] + location
	    i = i + 1
	# __________________________________________________
	# Straighten out the global data.
	i = location
	while i < len(self.treeList):
	    parentLoc = self.parentList[i]
	    if parentLoc >= location:
		self.parentList[i] = parentLoc + count
	    i = i + 1
	index = parentIndex
	while index != None:
	    self.subordinateList[index] = (self.subordinateList[index] + count)
	    index = self.parentList[index]
	# __________________________________________________
	# Insert the branch at the given location
	self.treeList[location:location] = appendBranch
	self.levelList[location:location] = appendBranchLevels
	self.parentList[location:location] = appendBranchParents
	self.subordinateList[location:location] = appendBranchSubs
	self.expandedList[location:location] = appendBranchExpand
	self.widgetList[location:location] = [None] * count
	# __________________________________________________
	# Update the GUI.
	drawNode = ((self.widgetList[parentIndex] != None) and
		    (self.expandedList[parentIndex] == 1))
	# Find the next displayed element.
	below = self.belowItem(location + count - 1)
	if below != None:
	    # Move everything down.
	    wID = self.widgetList[below][0]
	    elemBox = self.bbox(wID)
	    allBox = self.bbox(Tkinter.ALL)
	    self.addtag_overlapping("moveMe", allBox[0], elemBox[1],
				    allBox[2], allBox[3])
	    wIDs = self.find_withtag("moveMe")
	    for wID in wIDs:
		if self.widgetMap.has_key(wID):
		    self.widgetMap[wID] = self.widgetMap[wID] + count
	    if drawNode:
		self.move("moveMe", 0, self.dy)
		self.drawNode(location, elemBox[1])
	    self.dtag("moveMe")
	elif drawNode:
	    above = self.aboveItem(location)
	    if above != None:
		wID = self.widgetList[above][0]
		elemBox = self.bbox(wID)
		self.drawNode(location, elemBox[1] + self.dy)
	self.invalidateParents(parentIndex)
	if self.currentItem != None and self.currentItem >= location:
	    self.setCurrentItem(self.currentItem + count)
	else:
	    self.updateCurrentItem()
	self.updateScroll()

    # ____________________________________________________________
    def _flattenTree (self, treeTuple, level, parentIndex):
	"""TreeBox._flattenTree()

	Recursive method for flattening a tree structure into a set of lists
	used to manage the GUI tree representation.
	Returns the number of nodes subordinate to the current node, plus one
	(thus including the current node in its count.)
	"""
	myIndex = len(self.treeList)
	self.treeList.append(treeTuple)
	self.levelList.append(level)
	self.parentList.append(parentIndex)
	self.subordinateList.append(0)
	sum = 0
	for child in treeTuple[1]:
	    sum = self._flattenTree(child, level + 1, myIndex) + sum
	self.subordinateList[myIndex] = sum
	return sum + 1

    # ____________________________________________________________
    def flattenTree (self, tree):
	"""TreeBox.flattenTree()

	Staging method for creating flat (list) structures from a tree
	structure.
	"""
	self.treeList = []
	self.levelList = []
	self.parentList = []
	self.subordinateList = []
	if tree != None:
	    nodes = self._flattenTree(tree, 0, None)

    # ____________________________________________________________
    def setTree (self, tree):
	"""TreeBox.setTree()

	Resets the current tree data structure, and rebuilds the GUI support
	data and the GUI itself.
	"""
	# Set the tree data strucutres.
	self.tree = tree
	self.flattenTree(tree)
	self.expandedList = [0] * len(self.treeList)
	if tree != None:
	    self.expandedList[0] = 1
	# Update the GUI.
	self.currentItem = None
	self.updateTree()

    # ____________________________________________________________
    def __init__ (self, root = None, tree = None, **kw):
	"""TreeBox.__init__()
	"""
	apply(ScrolledCanvas.ScrolledCanvas.__init__, (self, root), kw)
	# __________________________________________________
	self.dx = 20
	self.dy = 16
	# __________________________________________________
	self.setTree(tree)

    # ____________________________________________________________
    def enableDefaultHandlers (self):
	"""TreeBox.enableDefaultHandlers()
	"""
	self.bind("<KeyPress-Home>", self._homeHandler)
	self.bind("<KeyPress-End>", self._endHandler)
	self.bind("<KeyPress-Up>", self._upHandler)
	self.bind("<KeyPress-Down>", self._dnHandler)
	self.bind("<KeyPress-Return>", self._returnHandler)
	self.bind("<1>", self._clickHandler)

    # ____________________________________________________________
    def _homeHandler (self, event):
	self.setCurrentItem(0)

    # ____________________________________________________________
    def _endHandler (self, event):
	index = len(self.treeList) - 1
	while self.widgetList[index] == None:
	    index = index - 1
	self.setCurrentItem(index)

    # ____________________________________________________________
    def _upHandler (self, event):
	nextIndex = self.aboveItem()
	if nextIndex != None:
	    self.setCurrentItem(nextIndex)

    # ____________________________________________________________
    def _dnHandler (self, event):
	nextIndex = self.belowItem()
	if nextIndex != None:
	    self.setCurrentItem(nextIndex)

    # ____________________________________________________________
    def _returnHandler (self, event):
	if ((self.currentItem != None) and
	    (self.widgetList[self.currentItem] != None)):
	    self.toggleNode(self.currentItem)

    # ____________________________________________________________
    def _clickHandler (self, event):
	self.focus_set()
	ids = self.find_withtag(Tkinter.CURRENT)
	if len(ids) > 0:
	    wID = ids[0]
	    if self.widgetMap.has_key(wID):
		textElems = self.find_withtag("primary")
		index = self.widgetMap[wID]
		if wID not in textElems:
		    self.toggleNode(index)
		self.setCurrentItem(index)

# ______________________________________________________________________

_tkInst = None

def showTree (tree, tkInst = None):
    """showTree (tree, [tkInst])

    Utility function for quickly displaying a tree in a window.
    The optional tkInst argument is the main Tk widget.

    Returns the Tk widget used (so that mainloop() can be called after
    all the tree have been displayed.
    """
    global _tkInst
    if None == tkInst:
        if None == _tkInst:
            _tkInst = Tkinter.Tk()
            topLev = _tkInst # XXX I know these are different thingies...
        else:
            topLev = Tkinter.Toplevel(_tkInst)
        tkInst = _tkInst
    else:
        topLev = Tkinter.Toplevel(tkInst)
    can = TreeBox(topLev, tree)
    can.enableDefaultHandlers()
    can.pack(expand = Tkinter.YES, fill = Tkinter.BOTH, anchor = Tkinter.N)
    return tkInst

# ______________________________________________________________________

def main ():
    from basil.utils.TreeUtils import makeTestObjTree
    tk = Tkinter.Tk()
    can = TreeBox(tk, makeTestObjTree(4,3))
    def _testMouse2 (event, can = can, makeTestTree = makeTestObjTree):
	can.focus_set()
	ids = can.find_withtag(Tkinter.CURRENT)
	if len(ids) > 0:
	    if can.widgetMap.has_key(ids[0]):
		index = can.widgetMap[ids[0]]
		can.appendNode(index, makeTestTree(2,2))
    def _testMouse3 (event, can = can):
	can.focus_set()
	ids = can.find_withtag(Tkinter.CURRENT)
	if len(ids) > 0:
	    if can.widgetMap.has_key(ids[0]):
		can.removeNode(can.widgetMap[ids[0]])
    can.enableDefaultHandlers()
    can.bind("<2>", _testMouse2)
    can.bind("<3>", _testMouse3)
    can.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
    tk.mainloop()

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of TreeBox.py
