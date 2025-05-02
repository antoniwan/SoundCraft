import channels
import mixer
import patterns
import transport
import ui
import device
import plugins
import midi
import MiniLabmk2Plugin


from MiniLabmk2Dispatch import MidiEventDispatcher
from MiniLabmk2Leds import MiniLabmk2Led
from MiniLabmk2Dispatch import send_to_device


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

# MIXER
MIXER_MODE = 0

ANALOGLAB_KNOB_ID = (0x01,
                    0x70,
                    0x71,
                    0x72,
                    0x73,
                    0x4A,
                    0x47, 
                    0x4C, 
                    0x4D, 
                    0x5D, 
                    0x49, 
                    0x4B, 
                    0x12, 
                    0x13, 
                    0x10, 
                    0x11, 
                    0x5B, 
                    0x4F, 
                    0x48)
                    
                    
V_COL = ['Analog Lab V',
         'ARP 2600 V3',
         'B-3 V2',
         'Buchla Easel V',
         'Clavinet V',
         'CMI V',
         'CS-80 V3',
         'CZ V',
         'DX7 V',
         'Emulator II V',
         'Farfisa V',
         'Jun-6 V',
         'Jup-8 V4',
         'Matrix-12 V2',
         'Mellotron V',
         'Mini V3',
         'Modular V3',
         'OB-Xa V',
         'PatchWorks',
         'Piano V2',
         'Prophet V3',
         'SEM V2',
         'Solina V2',
         'Stage-73 V2',
         'Synclavier V',
         'Synthi V',
         'Synthopedia',
         'Vocoder V',
         'Vox Continental V2',
         'Wurli V2'
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
            "43":44
            }


