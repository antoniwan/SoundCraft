import channels
import mixer
import patterns
import transport
import ui
import device
import plugins
import midi
import general

import KL3Plugin as PL
import KL3SeqParam as SQ
import ArturiaCrossKeyboardKL3 as AKL3

from KL3Dispatch import MidiEventDispatcher
from KL3Navigation import NavigationMode
from KL3Dispatch import send_to_device

from IntegrationPatchId import eIntegrationPatchId
from LedId import eLedId

import ArturiaVCOL



# This class processes all CC coming from the controller
# The class creates new handler for each function
# The class calls the right fonction depending on the incoming CC


## CONSTANT

PORT_MIDICC_ANALOGLAB = 10
WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidPianoRoll = 3
WidBrowser = 4
WidPlugin = 5
WidPluginEffect = 6
WidPluginGenerator = 7

# Current focused window
global FOCUSED_WINDOW
FOCUSED_WINDOW = 0

# Sequencer page number
SEQUENCER_PAGE_NUMBER = 4

# Active sequencer page
SEQUENCER_PAGE = 0

# Is sequencer mode active
IS_SEQ_MODE = 0

# Allow step editing in Sequencer Mode
EDIT_MODE = 0

# Event code indicating stop event
SS_STOP = 0

# Event code indicating start start event
SS_START = 2

# Part State
PART_STATE = 0

# String of the selected tab in the browser
BROWSER_TAB = "ALL"

# When Mixer is pressed
IS_MIXER_PRESSED = 0

#When the user selects a custom part
IS_CUSTOM_MIXER = 0

# CC Used by Analog Lab that FL Studio has to forward to the PORT_MIDICC_ANALOGLAB
ANALOGLAB_ID = (
    1,
    16,
    17,
    18,
    19,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    65,
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
    115,
)


KNOB_MAP = {
    91:1,
    92:2,
    94:3,
    95:4,
    96:5,
    97:6,
    102:7,
    103:8,
}

FADER_MAP = {
    105:1,
    106:2,
    107:3,
    108:4,
    109:5,
    110:6,
    111:7,
    112:8,
}

KNOB_TOUCH_MAP = {
    8:1,
    9:2,
    10:3,
    11:4,
    12:5,
    13:6,
    14:7,
    15:8,
}

FADER_TOUCH_MAP = {
    28:1,
    29:2,
    30:3,
    31:4,
    33:5,
    34:6,
    35:7,
    36:8,
}

PAD_MATRIX = [        
        eLedId.ePad1BankDaw, eLedId.ePad2BankDaw, eLedId.ePad3BankDaw, eLedId.ePad4BankDaw,
        eLedId.ePad5BankDaw, eLedId.ePad6BankDaw, eLedId.ePad7BankDaw, eLedId.ePad8BankDaw,
        eLedId.ePad9BankDaw, eLedId.ePad10BankDaw, eLedId.ePad11BankDaw, eLedId.ePad12BankDaw,       
]

# INDEX PRESSED
INDEX_PRESSED = []

# STATE_MATRIX FOR SEQUENCER
PAD_MATRIX_STATE = [
                4*[0],
                4*[0],
                ]
# LED_MATRIX FOR SEQUENCER
PAD_MATRIX_LED = [
                4*[0],
                4*[0],
                4*[0],
                ]

# FPC MAP
FPC_MAP = {
            # RAW 1
            "36":37,
            "37":36,
            "38":42,
            "39":54,

            #RAW 2
            "40":40,
            "41":38,
            "42":46,
            "43":44,
            
            #RAW 3
            "44":48,
            "45":47,
            "46":45,
            "47":43,

            #RAW 4
            "48":60,
            "49":61,
            "50":62,
            "51":63,

            #RAW 5
            "52":64,
            "53":65,
            "54":66,
            "55":67,

            #RAW 6
            "56":68,
            "57":69,
            "58":70,
            "59":71,
            
            }

# Drumaxx MAP
DRUMAXX_MAP = {
            # RAW 1
            "36":49,
            "37":45,
            "38":38,
            "39":42,

            #RAW 2
            "40":36,
            "41":38,
            "42":42,
            "43":44,
            
            #RAW 3
            "44":37,
            "45":43,
            "46":0,
            "47":0,

            #RAW 4
            "48":45,
            "49":61,
            "50":62,
            "51":63,

            #RAW 5
            "52":64,
            "53":65,
            "54":66,
            "55":67,

            #RAW 6
            "56":68,
            "57":69,
            "58":70,
            "59":71,
            
            }


