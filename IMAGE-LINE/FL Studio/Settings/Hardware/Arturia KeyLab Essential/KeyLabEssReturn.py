import device
import ui
import time
import transport
import mixer
import channels
from KeyLabEssDispatch import send_to_device 


# This class handles visual feedback functions.

# MAPS

PAD_MAP = [
        0x70, 0x71, 0x72, 0x73,
        0x74, 0x75, 0x76, 0x77]
        
COLOR_MAP = [
        [0x7F, 0x00, 0x00], # RED
        [0x00, 0x00, 0x7F], # GREEN
        [0x00, 0x7F, 0x00], #BLUE
        [0x7F, 0x00, 0x7F], # YELLOW
        [0x00, 0x7F, 0x7F], # CYAN
        [0x7F, 0x7F, 0x00]] # MAGENTA

SELECT_MAP = [0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29]

class KeyLabEssLightReturn:

    def init(self) :
        
        for i in range(0,8) :
            send_to_device(bytes([0x02, 0x00, 0x16, PAD_MAP[i], 0x00, 0x00, 0x00, 0x7F]))
        
        for j in range(len(COLOR_MAP)) :
            
            colour = COLOR_MAP[j]
            
            for i in range(0,8) :
                time.sleep(0.02)
                send_to_device(bytes([0x02, 0x00, 0x16, PAD_MAP[i], colour[0], colour[1], colour[2], 0x7F]))
                
            for i in range(0,8) :
                time.sleep(0.02)
                send_to_device(bytes([0x02, 0x00, 0x16, PAD_MAP[i], 0x00, 0x00, 0x00, 0x7F]))
        
        time.sleep(0.5)
        for i in range(0,8) :
            send_to_device(bytes([0x02, 0x00, 0x16, PAD_MAP[i], 0x7F, 0x7F, 0x7F, 0x7F]))
        time.sleep(0.5)
        for i in range(0,8) :
            send_to_device(bytes([0x02, 0x00, 0x16, PAD_MAP[i], 0x00, 0x00, 0x00, 0x00]))   

    def MetronomeReturn(self) :
        if ui.isMetronomeEnabled() :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x59, 0x7F])) # METRO
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x59, 0x00])) # METRO
            
    def CountdownReturn(self) :
        if ui.isPrecountEnabled() :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x56, 0x7F]))
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x56, 0x00]))

    def RecordReturn(self) :
        if transport.isRecording() :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5F, 0x7F])) # RECORD
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5F, 0x00])) # RECORD

    def PlayReturn(self) :
        if mixer.getSongTickPos() != 0 :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5E, 0x7F])) # PLAY
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5D, 0x00])) # STOP
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5E, 0x00])) # PLAY
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5D, 0x7F])) # STOP
            
    def LoopReturn(self) :
        if ui.isLoopRecEnabled() :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5A, 0x7F])) # LOOP
        else :
            send_to_device(bytes([0x02, 0x00, 0x10, 0x5A, 0x00])) # LOOP
           

    # def IsChannelSolo(self) :
        # if channels.isChannelSolo(channels.channelNumber()) :
            # send_to_device(bytes([0x02, 0x00, 0x10, 0x1A, 0x7F])) # PART1/NEXT          
        # else :
            # send_to_device(bytes([0x02, 0x00, 0x10, 0x1A, 0x00])) # PART1/NEXT
    
 
    # def IsChannelMuted(self) :
        # if channels.isChannelMuted(channels.channelNumber()):
            # send_to_device(bytes([0x02, 0x00, 0x10, 0x1B, 0x7F])) # PART2/PREV
        # else :
            # send_to_device(bytes([0x02, 0x00, 0x10, 0x1B, 0x00])) # PART2/PREV


    def ProcessPlayBlink(self, value):
        COLOR_PLAY_ON = bytes([0x02, 0x00, 0x10, 0x5E, 0x7F]) # PLAY
        COLOR_PLAY_OFF = bytes([0x02, 0x00, 0x10, 0x5E, 0x00]) # PLAY
        if value == 0 :
            send_to_device(COLOR_PLAY_OFF)
        else :
            send_to_device(COLOR_PLAY_ON)
        
    def ProcessRecordBlink(self, value) :
        if transport.isRecording() :            
            COLOR_RECORDING_ON = bytes([0x02, 0x00, 0x10, 0x5F, 0x7F]) # RECORD
            COLOR_RECORDING_OFF = bytes([0x02, 0x00, 0x10, 0x5F, 0x00]) # RECORD
            if value == 0 :
                send_to_device(COLOR_RECORDING_OFF)
            else :
                send_to_device(COLOR_RECORDING_ON)

    def NotBlinkingLed(self) :
    
        # DAW CONTROL LED
    
        send_to_device(bytes([0x02, 0x00, 0x10, 0x57, 0x7F])) # UNDO
        send_to_device(bytes([0x02, 0x00, 0x10, 0x58, 0x7F])) # PUNCH
        send_to_device(bytes([0x02, 0x00, 0x10, 0x5B, 0x7F])) # <<
        send_to_device(bytes([0x02, 0x00, 0x10, 0x5C, 0x7F])) # >>
        # send_to_device(bytes([0x02, 0x00, 0x10, 0x1C, 0x7F])) # LIVE/BANK
        # send_to_device(bytes([0x02, 0x00, 0x10, 0x56, 0x7F])) # LIVE/BANK

        
        # CENTER LED
        
        send_to_device(bytes([0x02, 0x00, 0x10, 0x18, 0x7F])) # <-
        send_to_device(bytes([0x02, 0x00, 0x10, 0x19, 0x7F])) # ->
 
