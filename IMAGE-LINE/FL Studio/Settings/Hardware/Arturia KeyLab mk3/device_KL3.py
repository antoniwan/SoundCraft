# name=KeyLab mk3
# supportedHardwareIds=00 20 6B 02 00 0A 02 7F 7F 7F 7F,00 20 6B 02 00 0A 04 7F 7F 7F 7F,00 20 6B 02 00 0A 08 7F 7F 7F 7F


"""
[[
	Surface:	KeyLab mk3
	Developer:	Farès MEZDOUR
	Version:	1.0
]]
"""

import time

import channels
import device
import midi
import mixer
import patterns
import playlist
import plugins
import transport
import ui

from KL3Connexion import Connexion
from KL3Dispatch import send_to_device
from KL3Display import Display
from KL3Pages import PagedDisplay
from KL3Process import MidiProcessor
from KL3Return import Return
from images_sub_enums import eCenterIcon


## CONSTANT

PORT_MIDICC_ANALOGLAB = 10

#-----------------------------------------------------------------------------------------

# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events


class MidiControllerConfig :

    def __init__(self):
        self._display = Display()
        self._paged_display = PagedDisplay(self._display)
        self._connexion = Connexion()
        self._return = Return(self._paged_display)
        
        
    def display(self):
        return self._display

    def paged_display(self):
        return self._paged_display

    def Return(self) :
        return self._return
    
    def connexion(self):
        return self._connexion
        
    def Idle(self):
        
        self._return.IdleSequencer()
        self._return.IdleTimeline()


#----------------------------------------------------------------------------------------

# Function called for each event 

def OnMidiMsg(event) :
    if _processor.ProcessEvent(event):
        event.handled = False



# Function called when FL Studio is starting

def OnInit():
    print('Loaded MIDI script for Arturia KeyLab mk3')
    init()

    _KL3.connexion().DAWConnexion()
    _KL3.Return().init()


    _KL3._paged_display.SetCenterPage(
        31,
        line1=ui.getProgTitle(),
        colortype1=1,
        color1=[127, 127, 127],
        line2="Connected",
        colortype2=1,
        color2=[127, 127, 127],
        icon = eCenterIcon.ekIconsFlStudio_image,
        )


    print("### Messages successfully sent to KeyLab mk3 ###")


        
def init() :
    # Connxexion

    global _KL3 
    _KL3 = MidiControllerConfig()
    global _processor
    _processor = MidiProcessor(_KL3) 
    print("### Successfully created class objects ###")

    
    
# Handles the script when FL Studio closes

def OnDeInit():
    pass
    # Deconnxexion

    _KL3.connexion().DAWDisconnection()
   
  
# Function called when Play/Pause button is ON

def OnUpdateBeatIndicator(value):
    _KL3.Return().ProcessPlayBlink(value)
    _KL3.Return().ProcessRecordBlink(value)
    _KL3.Return().ProcessSequencerBlink(value)
 

# Function called at refresh, flag value changes depending on the refresh type 

def OnRefresh(flags) :



    if flags not in [4,4096] :
        _KL3.Return().RecordReturn()
        _KL3.Return().PlayReturn()
        _KL3.Return().LoopReturn()
        _KL3.Return().MetronomeReturn()
        _KL3.Return().SequencerReturn()
        _KL3.Return().UndoHistoryReturn()
        _KL3.Return().BackReturn()
        _KL3.Return().DrumrackReturn()

        _KL3.Return().ChannelRackReturn()
        _KL3.Return().MixerReturn()
    

# Function called time to time mainly to update the beat indicator

def OnIdle():
    
    _KL3.Idle()
    #_mk3.LightReturn().LEDTest()

    
