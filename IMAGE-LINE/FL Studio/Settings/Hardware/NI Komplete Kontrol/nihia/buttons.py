# MIT License

# Copyright (c) 2021 Pablo Peral

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Subfile of flmidi-nihia used to manipulate the state of buttons of Komplete Kontrol keyboards.
"""

import nihia

# Button name to button ID dictionary
# The button ID is the number in hex that is used as the DATA1 parameter when a MIDI message related to that button is
# sent or recieved from the device
button_list = {
    "PLAY": 16,
    "RESTART": 17,
    "REC": 18,
    "COUNT_IN": 19,
    "STOP": 20,
    "CLEAR": 21,
    "LOOP": 22,
    "METRO": 23,
    "TEMPO": 24,
    
    "UNDO": 32,
    "REDO": 33,
    "QUANTIZE": 34,
    "AUTO": 35,

    "MUTE": 67,
    "SOLO": 68,

    "MUTE_SELECTED": 102,
    "SOLO_SELECTED": 103,

    "ENCODER_BUTTON": 96,
    "ENCODER_BUTTON_SHIFTED": 97,
    
    # The 4D encoder events use the same data1, and direction in data2
    # 
    # data1 values are inverted for the axis of the 4D Encoder between A/M devices and S devices
    "ENCODER_X_A": 50,
    "ENCODER_X_S": 48,
    
    "ENCODER_Y_A": 48,
    "ENCODER_Y_S": 50,

    "NAVIGATE_BANKS": 49,

    # Jog / knob
    "ENCODER_GENERAL": 52,
    "ENCODER_VOLUME_SELECTED": 100,
    "ENCODER_PAN_SELECTED": 101
}

# Method for controlling the lighting on the buttons (for those who have idle/highlighted two state lights)
# Examples of this kind of buttons are the PLAY or REC buttons, where the PLAY button alternates between low and high light and so on.
# SHIFT buttons are also included in this range of buttons, but instead of low/high light they alternate between on/off light states.
def setLight(buttonName: str, lightMode: int):
    """ Method for controlling the lights on the buttons of the device. 
    
    ### Parameters

     - buttonName: Name of the button as shown in the device in caps and enclosed in quotes. ("PLAY", "AUTO", "REDO"...)
        - EXCEPTION: declare the Count-In button as COUNT_IN
    
     - lightMode: If set to 0, sets the first light mode of the button. If set to 1, sets the second light mode.
        - EXCEPTION: Navigation components (4D encoder and bank buttons) are using the two lowest bits per direction (0..3)"""

    # Then sends the MIDI message using dataOut
    nihia.dataOut(button_list.get(buttonName), lightMode)