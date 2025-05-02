import device
from MiniLabmk2Dispatch import send_to_device 


# This class organize the LED functions usefull for visual returns.
# The class sets up a LED map depending on the controller

class MiniLabmk2Led:


    # Value for turning on an LED
    LED_ON = 127
    # Value for turning off an LED
    LED_OFF = 0

    SET_COLOR_COMMAND = bytes([0x02, 0x00, 0x10])

    # 8*2-pad
    
    ID_PAD1 = 0x70
    ID_PAD2 = 0x71
    ID_PAD3 = 0x72
    ID_PAD4 = 0x73
    ID_PAD5 = 0x74
    ID_PAD6 = 0x75
    ID_PAD7 = 0x76
    ID_PAD8 = 0x77
    
    ID_PAD9 = 0x78
    ID_PAD10 = 0x79
    ID_PAD11 = 0x7A
    ID_PAD12 = 0x7B
    ID_PAD13 = 0x7C
    ID_PAD14 = 0x7D
    ID_PAD15 = 0x7E
    ID_PAD16 = 0x7F


    # 8*2 lookup for the pad ids MiniLabMkII
    
    MATRIX_IDS_PAD = [
        [ID_PAD1, ID_PAD2, ID_PAD3, ID_PAD4, ID_PAD5, ID_PAD6, ID_PAD7, ID_PAD8],
        [ID_PAD9, ID_PAD10, ID_PAD11, ID_PAD12, ID_PAD13, ID_PAD14, ID_PAD15, ID_PAD16],
    ]


    def SetPadLights(self, matrix_values):
        """ Set the pad lights given a matrix of color values to set the pad with.
        :param matrix_values: 8x2 array of arrays containing the LED color values.
        """
        led_map = {}
        for r in range(2):
            for c in range(8):
                led_map[MiniLabmk2Led.MATRIX_IDS_PAD[r][c]] = matrix_values[r][c]
        self.SetLights(led_map)


    def SetLights(self, led_mapping):
        #Given a map of LED ids to color value, construct and send a command with all the led mapping.
        
        data = bytes([])
        for led_id, led_value in led_mapping.items():
            data += bytes([led_id, led_value])
            send_to_device(MiniLabmk2Led.SET_COLOR_COMMAND + data)