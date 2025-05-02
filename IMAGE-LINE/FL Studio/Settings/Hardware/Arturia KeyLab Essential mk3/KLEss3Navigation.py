import transport
import ui
import channels
import patterns
import mixer
import arrangement
import playlist
import math
import KLEss3Process as KLEssPr
import ArturiaCrossKeyboardKLEss3 as AKLEss3

from Icons import eIcons


# This class allows FL Studio to send hint messages to Arturia KeyLab's screen

WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5



class NavigationMode:
    def __init__(self, paged_display):
        self._paged_display = paged_display
 
        
        
    def VolumeChRefresh(self, HW_value, clef) :
        if clef == 0 :
            track = str(mixer.trackNumber())
        else :
            track = str(clef+8*AKLEss3.PART_OFFSET)
        value_disp = str(round(HW_value*125/127))

        self._paged_display.SetCenterPage(15,
                                            line1='Volume - ' + track,
                                            line2= value_disp + '%',
                                            hw_value=HW_value,
                                            transient=1,
                                            )

    def VolumeMasterChRefresh(self, HW_value) :
        value_disp = str(round(HW_value*125/127))

        self._paged_display.SetCenterPage(15,
                                            line1='Volume - Master',
                                            line2= value_disp + '%',
                                            hw_value=HW_value,
                                            transient=1,
                                            )


        
    def PanChRefresh(self, HW_value, clef) :
        if clef == 0 :
            track = str(mixer.trackNumber())
        else :
            track = str((clef+8*AKLEss3.PART_OFFSET))
        value_disp = str(round(HW_value*100/127))
        self._paged_display.SetCenterPage(14,
                                            line1='Pan - ' + track,
                                            line2= value_disp + '%',
                                            hw_value=HW_value,
                                            transient=1,
                                            )

    def PanMasterChRefresh(self, HW_value) :
        value_disp = str(round(HW_value*100/127))

        self._paged_display.SetCenterPage(14,
                                            line1='Pan - Master',
                                            line2= value_disp + '%',
                                            hw_value=HW_value,
                                            transient=1,
                                            )
    
    
    def StereoSepChRefresh(self, value, page_type) :
        track = str(mixer.trackNumber())
        value_disp = str(round(mixer.getTrackStereoSep(mixer.trackNumber()) * 100))
        value_process = 100*(value+1)/2
        self._paged_display.SetPageLines('Stereo',
                                        page_type,
                                        value_process,
                                        line1= 'Stereo - ' + track,
                                        line2= value_disp + '%'
                                        )
        self._paged_display.SetActivePage('Stereo', expires=self._display_ms)
        
    
    def SetRouteChRefresh(self, value, event, page_type) :
        track = str(mixer.trackNumber())
        value_disp = str(round(event.data2/127)*100)
        value_process = 100*(value+1)/2
        self._paged_display.SetPageLines('Route',
                                        page_type,
                                        value,
                                        line1= track + ' - To Master',
                                        line2= value_disp + '%'
                                        )
        self._paged_display.SetActivePage('Route', expires=self._display_ms)
        
    
    def NoPlugin(self) :
        if not ui.getFocused(WidPlugin) :
            self._paged_display.SetCenterPage(12,
                                            line1= 'No Plugin', 
                                            line2= 'Focused',
                                            transient=1,
                                            )
            #self._paged_display.SetFooterPage()


 
    def PluginRefresh(self, parameter, value, mapped, HW_value, page_type) :
        if mapped == 1 :
            self._paged_display.SetCenterPage(page_type,
                                            line1= parameter, 
                                            line2= value + "%",
                                            hw_value=HW_value,
                                            transient=1
                                            )

        else :
            self._paged_display.SetCenterPage(page_type,           
                                            line1= parameter,
                                            line2= str(HW_value),
                                            hw_value=round(HW_value),
                                            transient=1
                                            )
            
 

            
    def RewindRefresh(self) :
        
        self._paged_display.SetCenterPage(17,
                                        line1='Song Position\n' + transport.getSongPosHint(),
                                        line2='',
                                        hw_value=None,
                                        transient=1,
                                        )
 
 
    def FastForwardRefresh(self) :
        self._paged_display.SetCenterPage(17,
                                        line1='Song Position\n' + transport.getSongPosHint(),
                                        line2='',
                                        hw_value=None,
                                        transient=1,
                                        )
 
 
    def SaveRefresh(self) :
        self._paged_display.SetCenterPage(17,
                                        line1='Saving project...',
                                        line2='',
                                        hw_value=None,
                                        transient=1,
                                        )
   
            
    def QuantizeRefresh(self) :
        self._paged_display.SetCenterPage(17,
                                        line1='Track Quantized',
                                        line2='',
                                        hw_value=None,
                                        transient=1,
                                        )
   
   
    def UndoRefresh(self) :
        self._paged_display.SetCenterPage(17,
                                        line1='Action Undone',
                                        line2='',
                                        hw_value=None,
                                        transient=1,
                                        )


    def RedoRefresh(self) :
        self._paged_display.SetCenterPage(17,
                                        line1='Action Redone',
                                        line2='',
                                        hw_value=None,
                                        transient=1,
                                        )
        
        
    def MetronomeRefresh(self) :
        if ui.isMetronomeEnabled() :
            self._paged_display.SetPageLines('MetroOn',
                                            10,
                                            line1= 'Metronome', 
                                            line2= 'ON'
                                        )
            self._paged_display.SetActivePage('MetroOn', expires=self._display_ms)
        else :
            self._paged_display.SetPageLines('MetroOff',
                                            10,
                                            line1= 'Metronome',
                                            line2= 'OFF'
                                            )
            self._paged_display.SetActivePage('MetroOff', expires=self._display_ms)

            
    def TapTempoRefresh(self) :
        tempo = str(mixer.getCurrentTempo(0))
        if mixer.getCurrentTempo(0) > 99000 :
            tempo_str = tempo[:3]
        else :
            tempo_str = tempo[:2]
        self._paged_display.SetCenterPage(17,
                                        line1= "Tap Tempo\n" + tempo_str + ' BPM',
                                        #line2= 'OFF' -- Not working for now
                                        )
        
        
    def SnapModeRefresh(self) :
        SNAP_MODE = {'0' : 'Line',
                     '1' : 'Cell',
                     '3' : 'None',
                     '4' : '1/6 Step',
                     '5' : '1/4 Step',
                     '6' : '1/3 Step',
                     '7' : '1/2 Step', 
                     '8' : 'Step',
                     '9' : '1/6 Beat',
                     '10' : '1/4 Beat',
                     '11' : '1/3 Step',
                     '12' : '1/2 Beat',
                     '13' : 'Beat',
                     '14' : 'Bar'}
        cle = str(ui.getSnapMode())
        snap = SNAP_MODE.get(cle)
        self._paged_display.SetPageLines('Snap',
                                        10,
                                        line1= 'Snap Mode',
                                        line2= snap
                                        )
        self._paged_display.SetActivePage('Snap', expires=self._display_ms)
        
            
            
            
    def BrowserRefresh(self) :

        self._paged_display.SetCenterPage(12,
                                        line1='Turn to',
                                        line2= 'BROWSE',
                                        hw_value=None,
                                        transient=0,
                                        )  
        
        
    def ChannelRackRefresh(self) :

        active_index = channels.selectedChannel()
        channel_name = channels.getChannelName(active_index)
 
        pattern_number = patterns.patternNumber()
        pattern_name = patterns.getPatternName(pattern_number)

        self._paged_display.SetCenterPage(12, 
                                            line1='%d - %s' % (active_index + 1, channel_name), 
                                            line2=pattern_name, 
                                            transient=0
                                            )


    def MixerRefresh(self) :
        self._paged_display.SetCenterPage(12,
                                        line1='Controlling the',
                                        line2= 'MIXER',
                                        hw_value=None,
                                        transient=0,
                                        )


    def PartRefresh(self) :
        bankinf = str(1 + AKLEss3.PART_OFFSET*8)
        banksup = str(8 + AKLEss3.PART_OFFSET*8)
        self._paged_display.SetCenterPage(17,
                                        line1= "Tracks",
                                        line2= bankinf + ' - ' + banksup,
                                        )

    
    def PartOnRefresh(self) :

        self._paged_display.SetButton(3, 1, "", eIcons.eLeftArrow)
        self._paged_display.SetButton(4, 1, "", eIcons.eRightArrow)

        self._paged_display.SetFooterPage()



        
    def HintRefresh(self, string) :
              
        if ui.isInPopupMenu() :
            # LABELS = {
                    # "Send to selected channel or focused plugin" : "Replace",
                    # "Open in new channel" : "New Channel",
                    # "Add to plugin database (flag as favorite)" : "Like",
                    # "Open Windows shell menu for this file" : "Windows menu",
                    # "Send file to the trash bin" : "Delete file"
                    # }    

            self._paged_display.SetHeaderPage("Browser")
            #print(ui.getHintMsg())
            self._paged_display.SetCenterPage(11,
                                            line1= ui.getHintMsg()
                                            )

        else :
            self._paged_display.SetCenterPage(11,
                                            line1= string
                                            )

        self._paged_display.SetHeaderPage("Browser")
        self._paged_display.SetFooterPage()

            
    def PressRefresh(self) :
        self._paged_display.SetCenterPage(11,
                                            line1= "Select an option"
                                            )
        
        
    def BackRefresh(self) :
        self._paged_display.SetCenterPage(11,
                                            line1= "Back <-"
                                            )
        self._paged_display.SetButton(3, 2, "", 2)
        self._paged_display.SetFooterPage()
        
    
    def PreviousONRefresh(self) :
        self._paged_display.SetButton(3, 0, "", eIcons.eLeftArrowFull)
        self._paged_display.SetFooterPage()
    
    def PreviousOFFRefresh(self) :
        self._paged_display.SetButton(3, 0, "", eIcons.eLeftArrow)
        self._paged_display.SetFooterPage()

    def NextONRefresh(self) :
        self._paged_display.SetButton(4, 0, "", eIcons.eRightArrowFull)
        self._paged_display.SetFooterPage()
    
    def NextOFFRefresh(self) :
        self._paged_display.SetButton(4, 0, "", eIcons.eRightArrow)
        self._paged_display.SetFooterPage()

