import channels
import mixer
import patterns
import transport
import ui
import device
import plugins
import midi

import KLEss3Plugin
import ArturiaCrossKeyboardKLEss3 as AKLEss3

from KLEss3Dispatch import MidiEventDispatcher
from KLEss3Navigation import NavigationMode
from KLEss3Connexion import KLEssConnexion
from KLEss3Dispatch import send_to_device

from Patch import ePatch
from LedIds import eLedIds

import ArturiaVCOL



# This class processes all CC coming from the controller
# The class creates new handler for each function
# The class calls the right fonction depending on the incoming CC


## CONSTANT

PORT_MIDICC_ANALOGLAB = 10
WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5
WidPluginEffect = 6
WidPluginGenerator = 7


# Event code indicating stop event
SS_STOP = 0

# Event code indicating start start event
SS_START = 2

# MIXER
MIXER_MODE = 0

# Part State
PART_STATE = 0

# When part is pressed
IS_PART_PRESSED = 0

#When the user selects a custom part
IS_CUSTOM_PART = 0




ANALOGLAB_ID = (
                1,
                16,
                17,
                18,
                19,
                30,
                31,
                52,
                54,
                55,
                71,
                72,
                73,
                74,
                75,
                76,
                77,
                79,
                80,
                81,
                82,
                83,
                85,
                86,
                87,
                89,
                90,
                93,
                114,
                115
                )


KNOB_ID = (
            96,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            )

FADER_ID = (
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            )


PAD_MATRIX = [        
        eLedIds.eLedPad5BankA, eLedIds.eLedPad6BankA, eLedIds.eLedPad7BankA, eLedIds.eLedPad8BankA,
        eLedIds.eLedPad1BankA, eLedIds.eLedPad2BankA, eLedIds.eLedPad3BankA, eLedIds.eLedPad4BankA,       
        eLedIds.eLedPad5BankB, eLedIds.eLedPad6BankB, eLedIds.eLedPad7BankB, eLedIds.eLedPad8BankB,
        eLedIds.eLedPad1BankB, eLedIds.eLedPad2BankB, eLedIds.eLedPad3BankB, eLedIds.eLedPad4BankB,
]

PAD_MATRIX_STATE = [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0
]

                    

# FPC MAP
FPC_MAP = {
            "36":37,
            "37":36,
            "38":42,
            "39":54,
            "40":40,
            "41":38,
            "42":46,
            "43":44,
            
            
            "44":48,
            "45":47,
            "46":45,
            "47":43,
            "48":49,
            "49":55,
            "50":51,
            "51":53,
            
            }