class MidiProcessor:
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
            .NewHandler(40, self.Back)
            .NewHandler(41, self.Save)
            .NewHandler(42, self.Quantize)
            .NewHandler(43, self.Undo, ignore_release)
            .NewHandler(44, self.Redo, ignore_release)
            .NewHandler(117, self.SwitchWindow, ignore_release)
            .NewHandler(116, self.OnKnobEvent)
            .NewHandler(45, self.Context1)
            .NewHandler(46, self.Context2)
            .NewHandler(47, self.Context3)
            .NewHandler(48, self.Context4)
            .NewHandler(49, self.Context5)
            .NewHandler(50, self.Context6)
            .NewHandler(51, self.Context7)
            .NewHandler(52, self.Context8)

            
            
            # MAPPING KNOBS
            
            .NewHandler(113, self.SetVolumeMasterTrack)
            .NewHandler(37, self.SetVolumeTouchMasterTrack)
            .NewHandler(104, self.SetPanMasterTrack)
            .NewHandler(38, self.SetPanTouchMasterTrack)
            .NewHandlerForKeys(ANALOGLAB_ID, self.ForwardAnalogLab)
            .NewHandlerForKeys(KNOB_MAP.keys(), self.KnobProcess)
            .NewHandlerForKeys(FADER_MAP.keys(), self.FaderProcess)
            .NewHandlerForKeys(KNOB_TOUCH_MAP.keys(), self.KnobTouchProcess)
            .NewHandlerForKeys(FADER_TOUCH_MAP.keys(), self.FaderTouchProcess)

            
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
        if event.status in [153,137] :
            if event.data1 not in range(0,12) :
                return self.OnDrumEvent(event)
            else :
                return self.OnSeqEvent(event)
                
        else :

            return self._midi_id_dispatcher.Dispatch(event)

            


    def OnCommandEvent(self, event):
        self._midi_command_dispatcher.Dispatch(event)

    def OnWheelEvent(self, event):
        if channels.selectedChannel(1) != -1 :
            if plugins.isValid(channels.selectedChannel()) : 
                if plugins.getPluginName(channels.selectedChannel()) not in ArturiaVCOL.V_COL :
                    if event.midiId == midi.MIDI_PITCHBEND :
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

        plugin_name = plugins.getPluginName(channels.selectedChannel())
        
        if plugin_name in ['FPC', 'Drumaxx'] :
            
            event.handled = False
            
            if plugin_name == 'FPC' :

                if event.status == 153 :
                    event.data1 = FPC_MAP.get(str(event.data1))

                elif event.status == 137 :
                    event.data1 = FPC_MAP.get(str(event.data1))
            
            elif plugin_name == 'Drumaxx' :

                if event.status == 153 :
                    event.data1 = DRUMAXX_MAP.get(str(event.data1))

                elif event.status == 137 :
                    event.data1 = DRUMAXX_MAP.get(str(event.data1)) 
                

    def OnSeqEvent(self, event) :

        event.handled = True

        if event.data1 not in range(0,8) :
                self.SequencerPage(event)

        else :
            if event.status == 153 :     
                self.PressSequencer(event)

            elif event.status == 137 :                         
                self.ReleaseSequencer(event)

                

    # WINDOW



    def _show_and_focus(self, window):
        if not ui.getVisible(window):
            ui.showWindow(window)
        if not ui.getFocused(window):
            ui.setFocused(window)
  
  
    def _hideAll(self, event) :
        for i in range (channels.channelCount()) :
            channels.showEditor(i,0)


    def showPlugin(self, event) :
        #channels.showEditor(channels.selectedChannel())
        channels.showCSForm(channels.selectedChannel(), -1)


    def SwitchWindow(self, event) :
        if ui.getFocused(WidChannelRack) :
            self.showPlugin(event)
        elif ui.getFocused(WidPlugin) :
            self.ForwardAnalogLab(event)
        elif ui.getFocused(WidMixer) :
            mixer.armTrack(mixer.trackNumber())
            # plugin = channels.selectedChannel()
            # for i in range(plugins.getParamCount(plugin)) :
                # print(i, plugins.getPluginName(channels.selectedChannel()),plugins.getParamName(i,plugin), plugins.getParamValue(i,plugin))

                    
    


    # NAVIGATION



    def ToggleBrowserChannelRack(self, event) :
        self.FakeMIDImsg()
        if ui.getFocused(WidBrowser) != True :
            self._hideAll(event)
            self._show_and_focus(WidBrowser)
        else :
            self._hideAll(event)
            self._show_and_focus(WidChannelRack)

    def ToggleMixerChannelRack(self, event) :
        self.FakeMIDImsg()
        self._hideAll(event)
        if not ui.getFocused(WidMixer) :
            self._show_and_focus(WidMixer)
        else :
            self._show_and_focus(WidChannelRack)

            
    def TogglePlaylistChannelRack(self, event) :
        self.FakeMIDImsg()
        if ui.getFocused(WidPlaylist) != True :
            self._hideAll(event)
            self._show_and_focus(WidPlaylist)
        else :
            self._hideAll(event)
            self._show_and_focus(WidChannelRack)
            
            

    def Navigator(self, event):
    
        # No acceleration with the main encoder
        if event.data2 in range(65,73) :
            event.data2 = 64
        elif event.data2 in range(55,64) :
            event.data2 = 62
            
        if ui.getFocused(WidPlugin) == True :
            self._hideAll(event)         
        elif ui.getFocused(WidBrowser) :
            self._show_and_focus(WidBrowser)
            if ui.isInPopupMenu() :  
                if event.data2 == 62 :
                    ui.up()
                elif event.data2 == 64 :
                    ui.down()
                self._navigation.HintRefresh(ui.getFocusedNodeCaption())
            else :
                if event.data2 == 62 :
                    self._navigation.HintRefresh(ui.navigateBrowser(midi.FPT_Up, 0))
                elif event.data2 == 64 :
                    self._navigation.HintRefresh(ui.navigateBrowser(midi.FPT_Down, 0))
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
            self._hideAll(event)
            self._show_and_focus(WidMixer)
            if event.data2 == 62 :
                if IS_MIXER_PRESSED : 
                    self.PartPrevoiusOffset(event)
                else :
                    ui.previous()  

            elif event.data2 == 64 :
                if IS_MIXER_PRESSED :
                    self.PartNextOffset(event)
                else :
                    ui.next() 
                
        else :
            ui.setFocused(WidChannelRack)



    def Context1(self, event) :
        if not self._is_pressed(event) :
            self._show_and_focus(WidChannelRack)
    
    def Context2(self, event) :
        global IS_MIXER_PRESSED
        global IS_CUSTOM_MIXER

        if self._is_pressed(event) :
            IS_MIXER_PRESSED = 1
            IS_CUSTOM_MIXER = 0      
        else :
            if IS_CUSTOM_MIXER == 0 :
                self._show_and_focus(WidMixer)        
            IS_MIXER_PRESSED = 0
        
    
    def Context3(self, event) :
        # if IS_MIXER_PRESSED : 
        #     if ui.getFocused(WidMixer) :
        #         self.PartPrevoiusOffset(event) -- This feature has been moved to main encoder
        # else :
        if ui.getFocused(WidChannelRack) :
            self.PrevPattern(event)
        elif ui.getFocused(WidPlugin) :
            if plugins.getPluginName(channels.selectedChannel()) in PL.NATIVE_PLUGIN_LIST :
                self.PrevPreset(event)
        elif ui.getFocused(WidBrowser) :
            if self._is_pressed(event) :
                global BROWSER_TAB
                BROWSER_TAB = ui.navigateBrowserTabs(midi.FPT_Left)
                transport.globalTransport(midi.FPT_Down, 1)


    def Context4(self, event) :
        # if IS_MIXER_PRESSED :
        #     if ui.getFocused(WidMixer) : 
        #         self.PartNextOffset(event) -- This feature has been moved to main encoder
        # else :
        if ui.getFocused(WidChannelRack) :
            self.NextPattern(event)
        elif ui.getFocused(WidPlugin) :
            if plugins.getPluginName(channels.selectedChannel()) in PL.NATIVE_PLUGIN_LIST :
                self.NextPreset(event)


    def Context5(self, event) :
        if self._is_pressed(event) :
            self.Mute(event)

    def Context6(self, event) :
        if self._is_pressed(event) :
            self.Solo(event)

    def Context7(self, event) :
        pass

    def Context8(self, event) :
        if self._is_pressed(event) :
                self.Arm(event)


                
    def Back(self, event) :
        if self._is_pressed(event) :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eBack, 0x7F, 0x7F, 0x7F, 0x00]))
            if ui.getFocused(WidBrowser) :
                if ui.isInPopupMenu():
                    ui.closeActivePopupMenu()
                    transport.globalTransport(midi.FPT_Escape, 1)
                else :
                    transport.globalTransport(midi.FPT_Left, 1)
            elif ui.getFocused(WidPlugin) :
                self.showPlugin(event)
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eBack, 0x00, 0x00, 0x00, 0x00]))

    
    # FUNCTIONS
    
    def Record(self, event) :
        transport.record()
    
    
    def Start(self, event) :
        transport.start()      
    
    
    def Stop(self, event) :
        if self._is_pressed(event) :
            transport.stop()
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eStop, 0x7F, 0x7F, 0x7F, 0x00]))
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eStop, 0x20, 0x20, 0x20, 0x00]))
    

    def Loop(self, event) :
        transport.globalTransport(midi.FPT_LoopRecord, 1)

  
    def Overdub(self, event) :
        transport.globalTransport(midi.FPT_Overdub, 1)
        self._navigation.OverdubRefresh()
        
   
    def FastForward(self, event) :
        state = 0

        if self._is_pressed(event) :
            transport.continuousMove(2, SS_START)
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eForward, 0x7F, 0x7F, 0x7F, 0x00]))
            state = 1
        else :
            transport.continuousMove(2, SS_STOP)
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eForward, 0x20, 0x20, 0x20, 0x00]))
        self._navigation.FastForwardRefresh(state)

    
    def Rewind(self, event) :
        state = 0

        if self._is_pressed(event) :
            transport.continuousMove(-2, SS_START)
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eBackward, 0x7F, 0x7F, 0x7F, 0x00]))
            state = 1
        else :
            transport.continuousMove(-2, SS_STOP)
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eBackward, 0x20, 0x20, 0x20, 0x00]))
        self._navigation.RewindRefresh(state)


    def SetClick(self, event) :
        transport.globalTransport(midi.FPT_Metronome, 1)
        # self._navigation.MetronomeRefresh() Screen priority...
        
    
    def TapTempo(self, event) :
        if self._is_pressed(event) :
            transport.globalTransport(midi.FPT_TapTempo, 1)
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eTap, 0x7F, 0x7F, 0x7F, 0x00]))
            #self._navigation.TapTempoRefresh() Screen priority...
            
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eTap, 0x20, 0x20, 0x20, 0x00]))
            


    def KnobProcess(self, event) :
        
        if EDIT_MODE == 1 :
            global SEQ_PARAM
            SQ.Param(event)
            self.FakeMIDImsg()
            SEQ_PARAM = 1
        
        else :
        
            if ui.getFocused(WidMixer) :
                AKL3.SetPanTrack(event)
                clef = KNOB_MAP.get(event.data1)
                self._navigation.PanChRefresh(clef) 
            else :
                self.Plugin(event, False)


    def FaderProcess(self, event) :
        if ui.getFocused(WidMixer) :
            AKL3.SetVolumeTrack(event)
            clef = FADER_MAP.get(event.data1)
            self._navigation.VolumeChRefresh(clef)
        else :
            self.Plugin(event, False)


    def KnobTouchProcess(self, event) :
        if INDEX_PRESSED == [] :
            if self._is_pressed(event) :
                if ui.getFocused(WidMixer) :
                    clef = KNOB_TOUCH_MAP.get(event.data1)
                    self._navigation.PanChRefresh(clef)
                else :
                    self.Plugin(event, False)

    
    def FaderTouchProcess(self, event) :
        if self._is_pressed(event) :
            if ui.getFocused(WidMixer) :
                clef = FADER_TOUCH_MAP.get(event.data1)
                self._navigation.VolumeChRefresh(clef)
            else :
                self.Plugin(event, False)

    
    def SetVolumeMasterTrack(self, event) :
        AKL3.SetVolumeTrack(event)
        self._navigation.VolumeChRefresh(0)

    def SetVolumeTouchMasterTrack(self, event) :
        AKL3.SetVolumeTrack(event)
        self._navigation.VolumeChRefresh(0)    

    def SetPanMasterTrack(self, event) :
        AKL3.SetPanTrack(event)
        self._navigation.PanChRefresh(0)

    def SetPanTouchMasterTrack(self, event) :
        AKL3.SetPanTrack(event)
        self._navigation.PanChRefresh(0)   



    def AnalogLabPreset(self, event) :
        if event.data2 == 65 :
            device.forwardMIDICC(event.status + (0x1D << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        elif event.data2 == 63 :
            device.forwardMIDICC(event.status + (0x1C << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))


    def Plugin(self, event, is_bypassed) :

        hw_param = event.data1
        hw_value = event.data2
        
        str_parameter, str_value_disp, widget_value, is_mapped, is_released = PL.Plugin(hw_param, hw_value, is_bypassed)
        
        # if mapped :
        if not is_released :
            if event.data1 in (KNOB_MAP.keys()) :

                self._navigation.PluginRefresh(
                    str_parameter, 
                    str_value_disp, 
                    widget_value,
                    is_mapped,
                    28,
                    )
                
            if event.data1 in (KNOB_TOUCH_MAP.keys()) :

                self._navigation.PluginRefresh(
                    str_parameter, 
                    str_value_disp, 
                    widget_value,
                    is_mapped,
                    28,
                    )
                
            elif event.data1 in (FADER_MAP.keys()) :

                self._navigation.PluginRefresh(
                    str_parameter, 
                    str_value_disp, 
                    widget_value,
                    is_mapped, 
                    29,
                    )
                
            elif event.data1 in (FADER_TOUCH_MAP.keys()) :

                self._navigation.PluginRefresh(
                    str_parameter, 
                    str_value_disp, 
                    widget_value,
                    is_mapped, 
                    29,
                    )

            

    def NextPreset(self, event) :
        if event.data2 != 0 :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eContextual4, 0x7F, 0x7F, 0x7F, 0x00]))
            plugins.nextPreset(channels.selectedChannel())
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eContextual4, 0x7F, 0x7F, 0x7F, 0x00]))

    def PrevPreset(self, event) :
        if event.data2 != 0 :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eContextual3, 0x7F, 0x7F, 0x7F, 0x00]))
            plugins.prevPreset(channels.selectedChannel())
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eContextual3, 0x7F, 0x7F, 0x7F, 0x00]))
            

    
    def NextPattern(self, event) :
        if event.data2 != 0 :
            patterns.jumpToPattern(patterns.patternNumber()+1)


    def PrevPattern(self, event) :
        if event.data2 != 0 :
            patterns.jumpToPattern(patterns.patternNumber()-1)

    

    def ForwardAnalogLab(self, event) :
        if channels.selectedChannel(1) != -1 :
            if plugins.isValid(channels.selectedChannel()) : 
                if plugins.getPluginName(channels.selectedChannel()) in ArturiaVCOL.V_COL :
                    device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
                else :
                    self.Plugin(event, is_bypassed=True)
        
        
    def Save(self, event) :
        if self._is_pressed(event) :
            transport.globalTransport(midi.FPT_Save, 1)
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eSave, 0x7F, 0x7F, 0x7F, 0x00]))
            self._navigation.SaveRefresh()
        else :
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eSave, 0x10, 0x10, 0x10, 0x00]))


    def Quantize(self, event) :
        if self._is_pressed(event) :
            channels.quickQuantize(channels.selectedChannel())
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eQuantize, 0x7F, 0x7F, 0x7F, 0x00]))
            self._navigation.QuantizeRefresh()
        else :
            ui.hideWindow(WidPianoRoll)
            send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, 0x03, eLedId.eQuantize, 0x10, 0x10, 0x10, 0x00]))


    def Undo(self, event) :
        general.undoUp()
            



    def Redo(self, event) :
        general.undoDown()



    def Solo(self, event) :
        mixer.soloTrack(mixer.trackNumber())


    def Mute(self, event) :
        mixer.muteTrack(mixer.trackNumber())


    def Arm(self, event) :
        mixer.armTrack(mixer.trackNumber())
        
        
        
    
    def PartOn(self , event) :
        global IS_MIXER_PRESSED
        global IS_CUSTOM_MIXER
        

        if self._is_pressed(event) :
            IS_MIXER_PRESSED = 1
            IS_CUSTOM_MIXER = 0

        else :
            IS_MIXER_PRESSED = 0
            #self.FakeMIDImsg()


        if (IS_CUSTOM_MIXER == 0 and IS_MIXER_PRESSED == 0) :
            if AKL3.PART_OFFSET == 0 :
                AKL3.PART_OFFSET = 1
                ui.miDisplayRect(1+(8*AKL3.PART_OFFSET),8+(8*AKL3.PART_OFFSET),1000)
                send_to_device(bytes([0x04, eIntegrationPatchId.eDaw, 0x16, eLedId.eLedPart, 0x7F, 0x7F, 0x7F]))
                self._navigation.PartRefresh()
            else :
                AKL3.PART_OFFSET = 0
                ui.miDisplayRect(1+(8*AKL3.PART_OFFSET),8+(8*AKL3.PART_OFFSET),1000)
                send_to_device(bytes([0x04, eIntegrationPatchId.eDaw, 0x16, eLedId.eLedPart, 0x20, 0x20, 0x20]))
                self._navigation.PartRefresh()
        elif (IS_CUSTOM_MIXER == 1 and IS_MIXER_PRESSED == 0) :                                        # This is a LED Return function exception because of flag issue
            if AKL3.PART_OFFSET != 0 :
                send_to_device(bytes([0x04, eIntegrationPatchId.eDaw, 0x16, eLedId.eLedPart, 0x7F, 0x7F, 0x7F]))
            else :
                send_to_device(bytes([0x04, eIntegrationPatchId.eDaw, 0x16, eLedId.eLedPart, 0x20, 0x20, 0x20]))
    

    def PartPrevoiusOffset(self, event) :
        global IS_CUSTOM_MIXER
        IS_CUSTOM_MIXER = 1

        if AKL3.PART_OFFSET > 0 : 
            AKL3.PART_OFFSET -= 1
        ui.miDisplayRect(1+(8*AKL3.PART_OFFSET),8+(8*AKL3.PART_OFFSET),1000)
        self._navigation.PartRefresh()
        


    def PartNextOffset(self, event) :
        global IS_CUSTOM_MIXER
        IS_CUSTOM_MIXER = 1

        if AKL3.PART_OFFSET < 14 : 
            AKL3.PART_OFFSET += 1
        ui.miDisplayRect(1+(8*AKL3.PART_OFFSET),8+(8*AKL3.PART_OFFSET),1000)
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
        for i in range(16) :
            if Matrix[i] :
                send_to_device(bytes([0x04, eIntegrationPatchId.eDaw, 0x16, PAD_MATRIX[i], 0x7F, 0x7F, 0x7F]))
            else :
                send_to_device(bytes([0x04, eIntegrationPatchId.eDaw, 0x16, PAD_MATRIX[i], 0x16, 0x16, 0x16]))
                
    
    

    # SEQUENCER      
            
    def HoldBit(self, event) :

        global PAD_MATRIX_STATE
        global INDEX_PRESSED
        global EDIT_MODE
        EDIT_MODE = 1
          
        # State Matrix Init
        BIT_MAP = {
        '0':0,
        '1':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        }

        cle = str(event.data1)
        PAD_MATRIX_STATE[BIT_MAP.get(cle)//4][BIT_MAP.get(cle)%4] = 1
        INDEX_PRESSED.append(BIT_MAP.get(cle))

    def PressSequencer(self, event) :
        global SEQ_PARAM
        SEQ_PARAM = 0
        if channels.isGraphEditorVisible() :
            SEQ_PARAM = 1
        self.HoldBit(event) 


    def ReleaseSequencer(self, event) :
        global PAD_MATRIX_STATE
        global EDIT_MODE
        
        # State Matrix Init
        EDIT_MODE = 0
        BIT_MAP = {
        '0':0,
        '1':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        }
        cle = str(event.controlNum)
        PAD_MATRIX_STATE[BIT_MAP.get(cle)//4][BIT_MAP.get(cle)%4] = 0
        INDEX_PRESSED.remove(BIT_MAP.get(cle))
                
        # While at least one pad is pressed, stay in edit mode 
        if INDEX_PRESSED != [] :
            EDIT_MODE = 1
        else :
            channels.closeGraphEditor(1)
        
        # If a parameter changed, let the pad on
        step = event.controlNum
        if SEQ_PARAM == 1 :
            return
        else :    
            if channels.getGridBit(channels.selectedChannel(), step+(SEQUENCER_PAGE*8)) == 0 :
                channels.setGridBit(channels.selectedChannel(), step+(SEQUENCER_PAGE*8),1)
                PAD_MATRIX_LED[step//4][step%4] = 1
            else :
                channels.setGridBit(channels.selectedChannel(), step+(SEQUENCER_PAGE*8),0)
                PAD_MATRIX_LED[step//4][step%4] = 0



    def SequencerPage(self, event) :

        if self._is_pressed(event) :

            global SEQUENCER_PAGE
            index = event.data1-8
            SEQUENCER_PAGE = index

            left = SEQUENCER_PAGE*8
            top = channels.selectedChannel()
            ui.crDisplayRect(left,top,8,1,1000)

            self._navigation.BarRefresh()
            

    # UTILITY
   
        
    def FakeMIDImsg(self) :
        transport.globalTransport(midi.FPT_Punch, 1, midi.GT_All)