import device
import ui
import time
import transport
import mixer
from MiniLabmk2Dispatch import send_to_device 


# This class handles visual feedback functions.


WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5


class MiniLabLightReturn:

    

    def MetronomeReturn(self) :
        if ui.isMetronomeEnabled() :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7C, 0x05]))
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7C, 0x00]))
            
    def LoopReturn(self) :
        if ui.isLoopRecEnabled() :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7E, 0x11]))
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7E, 0x00]))


    def RecordReturn(self) :
        if transport.isRecording() :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7A, 0x01]))
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7A, 0x00]))


    def PlayReturn(self) :
        if mixer.getSongTickPos() != 0 :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x78, 0x04]))
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x78, 0x00]))
    
    
    def BrowserReturn(self) :
        if ui.getFocused(WidBrowser) == True :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7F, 0x7F]))
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x7F, 0x00]))
            

    def ProcessPlayBlink(self, value):
        COLOR_PLAY_ON = bytes([0x02, 0x00, 0x10, 0x78, 0x04]) 
        COLOR_PLAY_OFF = bytes([0x02, 0x00, 0x10, 0x78, 0x00])
        if value == 0 :
            send_to_device(COLOR_PLAY_OFF)
        else :
            send_to_device(COLOR_PLAY_ON)
        
    def ProcessRecordBlink(self, value) :
        if transport.isRecording() :            
            COLOR_RECORDING_ON = bytes([0x02, 0x00, 0x10, 0x7A, 0x01]) 
            COLOR_RECORDING_OFF = bytes([0x02, 0x00, 0x10, 0x7A, 0x00])
            if value == 0 :
                send_to_device(COLOR_RECORDING_OFF)
            else :
                send_to_device(COLOR_RECORDING_ON)
   
   
    def NotBlinkingLed(self) :
        
        send_to_device(bytes([0x02, 0x00, 0x10, 0x79, 0x10]))
        send_to_device(bytes([0x02, 0x00, 0x10, 0x7D, 0x11]))
        send_to_device(bytes([0x02, 0x00, 0x10, 0x7B, 0x05]))

 
