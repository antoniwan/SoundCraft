import time
import channels
import transport
import mixer
import ui

from KL3Dispatch import send_to_device
from ScreenId import eScreenId
from IntegrationPatchId import eIntegrationPatchId
from ParamId import eParamId

# MIT License
# Copyright (c) 2020 Ray Juang

PLAY_STATUS = [0x00, 0x02]
REC_STATUS = [0x00, 0x03]

class Display:
    
    def __init__(self):
        # Data String
        self._data_string = bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eDisplay])



    def _get_line_src(self, line, length, line_is_upper_case) :

        is_ascii = True


        for i in line :
            if ord(i) not in range (0,128) :          #Undefined char '?'
                is_ascii = False
    
        if is_ascii :
            if len(line) > length :
                line_src = line[:length-4] + "..."
            else :
                line_src = line

        else :
            line_src = ".Undefined text."
        
        if line_is_upper_case :
            line_src = line_src.upper()

        return line_src

    def _get_line_bytes(self, line, length, line_is_upper_case=False):
        # Get up to 31-bytes the exact chars to display for line 1.
        line_src = self._get_line_src(line, length, line_is_upper_case) # Define above / Sort the ASCII char
        
        if line_src == None :
            return bytes()
        else :
            return bytearray(line_src, 'ascii')
    
    def _get_int_bytes(self, line):
        if line == None :
            return bytes([])
        else :
            return bytes([line])

    




    ### CONTEXTUAL BUTTONS ###
    def CTXButtonScreen(self, button) : 

        string = []
        data_button = button

        string = self._data_string + data_button

        send_to_device(string)


    def CleanCTXButtonScreen(self, ID) : 

        string = []
        data_button = bytes([ID]) + bytes([0]*3)

        string = self._data_string + data_button

        send_to_device(string)


    ### Properties ###
    def Screen_Prop(self, color1) :

        string = []
        data_screenID = bytes([eScreenId.eScreenProperties])
        data_color1 = bytes([0x00]) + bytes(color1) + bytes([0x00])

        string = self._data_string + data_screenID + data_color1

        send_to_device(string)

    ### F1L ###
    def Screen_F1L(self, line1, colortype1, color1) :

        string = []
        data_screenID = bytes([eScreenId.eScreen1L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1

        send_to_device(string)


    ### F1LInv ###
    def Screen_F1LInv(self, line1, colortype1, color1) :

        string = []
        data_screenID = bytes([eScreenId.eScreen1LInverted])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1

        send_to_device(string)


    ### F2L ###
    def Screen_F2L(self, line1, colortype1, color1, line2, colortype2, color2) :

        string = []
        data_screenID = bytes([eScreenId.eScreen2L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        data_line2 = bytes([0x03]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_colortype2 = bytes([0x04]) + bytes([colortype2]) + bytes([0x00])
        data_color2 = bytes([0x05]) + bytes(color2) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1 + data_line2 + data_colortype2 + data_color2

        send_to_device(string)


    ### F2LInv ###
    def Screen_F2LInv(self, line1, colortype1, color1, line2, colortype2, color2) :

        string = []
        data_screenID = bytes([eScreenId.eScreen2LInverted])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        data_line2 = bytes([0x03]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_colortype2 = bytes([0x04]) + bytes([colortype2]) + bytes([0x00])
        data_color2 = bytes([0x05]) + bytes(color2) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1 + data_line2 + data_colortype2 + data_color2

        send_to_device(string)


    ### FB2L ###
    def Screen_FB2L(self, line1, colortype1, color1, line2, colortype2, color2) :

        string = []
        data_screenID = bytes([eScreenId.eScreen2LBig])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        data_line2 = bytes([0x03]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_colortype2 = bytes([0x04]) + bytes([colortype2]) + bytes([0x00])
        data_color2 = bytes([0x05]) + bytes(color2) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1 + data_line2 + data_colortype2 + data_color2

        send_to_device(string)

    
    ### LI1L ###
    def Screen_LI1L(self, line1, color, icon) :

        string = []
        data_screenID = bytes([eScreenId.eScreenLI_1L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_icon = bytes([])
        
        if icon != None :
            data_icon = bytes([0x01]) + bytes([icon]) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_icon

        send_to_device(string)


    ### LI2L ###
    def Screen_LI2L(self, line1, line2, color, icon) :

        string = []
        data_screenID = bytes([eScreenId.eScreenLI_2L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_line2 = bytes([0x01]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_icon = bytes([])
        
        if icon != None :
            data_icon = bytes([0x02]) + bytes([icon]) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_line2 + data_icon

        send_to_device(string)

    
    ### P1L ###
    def Screen_P1L(self, line1, color) :

        string = []
        data_screenID = bytes([eScreenId.eScreenPopup1L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1

        send_to_device(string)


    ### P2L ###
    def Screen_P2L(self, line1, colortype1, color1, line2, colortype2, color2) :

        string = []
        data_screenID = bytes([eScreenId.eScreenPopup2L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        data_line2 = bytes([0x03]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_colortype2 = bytes([0x04]) + bytes([colortype2]) + bytes([0x00])
        data_color2 = bytes([0x05]) + bytes(color2) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1 + data_line2 + data_colortype2 + data_color2

        send_to_device(string)


    ### P3L ###
    def Screen_P3L(self, line1, colortype1, color1, line2, colortype2, color2, line3, colortype3, color3) :

        string = []
        data_screenID = bytes([eScreenId.eScreenPopup3L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        data_line2 = bytes([0x03]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_colortype2 = bytes([0x04]) + bytes([colortype2]) + bytes([0x00])
        data_color2 = bytes([0x05]) + bytes(color2) + bytes([0x00])

        data_line3 = bytes([0x06]) + self._get_line_bytes(line3, 32, True) + bytes([0x00])
        data_colortype3 = bytes([0x07]) + bytes([colortype3]) + bytes([0x00])
        data_color3 = bytes([0x08]) + bytes(color3) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1 + data_line2 + data_colortype2 + data_color2 + data_line3 + data_colortype3 + data_color3

        send_to_device(string)

    
    ### PLI1L ###
    def Screen_PLI1L(self, line1, color, icon) :

        string = []
        data_screenID = bytes([eScreenId.eScreenPopupLI_1L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_icon = bytes([])
        
        if icon != None :
            data_icon = bytes([0x01]) + bytes([icon]) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_icon

        send_to_device(string)


    ### PLI2L ###
    def Screen_PLI2L(self, line1, colortype1, color1, line2, colortype2, color2, icon) :

        string = []
        data_screenID = bytes([eScreenId.eScreenPopupLI_2L])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        data_line2 = bytes([0x03]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_colortype2 = bytes([0x04]) + bytes([colortype2]) + bytes([0x00])
        data_color2 = bytes([0x05]) + bytes(color2) + bytes([0x00])

        data_icon = bytes([])

        if icon != None :
            data_icon = bytes([0x06]) + bytes([icon]) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1 + data_line2 + data_colortype2 + data_color2 + data_icon

        send_to_device(string)


    ### K ###
    def Screen_K(self, line1, line2, hw_value, colortype1, color1) :

        string = []
        data_screenID = bytes([eScreenId.eScreenKnob])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line2, 32) + bytes([0x00]) #Line 1 and 2 inverted to respect the order in popup
        data_line2 = bytes([0x01]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_hw = bytes([0x02]) + bytes([hw_value]) + bytes([0x00])
        data_colortype1 = bytes([0x03]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x04]) + bytes(color1) + bytes([0x00])
         
        string = self._data_string + data_screenID + data_line1 + data_line2 + data_hw + data_colortype1 + data_color1

        send_to_device(string)


    ### F ###
    def Screen_F(self, line1, line2, hw_value, colortype, color) :

        string = []
        data_screenID = bytes([eScreenId.eScreenFader])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line2, 32) + bytes([0x00])
        data_line2 = bytes([0x01]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_hw = bytes([0x02]) + bytes([hw_value]) + bytes([0x00])
        data_colortype = bytes([0x03]) + bytes([colortype]) + bytes([0x00])
        data_color = bytes([0x04]) + bytes(color) + bytes([0x00])
         
        string = self._data_string + data_screenID + data_line1 + data_line2 + data_hw + data_colortype + data_color

        send_to_device(string)



    ### P ###
    def Screen_P(self, line1, line2, hw_value, colortype, color) :

        string = []
        data_screenID = bytes([eScreenId.eScreenPad])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line2, 32) + bytes([0x00])
        data_line2 = bytes([0x01]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_hw = bytes([0x02]) + bytes([hw_value]) + bytes([0x00])
        data_colortype = bytes([0x03]) + bytes([colortype]) + bytes([0x00])
        data_color = bytes([0x04]) + bytes(color) + bytes([0x00])
         
        string = self._data_string + data_screenID + data_line1 + data_line2 + data_colortype + data_color + data_hw

        send_to_device(string)

    
    ### TI2LFIX ###
    def Screen_TI2LFIX(self, line1, colortype1, color1, line2, colortype2, color2, icon) :

        string = []
        data_screenID = bytes([eScreenId.eScreenPopupFull])
        data_line1 = bytes([0x00]) + self._get_line_bytes(line1, 32) + bytes([0x00])
        data_colortype1 = bytes([0x01]) + bytes([colortype1]) + bytes([0x00])
        data_color1 = bytes([0x02]) + bytes(color1) + bytes([0x00])

        data_line2 = bytes([0x03]) + self._get_line_bytes(line2, 32, True) + bytes([0x00])
        data_colortype2 = bytes([0x04]) + bytes([colortype2]) + bytes([0x00])
        data_color2 = bytes([0x05]) + bytes(color2) + bytes([0x00])

        data_icon = bytes([])

        if icon != None :
            data_icon = bytes([0x06]) + bytes([icon]) + bytes([0x00])

        string = self._data_string + data_screenID + data_line1 + data_colortype1 + data_color1 + data_line2 + data_colortype2 + data_color2 + data_icon

        send_to_device(string)



    ### Clear Screen ##
    def ClearScreen(self) :

        string = []

        #TODO

        send_to_device(string) 
              

    # def SetLines(self, page_type, value, line1=None, line2=None, expires=None):
    #     """ Update lines on the display, or leave alone if not provided.

    #     :param line1:    first line to update display with or None to leave as is.
    #     :param line2:    second line to update display with or None to leave as is.
    #     :param type:     sets the type of display
    #     :param expires:  number of milliseconds that the line persists before expiring. Note that when an expiration
    #         interval is provided, lines are interpreted as a blank line if not provided.
    #     """
    #     if expires is None:
    #         if line1 is not None:
    #             self._line1 = line1
    #         if line2 is not None:
    #             self._line2 = line2
    #     else:
    #         self._expiration_time_ms = self.time_ms() + expires
    #         if line1 is not None:
    #             self._ephemeral_line1 = line1
    #         if line2 is not None:
    #             self._ephemeral_line2 = line2

    #     self._refresh_display(page_type, value)
    #     return self

    # def Refresh(self, page_type, value):
    #     """ Called to refresh the display, possibly with updated text. """
    #     if self.time_ms() - self._last_update_ms >= self._scroll_interval_ms:
    #         self._refresh_display(page_type, value)
    #     return self