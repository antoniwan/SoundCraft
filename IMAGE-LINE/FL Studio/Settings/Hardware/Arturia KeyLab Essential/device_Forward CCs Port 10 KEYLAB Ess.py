# name=Forward CCs Port 10 KEYLAB ESS V2
# receiveFrom=Forward CCsPort 10 KEYLAB ESS

"""
[[
	Surface:	KeyLab Essential 
	Developer:	Farès MEZDOUR
	Version:	Beta 1.0
]]
"""

import ui
import device
import midi
import channels
import device_KeyLabEss as KL
import ArturiaVCOL



class TSimple():

    def OnInit(self):
        KL.init()
        
    def OnMidiIn(self, event) :
    
   
        #VCol Test
        v_collection = False
        string = ui.getFocusedPluginName()
        for i in ArturiaVCOL.V_COL :
            if string == i :
                v_collection = True
        
        
        
        if (event.status == midi.MIDI_CONTROLCHANGE and v_collection == True) or event.status == 224 :
            # Manage Analog Lab Plugin
            
            msg = event.status + (event.data1 << 8) + (event.data2 << 16) + (10 << 24)
            device.forwardMIDICC(msg, 2)
            event.handled = True
        
        # else :
            # Manage Mod wheel

            # KL._processor.FLEX(event, clef = event.controlNum)
            # event.handled = False  

    def OnMidiMsg(self, event):
        if event.status == 153 :
            if KL._processor.ProcessEvent(event):
                event.handled = False 
        event.handled = False 



Simple = TSimple()


def OnInit():
    Simple.OnInit()

def OnDeInit():
    return

def OnMidiMsg(event):
    Simple.OnMidiMsg(event)

def OnMidiIn(event):
    Simple.OnMidiIn(event)
    
def OnPitchBend(event) :
    channels.setChannelPitch(channels.channelNumber(),(100/64)*event.data2-100,1)
    event.handled = True


