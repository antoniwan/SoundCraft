import time
import channels
import transport
import mixer
import ui
from KLEss3Dispatch import send_to_device

from Displays import eDisplays

# MIT License
# Copyright (c) 2020 Ray Juang

PLAY_STATUS = [0x00, 0x02]
REC_STATUS = [0x00, 0x03]

class KLEssDisplay:
    """ Manages scrolling display of two lines so that long strings can be scrolled on each line. """
    def __init__(self):
        # Holds the text to display on first line. May exceed the 16-char display limit.
        self._line1 = ' '
        # Holds the text to display on second line. May exceed the 16-char display limit.
        self._line2 = ' '
        # Sets the kind of display
        self._page_type = ' '

        # Holds ephemeral text that will expire after the expiration timestamp. These lines will display if the
        # the expiration timestamp is > current timestamp.
        self._ephemeral_line1 = ' '
        self._ephemeral_line2 = ' '
        self._expiration_time_ms = 0

        # Holds the starting offset of where the line1 text should start.
        self._line1_display_offset = 0
        
        # Holds the starting offset of where the line2 text should start.
        self._line2_display_offset = 0
        
        # Last timestamp in milliseconds in which the text was updated.
        self._last_update_ms = 0
        
        # Minimum interval before text is scrolled
        self._scroll_interval_ms = 1000
        
        # How many characters to allow last char to scroll before starting over.
        self._end_padding = 0
        
        # Track what's currently being displayed
        self._last_payload = bytes()

        # Data String
        self._data_string = bytes([0x04, 0x01, 0x60])
        
    # def _get_line1_bytes(self):
    #     # Get up to 31-bytes the exact chars to display for line 1.
    #     start_pos = self._line1_display_offset
    #     end_pos = start_pos + 31
    #     line_src = self._line1
    #     if self._expiration_time_ms > self.time_ms():
    #         line_src = self._ephemeral_line1
    #     return bytearray(line_src[start_pos:end_pos], 'ascii')

    # def _get_line2_bytes(self):
    #     # Get up to 31-bytes the exact chars to display for line 2.
    #     start_pos = self._line2_display_offset
    #     end_pos = start_pos + 31
    #     line_src = self._line2
    #     if self._expiration_time_ms > self.time_ms():
    #         line_src = self._ephemeral_line2
    #     return bytearray(line_src[start_pos:end_pos], 'ascii')

    def _get_line_src(self, line, length) :

        is_ascii = True

        # if line == "" :
        #     line_src == ".Empty."
        # else :

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
        
        return line_src

    def _get_line_bytes(self, line, length):
        # Get up to 31-bytes the exact chars to display for line 1.
        line_src = self._get_line_src(line, length) # Define above / Sort the ASCII char
        
        if line_src == None :
            return bytes()
        else :
            return bytearray(line_src, 'ascii')
    
    def _get_int_bytes(self, line):
        if line == None :
            return bytes([])
        else :
            return bytes([line])


    @staticmethod
    def time_ms():
        # Get the current timestamp in milliseconds
        return time.monotonic() * 1000


    # def _refresh_display(self, page_type, value):
    #     # Internally called to refresh the display now.
    #     string = []
        
    #     data_control = bytes([])
    #     data_string = bytes([0x04, 0x01, 0x60])
    #     data_line1 = bytes([0x01]) + self._get_line1_bytes() + bytes([0x00])
    #     data_line2 = bytes([0x02]) + self._get_line2_bytes() + bytes([0x00])
    #     #data += bytes([0x7F])
        
    #     if page_type == 1 :
    #         #print("Defaut")
    #         #Defaut Screen
    #         data_control = bytes([])
        
    #     elif page_type == 3 :
    #         #print("Two Lines")
    #         #Two Lines Screen
    #         data_control += bytes([0x1F, 0x02, 0x01, 0x00])
            
    #     elif page_type == 10 :
    #         #print("Encoder")
    #         #Encoder Screen
    #         data_control += bytes([0x01, 0x31, 0x32, 0x34, 0x00, 0x00])
            
    #     elif page_type == 11 :
    #         #print("Fader")
    #         #Fader Screen
    #         scaled_value = int(int(value)*127/100)
    #         data_control += bytes([0x1F, 0x04, 0x01, scaled_value, 0x00, 0x00])
            
    #     elif page_type == 12 :
    #         #print("scroll")
    #         #Scroll Screen
    #         data_control += bytes([0x12])
            
    #     elif page_type == 13 :
    #         #print("Picto")
    #         #Picto Screen
    #         data_control += bytes([0x1F, 0x07, 0x01, REC_STATUS[transport.isRecording()], PLAY_STATUS[transport.isPlaying() != 0], 0x01, 0x00])

    #     elif page_type == 14 :
    #         #print("scroll")
    #         #Scroll Screen
    #         data_control += bytes([0x1F, 0x05, 0x01, 0x00, 0x00, 0x00])

    #     elif page_type == 15 :
    #         #print("scroll")
    #         #Scroll Screen
    #         data_control += bytes([0x1F, 0x05, 0x01, 0x00, 0x00, 0x00])

    #     elif page_type == 16 :
    #         #print("scroll")
    #         #Scroll Screen
    #         data_control += bytes([0x1F, 0x05, 0x01, 0x00, 0x00, 0x00])

    #     elif page_type == 17 :
    #         #print("scroll")
    #         #Scroll Screen
    #         data_control += bytes([0x1F, 0x05, 0x01, 0x00, 0x00, 0x00])
            
        
    #     string = data_string + data_control + data_line1 + data_line2

    #     #self._update_scroll_pos()
    #     if self._last_payload != string:
    #         send_to_device(string)
    #         #print(page_type)
    #         self._last_payload = string

    ### Header ###
    def Header(self, line) :

        string = []
        data_control = bytes([eDisplays.eHeader])

        #data_icon = bytes([0x01]) + self._get_line_bytes(icon) + bytes([0x00])
        data_line = bytes([0x02]) + self._get_line_bytes(line, 16) + bytes([0x00])

        string = self._data_string + data_control + data_line + bytes([0x00])

        send_to_device(string)


    ### Footer ### Has its own bytearray function
    def Footer(self, button1, button2, button3, button4) :

        string = []
        data_control = bytes([eDisplays.eFooter])
        #data_button1 = bytes([0x10]) + self._get_int_bytes(button1.state()) + bytes([0x00]) + bytes([0x11]) + self._get_line_bytes(button1.text()) + bytes([0x00]) + bytes([0x12]) + self._get_int_bytes(button1.icon()) + bytes([0x00])
        #data_button2 = bytes([0x20]) + self._get_int_bytes(button2.state()) + bytes([0x00]) + bytes([0x21]) + self._get_line_bytes(button2.text()) + bytes([0x00]) + bytes([0x22]) + self._get_int_bytes(button2.icon()) + bytes([0x00])
        #data_button3 = bytes([0x30]) + self._get_int_bytes(button3.state()) + bytes([0x00]) + bytes([0x31]) + self._get_line_bytes(button3.text()) + bytes([0x00]) + bytes([0x32]) + self._get_int_bytes(button3.icon()) + bytes([0x00])
        #data_button4 = bytes([0x40]) + self._get_int_bytes(button4.state()) + bytes([0x00]) + bytes([0x41]) + self._get_line_bytes(button4.text()) + bytes([0x00]) + bytes([0x42]) + self._get_int_bytes(button4.icon()) + bytes([0x00])
        data_button1 = button1.ButtonSysEx(0)
        data_button2 = button2.ButtonSysEx(1)
        data_button3 = button3.ButtonSysEx(2)
        data_button4 = button4.ButtonSysEx(3)
        
        string = self._data_string + data_control + data_button1 + data_button2 + data_button3 + data_button4
        #string = self._data_string + data_control + data_button1

        send_to_device(string)


    ### F1L ###
    def Screen10(self, line1, transient) :

        string = []
        data_control = bytes([eDisplays.eFS_1Line])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + bytes([0x00])

        send_to_device(string)


    ### 1L ###
    def Screen11(self, line1, transient) :

        string = []
        data_control = bytes([eDisplays.e1Line])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + bytes([0x00])

        send_to_device(string)


    ### 2L ###
    def Screen12(self, line1, line2, transient) :

        string = []
        data_control = bytes([eDisplays.e2Lines])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 16) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + data_line2 + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + data_line2 + bytes([0x00])

        send_to_device(string)


    ### 2LS ###
    def Screen13(self, line1, line2) :

        string = []
        data_control = bytes([eDisplays.e2LinesScroll])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 16) + bytes([0x00])

        string = self._data_string + data_control + data_line1 + data_line2

        send_to_device(string)


    ### K ###
    def Screen14(self, line1, line2, hw_value, transient) :

        string = []
        data_control = bytes([eDisplays.eKnob])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 14) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 14) + bytes([0x00])
        data_hw = bytes([0x03]) + bytes([hw_value]) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + data_line2 + data_hw + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + data_line2 + data_hw + bytes([0x00])

        #print(string)
        send_to_device(string)


    ### F ###
    def Screen15(self, line1, line2, hw_value, transient) :

        string = []
        data_control = bytes([eDisplays.eFader])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 14) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 14) + bytes([0x00])
        data_hw = bytes([0x03]) + bytes([hw_value]) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + data_line2 + data_hw + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + data_line2 + data_hw + bytes([0x00])

        send_to_device(string)


    ### P ###
    def Screen16(self, line1, line2, hw_value, transient) :

        string = []
        data_control = bytes([eDisplays.ePad])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 14) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 14) + bytes([0x00])
        data_hw = bytes([0x03]) + bytes([hw_value]) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + data_line2 + data_hw + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + data_line2 + data_hw + bytes([0x00])

        send_to_device(string)


    ### P2L ###
    def Screen17(self, line1, line2) :

        string = []
        data_control = bytes([eDisplays.ePopup])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 16) + bytes([0x00])

        string = self._data_string + data_control + data_line1 + data_line2

        send_to_device(string)


    ### B2L ###
    def Screen18(self, line1, line2) :

        string = []
        data_control = bytes([eDisplays.eBlinkScreen])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 16) + bytes([0x00])

        string = self._data_string + data_control + data_line1 + data_line2

        send_to_device(string)

    
    ### LI2L ###
    def Screen19(self, line1, line2, icon, transient) :

        string = []
        data_control = bytes([eDisplays.eLeftIcon])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 16) + bytes([0x00])
        data_icon = bytes([0x03]) + bytes([icon]) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + data_line2 + data_icon + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + data_line2 + data_icon + bytes([0x00])

        send_to_device(string)


    ### TI2L ###
    def Screen20(self, line1, line2, icon, transient) :

        string = []
        data_control = bytes([eDisplays.eTopIcon])
        data_line1 = bytes([0x01]) + self._get_line_bytes(line1, 16) + bytes([0x00])
        data_line2 = bytes([0x02]) + self._get_line_bytes(line2, 16) + bytes([0x00])
        data_icon = bytes([0x03]) + bytes([icon]) + bytes([0x00])

        if transient :
            string = self._data_string + data_control + data_line1 + data_line2 + data_icon + bytes([0x01])
        else :
            string = self._data_string + data_control + data_line1 + data_line2 + data_icon + bytes([0x00])

        send_to_device(string)

    

    ### Clear Screen ##
    def ClearScreen(self) :

        string = []
        data_control = bytes([0x61])

        string = self._data_string + data_control + bytes([0x00])

        send_to_device(string) 
              

    def SetLines(self, page_type, value, line1=None, line2=None, expires=None):
        """ Update lines on the display, or leave alone if not provided.

        :param line1:    first line to update display with or None to leave as is.
        :param line2:    second line to update display with or None to leave as is.
        :param type:     sets the type of display
        :param expires:  number of milliseconds that the line persists before expiring. Note that when an expiration
            interval is provided, lines are interpreted as a blank line if not provided.
        """
        if expires is None:
            if line1 is not None:
                self._line1 = line1
            if line2 is not None:
                self._line2 = line2
        else:
            self._expiration_time_ms = self.time_ms() + expires
            if line1 is not None:
                self._ephemeral_line1 = line1
            if line2 is not None:
                self._ephemeral_line2 = line2

        self._refresh_display(page_type, value)
        return self

    def Refresh(self, page_type, value):
        """ Called to refresh the display, possibly with updated text. """
        if self.time_ms() - self._last_update_ms >= self._scroll_interval_ms:
            self._refresh_display(page_type, value)
        return self
        
