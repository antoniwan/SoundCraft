import device
import ui
import time
import transport
import mixer
import channels
import patterns
import plugins
import utils
import midi
import playlist
import general

from KL3Dispatch import send_to_device
import ArturiaCrossKeyboardKL3 as AKL3 
import KL3Process as PR
import KL3Plugin as PL

# from Icons import eIcons
from LedId import eLedId
from IntegrationPatchId import eIntegrationPatchId
from ParamId import eParamId
from images_sub_enums import eSmallIcon
from images_sub_enums import eCenterIcon

# This class handles visual feedback functions.


WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5

ANALOG_LAB_BLUE = [0, 108, 122]
WHITE = [127, 127, 127]

CURRENT_STEP = 0
CURRENT_TIMELINE_BAR = 0
CURRENT_TIMELINE_STEP = 0 
IS_TIMELINE_DISPLAYED = 0

PLUGIN_IS_OPEN = ""


# MAPS

PAD_MAP = [
        eLedId.ePad1BankDaw, eLedId.ePad2BankDaw, eLedId.ePad3BankDaw, eLedId.ePad4BankDaw,
        eLedId.ePad5BankDaw, eLedId.ePad6BankDaw, eLedId.ePad7BankDaw, eLedId.ePad8BankDaw]

        
COLOR_MAP = [
        [0x00, 0x7F, 0x0d],
        [0x00, 0x7F, 0x19],
        [0x00, 0x7F, 0x32],
        [0x00, 0x7F, 0x4B],
        [0x00, 0x7F, 0x64],
        [0x00, 0x7F, 0x7F],
        [0x00, 0x64, 0x7F],
        [0x00, 0x4B, 0x7F],
        [0x00, 0x32, 0x7F],
        [0x00, 0x19, 0x7F],
        [0x00, 0x00, 0x7F],
        [0x19, 0x00, 0x7F],
        [0x32, 0x00, 0x7F],
        [0x4B, 0x00, 0x7F],
        [0x64, 0x00, 0x7F],
        [0x7F, 0x00, 0x7F],
        [0x7F, 0x00, 0x64],
        [0x7F, 0x00, 0x4B],
        [0x7F, 0x00, 0x32],
        [0x7F, 0x00, 0x19],
        [0x7F, 0x00, 0x00],
        [0x7F, 0x19, 0x00],
        [0x7F, 0x32, 0x00],
        [0x7F, 0x4B, 0x00],
        ]

WHITE_DEFAULT = 16777215


