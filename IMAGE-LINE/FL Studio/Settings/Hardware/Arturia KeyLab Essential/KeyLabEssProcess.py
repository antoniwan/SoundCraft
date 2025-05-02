import channels
import midi
import mixer
import patterns
import transport
import ui
import device
import plugins
import ArturiaCrossKeyboardEss as AKLESS
import KeyLabEssPlugin

from KeyLabEssDispatch import MidiEventDispatcher
from KeyLabEssDispatch import send_to_device
from KeyLabEssDisplay import KeyLabDisplay
from KeyLabEssPages import KeyLabPagedDisplay
from KeyLabEssNavigation import NavigationMode

## CONSTANT

PORT_MIDICC_ANALOGLAB = 10
WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5
ANALOGLAB_KNOB_ID = [0x4A, 0x47, 0x4C, 0x4D, 0x5D, 0x49, 0x4B]


# Event code indicating stop event
SS_STOP = 0

# Event code indicating start start event
SS_START = 2

# MIXER
MIXER_MODE = 0

# Max Tracks
MAX_TRACKS = 125


FPC_MAP = {
            "36":40,
            "37":38,
            "38":46,
            "39":44,
            "40":37,
            "41":36,
            "42":42,
            "43":54
            }
# This class processes all CC coming from the controller
# The class creates new handler for each function
# The class calls the right fonction depending on the incoming CC

