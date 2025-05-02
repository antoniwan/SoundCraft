# name= MiniLab mkII V2

"""
[[
	Surface:	MiniLab mkII
	Developer:	Farès MEZDOUR
	Version:	Beta 1.0
	Date:		6/11/2021

]]
"""


import time
import midi
import ui
import sys
import mixer
import transport
import channels
import playlist
import patterns
import device



from MiniLabmk2Leds import MiniLabmk2Led
from MiniLabmk2Process import MiniLabMidiProcessor
from MiniLabmk2Return import MiniLabLightReturn

## CONSTANT

TEMP = 0.25
COLOUR = [0x10,0x11,0x04,0x05,0x14,0x7F,0x01]
C_OFF = 0x00
C_RED = 0x01
C_BLUE = 0x10
C_PURPLE = 0x11
C_GREEN = 0x04
C_YELLOW = 0x05
C_CYAN = 0x14
C_WHITE = 0x7F
AL_MEMORY = 0

#-----------------------------------------------------------------------------------------

# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events


class MidiControllerConfig :

    def __init__(self):
        self._lights = MiniLabmk2Led()
        self._lightReturn = MiniLabLightReturn()
        
    def lights(self):
        return self._lights

    def blink(self):
        return self._blink

    def LightReturn(self) :
        return self._lightReturn
        
    def Sync(self, colour):
    
        # Syncs up all visual indicators on keyboard with changes from FL Studio. 
        
        led_map = {
            MiniLabmk2Led.ID_PAD1 : colour,
            MiniLabmk2Led.ID_PAD2 : colour,
            MiniLabmk2Led.ID_PAD3 : colour,
            MiniLabmk2Led.ID_PAD4 : colour,
            MiniLabmk2Led.ID_PAD5 : colour,
            MiniLabmk2Led.ID_PAD6 : colour,
            MiniLabmk2Led.ID_PAD7 : colour,
            MiniLabmk2Led.ID_PAD8 : colour
        }
        self._lights.SetLights(led_map)
        
        
        led_map = {
            MiniLabmk2Led.ID_PAD9 : C_GREEN,
            MiniLabmk2Led.ID_PAD10 : C_BLUE,
            MiniLabmk2Led.ID_PAD11 : C_RED,
            MiniLabmk2Led.ID_PAD12 : C_YELLOW,
            MiniLabmk2Led.ID_PAD13 : C_YELLOW,
            MiniLabmk2Led.ID_PAD14 : C_PURPLE,
            MiniLabmk2Led.ID_PAD15 : C_CYAN,
            MiniLabmk2Led.ID_PAD16 : C_WHITE
        }
        self._lights.SetLights(led_map)
        
        
        



_mk2 = MidiControllerConfig()
_processor = MiniLabMidiProcessor(_mk2)


#----------------------------------------------------------------------------------------

# Function called for each event 

def OnMidiMsg(event) :
    if _processor.ProcessEvent(event):
        event.handled = False


# Function called when FL Studio is starting

def OnInit():
    print('Loaded MIDI script for Arturia MiniLab mkII')
    for i in COLOUR :
        _mk2.Sync(i)
        time.sleep(TEMP)
    

# Handles the script when FL Studio closes

def OnDeInit():
    return
        
  
# Function called when Play/Pause button is ON

def OnUpdateBeatIndicator(value):
    if not AL_MEMORY :
        _mk2.LightReturn().ProcessPlayBlink(value)
        _mk2.LightReturn().ProcessRecordBlink(value)
 

# Function called at refresh, flag value changes depending on the refresh type 

def OnRefresh(flags) :
    if not AL_MEMORY :
        _mk2.LightReturn().MetronomeReturn()
        _mk2.LightReturn().RecordReturn()
        _mk2.LightReturn().PlayReturn()
        _mk2.LightReturn().BrowserReturn()
        _mk2.LightReturn().NotBlinkingLed()
    


def OnPitchBend(event) :
    channels.setChannelPitch(channels.channelNumber(),(100/64)*event.data2-100,1)
    event.handled = True


def OnSysEx(event) :
    if not event.sysex in [b'\xf0\x00 k\x7fB\x02\x00\x00.\x00\xf7', b'\xf0\x00 k\x7fB\x02\x00\x00.\x7f\xf7'] :
        if event.sysex == b'\xf0\x00 k\x7fB\x1b\x00\xf7' :
            global AL_MEMORY
            AL_MEMORY = 1
        else :
            AL_MEMORY = 0
        