class Return:

    def __init__(self, paged_display) :
        self._paged_display = paged_display

        self._last_line1 = ""
        self._last_line2 = ""


    def init(self) :


        ### TRANSPORT LED ###
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eStop, 0x0d, 0x0d, 0x0d, 0x00])) #Stop
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePlay, 0x00, 0x0d, 0x00, 0x00])) 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRecord, 0x0d, 0x00, 0x00, 0x00])) 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eTap, 0x0d, 0x0d, 0x0d, 0x00])) 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRepeat, 0x0d, 0x0a, 0x00, 0x00])) #Loop
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eBackward, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eForward, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eMetronome, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual1, 0x0d, 0x0d, 0x0d, 0x00])) #context 1
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual2, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual3, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual4, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eBack, 0x0d, 0x0d, 0x0d, 0x00])) #back LED
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual5, 0x0d, 0x0d, 0x0d, 0x00])) #context 5
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual6, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual7, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eContextual8, 0x0d, 0x0d, 0x0d, 0x00]))

        ### DAW COMMAND LED ###
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eSave, 0x0d, 0x0d, 0x0d, 0x00])) #Save
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eQuantize, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eUndo, 0x0d, 0x0d, 0x0d, 0x00]))
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRedo, 0x0d, 0x0d, 0x0d, 0x00]))

        ### PAD LED ###
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad1BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad1BankA 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad2BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad2BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad3BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad3BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad4BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad4BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad5BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad5BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad6BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad6BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad7BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad7BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad8BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad8BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad9BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad9BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad10BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad10BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad11BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad11BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad12BankA, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad12BankA
        
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad1BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad1BankB
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad2BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad2BankB 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad3BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad3BankB 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad4BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad4BankB 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad5BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad5BankB 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad6BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad6BankB 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad7BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad7BankB 
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad8BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad8BankB
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad9BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad9BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad10BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad10BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad11BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad11BankA
        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad12BankB, 0x00, 0x00, 0x0d, 0x00])) #eLedId.ePad12BankA

        send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eProperties, 0x14, 0x02, 0x01, 0x00])) # Pad MIDI Port






    def MetronomeReturn(self) :

        if ui.isMetronomeEnabled() :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eMetronome, 0x7F, 0x7F, 0x7F, 0x00]))
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eMetronome, 0x0d, 0x0d, 0x0d, 0x00]))


            
    def LoopReturn(self) :
        if ui.isLoopRecEnabled() :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRepeat, 0x7F, 0x48, 0x00, 0x00]))
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRepeat, 0x0d, 0x0a, 0x00, 0x00]))


    def RecordReturn(self) :
        if transport.isRecording() :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRecord, 0x7F, 0x00, 0x00, 0x00]))
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRecord, 0x0d, 0x00, 0x00, 0x00]))



    def PlayReturn(self) :
        if mixer.getSongTickPos() != 0 :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePlay, 0x00, 0x7F, 0x00, 0x00]))
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePlay, 0x00, 0x0d, 0x00, 0x00]))

    def UndoHistoryReturn(self) :
        if general.getUndoHistoryLast() == (general.getUndoHistoryCount() - 1) :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eUndo, 0x00, 0x00, 0x00, 0x00]))
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eRedo, 0x0d, 0x0d, 0x0d, 0x00]))
        elif general.getUndoHistoryLast() == 0 :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eUndo, 0x0d, 0x0d, 0x0d, 0x00]))
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eRedo, 0x00, 0x00, 0x00, 0x00]))
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eUndo, 0x0d, 0x0d, 0x0d, 0x00]))
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eRedo, 0x0d, 0x0d, 0x0d, 0x00]))

    def BackReturn(self) :
        if ui.getFocused(WidPlugin) :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eBack, 0x0d, 0x0d, 0x0d, 0x00]))
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eBack, 0x00, 0x00, 0x00, 0x00]))


    def DrumrackReturn(self) :

        if channels.selectedChannel(1) != -1 :
            if plugins.isValid(channels.selectedChannel()) : 
                if plugins.getPluginName(channels.selectedChannel()) == "FPC" :
                    for i in range(12) :
                        color = getPadColor(i)
                        send_to_device(bytes([0x02, eIntegrationPatchId.eDaw, eParamId.eSetLed, (eLedId.ePad9BankA + i) - (8*(i//4)), color[0], color[1], color[2], 0x00]))
                else :
                    SetDrumrackDefaultColor()
            else :
                SetDrumrackDefaultColor()


                        
    
    def SequencerReturn(self) :
        for j in range(PR.SEQUENCER_PAGE_NUMBER) :
            if j != PR.SEQUENCER_PAGE :
                send_to_device(bytes([0x02, eIntegrationPatchId.eDaw, eParamId.eSetLed, PR.PAD_MATRIX[j+8], 0x0d, 0x05, 0x00, 0x00]))
            else :
                send_to_device(bytes([0x02, eIntegrationPatchId.eDaw, eParamId.eSetLed, PR.PAD_MATRIX[j+8], 0x64, 0x32, 0x00, 0x00]))

        for i in range (len(PAD_MAP)) :
            if channels.getGridBit(channels.selectedChannel(),i+(8*PR.SEQUENCER_PAGE)) == 1 :
                bit_velocity = channels.getCurrentStepParam(channels.selectedChannel(), i+(8*PR.SEQUENCER_PAGE), 1)
                if bit_velocity != -1 : 
                    send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, PR.PAD_MATRIX[i], bit_velocity, bit_velocity, bit_velocity, 0x00]))
            else :
                send_to_device(bytes([0x02, eIntegrationPatchId.eDaw, eParamId.eSetLed, PR.PAD_MATRIX[i], 0x01, 0x01, 0x01, 0x00]))

            

    def ProcessPlayBlink(self, value):
        COLOR_PLAY_ON = bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePlay, 0x00, 0x7F, 0x00, 0x00]) 
        COLOR_PLAY_OFF =  bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePlay, 0x00, 0x0d, 0x00, 0x00]) 
        if value == 0 :
            send_to_device(COLOR_PLAY_OFF)
        else :
            send_to_device(COLOR_PLAY_ON)


    def ProcessRecordBlink(self, value) :
        if transport.isRecording() :            
            COLOR_RECORDING_ON = bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRecord, 0x7F, 0x00, 0x00, 0x00]) 
            COLOR_RECORDING_OFF = bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.eRecord, 0x0d, 0x00, 0x00, 0x00]) 
            if value == 0 :
                send_to_device(COLOR_RECORDING_OFF)
            else :
                send_to_device(COLOR_RECORDING_ON)

    
    def ProcessSequencerBlink(self, value) :
        global CURRENT_STEP
        

    def IdleSequencer(self) :
        global CURRENT_STEP
        new_step = mixer.getSongStepPos()
        if new_step != CURRENT_STEP :
            self.SequencerReturn()
            CURRENT_STEP = new_step
            if CURRENT_STEP in range (PR.SEQUENCER_PAGE*8,8+PR.SEQUENCER_PAGE*8) :
                send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eSetLed, PAD_MAP[CURRENT_STEP%8], 0x0d, 0x05, 0x00, 0x00]))
        
    
    
    
    def isTimelineDisplayed(self, value) :
        global IS_TIMELINE_DISPLAYED
        
        IS_TIMELINE_DISPLAYED = value
    
    def IdleTimeline(self) :
        
        global CURRENT_TIMELINE_BAR
        global CURRENT_TIMELINE_STEP

        CURRENT_TIMELINE_BAR = str(playlist.getVisTimeBar() + 1) 
        CURRENT_TIMELINE_STEP = str(playlist.getVisTimeStep() + 1)

        if IS_TIMELINE_DISPLAYED :
        
            self._paged_display.SetCenterPage(
                24,
                line1="Track Position",
                colortype1= 1,
                color1= ANALOG_LAB_BLUE,
                line2= 'Bar '+ CURRENT_TIMELINE_BAR + ' Step ' + CURRENT_TIMELINE_STEP,
                colortype2= 1,
                color2= WHITE,
            )



    def PluginParamReturn(self):
        if channels.selectedChannel(1) != -1 :
            if plugins.isValid(channels.selectedChannel()) : 
                if plugins.getPluginName(channels.selectedChannel()) in PL.NATIVE_PLUGIN_LIST :
                    parameter, value, mapped = PL.Plugin(0, 0, 0)


    def MixerReturn(self) :
        
        if ui.getFocused(WidMixer) == True :

            PR.MIXER_MODE = 1


            ### Contextual buttons functions ###
            
            # 1 #
            self._paged_display.SetButton(4, 4, 1, 1, None, WHITE, "PLUGIN", "")
            
            # 2 #
            self._paged_display.SetButton(5, 6, 1,  1, None, WHITE, "MIXER", "")
            
            # 3 #
            self._paged_display.SetButton(6, 0, 1, 1, None, WHITE, "", "")

            # 4 #
            self._paged_display.SetButton(7, 0, 1, 1, None, WHITE, "", "")
            
            # 5 #
            if mixer.isTrackMuted(mixer.trackNumber()) :
                self._paged_display.SetButton(0, 11, 1, 1, eSmallIcon.ekPictosButtonMuteDefault_image, [16, 16, 16], "", "")
            else :
                self._paged_display.SetButton(0, 10, 1, 1, eSmallIcon.ekPictosButtonMuteDefault_image, WHITE, "", "")

            # 6 #
            if mixer.isTrackSolo(mixer.trackNumber()) :
                self._paged_display.SetButton(1, 11, 1, 1, eSmallIcon.ekPictosButtonSoloDefault_image, [0, 127, 0], "", "")
            else :
                self._paged_display.SetButton(1, 10, 1, 1, eSmallIcon.ekPictosButtonSoloDefault_image, WHITE, "", "")
                
            # 7 #
            self._paged_display.SetButton(2, 0, 1, 1, None, WHITE, "", "")


            # 8 #          
            if mixer.isTrackArmed(mixer.trackNumber()) :
                self._paged_display.SetButton(3,11, 1, 1, eSmallIcon.ekPictosButtonArmedAudioDefault_image, [127, 0, 0], "", "")
            else :
                self._paged_display.SetButton(3, 10, 1, 1, eSmallIcon.ekPictosButtonArmedAudioDefault_image, WHITE, "", "")


            ###

            track = str(mixer.trackNumber())
            active_index = mixer.trackNumber()

            # This was an intent to screen filtering priority
            # if track != self._last_line1 :

            #     self._last_line1 = track

            self._paged_display.SetCenterPage(
                11,
                line1= track + " - " + mixer.getTrackName(mixer.trackNumber()),
                colortype1=1,
                color1=get_track_color(active_index),
            )
            
            self._paged_display.RefreshAllCTXButtons()


    def ChannelRackReturn(self) :
        
        if ui.getFocused(WidChannelRack) or ui.getFocused(WidPlugin) == True :

            PR.MIXER_MODE = 0
            PR.FOCUSED_WINDOW = WidChannelRack


            ### Contextual buttons functions ###
        
            # 1 #
            self._paged_display.SetButton(4, 6, 1, 1, None, WHITE, "PLUGIN", "")

            # 2 #
            self._paged_display.SetButton(5, 4, 1, 1, None, WHITE, "MIXER", "")
            

            # 3/4 #
            if ui.getFocused(WidPlugin) == True : # Manage arrow icon for Stock plugins
                
                global PLUGIN_IS_OPEN
                PLUGIN_IS_OPEN = '*'
           
                if plugins.isValid(channels.selectedChannel()) : 
                    if plugins.getPluginName(channels.selectedChannel()) in PL.NATIVE_PRESET_CONTROLLABLE_PLUGIN_LIST :
                        self._paged_display.SetButton(6, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowLeft_image, WHITE, "", "")
                        self._paged_display.SetButton(7, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowRight_image, WHITE, "", "")

                    else :
                        self._paged_display.SetButton(6, 0, 2, 1, None, WHITE, "", "")
                        self._paged_display.SetButton(7, 0, 2, 1, None, WHITE, "", "")

            else :
                
                PLUGIN_IS_OPEN = ''
                
                if patterns.patternNumber() == 1 :
                    self._paged_display.SetButton(6, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowDefault_image, [32, 32, 32], "", "")
                    self._paged_display.SetButton(7, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowDown_image, WHITE, "", "")
                elif patterns.patternNumber() == patterns.patternMax() :
                    self._paged_display.SetButton(6, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowDefault_image, WHITE, "", "")
                    self._paged_display.SetButton(7, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowDown_image, [32, 32, 32], "", "")
                else :
                    self._paged_display.SetButton(6, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowDefault_image, WHITE, "", "")
                    self._paged_display.SetButton(7, 10, 2, 1, eSmallIcon.ekPictosBrowsingArrowDown_image, WHITE, "", "")
                    
            
            # 5 #
            if mixer.isTrackMuted(mixer.trackNumber()) :
                self._paged_display.SetButton(0, 11, 1, 1, eSmallIcon.ekPictosButtonMuteDefault_image, [16, 16, 16], "", "")
            else :
                self._paged_display.SetButton(0, 10, 1, 1, eSmallIcon.ekPictosButtonMuteDefault_image, WHITE, "", "")

            # 6 #
            if mixer.isTrackSolo(mixer.trackNumber()) :
                self._paged_display.SetButton(1, 11, 1, 1, eSmallIcon.ekPictosButtonSoloDefault_image, [0, 127, 0], "", "")
            else :
                self._paged_display.SetButton(1, 10, 1, 1, eSmallIcon.ekPictosButtonSoloDefault_image, WHITE, "", "")

            # 7 #
            self._paged_display.SetButton(2, 0, 1, 1, None, WHITE, "", "")


            # 8 #          
            if mixer.isTrackArmed(mixer.trackNumber()) :
                self._paged_display.SetButton(3,11, 1, 1, eSmallIcon.ekPictosButtonArmedAudioDefault_image, [127, 0, 0], "", "")
            else :
                self._paged_display.SetButton(3, 10, 1, 1, eSmallIcon.ekPictosButtonArmedAudioDefault_image, WHITE, "", "")
                
            ###
                

            active_index = channels.selectedChannel()
            channel_name = channels.getChannelName(active_index)
            
 
            pattern_number = patterns.patternNumber()
            pattern_name = patterns.getPatternName(pattern_number)
            DEFAULT_PATTERN_NAME = ("Pattern " + str(pattern_number))  
            if pattern_name == DEFAULT_PATTERN_NAME :
                pattern_name = str(pattern_number)

            
            # This was an intent to screen filtering priority
                
            # if channel_name != self._last_line1 or pattern_name != self._last_line2 :

            #     self._last_line1 = channel_name
            #     self._last_line2 = pattern_name
                
            
            if active_index != -1 :  
                self._paged_display.SetCenterPage(
                    13, 
                    line1='%s%s' % (PLUGIN_IS_OPEN,channel_name),
                    colortype1=1, 
                    color1=get_channel_color(active_index),
                    line2= '%s%s' % ("Pattern ", pattern_name),
                    colortype2=1, 
                    color2=get_pattern_color(pattern_number),
                    )
            else :
                self._paged_display.SetCenterPage(
                    10, 
                    line1='No Selection', 
                    colortype1=0,
                    color1=[0, 0, 0]
                        )


            self._paged_display.RefreshAllCTXButtons()