class MiniLabMidiProcessor:
    @staticmethod
    def _is_pressed(event):
        return event.controlVal != 0

    def __init__(self, controller):
        def by_midi_id(event) : return event.midiId
        def by_control_num(event) : return event.controlNum
        def by_velocity(event) : return event.data2
        def by_status(event) : return event.status
        def ignore_release(event): return self._is_pressed(event)
        def ignore_press(event): return not self._is_pressed(event)

        self._controller = controller

        self._midi_id_dispatcher = (
            MidiEventDispatcher(by_midi_id)
            .NewHandler(176, self.OnCommandEvent)
            .NewHandler(224, self.OnWheelEvent)
            )
        
        self._midi_command_dispatcher = (
            MidiEventDispatcher(by_control_num)
            
            # MAPPING PAD
            
            .NewHandler(40, self.Start, ignore_press)
            .NewHandler(41, self.Stop, ignore_release)
            .NewHandler(42, self.Record, ignore_press)
            .NewHandler(43, self.TapTempo, ignore_release)
            .NewHandler(44, self.SetClick, ignore_press)
            .NewHandler(45, self.Overdub, ignore_press)
            .NewHandler(46, self.Undo, ignore_press)
            .NewHandler(47, self.ToggleBrowserChannelRack, ignore_press)
            .NewHandler(125, self.SwitchWindow, ignore_release)
            .NewHandler(126, self.ToggleMixerChannelRack, ignore_release)
            .NewHandler(101, self.OnKnobEvent)
            .NewHandler(55, self.PluginTest)
            
            
            # MAPPING KNOBS
            
            .NewHandler(8, self.SetVolumeTrack)
            .NewHandler(37, self.SetPanTrack)
            .NewHandlerForKeys(ANALOGLAB_KNOB_ID, self.ForwardAnalogLab)
            .NewHandlerForKeys(range(2,8), self.Plugin)
            .NewHandlerForKeys(range(31,37), self.Plugin)
            .NewHandler(1, self.Plugin)
            .NewHandler(35, self.MixerParam)
            .NewHandler(36, self.MixerParam)
            .NewHandler(6, self.MixerParam)
            .NewHandler(7, self.MixerParam)
            
        )
        
        self._knob_dispatcher = (
            MidiEventDispatcher(by_velocity)
            .NewHandler(65, self.Navigator)
            .NewHandler(63, self.Navigator)
        )
        
            # MAPPING WHEEL
        
        self._wheel_dispatcher = (
            MidiEventDispatcher(by_status)
        )



    # DISPATCH



    def ProcessEvent(self, event) :
        if event.status in [153,137] :
            return self.OnDrumEvent(event)
        else :
            #print(event.status,"\t",event.data1,"\t",event.controlNum,"\t",event.data2,"\t",event.midiId)
            return self._midi_id_dispatcher.Dispatch(event)


    def OnCommandEvent(self, event):
        self._midi_command_dispatcher.Dispatch(event)

    def OnWheelEvent(self, event):
        self._wheel_dispatcher.Dispatch(event)

    def OnKnobEvent(self, event):
        self._knob_dispatcher.Dispatch(event)

    def OnDrumEvent(self, event) :
        if event.status == 153 :
            event.data1 = FPC_MAP.get(str(event.data1))
            event.data2 = 127
        elif event.status == 137 :
            event.data1 = FPC_MAP.get(str(event.data1))
            event.data2 = 0
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
            # plugin = channels.channelNumber()
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
        
    
    def ToggleBrowserChannelRack(self, event) :
        if ui.getFocused(WidBrowser) != True :
            self._hideAll(event)
            self._show_and_focus(WidBrowser)
        else :
            self._hideAll(event)
            self._show_and_focus(WidChannelRack)
            
            
    def TogglePlaylistChannelRack(self, event) :
        if ui.getFocused(WidPlaylist) != True :
            self._hideAll(event)
            self._show_and_focus(WidPlaylist)
        else :
            self._hideAll(event)
            self._show_and_focus(WidChannelRack)



    # NAVIGATION

    


    def TestCutOrNav(self, event) :
        if ui.getFocused(WidChannelRack) :
            self.Cut(event)
        elif ui.getFocused(WidPlugin) :
            self.PluginPreset
            

    def Navigator(self, event):
        if ui.getFocused(WidPlugin) == True :
            self._hideAll(event)    
        elif ui.getFocused(WidBrowser) == True :
            if event.data2 == 63 :
                self._show_and_focus(WidBrowser)
                self._hideAll(event)
                ui.up()
            elif event.data2 == 65 :  
                self._show_and_focus(WidBrowser)
                self._hideAll(event)
                ui.down()
        elif ui.getFocused(WidMixer) == True :
            if event.data2 == 63 :
                self._show_and_focus(WidMixer)
                self._hideAll(event)
                ui.previous()
            elif event.data2 == 65 :  
                self._show_and_focus(WidMixer)
                self._hideAll(event)
                ui.next()
        else :
            self._show_and_focus(WidChannelRack)
            if event.data2 == 63 :
                self._show_and_focus(WidChannelRack)
                self._hideAll(event)
                ui.previous()
                mixer.setTrackNumber(channels.getTargetFxTrack(channels.channelNumber()),3)
            elif event.data2 == 65 :  
                self._show_and_focus(WidChannelRack)
                self._hideAll(event)
                ui.next()
                mixer.setTrackNumber(channels.getTargetFxTrack(channels.channelNumber()),3)


    def PluginTest(self, event) :
        if ui.getFocused(WidPlugin) :
            string = channels.getChannelName(channels.channelNumber())
            if string in V_COL :
                self.AnalogLabPreset(event)
            else :
                self.PluginPreset(event)
        elif ui.getFocused(WidPlaylist) :
            zoom = event.data2 - 64
            ui.horZoom(zoom)


    def showPlugin(self, event) :
        channels.showEditor(channels.channelNumber())


    # FUNCTIONS



    def Record(self, event) :
        transport.record()
    
    
    def Start(self, event) :
        transport.start()          
    
    
    def Stop(self, event) :
        transport.stop()
     

    def Loop(self, event) :
        transport.globalTransport(midi.FPT_LoopRecord,1)
    

    def Cut(self, event) :
        self._show_and_focus(midi.widChannelRack)
        ui.cut()
        
    def Undo(self, event) :
        transport.globalTransport(midi.FPT_Undo, midi.FPT_Undo, event.pmeFlags)
        

    def Overdub(self, event) :
        transport.globalTransport(midi.FPT_Overdub,1)
    

    def SetClick(self, event) :
        transport.globalTransport(midi.FPT_Metronome,1)
        
    
    def TapTempo(self, event) :
        transport.globalTransport(midi.FPT_TapTempo,1)
      
      
    def SetVolumeTrack(self, event) :
        value = event.data2/127
        mixer.setTrackVolume(mixer.trackNumber(),0.8*value)
            
   
    def SetPanTrack(self, event) :
        value = (event.data2-64)/64
        mixer.setTrackPan(mixer.trackNumber(),value)

  
    def AnalogLabPreset(self, event) :
        if event.data2 == 65 :
            device.forwardMIDICC(event.status + (0x1D << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        elif event.data2 ==63 :
            device.forwardMIDICC(event.status + (0x1C << 8) + (0x7F << 16) + (PORT_MIDICC_ANALOGLAB << 24))


    def Plugin(self, event) :
        if ui.getFocused(WidPlugin) :
            if event.status != 224 :
                clef = event.data1
            else :
                clef = 224
            param, value = MiniLabmk2Plugin.Plugin(event, clef)
            

    def PluginPreset(self, event) :
        if event.data2 == 65  :
            plugins.nextPreset(channels.channelNumber())
        elif event.data2 == 63 :
            plugins.prevPreset(channels.channelNumber())
    
    
    def ForwardAnalogLab(self, event) :
        if channels.getChannelName(channels.channelNumber()) in V_COL :
            device.forwardMIDICC(event.status + (event.data1 << 8) + (event.data2 << 16) + (PORT_MIDICC_ANALOGLAB << 24))
        else :            
            self.Plugin(event)
 
 
    def MixerParam(self, event) :
        if event.controlNum == 35 :
            value = 32*(event.data2-64)
            self.HandleKnob(midi.REC_Mixer_EQ_Gain + 0 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)
        elif event.controlNum == 36 :
            value = 32*(event.data2-64)
            self.HandleKnob(midi.REC_Mixer_EQ_Gain + 2 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)
        elif event.controlNum == 6 :
            value = 512*event.data2
            self.HandleKnob(midi.REC_Mixer_EQ_Freq + 0 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)    
        elif event.controlNum == 7 :
            value = 512*event.data2
            self.HandleKnob(midi.REC_Mixer_EQ_Freq + 2 + mixer.getTrackPluginId(mixer.trackNumber(), 0), value)
 

    def HandleKnob(self, ID, Data2):
        mixer.automateEvent(ID, Data2, midi.REC_Mixer_EQ_Gain, 0, 0, 0) 
        
    # UTILITY
   
        
        
    def FakeMIDImsg(self) :
        transport.globalTransport(midi.FPT_Punch,1)