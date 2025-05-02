# This class creates the contextual buttons for KLEss3


class KLEssCTXButton() :

    def __init__(self) :
        
        self._text = ""
        self._icon = 0
        self._state = 0

    def text(self) :
        return self._text

    def icon(self) :
        return self._icon
    
    def state(self) :
        return self._state

    def Update(self, state, text, icon) :
        self._state = state
        self._text = text
        self._icon = icon

    def _get_line_bytes(self, line):
        return bytearray(line, 'ascii')
    
    def _get_int_bytes(self, line):
        return bytes([line])

    def ButtonSysEx(self, ID) :

        data_button = bytes()

        if self._state != None :
            data_button = data_button + bytes([0x10+ID*16]) + self._get_int_bytes(self.state()) + bytes([0x00])

        if self._text != None :
            data_button = data_button + bytes([0x11+ID*16]) + self._get_line_bytes(self.text()) + bytes([0x00])

        if self._icon != None :
            data_button = data_button + bytes([0x12+ID*16]) + self._get_int_bytes(self.icon()) + bytes([0x00])

        return data_button
        