class KLEssMidiProcessor:
    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, KLEss3):
        def by_midi_id(event) : return event.midiId
        def by_control_num(event) : return event.controlNum
        def by_velocity(event) : return event.data2
        def by_status(event) : return event.status
        def ignore_release(event): return self._is_pressed(event)
        def ignore_press(event): return not self._is_pressed(event)

        self._KLEssmk3 = KLEss3

        self._midi_id_dispatcher = (
            MidiEventDispatcher(by_midi_id)
            .NewHandler(176, self.OnCommandEvent)
            .NewHandler(224, self.OnWheelEvent)
            )
        
        self._midi_command_dispatcher = (
            MidiEventDispatcher(by_control_num)
            
            # MAPPING PAD
            
            .NewHandler(21, self.Start, ignore_press)
            .NewHandler(20, self.Stop)
            .NewHandler(22, self.Record, ignore_press)
            .NewHandler(23, self.TapTempo)
            .NewHandler(27, self.SetClick, ignore_press)
            .NewHandler(24, self.Loop, ignore_press)
            .NewHandler(25, self.Rewind)
            .NewHandler(26, self.FastForward)
            .NewHandler(40, self.Save, ignore_release)
            .NewHandler(41, self.Quantize, ignore_release)
            .NewHandler(42, self.Undo, ignore_release)
            #.NewHandler(43, self.Redo, ignore_release)
            .NewHandler(117, self.SwitchWindow, ignore_release)
            .NewHandler(116, self.OnKnobEvent)
            .NewHandler(44, self.Context1)
            .NewHandler(45, self.Context2)
            .NewHandler(46, self.Context3)
            .NewHandler(47, self.Context4)
            #.NewHandler(27, self.ShiftOn)
            .NewHandler(119, self.PartOn)

            
            
            # MAPPING KNOBS
            
            .NewHandler(113, self.SetVolumeMasterTrack)
            .NewHandler(104, self.SetPanMasterTrack)
            .NewHandlerForKeys(ANALOGLAB_ID, self.ForwardAnalogLab)
            .NewHandlerForKeys(KNOB_ID, self.KnobProcess)
            .NewHandlerForKeys(FADER_ID, self.FaderProcess)
            .NewHandler(1, self.OnWheelEvent)            
            
        )
        
        self._knob_dispatcher = (
            MidiEventDispatcher(by_velocity)
            .NewHandlerForKeys(range(65,73), self.Navigator)
            .NewHandlerForKeys(range(55,64), self.Navigator)
        )
        
        
            # NAVIGATION
        
        self._navigation = NavigationMode(self._KLEssmk3.paged_display())



    # DISPATCH



    def ProcessEvent(self, event) :
        if event.status in [154,138] :
            return self.OnDrumEvent(event)
        else :
            #print(event.status,"\t",event.data1,"\t",event.controlNum,"\t",event.data2,"\t",event.midiId)
            #print("Mixer :", ui.getFocused(0))
            #print("CR :", ui.getFocused(1))
            #print("Playlist :", ui.getFocused(2))
            #print("Piano Roll :", ui.getFocused(3))
            #print("Browser :", ui.getFocused(4))
            #print("Plugin :", ui.getFocused(5))
            #print("Effect :", ui.getFocused(6))
            #print("Instrument :", ui.getFocused(7))
            return self._midi_id_dispatcher.Dispatch(event)

            


    def OnCommandEvent(self, event):
        self._midi_command_dispatcher.Dispatch(event)

    def OnWheelEvent(self, event):
        if channels.selectedChannel(1) != -1 :
            if plugins.isValid(channels.selectedChannel()) : 
                if plugins.getPluginName(channels.selectedChannel()) not in ArturiaVCOL.V_COL :
                    if event.status == midi.MIDI_PITCHBEND :
                        channels.setChannelPitch(channels.selectedChannel(),(event.data2-64)*(100/64)*channels.getChannelPitch(channels.selectedChannel(),2),1) # SMALL RANGE
                    #channels.setChannelPitch(channels.selectedChannel(),round(18.75 * event.data2 - 1200),1) #FULL RANGE     
                    else:
                        pass
                else :
                    device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        # self._wheel_dispatcher.Dispatch(event)

    def OnKnobEvent(self, event):
        self._knob_dispatcher.Dispatch(event)

    def OnDrumEvent(self, event) :
        index = event.data1 
        if event.status == 154 :
            self.PadOn(index)
            event.data1 = FPC_MAP.get(str(event.data1))
        elif event.status == 138 : 
            self.PadOff(index)
            event.data1 = FPC_MAP.get(str(event.data1))
        event.handled = False

    # WINDOW



    def _show_and_focus(self, window):
        if not ui.getVisible(window):
            ui.showWindow(window)
        if not ui.getFocused(window):
            ui.setFocused(window)
  
  
    def _hideAll(self, event) :
        for i in range (channels.channelCount()) :
            channels.showEditor(i,0)


    def SwitchWindow(self, event) :
        if ui.getFocused(WidChannelRack) :
            self.showPlugin(event)
        elif ui.getFocused(WidPlugin) :
            self.showPlugin(event)
        elif ui.getFocused(WidMixer) :
            mixer.armTrack(mixer.trackNumber())
            plugin = channels.selectedChannel()
            #for i in range(plugins.getParamCount(plugin)) :
                #print(i, plugins.getPluginName(channels.selectedChannel()),plugins.getParamName(i,plugin), plugins.getParamValue(i,plugin))
        elif ui.getFocused(WidBrowser) :
            self.FakeMIDImsg()
            nodeFileType = ui.getFocusedNodeFileType()
            if nodeFileType == -1:
                return
            if nodeFileType <= -100:
                transport.globalTransport(midi.FPT_Enter, 1)
                #transport.globalTransport(midi.FPT_Down, 1) -- Increase 1 item for navigation
            else:
                ui.selectBrowserMenuItem()
                if not ui.isInPopupMenu() :
                    self._navigation.PressRefresh()
                else :
                    transport.globalTransport(midi.FPT_Yes, 1)
                    self._show_and_focus(WidPluginGenerator)

                    
        



    # NAVIGATION



    def ToggleBrowserChannelRack(self, event) :
        self.FakeMIDImsg()
        global MIXER_MODE
        if ui.getFocused(WidBrowser) != True :
            MIXER_MODE = 0
            self._hideAll(event)
            self._show_and_focus(WidBrowser)
            #self._navigation.BrowserRefresh()
        else :
            self._hideAll(event)
            self._show_and_focus(WidChannelRack)
            #self._navigation.ChannelRackRefresh()

    def ToggleMixerChannelRack(self, event) :
        self.FakeMIDImsg()
        self._hideAll(event)
        global MIXER_MODE
        if MIXER_MODE == 0 :
            MIXER_MODE = 1
            self._show_and_focus(WidMixer)
            #self._navigation.MixerRefresh()
        else :
            MIXER_MODE = 0
            self._show_and_focus(WidChannelRack)
            #self._navigation.ChannelRackRefresh()

            
    def TogglePlaylistChannelRack(self, event) :
        self.FakeMIDImsg()
        if ui.getFocused(WidPlaylist) != True :
            self._hideAll(event)
            self._show_and_focus(WidPlaylist)
        else :
            self._hideAll(event)
            self._show_and_focus(WidChannelRack)
            
            

    def Navigator(self, event):
    
        if event.data2 in range(65,73) :
            event.data2 = 64
        elif event.data2 in range(55,64) :
            event.data2 = 62
            
        if ui.getFocused(WidPlugin) == True :
            self._hideAll(event)         
        elif ui.getFocused(WidBrowser) :
            if not ui.isInPopupMenu() :  
                if event.data2 == 62 :
                    ui.previous()
                elif event.data2 == 64 :
                    ui.next()
                self._navigation.HintRefresh(ui.getFocusedNodeCaption())
            else :
                if event.data2 == 62 :
                    ui.up()
                elif event.data2 == 64 :
                    ui.down()
                self._navigation.HintRefresh(ui.getFocusedNodeCaption())
        elif ui.getFocused(WidChannelRack) :
            self._show_and_focus(WidChannelRack)
            if event.data2 == 62 :
                self._show_and_focus(WidChannelRack)
                self._hideAll(event)
                ui.previous()
                mixer.setTrackNumber(channels.getTargetFxTrack(channels.selectedChannel()),3)
            elif event.data2 == 64 :
                self._show_and_focus(WidChannelRack)
                self._hideAll(event)
                ui.next()
                mixer.setTrackNumber(channels.getTargetFxTrack(channels.selectedChannel()),3)
        elif ui.getFocused(WidMixer) :
            if IS_PART_PRESSED : 
                if ui.getFocused(WidMixer) :
                    if event.data2 <= 62 :
                        self.PartPrevoiusOffset(event)
                    elif event.data2 >= 64 :
                        self.PartNextOffset(event)
            else :
                self._show_and_focus(WidMixer)
                self._hideAll(event)
                if event.data2 <= 62 :
                    ui.previous()    
                elif event.data2 >= 64 :
                    ui.next() 
                
        else :
            ui.setFocused(WidChannelRack)
            

    def PluginTest(self, event) :
        if ui.getFocused(WidPlugin) :
            string = channels.getChannelName(channels.selectedChannel())
            if string in ArturiaVCOL.V_COL :
                self.ForwardAnalogLab(event)
            else :
                self.PluginPreset(event)
        else :
            if event.data2 > 63 :
                self.FastForward(event)
            else :
                self.Rewind(event)


    def showPlugin(self, event) :
        channels.showEditor(channels.selectedChannel())

    def Context1(self, event) :
        if self._is_pressed(event) :
            self.ToggleBrowserChannelRack(event)
    
    def Context2(self, event) :
        if self._is_pressed(event) :
            self.ToggleMixerChannelRack(event)
    
    def Context3(self, event) :
        # if IS_PART_PRESSED : 
        #     if ui.getFocused(WidMixer) :
        #         self.PartPrevoiusOffset(event) -- This feature has been moved to main encoder
        # else :
        if ui.getFocused(WidChannelRack) :
            self.PrevPattern(event)
        elif ui.getFocused(WidPlugin) :
            if plugins.getPluginName(channels.selectedChannel()) in KLEss3Plugin.NATIVE_PLUGIN_LIST :
                self.PrevPreset(event)
        elif ui.getFocused(WidMixer) :
            if self._is_pressed(event) :
                self.Mute(event)
        elif ui.getFocused(WidBrowser) :
            if event.data2 == 127 :
                self.Back(event)


    def Context4(self, event) :
        # if IS_PART_PRESSED :
        #     if ui.getFocused(WidMixer) : 
        #         self.PartNextOffset(event) -- This feature has been moved to main encoder
        # else :
        if ui.getFocused(WidChannelRack) :
            self.NextPattern(event)
        elif ui.getFocused(WidPlugin) :
            if plugins.getPluginName(channels.selectedChannel()) in KLEss3Plugin.NATIVE_PLUGIN_LIST :
                self.NextPreset(event)
        elif ui.getFocused(WidMixer) :
            if self._is_pressed(event) :
                self.Solo(event)
        elif ui.getFocused(WidBrowser) :
            if self._is_pressed(event) :
                self.SwitchWindow(event)


    # FUNCTIONS



    def Record(self, event) :
        transport.record()
    
    
    def Start(self, event) :
        transport.start()      
    
    
    def Stop(self, event) :
        if self._is_pressed(event) :
            transport.stop()
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedStop, 0x7F, 0x7F, 0x7F]))
        else :
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedStop, 0x16, 0x16, 0x16]))
     

    def Loop(self, event) :
        transport.globalTransport(midi.FPT_LoopRecord,1)

    def Overdub(self, event) :
        transport.globalTransport(midi.FPT_Overdub,1)
        self._navigation.OverdubRefresh()
        
   
    def FastForward(self, event) :
        if self._is_pressed(event) :
            transport.continuousMove(2, SS_START)
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedForward, 0x7F, 0x7F, 0x7F]))
        else :
            transport.continuousMove(2, SS_STOP)
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedForward, 0x16, 0x16, 0x16]))
        self._navigation.FastForwardRefresh()

    
    def Rewind(self, event) :
        if self._is_pressed(event) :
            transport.continuousMove(-2, SS_START)
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedBackward, 0x7F, 0x7F, 0x7F]))
        else :
            transport.continuousMove(-2, SS_STOP)
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedBackward, 0x16, 0x16, 0x16]))
        self._navigation.RewindRefresh()


    def SetClick(self, event) :
        transport.globalTransport(midi.FPT_Metronome,1)
        
    
    def TapTempo(self, event) :
        if self._is_pressed(event) :
            transport.globalTransport(midi.FPT_TapTempo,1)
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedTap, 0x58, 0x58, 0x58]))
            self._navigation.TapTempoRefresh()
        else :
            send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedTap, 0x16, 0x16, 0x16]))
        



    def KnobProcess(self, event) :
        if MIXER_MODE == 1 :
            AKLEss3.SetPanTrack(event)
            HW_value = event.data2
            clef = event.data1-95
            self._navigation.PanChRefresh(HW_value, clef)
            
        else :
            self.Plugin(event, 1)

    def FaderProcess(self, event) :
        if MIXER_MODE == 1 :
            AKLEss3.SetVolumeTrack(event)
            HW_value = event.data2
            clef = event.data1-104
            self._navigation.VolumeChRefresh(HW_value, clef)
        else :
            self.Plugin(event, 1)

    def SetVolumeMasterTrack(self, event) :
        HW_value = event.data2
        if MIXER_MODE == 1 :
            mixer.setTrackVolume(0,HW_value/127, 2)
            self._navigation.VolumeMasterChRefresh(HW_value)
        else :
            mixer.setTrackVolume(mixer.trackNumber(),HW_value/127)
            clef = 0
            self._navigation.VolumeChRefresh(HW_value, clef)

    def SetPanMasterTrack(self, event) :
        HW_value = event.data2
        value = round(event.data2*(128/127)-64)/64
        if MIXER_MODE == 1 :
            mixer.setTrackPan(0,(HW_value*(128/127)-64)/64)
            self._navigation.PanMasterChRefresh(HW_value)
        else :
            mixer.setTrackPan(mixer.trackNumber(),(HW_value*(128/127)-64)/64)
            clef = 0
            self._navigation.PanChRefresh(HW_value, clef)


    def AnalogLabPreset(self, event) :
        if event.data2 == 65 :
            device.forwardMIDICC(event.status + (0x1D << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        elif event.data2 == 63 :
            device.forwardMIDICC(event.status + (0x1C << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))


    def Plugin(self, event, moved_param) :
        # if ui.getFocused(WidPlugin) :

            # if event.status != 224 :
            #     clef = event.data1
            # else :
            #     clef = 224

        hw_param = event.data1
        hw_value = event.data2
        parameter, value, mapped = KLEss3Plugin.Plugin(hw_param, hw_value, moved_param)

        # if mapped :
        if event.data1 in (KNOB_ID) :
            self._navigation.PluginRefresh(parameter, value, mapped, event.data2, 14)
        elif event.data1 in (FADER_ID) :
            self._navigation.PluginRefresh(parameter, value, mapped, event.data2, 15)
        # else :
        #     if event.data1 in (KNOB_ID) :
        #         self._navigation.PluginRefresh(parameter, value, mapped, event.data2, 21)
        #     elif event.data1 in (FADER_ID) :
        #         self._navigation.PluginRefresh(parameter, value, mapped, event.data2, 21)

        # else :
        #     self._navigation.NoPlugin()
            

    def NextPreset(self, event) :
        if event.data2 != 0 :
            self._navigation.NextONRefresh()
            plugins.nextPreset(channels.selectedChannel())
        else :
            self._navigation.NextOFFRefresh()

    def PrevPreset(self, event) :
        if event.data2 != 0 :
            self._navigation.PreviousONRefresh()
            plugins.prevPreset(channels.selectedChannel())
        else :
            self._navigation.PreviousOFFRefresh()
            

    
    def NextPattern(self, event) :
        if event.data2 != 0 :
            patterns.jumpToPattern(patterns.patternNumber()+1)


    def PrevPattern(self, event) :
        if event.data2 != 0 :
            patterns.jumpToPattern(patterns.patternNumber()-1)

    

    def ForwardAnalogLab(self, event) :
        if plugins.getPluginName(channels.selectedChannel()) in ArturiaVCOL.V_COL :
            device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        else :
            self.Plugin(event)
        
        
    def Save(self, event) :
        transport.globalTransport(midi.FPT_Save, midi.FPT_Save, event.pmeFlags)
        self._navigation.SaveRefresh()


    def Quantize(self, event) :
        channels.quickQuantize(channels.selectedChannel())
        self._navigation.QuantizeRefresh()


    def Undo(self, event) :
        transport.globalTransport(midi.FPT_Undo, midi.FPT_Undo, event.pmeFlags)
        self._navigation.UndoRefresh()

    def Redo(self, event) :
        transport.globalTransport(midi.FPT_Undo, midi.FPT_Undo, event.pmeFlags)
        self._navigation.RedoRefresh()

    def Solo(self, event) :
        mixer.soloTrack(mixer.trackNumber())
        
    def Mute(self, event) :
        mixer.muteTrack(mixer.trackNumber())
        
        
        
    # UTILITY
   
   
        
    def FakeMIDImsg(self) :
        transport.globalTransport(midi.FPT_Punch,1)


    # def ShiftIsPressed(self, event) :
    #     if ui.getFocused(WidBrowser) :
    #         if ui.isInPopupMenu():
    #             transport.globalTransport(midi.FPT_Escape, 1)
    #             self._navigation.BackRefresh()
    #     return self._is_pressed(event)


    # def ShiftOn(self, event) :
    #     global SHIFT
    #     SHIFT = self.ShiftIsPressed(event)

    
    def PartOn(self , event) :
        global IS_PART_PRESSED
        global IS_CUSTOM_PART
        

        if self._is_pressed(event) :
            IS_PART_PRESSED = 1
            IS_CUSTOM_PART = 0

        else :
            IS_PART_PRESSED = 0
            #self.FakeMIDImsg()


        if (IS_CUSTOM_PART == 0 and IS_PART_PRESSED == 0) :
            if AKLEss3.PART_OFFSET == 0 :
                AKLEss3.PART_OFFSET = 1
                ui.miDisplayRect(1+(8*AKLEss3.PART_OFFSET),8+(8*AKLEss3.PART_OFFSET),1000)
                send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedPart, 0x7F, 0x7F, 0x7F]))
                self._navigation.PartRefresh()
            else :
                AKLEss3.PART_OFFSET = 0
                ui.miDisplayRect(1+(8*AKLEss3.PART_OFFSET),8+(8*AKLEss3.PART_OFFSET),1000)
                send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedPart, 0x20, 0x20, 0x20]))
                self._navigation.PartRefresh()
        elif (IS_CUSTOM_PART == 1 and IS_PART_PRESSED == 0) :                                        # This is a LED Return function exception because of flag issue
            #print("ca passe")
            if AKLEss3.PART_OFFSET != 0 :
                send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedPart, 0x7F, 0x7F, 0x7F]))
            else :
                send_to_device(bytes([0x04, ePatch.eDaw, 0x16, eLedIds.eLedPart, 0x20, 0x20, 0x20]))
    

    def PartPrevoiusOffset(self, event) :
        global IS_CUSTOM_PART
        IS_CUSTOM_PART = 1
        #self.FakeMIDImsg()

        if event.data2 != 0 :
            if AKLEss3.PART_OFFSET > 0 : 
                AKLEss3.PART_OFFSET -= 1
            ui.miDisplayRect(1+(8*AKLEss3.PART_OFFSET),8+(8*AKLEss3.PART_OFFSET),1000)
            self._navigation.PartRefresh()
        
          
    
    def PartNextOffset(self, event) :
        global IS_CUSTOM_PART
        IS_CUSTOM_PART = 1
        #self.FakeMIDImsg()

        if event.data2 != 0 :
            if AKLEss3.PART_OFFSET < 14 : 
                AKLEss3.PART_OFFSET += 1
            ui.miDisplayRect(1+(8*AKLEss3.PART_OFFSET),8+(8*AKLEss3.PART_OFFSET),1000)
            self._navigation.PartRefresh()   


    def PadOn(self, index) :
        index= index-36
        PAD_MATRIX_STATE[index] = 1
        self.PadRefresh(PAD_MATRIX_STATE)
 
    
    def PadOff(self, index) :
        index = index-36
        PAD_MATRIX_STATE[index] = 0
        self.PadRefresh(PAD_MATRIX_STATE)


    def PadRefresh(self, Matrix) :
        for i in range(16) : # TODO 
            if Matrix[i] :
                send_to_device(bytes([0x04, ePatch.eDaw, 0x16, PAD_MATRIX[i], 0x7F, 0x7F, 0x7F]))
            else :
                send_to_device(bytes([0x04, ePatch.eDaw, 0x16, PAD_MATRIX[i], 0x16, 0x16, 0x16]))
                
    
    def Back(self, event) :
        if ui.getFocused(WidBrowser) :
            if ui.isInPopupMenu():
                transport.globalTransport(midi.FPT_Escape, 1)
            else :
                transport.globalTransport(midi.FPT_Left, 1)
    
            
    
