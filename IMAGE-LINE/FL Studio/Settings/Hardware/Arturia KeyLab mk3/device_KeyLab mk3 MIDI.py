# name=KeyLab mk3 Arturia

"""
[[
	Surface:	KeyLab mkII MIDI
	Developer:	Farès MEZDOUR
	Version:	1.0
]]
"""

# This script allows the KeyLab mk3 to communicate with Arturia Software
# by forwarding CCs to port 10

import ui
import midi
import device
import ArturiaVCOL
import device_KL3 as KL
import channels



class TSimple():

        
    def OnMidiMsg(self, event) :


        if (event.status == midi.MIDI_CONTROLCHANGE) :    
            
            # Manage Analog Lab Plugin
            
            msg = event.status + (event.data1 << 8) + (event.data2 << 16) + (10 << 24)
            device.forwardMIDICC(msg, 2)                    
            event.handled = False

Simple = TSimple()

def OnMidiMsg(event):
    Simple.OnMidiMsg(event)
    