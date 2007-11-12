#! /bin/env python
# ______________________________________________________________________
"""Module ScrolledCanvas.py

Implements a Frame derived composite widget consisting of a canvas with
associated scrollbars.
Updates thanks to Arpad Kiss: added automatic scroll detection code modified
   from treebox.py.

Jonathan Riehl

$Id: ScrolledCanvas.py,v 1.1.1.1 2000/07/03 20:59:39 jriehl Exp $
"""
# ______________________________________________________________________
# Module imports.

import Tkinter
import string

# ______________________________________________________________________

class ScrolledCanvas (Tkinter.Canvas):
    # ____________________________________________________________
    def __init__ (self, parent = None, **kw):
	apply(Tkinter.Canvas.__init__, (self, parent), kw)
	self.scrollX = Tkinter.Scrollbar(self, orient = Tkinter.HORIZONTAL)
	self.scrollY = Tkinter.Scrollbar(self, orient = Tkinter.VERTICAL)
	self.scrollSize = (string.atoi(self.scrollY.cget("width")) + 
			   (string.atoi(self.scrollY.cget("borderwidth"))*2))
	self.corner = Tkinter.Frame(self, relief = Tkinter.RAISED,
				    borderwidth = 2)
	self['xscrollcommand'] = self.scrollX.set
	self['yscrollcommand'] = self.scrollY.set
	self.scrollX['command'] = self.xview
	self.scrollY['command'] = self.yview
	self.bind("<Configure>", self.configureHandler)

    # ____________________________________________________________
    def configureHandler (self, event):
	self.updateScroll()

    # ____________________________________________________________
    def updateScroll (self):
	myBBox = self.bbox(Tkinter.ALL)
	if myBBox == None: return
	lx, uy, rx, ly = myBBox
	self['scrollregion'] = (lx - 5, uy - 5,
				rx + self.scrollSize + 5,
				ly + self.scrollSize + 5)
	yviewMin, yviewMax = self.yview()
	xviewMin, xviewMax = self.xview()
	borderWidth = string.atoi(self.cget("borderwidth"))
	scrollYOffset = None
	scrollXOffset = None
	cornerNeeded = None
	wCorner = (-2 * borderWidth) - self.scrollSize
	woCorner = -2 * borderWidth
	if (yviewMax < 1) or (yviewMin != 0):
	    if (xviewMax < 1) or (xviewMin != 0):
		scrollYOffset = wCorner
		scrollXOffset = wCorner
		cornerNeeded = 1
	    else:
		scrollYOffset = woCorner
	elif (xviewMax < 1) or (xviewMin != 0):
	    scrollXOffset = woCorner
	if scrollYOffset != None:
	    self.scrollY.place(relx = 1, x = -borderWidth, rely = 0,
			       y = borderWidth, relheight = 1,
			       height = scrollYOffset, anchor = Tkinter.NE)
	    self.scrollY.set(yviewMin, yviewMax)
	else:
	    self.scrollY.place_forget()
	if scrollXOffset != None:
	    self.scrollX.place(relx = 0, x = borderWidth,rely = 1, 
			       y = -borderWidth, relwidth = 1,
			       width = scrollXOffset, anchor = Tkinter.SW)
	    self.scrollX.set(xviewMin, xviewMax)
	else:
	    self.scrollX.place_forget()
	if cornerNeeded:
	    self.corner.place(relx = 1, x = -borderWidth, rely = 1,
			      y = -borderWidth, width = self.scrollSize,
			      height = self.scrollSize,
			      anchor = Tkinter.SE)
	else:
	    self.corner.place_forget()

# ______________________________________________________________________


iData = ('#define bmp_width 16' + chr(10) + '#define bmp_height 12' + chr(10) +
	 'static char bmp_bits[] = {' + chr(10) + '0xfc, 0x3f, 0x4, 0x20, '
	 '0xf4, 0x2f, 0x4, 0x20, 0xf4, 0x2f, 0x4, 0x20, 0xf4, 0x2f, 0x4, 0x20,'
	 ' 0xf4, 0x2f, 0x4, 0x20, 0xfc, 0x3f, 0x0, 0x0};')
iMask = ('#define bmp_width 16' + chr(10) + '#define bmp_height 12' + chr(10) +
	 'static char bmp_bits[] = {'+chr(10)+'0xfc, 0x3f, 0xfc, 0x3f, 0xfc, '
	 '0x3f, 0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f, '
	 '0xfc, 0x3f, 0xfc, 0x3f, 0xfc, 0x3f, 0x0, 0x0};')

def main ():
    class ScrollTest:
	def __init__ (self, parent):
	    self.sc = ScrolledCanvas(parent)
	    self.x = None
	    self.y = None
	    self.iObj = Tkinter.BitmapImage(data = iData, maskdata = iMask)
	    self.sc.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
	    Tkinter.Button(parent, text = "Toggle X",
			   command = self.toggleX).pack(side = Tkinter.BOTTOM,
							fill = Tkinter.X)
	    Tkinter.Button(parent, text = "Toggle Y",
			   command = self.toggleY).pack(side = Tkinter.BOTTOM,
							fill = Tkinter.X)
	    self.createAll()
	def createAll (self):
	    self.sc.create_oval(0,0,10,10)
	    self.toggleX()
	    self.toggleY()
	def toggleX (self):
	    if self.x == None:
		self.x = self.sc.create_image(500,0,image = self.iObj)
	    else:
		self.sc.delete(self.x)
		self.x = None
	    self.sc.updateScroll()
	def toggleY (self):
	    if self.y == None:
		self.y = self.sc.create_image(0,500,image = self.iObj)
	    else:
		self.sc.delete(self.y)
		self.y = None
	    self.sc.updateScroll()
    tk = Tkinter.Tk()
    ScrollTest(tk)
    tk.mainloop()

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of ScrolledCanvas.py
