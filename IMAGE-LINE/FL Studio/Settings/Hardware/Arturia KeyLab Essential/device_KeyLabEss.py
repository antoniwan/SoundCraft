# name= KeyLab Essential V2

"""
[[
	Surface:	KeyLab Essential
	Developer:	Farès MEZDOUR
	Version:	Beta 1.0
]]
"""

import midi
import ui
import mixer
import transport
import channels
import patterns
import ArturiaCrossKeyboardEss
import ArturiaVCOL



from KeyLabEssProcess import KeyLabEssMidiProcessor
from KeyLabEssReturn import KeyLabEssLightReturn
from KeyLabEssDisplay import KeyLabDisplay
from KeyLabEssPages import KeyLabPagedDisplay
    
    

## CONSTANT

TEMP = 0.5
COLOUR = [0x10, 0x11, 0x04, 0x05, 0x14, 0x7F, 0x01]

#-----------------------------------------------------------------------------------------

# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events


class MidiControllerConfig :

    def __init__(self):
        self._lightReturn = KeyLabEssLightReturn()
        self._display = KeyLabDisplay()
        self._paged_display = KeyLabPagedDisplay(self._display)


    def LightReturn(self) :
        return self._lightReturn

    def display(self):
        return self._display

    def paged_display(self):
        return self._paged_display

    # def scheduler(self):
        # return self._scheduler
        
    def Idle(self):
        #self._scheduler.Idle()
        self._paged_display.Refresh()
          
    
    def Sync(self):
    

        # Update display
        
        active_index = channels.selectedChannel()
        channel_name = channels.getChannelName(active_index)
        pattern_number = patterns.patternNumber()
        pattern_name = patterns.getPatternName(pattern_number)
        
        self._paged_display.SetPageLines(
            'main',
            line1='%d - %s' % (active_index + 1, channel_name),
            line2='%s' % pattern_name)



#----------------------------------------------------------------------------------------

# Function called for each event 

def init() :
    print("### Successfully created class objects ###")
    global _ess 
    _ess = MidiControllerConfig()
    global _processor
    _processor = KeyLabEssMidiProcessor(_ess)
    global _v_col
    _v_col = ArturiaVCOL.ArturiaVCOLLECTION()


def OnMidiMsg(event) :
    processor =  _processor.ProcessEvent(event)




# Function called when FL Studio is starting

def OnInit():
    print("### INIT KEYLAB ESSENTIAL OKAY ###")
    init()
    _ess.paged_display().SetPageLines('welcome', line1='KeyLab Essential', line2=ui.getProgTitle())
    _ess.paged_display().SetActivePage('main')
    _ess.paged_display().SetActivePage('welcome', expires = 1500)
    _ess.Sync()
    print("### Messages successfully sent to KEYLAB Essential ###")
    _ess.LightReturn().init()
        
 
# Handles the script when FL Studio closes

def OnDeInit():
    _ess.paged_display().SetPageLines('goodbye', line1='KeyLab Essential', line2='Disconnected')
    _ess.paged_display().SetActivePage('goodbye')
    send_to_device(bytes([0x02, 0x7D, 0x7D, 0x0B, 0x00]))
    return
  
# Function called when Play/Pause button is ON

def OnUpdateBeatIndicator(value):
    _ess.LightReturn().ProcessPlayBlink(value)
    _ess.LightReturn().ProcessRecordBlink(value)
 


# Function called at refresh, flag value changes depending on the refresh type 

def OnRefresh(flags) :
    _ess.Sync()
    _ess.LightReturn().RecordReturn()
    _ess.LightReturn().PlayReturn()

    

   
def OnIdle():
    _ess.Idle()
    _ess.LightReturn().MetronomeReturn()
    _ess.LightReturn().LoopReturn()
    _ess.LightReturn().NotBlinkingLed()


def OnSysEx(event) :
    OnRefresh(32)