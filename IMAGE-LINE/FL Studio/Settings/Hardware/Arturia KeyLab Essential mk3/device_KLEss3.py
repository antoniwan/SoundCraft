# name=KeyLab Essential mk3

# supportedHardwareIds=00 20 6B 02 00 05 72,00 20 6B 02 00 05 74

"""
[[
	Surface:	KeyLab Essential mk3
	Developer:	Farès MEZDOUR
	Version:	0.1
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

import ArturiaVCOL
from KLEss3Buttons import KLEssCTXButton
from KLEss3Connexion import KLEssConnexion
from KLEss3Dispatch import send_to_device
from KLEss3Display import KLEssDisplay
from KLEss3Pages import KLEssPagedDisplay
from KLEss3Process import KLEssMidiProcessor
from KLEss3Return import KLEssReturn

from Icons import eIcons

## CONSTANT

TEMP = 0.5
COLOUR = [0x10,0x11,0x04,0x05,0x14,0x7F,0x01]
PORT_MIDICC_ANALOGLAB = 10

#-----------------------------------------------------------------------------------------

# This is the master class. It will run the init lights pattern 
# and call the others class to process MIDI events


class MidiControllerConfig :

    def __init__(self):
        self._display = KLEssDisplay()
        self._paged_display = KLEssPagedDisplay(self._display)
        self._connexion = KLEssConnexion()
        self._return = KLEssReturn(self._paged_display)
        self._disp = 0
        
        
    def display(self):
        return self._display

    def paged_display(self):
        return self._paged_display

    def Return(self) :
        return self._return
    
    def connexion(self):
        return self._connexion
        
    # def Idle(self):
    #     self._paged_display.Refresh()
        
    def RefreshMainScreen(self):
        # Update display

        active_index = channels.selectedChannel()
        channel_name = channels.getChannelName(active_index)
        for i in range(len(channel_name)) :
            if (ord(channel_name[i]) not in range(0,127)) :
                str1 = channel_name[0:i]
                str2 = channel_name[i+1::]
                channel_name = str1 + '?' + str2
        pattern_number = patterns.patternNumber()
        pattern_name = patterns.getPatternName(pattern_number)      
        _KLEss3._paged_display.SetCenterPage(12, 
                                            #line1='%d - %s' % (active_index + 1, channel_name),
                                            line1='%s' % (channel_name),  
                                            line2=pattern_name, 
                                            icon=eIcons.eNone, 
                                            hw_value=0, 
                                            transient=0
                                            )



#----------------------------------------------------------------------------------------

# Function called for each event 

def OnMidiMsg(event) :
    if _processor.ProcessEvent(event):
        event.handled = False



# Function called when FL Studio is starting

def OnInit():
    print('Loaded MIDI script for Arturia KeyLab Essential 3')
    init()
    time.sleep(2)
    _KLEss3.connexion().DAWConnexion()
    time.sleep(2)
    _KLEss3.Return().init()
    time.sleep(1)
    _KLEss3._paged_display.SetCenterPage(20, line1=ui.getProgTitle(), line2="Connected", icon=eIcons.eFL, transient=1)
    #time.sleep(3)
    #_KLEss3.RefreshMainScreen()
    print("### Messages successfully sent to KeyLab Essential 3 ###")


        
def init() :
    
    # Connxexion
    global _KLEss3 
    _KLEss3 = MidiControllerConfig()
    global _processor
    _processor = KLEssMidiProcessor(_KLEss3) 
    print("### Successfully created class objects ###")

    
    
# Handles the script when FL Studio closes

def OnDeInit():
    # Deconnxexion

    _KLEss3._paged_display.SetCenterPage(20, line1="KeyLab Essential mk3", line2="Disconnected", icon=eIcons.eFL, transient=1)
    _KLEss3.connexion().DAWDisconnection()
    # _KLEss3.connexion().ArturiaDisconnection()
   
  
# Function called when Play/Pause button is ON

def OnUpdateBeatIndicator(value):
    _KLEss3.Return().ProcessPlayBlink(value)
    _KLEss3.Return().ProcessRecordBlink(value)
 

# Function called at refresh, flag value changes depending on the refresh type 

def OnRefresh(flags) :

    if flags not in [4,4096] :
        _KLEss3.Return().RecordReturn()
        _KLEss3.Return().PlayReturn()
        _KLEss3.Return().LoopReturn()
        _KLEss3.Return().MetronomeReturn()
        _KLEss3.Return().ChannelRackReturn()
        _KLEss3.Return().MixerReturn()
        _KLEss3.Return().BrowserReturn()
        
        
    #_KLEss3.Return().PluginParamReturn()

    #print("flags : ", flags)
    #if flags in [4,256,260,4608] :
    #if flags in [98679, 115063] :
        #_KLEss3.RefreshMainScreen()
        # _KLEss3.Return().ChannelRackReturn()
        # _KLEss3.Return().MixerReturn()
        # _KLEss3.Return().BrowserReturn()
    


# Function called time to time mainly to update the beat indicator

#def OnIdle():
    #_KLEss3.Idle()
    #_mk3.LightReturn().LEDTest()

        

#def OnSysEx(event) :



def OnProjectLoad(status) :
    if status == midi.PL_Start :
        _KLEss3._paged_display.SetCenterPage(10, line1="Loading Project...", transient=1)
    