class KeyLabEssMidiProcessor:

    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, ess):
        def by_midi_id(event) : return event.midiId
        def by_control_num(event) : return event.controlNum
        def by_velocity(event) : return event.data2
        def by_status(event) : return event.status
        def by_sysex(event) : return event.sysex
        def ignore_release(event): return self._is_pressed(event)
        def ignore_press(event): return not self._is_pressed(event)

        self._ess = ess

        self._midi_id_dispatcher = (
            MidiEventDispatcher(by_midi_id)
            .NewHandler(144, self.OnCommandEvent)
            .NewHandler(176, self.OnKnobEvent)
            .NewHandler(224, self.OnSliderEvent)
            .NewHandler(153, self.OnDrumEvent)
            .NewHandler(137, self.OnDrumEvent)
            )
            

         
        self._sysex_dispatcher = (
            MidiEventDispatcher(by_sysex)
            .NewHandler(b'\xf0\x00 k\x7fB\x02\x00\x00\x18\x00\xf7', self.previousPreset, ignore_press)
            .NewHandler(b'\xf0\x00 k\x7fB\x02\x00\x00\x19\x00\xf7', self.nextPreset, ignore_press)
            )
        
        self._midi_command_dispatcher = (
            MidiEventDispatcher(by_control_num)

            
            .NewHandler(0x5E, self.Start, ignore_press)
            .NewHandler(0x5D, self.Stop, ignore_release)
            .NewHandler(0x5F, self.Record, ignore_press)
            .NewHandler(0x58, self.Overdub, ignore_press)
            .NewHandler(0x56, self.Loop, ignore_press)
            .NewHandler(0x59, self.SetClick, ignore_press)
            .NewHandler(0x51, self.Undo, ignore_press)
            .NewHandler(0x50, self.Cut, ignore_press)
            .NewHandler(0x5B, self.Rewind)
            .NewHandler(0x5C, self.FastForward)
            .NewHandler(0x54, self.SwitchWindow, ignore_release)
            .NewHandler(0x2E, self.BankSelect, ignore_release)
            .NewHandler(0x2F, self.BankSelect, ignore_release)
            .NewHandler(0x62, self.previousPattern, ignore_release)
            .NewHandler(0x63, self.nextPattern, ignore_release)
            .NewHandler(0x64, self.ToggleMixerChannelRack, ignore_release)
            .NewHandler(0x65, self.ToggleBrowserChannelRack, ignore_release)
        )
        
        self._slider_dispatcher = (
            MidiEventDispatcher(by_status)
            .NewHandlerForKeys(range(224,233), self.SetVolumeTrack)   
        )
        
        
        self._plugin_dispatcher = (
            MidiEventDispatcher(by_control_num)
            .NewHandler(0x4A, self.Plugin)
            .NewHandler(71, self.Plugin)
            .NewHandler(76, self.Plugin)
            .NewHandler(77, self.Plugin)
            .NewHandler(93, self.Plugin)
            .NewHandler(18, self.Plugin)
            .NewHandler(19, self.Plugin)
            .NewHandler(16, self.Plugin)
            
            .NewHandler(73, self.Plugin)
            .NewHandler(75, self.Plugin)
            .NewHandler(79, self.Plugin)
            .NewHandler(72, self.Plugin)
            .NewHandler(80, self.Plugin)
            .NewHandler(81, self.Plugin)
            .NewHandler(82, self.Plugin)
            .NewHandler(83, self.Plugin)
            .NewHandler(17, self.Plugin)
            .NewHandler(1, self.Plugin)
            
            .NewHandler(0x1C, self.previousPreset, ignore_release)
            .NewHandler(0x1D, self.nextPreset, ignore_release)
        )

            
        
        self._knob_dispatcher = (
            MidiEventDispatcher(by_control_num)
            .NewHandler(60, self.OnKnobNavEvent)
            .NewHandler(60, self.OnKnobNavEvent)
            .NewHandlerForKeys(range(16,24), self.SetPanTrack)
        )

        self._knob_nav_dispatcher = (
            MidiEventDispatcher(by_velocity)
            .NewHandler(1, self.TrackSelectMainKnob)
            .NewHandler(65, self.TrackSelectMainKnob)
        )
            # NAVIGATION
        
        self._navigation = NavigationMode(self._ess.paged_display())




    # DISPATCH



    def ProcessEvent(self, event) :
        if event.status in [153,137] :
            #print("status",event.status,"\t",event.data1,"\t",event.controlNum,"\t",event.data2,"\t",event.midiId)
            return self.OnDrumEvent(event)
        elif (event.status != event.midiId and event.midiId != 224) :
            #print("plugin",event.status,"\t",event.data1,"\t",event.controlNum,"\t",event.data2,"\t",event.midiId)
            return self._plugin_dispatcher.Dispatch(event)
        else :
            #print("midi id",event.status,"\t",event.data1,"\t",event.controlNum,"\t",event.data2,"\t",event.midiId)
            return self._midi_id_dispatcher.Dispatch(event)
            
    def OnCommandEvent(self, event) :
        event.handled = True
        if event.status == event.midiId :
            device.processMIDICC(event)
            self._midi_command_dispatcher.Dispatch(event)


    def OnKnobEvent(self, event):
        event.handled = True
        self._knob_dispatcher.Dispatch(event)
        
    def OnKnobNavEvent(self, event):
        event.handled = True
        self._knob_nav_dispatcher.Dispatch(event)
        
    def OnPluginEvent(self, event) :
        event.handled = True
        self._plugin_dispatcher.Dispatch(event)
        
    def OnSliderEvent(self, event) :
        event.handled = True
        self._slider_dispatcher.Dispatch(event)

    def OnDrumEvent(self, event) :
        if event.status == 153 :
            event.data1 = FPC_MAP.get(str(event.data1))
            event.data2 = midi.MIDI_NOTEON
        elif event.status == 137 :
            event.data1 = FPC_MAP.get(str(event.data1))
            event.data2 = midi.MIDI_NOTEOFF
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
        if (ui.getFocused(WidChannelRack) or ui.getFocused(WidPlugin)) :
            self.showPlugin(event)
        elif ui.getFocused(WidMixer) :
            track = mixer.trackNumber()
            mixer.armTrack(track)
            self._navigation.ArmRefresh(track)
            # for i in range(plugins.getParamCount(plugin)) :
                # print(i, plugins.getParamName(i,plugin), plugins.getParamValue(i,plugin))
        else :
            nodeFileType = ui.getFocusedNodeFileType()
            if nodeFileType == -1:
                return
            if nodeFileType <= -100:
                transport.globalTransport(midi.FPT_Enter, 1)
            else:
                ui.selectBrowserMenuItem()
                if not ui.isInPopupMenu() :
                    self._navigation.PressRefresh()

    
    def showPlugin(self, event) :
        channels.showEditor(channels.channelNumber())
        
    
    def ToggleBrowserChannelRack(self, event) :
        if ui.getFocused(4) != True :
            self._show_and_focus(4)
            self._navigation.BrowserRefresh()
        else :
            self._show_and_focus(1)
            self._navigation.ChannelRackRefresh()
            
    
    def ToggleMixerChannelRack(self, event) :
        self.FakeMIDImsg()
        self._hideAll(event)
        global MIXER_MODE
        if MIXER_MODE == 0 :
            MIXER_MODE = 1
            self._show_and_focus(WidMixer)
        else :
            MIXER_MODE = 0
            self._show_and_focus(WidChannelRack)
        self._navigation.MixerToggleRefresh()



    # NAVIGATION



    def TrackSelectMainKnob(self, event):
        if ui.getFocused(WidPlugin) == True :
            self._hideAll(event)    
        elif ui.getFocused(WidBrowser) == True :
            if ui.isInPopupMenu() :  
                if event.data2 == 65 :
                    ui.up()
                elif event.data2 == 1 :
                    ui.down()
                self._navigation.HintRefresh(ui.getFocusedNodeCaption())
            else :
                if event.data2 == 65 :
                    ui.previous()
                elif event.data2 == 1 :
                    ui.next()
                self._navigation.HintRefresh(ui.getFocusedNodeCaption())
        elif ui.getFocused(WidMixer) == True :
            if event.data2 == 65 :
                self._show_and_focus(WidMixer)
                self._hideAll(event)
                ui.previous()
    
            elif event.data2 == 1 :  
                self._show_and_focus(WidMixer)
                self._hideAll(event)
                ui.next()
        else :
            if event.data2 == 65 :
                self._show_and_focus(WidChannelRack)
                self._hideAll(event)
                ui.previous()
                mixer.setTrackNumber(channels.getTargetFxTrack(channels.channelNumber()),3)
            elif event.data2 == 1 :  
                self._show_and_focus(WidChannelRack)
                self._hideAll(event)
                ui.next()
                mixer.setTrackNumber(channels.getTargetFxTrack(channels.channelNumber()),3)


    def BankSelect(self, event) :
        if MIXER_MODE == 1 :
            self.FakeMIDImsg()
            if event.controlNum == 0x2E :
                AKLESS.MX_OFFSET -= 1
                if AKLESS.MX_OFFSET < 0 :
                    AKLESS.MX_OFFSET = 0
                self._navigation.BankMixRefresh()
            elif event.controlNum == 0x2F :
                if (AKLESS.MX_OFFSET + 1)*8 < MAX_TRACKS :
                    AKLESS.MX_OFFSET += 1
                    self._navigation.BankMixRefresh()
            #ui.miDisplayRect(1+(AKLESS.MX_OFFSET*8),9+(AKLESS.MX_OFFSET*8),100) # does not seem to work
        else :
            self.FakeMIDImsg()
            if event.controlNum == 0x2E :
                AKLESS.CH_OFFSET -= 1
                if AKLESS.CH_OFFSET < 0 :
                    AKLESS.CH_OFFSET = 0
                self._navigation.BankChanRefresh()
            elif event.controlNum == 0x2F :
                if (AKLESS.CH_OFFSET + 1)*8 < channels.channelCount() :
                    AKLESS.CH_OFFSET += 1
                    self._navigation.BankChanRefresh()
                    

    def previousPattern(self, event) :
        if ui.getFocused(5) :
            self.previousPreset(event)
        else :
            pattern = patterns.patternNumber()
            patterns.jumpToPattern(pattern - 1)
        
     
    def nextPattern(self, event) :
        if ui.getFocused(5) :
            self.nextPreset(event)
        else :
            pattern = patterns.patternNumber()
            patterns.jumpToPattern(pattern + 1)
    
    
    
    # PLUGIN



    # def NewPlugin(self, event) :
        # transport.globalTransport(67,1)


    def nextPreset(self, event) :
        if ui.getFocused(5) :
            plugins.nextPreset(channels.channelNumber())


    def previousPreset(self, event) :
        if ui.getFocused(5) :
            plugins.prevPreset(channels.channelNumber())


    def Plugin(self, event, clef) :
        if ui.getFocused(5) :
            param, value = KeyLabEssPlugin.Plugin(event,clef)
            if event.controlNum != 1 :
                self._navigation.PluginRefresh(param, value)



    # FUNCTIONS



    def Record(self, event) :
        transport.record()
        self._navigation.RecordRefresh()
    
    
    def Start(self, event) :
        transport.start()
        self._navigation.PlayRefresh()        
    
    
    def Stop(self, event) :
        transport.stop()
        self._navigation.StopRefresh()
        
    def FastForward(self, event) :
        if self._is_pressed(event):
            transport.continuousMove(1, SS_START)
            self._navigation.FastForwardRefresh()
        else:
            transport.continuousMove(1, SS_STOP)
            self._navigation.FastForwardRefresh()
    
    def Rewind(self, event) :
        if self._is_pressed(event):
            transport.continuousMove(-1, SS_START)
            self._navigation.RewindRefresh()
        else:
            transport.continuousMove(-1, SS_STOP)
            self._navigation.RewindRefresh()
    

    def Loop(self, event) :
        transport.globalTransport(midi.FPT_LoopRecord,1)
        self._navigation.LoopRefresh()

    def Overdub(self, event) :
        transport.globalTransport(midi.FPT_Overdub,1)
        self._navigation.OverdubRefresh()
    

    def SetClick(self, event) :
        transport.globalTransport(midi.FPT_Metronome,1)
        self._navigation.MetronomeRefresh()  
    
    def Undo(self, event) :
        transport.globalTransport(midi.FPT_Undo, midi.FPT_Undo, event.pmeFlags)
        self._navigation.UndoRefresh() 

    def Cut(self, event) :
        self._show_and_focus(midi.widChannelRack)
        ui.cut()
        self._navigation.CutRefresh()        


    def TapTempo(self, event) :
        transport.globalTransport(midi.FPT_TapTempo,1)
        self._navigation.TapTempoRefresh()

    def SnapMode(self, event) :
        ui.snapMode(1)
        self._navigation.SnapModeRefresh()
        
        
    def SetVolumeTrack(self, event) :
        if MIXER_MODE == 1 :
            if event.status == 232 and event.midiId == 224  :
                event.data1 = 1
                event.midiId = midi.MIDI_CONTROLCHANGE
                AKLESS.SetVolumeTrack(event) 
                value = round(mixer.getTrackVolume(0)*100)
                perc = str(value)
                self._navigation.VolumeMixerRefresh(event, perc)
            else :
                event.data1 = 2 + event.status - event.midiId
                event.midiId = midi.MIDI_CONTROLCHANGE
                track = (event.controlNum - 1) + (8*AKLESS.MX_OFFSET)
                if track < 126 :
                    AKLESS.SetVolumeTrack(event)
                    value = round(mixer.getTrackVolume(event.data1 - 1 + (8*AKLESS.MX_OFFSET)) * 100)
                    perc = str(value)
                    self._navigation.VolumeMixerRefresh(event, perc)
        else :
            if event.status != 232 :
                self.Plugin(event, clef = event.status)
                self._navigation.NoPlugin()
            else :
                value = event.data2/127
                mixer.setTrackVolume(mixer.trackNumber(),0.8*value)
                value = round(mixer.getTrackVolume(mixer.trackNumber())*100)
                perc = str(value)
                self._navigation.VolumeChRefresh(perc)


    def SetPanTrack(self, event) :
        if MIXER_MODE == 1 :
            track = (event.controlNum - 15) + (8*AKLESS.MX_OFFSET)
            AKLESS.SetPanTrack(event)
            value = round(mixer.getTrackPan(track) * 100)
            perc = str(value)
            self._navigation.PanMixerRefresh(event, perc)
        else :
            if event.controlNum != 24 :
                self.Plugin(event, clef = event.controlNum)
                self._navigation.NoPlugin()
            else :
                data = 0
                if event.data2 > 0x40 : data = -1
                elif event.data2 < 0x40 : data = 1
                mixer.setTrackPan(mixer.trackNumber(),mixer.getTrackPan(mixer.trackNumber())+ (data/20))
                value = round(mixer.getTrackPan(mixer.trackNumber()) * 100)
                perc = str(value)
                self._navigation.PanChRefresh(perc)
                
                
                
    # UTILITY
   
        
        
    def FakeMIDImsg(self) :
        transport.globalTransport(midi.FPT_Punch,1)

