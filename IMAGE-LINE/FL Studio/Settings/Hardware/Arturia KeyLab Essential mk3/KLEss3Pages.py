
from KLEss3Display import KLEssDisplay
from KLEss3Buttons import KLEssCTXButton
import device

# MIT License
# Copyright (c) 2020 Ray Juang

class KLEssPagedDisplay:
    def __init__(self, display):
        self._display = display

        # Header string
        self._header_line = {}

        # Sets the header icon
        self._header_icon = 0

        

        # String line 1
        self._line1 = {}
        
        # String line 2
        self._line2 = {}

        # Sets the type of the screen
        self._page_type = 12

        # Sets the hardware value for the widget on the screen
        self._value = 0

        # Sets the hardware value for the widget on the screen
        self._icon = 0

        # Sets if the page is a transient page or not
        self._transient = 0


        # Footer content
        self._button1 = KLEssCTXButton()
        self._button2 = KLEssCTXButton()
        self._button3 = KLEssCTXButton()
        self._button4 = KLEssCTXButton()


        

        #Sets the footer content

    def SetHeaderPage(self, line=None) :
        self._header_line = line
        #self._header_icon = icon
        
        self._display.Header(self._header_line)

    
    def SetButton(self, ID, state, text, icon) :
        if text == "" :
            text = None
        if icon == 0 :
            icon = None

        if ID == 1 :
            self._button1.Update(state, text, icon)
        if ID == 2 :
            self._button2.Update(state, text, icon)
        if ID == 3 :
            self._button3.Update(state, text, icon)
        if ID == 4 :
            self._button4.Update(state, text, icon)


    def SetFooterPage(self) :
        #print(self._button1.state(), self._button1.text(), self._button1.icon())
        #print(self._button2.state(), self._button2.text(), self._button2.icon())
        #print(self._button3.state(), self._button3.text(), self._button3.icon())
        #print(self._button4.state(), self._button4.text(), self._button4.icon())
        self._display.Footer(self._button1, self._button2, self._button3, self._button4)


    def SetCenterPage(self, page_type, line1=None, line2=None, hw_value=None, icon=None, transient=0):

        self._page_type = page_type
        self._value = hw_value
        self._icon = icon
        self._transient = transient
        self._line1 = line1
        self._line2 = line2

        #print(self._page_type, self._line1, self._line2)

        if self._page_type == 10 :
            self._display.Screen10(self._line1, self._transient)

        elif self._page_type == 11 :
            self._display.Screen11(self._line1, self._transient)

        elif self._page_type == 12 :
            self._display.Screen12(self._line1, self._line2, self._transient)

        elif self._page_type == 13 :
            self._display.Screen13(self._line1, self._line2)

        elif self._page_type == 14 :
            self._display.Screen14(self._line1, self._line2, self._value, self._transient)

        elif self._page_type == 15 :
            self._display.Screen15(self._line1, self._line2, self._value, self._transient)

        elif self._page_type == 16 :
            self._display.Screen16(self._line1, self._line2, self._value, self._transient)

        elif self._page_type == 17 :
            self._display.Screen17(self._line1, self._line2)

        elif self._page_type == 18 :
            self._display.Screen18(self._line1, self._line2)

        elif self._page_type == 19 :
            self._display.Screen19(self._line1, self._line2, self._icon, self._transient)

        elif self._page_type == 20 :
            self._display.Screen20(self._line1, self._line2, self._icon, self._transient)
        
        elif self._page_type == 0 :
            #print("Screen cleared")
            self._display.ClearScreen()



