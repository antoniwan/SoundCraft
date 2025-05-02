# This class creates the contextual buttons for KLEss3


class CTXButton() :

    def __init__(self) :

        self._type = 0
        self._line_number = 0
        self._color_type = 0
        self._icon = 0
        self._custom_color = [0, 0, 0]
        self._line1 = ""
        self._line2 = ""
        self._line3 = ""


    
    def get_type(self) :
        return self._type
    
    def get_line_number(self) :
        return self._line_number
    
    def get_color_type(self) :
        return self._color_type
    
    def get_icon(self) :
        return self._icon
    
    def get_custom_color(self) :
        return self._custom_color
    
    def get_line1(self) :
        return self._line1
    
    def get_line2(self) :
        return self._line2
    
    def get_line3(self) :
        return self._line3


    def Update(self, type, line_number, color_type, icon, custom_color, line1, line2) :
        self._type = type
        self._line_number = line_number
        self._color_type = color_type
        self._icon = icon
        self._custom_color = custom_color
        self._line1 = line1
        self._line2 = line2
  
    
    def _get_line_bytes(self, line):
        return bytearray(line, 'ascii')
    
    def _get_int_bytes(self, line):
        return bytes([line])



    def ButtonSysEx(self, ID) : # Check KeyLab mk3 SysEx frame

        data_button = bytes()

        data_button = data_button + bytes([ID+1])

        if self.get_type() != None :
            data_button = data_button + bytes([0x00]) + bytes([self.get_type()]) + bytes([0x00])
        
        if self.get_line_number() != None :
            data_button = data_button + bytes([0x01]) + bytes([self.get_line_number()]) + bytes([0x00])

        if self.get_color_type() != None :
            data_button = data_button + bytes([0x02]) + bytes([self.get_color_type()]) + bytes([0x00])

        if self.get_icon() != None :
            data_button = data_button + bytes([0x03]) + bytes([self.get_icon()]) + bytes([0x00])

        if self.get_custom_color() != None :
            data_button = data_button + bytes([0x04]) + bytes(self.get_custom_color()) + bytes([0x00])

        if self.get_line1() != None :
            data_button = data_button + bytes([0x05]) + self._get_line_bytes(self.get_line1()) + bytes([0x00])

        if self.get_line2() != None :
            data_button = data_button + bytes([0x06]) + self._get_line_bytes(self.get_line2()) + bytes([0x00])
            
        return data_button
        
