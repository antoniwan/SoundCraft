import device
import ui
import time
import transport
import mixer
import channels
import patterns
import plugins

from KLEss3Dispatch import send_to_device
import ArturiaCrossKeyboardKLEss3 as AKLEss3 
import KLEss3Process as KLEss3Pr
import KLEss3Plugin

from Icons import eIcons
from LedIds import eLedIds
import ArturiaCrossKeyboardKLEss3 as AKLEss3


# This class handles visual feedback functions.


WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5



PLUGIN_IS_OPEN = ""


# MAPS

PAD_MAP = [
        0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0A, 0x0B]

        
COLOR_MAP = [
        [0x00, 0x7F, 0x10],
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

class KLEssReturn:

    def __init__(self, paged_display) :
        self._paged_display = paged_display


    def init(self) :

        ### TRANSPORT LED ###
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedStop, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPlay, 0x00, 0x20, 0x00]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedRecord, 0x20, 0x00, 0x00]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedTap, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedRepeat, 0x20, 0x18, 0x00]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedBackward, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedForward, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedMetro, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_1, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_2, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_3, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_4, 0x20, 0x20, 0x20]))

        ### DAW COMMAND LED ###
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedSave, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPunch, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedUndo, 0x20, 0x20, 0x20]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedRedo, 0x00, 0x00, 0x00]))

        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPart, 0x20, 0x20, 0x20]))

        ### PAD LED ###
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad1BankA, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad2BankA, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad3BankA, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad4BankA, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad5BankA, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad6BankA, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad7BankA, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad8BankA, 0x16, 0x16, 0x16]))

        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad1BankB, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad2BankB, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad3BankB, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad4BankB, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad5BankB, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad6BankB, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad7BankB, 0x16, 0x16, 0x16]))
        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPad8BankB, 0x16, 0x16, 0x16]))

        ### Screen content ###
        # active_index = channels.selectedChannel()
        # channel_name = channels.getChannelName(active_index)

        # pattern_number = patterns.patternNumber()
        # pattern_name = patterns.getPatternName(pattern_number)      
        # self._paged_display.SetCenterPage(12, line1='%d - %s' % (active_index + 1, channel_name), line2=pattern_name, hw_value=100, transient=0)



    def MetronomeReturn(self) :
        if ui.isMetronomeEnabled() :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedMetro, 0x7F, 0x7f, 0x7f]))
        else :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedMetro, 0x20, 0x20, 0x20]))
            
    def LoopReturn(self) :
        if ui.isLoopRecEnabled() :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedRepeat, 0x7F, 0x48, 0x00]))
        else :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedRepeat, 0x20, 0x18, 0x00]))


    def RecordReturn(self) :
        if transport.isRecording() :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedRecord, 0x7F, 0x00, 0x00]))
        else :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedRecord, 0x20, 0x00, 0x00]))



    def PlayReturn(self) :
        if mixer.getSongTickPos() != 0 :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPlay, 0x00, 0x7F, 0x00]))
        else :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPlay, 0x00, 0x20, 0x00]))

            

    def ProcessPlayBlink(self, value):
        COLOR_PLAY_ON = bytes([0x04, 0x01, 0x16, eLedIds.eLedPlay, 0x00, 0x7F, 0x00]) 
        COLOR_PLAY_OFF =  bytes([0x04, 0x01, 0x16, eLedIds.eLedPlay, 0x00, 0x20, 0x00]) 
        if value == 0 :
            send_to_device(COLOR_PLAY_OFF)
        else :
            send_to_device(COLOR_PLAY_ON)


    def ProcessRecordBlink(self, value) :
        if transport.isRecording() :            
            COLOR_RECORDING_ON = bytes([0x04, 0x01, 0x16, eLedIds.eLedRecord, 0x7F, 0x00, 0x00]) 
            COLOR_RECORDING_OFF = bytes([0x04, 0x01, 0x16, eLedIds.eLedRecord, 0x20, 0x00, 0x00]) 
            if value == 0 :
                send_to_device(COLOR_RECORDING_OFF)
            else :
                send_to_device(COLOR_RECORDING_ON)

    def IsCustomPart(self) :
        if  AKLEss3.PART_OFFSET != 0 :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPart, 0x7F, 0x7F, 0x7F]))
        else :
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedPart, 0x20, 0x20, 0x20]))


    # def LEDTest(self) :
    #     send_to_device(bytes([0x02, 0x02, 0x16, 0x04, 0x00, 0x00, 0x7f]))
    #     send_to_device(bytes([0x02, 0x02, 0x16, 0x05, 0x00, 0x00, 0x00]))
    #     time.sleep(0.1)
    #     send_to_device(bytes([0x02, 0x02, 0x16, 0x04, 0x00, 0x00, 0x00]))
    #     send_to_device(bytes([0x02, 0x02, 0x16, 0x05, 0x00, 0x00, 0x7f]))
    #     time.sleep(0.1)

    def PluginParamReturn(self):
        if channels.selectedChannel(1) != -1 :
            if plugins.isValid(channels.selectedChannel()) : 
                if plugins.getPluginName(channels.selectedChannel()) in KLEss3Plugin.NATIVE_PLUGIN_LIST :
                    #print("Reresh parameter")
                    parameter, value, mapped = KLEss3Plugin.Plugin(0, 0, 0)


    def BrowserReturn(self) :
        if ui.getFocused(WidBrowser) == True :

            KLEss3Pr.MIXER_MODE = 0

            ### Contextual buttons functions ###
            self._paged_display.SetButton(1, 2, "", eIcons.eSearch)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_1, 0x7F, 0x7F, 0x7F]))
            self._paged_display.SetButton(2, 1, "", eIcons.eMixer)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_2, 0x20, 0x20, 0x20]))


            if ui.isInPopupMenu() :
                self._paged_display.SetCenterPage(11,
                                line1= 'Select an option',
                                transient=0,
                                )
            else :
                self._paged_display.SetCenterPage(11,
                                line1= ui.getFocusedNodeCaption(),
                                transient=0,
                                )

            self._paged_display.SetButton(3, 0, "", eIcons.eBack)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_3, 0x20, 0x20, 0x20]))
            self._paged_display.SetButton(4, 0, "", eIcons.eSelected)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_4, 0x20, 0x20, 0x20]))

            ###

            self._paged_display.SetHeaderPage("Browser")
            self._paged_display.SetFooterPage()



    def MixerReturn(self) :
        if ui.getFocused(WidMixer) == True :

            bankinf = str(1 + AKLEss3.PART_OFFSET*8)
            banksup = str(8 + AKLEss3.PART_OFFSET*8)
            KLEss3Pr.MIXER_MODE = 1


            ### Contextual buttons functions ###
            
            self._paged_display.SetButton(1, 1, "", eIcons.eSearch)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_1, 0x20, 0x20, 0x20]))
            self._paged_display.SetButton(2, 2, "", eIcons.eMixer)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_2, 0x7f, 0x7f, 0x7f]))

            if mixer.isTrackMuted(mixer.trackNumber()) :
                self._paged_display.SetButton(3, 3, "Mute", 0)
                send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_3, 0x7F, 0x00, 0x00]))
            else :
                self._paged_display.SetButton(3, 0, "Mute", 0)
                send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_3, 0x20, 0x00, 0x00]))

            if mixer.isTrackSolo(mixer.trackNumber()) :
                self._paged_display.SetButton(4, 3, "Solo", 0)
                send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_4, 0x00, 0x00, 0x7F]))
            else :
                self._paged_display.SetButton(4, 0, "Solo", 0)
                send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_4, 0x00, 0x00, 0x20]))

            ###

            # if mixer.trackNumber() == 0 :
            #     track = "Master"
            # else :
            track = str(mixer.trackNumber())

            self._paged_display.SetCenterPage(11,
                                line1= track + " - " + mixer.getTrackName(mixer.trackNumber()),
                                #line2= bankinf + " - " + banksup,
                                transient=0,
                                )
            
            self._paged_display.SetHeaderPage("Mixer")
            self._paged_display.SetFooterPage()


    def ChannelRackReturn(self) :
        if ui.getFocused(WidChannelRack) or ui.getFocused(WidPlugin) == True :

            KLEss3Pr.MIXER_MODE = 0


            ### Contextual buttons functions ###
            self._paged_display.SetButton(1, 1, "", eIcons.eSearch)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_1, 0x20, 0x20, 0x20]))
            self._paged_display.SetButton(2, 1, "", eIcons.eMixer)
            send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_2, 0x20, 0x20, 0x20]))

            if ui.getFocused(WidPlugin) == True :
                if plugins.isValid(channels.selectedChannel()) : 
                    if plugins.getPluginName(channels.selectedChannel()) in KLEss3Plugin.NATIVE_PLUGIN_LIST :
                        self._paged_display.SetButton(3, 0, "", eIcons.eLeftArrow)
                        self._paged_display.SetButton(4, 0, "", eIcons.eRightArrow)
                        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_3, 0x20, 0x20, 0x20]))
                        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_4, 0x20, 0x20, 0x20]))
                    else :
                        self._paged_display.SetButton(3, 0, "", eIcons.eNone)
                        self._paged_display.SetButton(4, 0, "", eIcons.eNone)
                        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_3, 0x00, 0x00, 0x00]))
                        send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_4, 0x00, 0x00, 0x00]))
            else :
                self._paged_display.SetButton(3, 0, "", eIcons.eTopBracket)
                self._paged_display.SetButton(4, 0, "", eIcons.eBottomBracket)
                send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_3, 0x20, 0x20, 0x20]))
                send_to_device(bytes([0x04, 0x01, 0x16, eLedIds.eLedContext_4, 0x20, 0x20, 0x20]))
            

            active_index = channels.selectedChannel()
            channel_name = channels.getChannelName(active_index)

            global PLUGIN_IS_OPEN
            if ui.getFocused(WidPlugin) :
                PLUGIN_IS_OPEN = '*'
            else :
                PLUGIN_IS_OPEN = ''

        
            pattern_number = patterns.patternNumber()
            pattern_name = patterns.getPatternName(pattern_number)      

            if active_index != -1 :  
                self._paged_display.SetCenterPage(12, line1='%s%s' % (PLUGIN_IS_OPEN,channel_name), line2=pattern_name, hw_value=100, transient=0)
            else :
                self._paged_display.SetCenterPage(11, line1='No Selection', transient=0)


            self._paged_display.SetHeaderPage("Channel Rack")
            self._paged_display.SetFooterPage()