### UTILITY ###


def get_channel_color(channel) :
    RGB_color = utils.ColorToRGB(channels.getChannelColor(channel))
    NEW_color = [0, 0, 0]
    for i in range(3) :
        NEW_color[i] = RGB_color[i]//2

    return NEW_color

def get_track_color(track) :
    RGB_color = utils.ColorToRGB(mixer.getTrackColor(track))
    NEW_color = [0, 0, 0]
    for i in range(3) :
        NEW_color[i] = RGB_color[i]//2

    return NEW_color

def get_pattern_color(pattern) :
    RGB_color = utils.ColorToRGB(patterns.getPatternColor(pattern))
    NEW_color = [0, 0, 0]
    if RGB_color == (35, 37, 45) :
        NEW_color = WHITE
    else :       
        for i in range(3) :
            NEW_color[i] = RGB_color[i]//2

    return NEW_color

def getPadColor(pad) :
    RGB_color = utils.ColorToRGB(plugins.getPadInfo(channels.selectedChannel(), -1, 2, pad))
    NEW_color = [0, 0, 0]
    for i in range(3) :
        NEW_color[i] = RGB_color[i]//2

    return NEW_color


def SetDrumrackDefaultColor() :
    for i in range(12) :
        send_to_device(bytes([0x02, eIntegrationPatchId.eDaw, eParamId.eSetLed, eLedId.ePad1BankA + i, 0x0d, 0x0d, 0x0d, 0x00]))