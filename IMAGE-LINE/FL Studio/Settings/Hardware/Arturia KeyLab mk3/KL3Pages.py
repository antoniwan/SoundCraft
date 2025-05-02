
from KL3Display import Display
from KL3Buttons import CTXButton
import device

# MIT License
# Copyright (c) 2020 Ray Juang

class PagedDisplay:
    def __init__(self, display):
        self._display = display

        # Footer content
        self._list_button = []

        for i in range (0,8) :
            CTX = CTXButton()
            self._list_button.append(CTX)





    def SetButton(self, ID, type, line_number, color_type, icon, custom_color, line1, line2) :

        self._list_button[ID].Update(type, line_number, color_type, icon, custom_color, line1, line2)




    def RefreshCTXButton(self, ID) :
        str_button = self._list_button[ID].ButtonSysEx(ID)
        self._display.CTXButtonScreen(str_button)
        
    def CleanCTXButton(self, ID) :
        self._display.CleanCTXButtonScreen(ID)


    def RefreshAllCTXButtons(self) :
        for ID in range (0,8) :
            self.RefreshCTXButton(ID)

    def CleanAllCTXButtons(self) :    
        for ID in range (0,8) :
            self.CleanCTXButton(ID)



    def SetCenterPage(
            self, 
            page_type, 
            line1=None, 
            colortype1=None, 
            color1=None, 
            line2=None,
            colortype2=None,  
            color2=None,
            line3=None,
            colortype3=None,  
            color3=None,   
            hw_value=None, 
            icon=None):

        self._page_type = page_type
        self._line1 = line1
        self._colortype1 = colortype1
        self._color1 = color1
        self._line2 = line2
        self._colortype2 = colortype2
        self._color2 = color2
        self._line3 = line3
        self._colortype3 = colortype3
        self._color3 = color3
        self._value = hw_value
        self._icon = icon


        if self._page_type == 10 :
            self._display.Screen_F1L(
                self._line1,
                self._colortype1,
                self._color1,
            )
        
        elif self._page_type == 11 :
            self._display.Screen_F1LInv(
                self._line1,
                self._colortype1,
                self._color1,
            )

        elif self._page_type == 12 :
            self._display.Screen_F2L(
                self._line1,
                self._colortype1,
                self._color1,
                self._line2,
                self._colortype2,
                self._color2,
            )
             
        elif self._page_type == 13 :
            self._display.Screen_F2LInv(
                self._line1,
                self._colortype1,
                self._color1,
                self._line2,
                self._colortype2,
                self._color2,
            )

        elif self._page_type == 14 :
            self._display.Screen_FB2L(
                self._line1,
                self._colortype1,
                self._color1,
                self._line2,
                self._colortype2,
                self._color2,
            )
            
        elif self._page_type == 15 :
            self._display.Screen_LI1L(
                self._line1,
                self._icon,
                self._color1,
            )

        elif self._page_type == 16 :
            self._display.Screen_LI2L(
                self._line1,
                self._line2,
                self._color1,
                self._icon,
            )

        elif self._page_type == 23 :
            self._display.Screen_P1L(
                self._line1,
                self._color1,
            )

        elif self._page_type == 24 :
            self._display.Screen_P2L(
                self._line1,
                self._colortype1,
                self._color1,
                self._line2,
                self._colortype2,
                self._color2,
            )

        elif self._page_type == 25 :
            self._display.Screen_P3L(
                self._line1,
                self._colortype1,
                self._color1,
                self._line2,
                self._colortype2,
                self._color2,
                self._line3,
                self._colortype3,
                self._color3,
            )

        elif self._page_type == 26 :
            self._display.Screen_PLI1L(
                self._line1,
                self._color1,
                self._icon,
            )

        elif self._page_type == 27 :
            self._display.Screen_PLI2L(
                self._line1,
                self._colortype1,
                self._color1,
                self._line2,
                self._colortype2,
                self._color2,
                self._icon,
            )


        elif self._page_type == 28 :
            self._display.Screen_K(
                self._line1,
                self._line2,
                self._value,
                self._colortype1,
                self._color1,  
            )

        elif self._page_type == 29 :
            self._display.Screen_F(
                self._line1,
                self._line2,
                self._value,
                self._colortype1,
                self._color1,
            )

        elif self._page_type == 30 :
            self._display.Screen_P(
                self._line1,
                self._line2,
                self._value,
                self._colortype1,
                self._color1, 
            )

        elif self._page_type == 31 :
            self._display.Screen_TI2LFIX(
                self._line1,
                self._colortype1,
                self._color1,
                self._line2,
                self._colortype2,
                self._color2,
                self._icon,

            )

        elif self._page_type == 0 :
            self._display.Screen_Prop(
                self._color1, 
            )



### UTILITY ###
