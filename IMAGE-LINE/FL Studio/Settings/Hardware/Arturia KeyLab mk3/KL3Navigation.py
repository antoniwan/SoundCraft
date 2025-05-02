import transport
import ui
import channels
import patterns
import mixer
import arrangement
import playlist
import math
import utils

import KL3Return as RE
import KL3Process as PR
import ArturiaCrossKeyboardKL3 as AKL3

from images_sub_enums import eCenterIcon




# This class allows FL Studio to send hint messages to Arturia KeyLab's screen

WidMixer = 0
WidChannelRack = 1
WidPlaylist = 2
WidBrowser = 4
WidPlugin = 5
WidPluginEffect = 6
WidPluginGenerator = 7

ANALOG_LAB_BLUE = [0, 108, 122]
WHITE = [127, 127, 127]


class NavigationMode:
    def __init__(self, paged_display):
        self._paged_display = paged_display
 
     
    def VolumeChRefresh(self, clef) :
        
        active_track = mixer.trackNumber()

        if clef == 0 :
            track = active_track
        else :
            track = clef+8*AKL3.PART_OFFSET
        
        HW_value = round(127*mixer.getTrackVolume(track))
        value_disp = str(round(100*mixer.getTrackVolume(track)))

        self._paged_display.SetCenterPage(
            29,
            line1='Volume - ' + str(track),
            line2= value_disp + '%',
            hw_value=HW_value,
            colortype1=1,
            color1=ANALOG_LAB_BLUE
            )

        
    def PanChRefresh(self, clef) :

        active_track = mixer.trackNumber()

        if clef == 0 :
            track = active_track
        else :
            track = clef+8*AKL3.PART_OFFSET
        
        HW_value = round(127*(mixer.getTrackPan(track)+1)/2)
        value_disp = str(round(100*mixer.getTrackPan(track)))
        
        self._paged_display.SetCenterPage(
            28,
            line1='Pan - ' + str(track),
            line2= value_disp + '%',
            hw_value=HW_value,
            colortype1=1,
            color1=ANALOG_LAB_BLUE
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
            self._paged_display.SetCenterPage(13,
                                            line1= 'No Plugin', 
                                            line2= 'Focused',
                                            transient=1,
                                            )
            #self._paged_display.SetFooterPage()


 
    def PluginRefresh(self, str_parameter, str_value_disp, widget_value, is_mapped, page_type) :

        active_index = channels.selectedChannel()

        if is_mapped == 1 :
            self._paged_display.SetCenterPage(
                page_type,
                line1= str_parameter, 
                line2= str_value_disp,
                hw_value=widget_value,
                colortype1=1,
                color1=ANALOG_LAB_BLUE,
                )

        else :
            self._paged_display.SetCenterPage(
                page_type,           
                line1= str_parameter,
                line2= str(widget_value),
                hw_value=widget_value,
                colortype1=1,
                color1=ANALOG_LAB_BLUE,
                )
            
 
            
    def RewindRefresh(self, state) :
        RE.Return(self).isTimelineDisplayed(state)
 
 
    def FastForwardRefresh(self, state) :
          RE.Return(self).isTimelineDisplayed(state)

 
 
    def SaveRefresh(self) :
        self._paged_display.SetCenterPage(
            23,
            line1='Saving project...',
            colortype1= 1,
            color1= ANALOG_LAB_BLUE
            )
   
            
    def QuantizeRefresh(self) :
        self._paged_display.SetCenterPage(
            23,
            line1='Track Quantized',
            colortype1= 1,
            color1= ANALOG_LAB_BLUE
            )
   
   
    def UndoRefresh(self) :
        self._paged_display.SetCenterPage(
            23,
            line1='Action Undone',
            colortype1= 1,
            color1= ANALOG_LAB_BLUE
            )


    def RedoRefresh(self) :
        self._paged_display.SetCenterPage(
            23,
            line1='Action Redone',
            colortype1= 1,
            color1= ANALOG_LAB_BLUE
            )
        
        
    def MetronomeRefresh(self) :
        state = ""
        if ui.isMetronomeEnabled() :
            state = "ON"
        else :
            state = "OFF"

        self._paged_display.SetCenterPage(
            27,
            line1="Metronome",
            colortype1= 1,
            color1= ANALOG_LAB_BLUE,
            line2= state,
            colortype2= 1,
            color2= [127, 127, 127],
            icon= eCenterIcon.ekIconsMetronome_image
        )

            
    def TapTempoRefresh(self) :
        tempo = str(mixer.getCurrentTempo(0))
        if mixer.getCurrentTempo(0) > 99000 :
            tempo_str = tempo[:3]
        else :
            tempo_str = tempo[:2]
        self._paged_display.SetCenterPage(
            27,
            line1="Tap Tempo",
            colortype1= 1,
            color1= ANALOG_LAB_BLUE,
            line2= tempo_str + " BPM",
            colortype2= 1,
            color2= [127, 127, 127],
            icon= eCenterIcon.ekIconsMetronome_image
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
        


    def PartRefresh(self) :
        bankinf = str(1 + AKL3.PART_OFFSET*8)
        banksup = str(8 + AKL3.PART_OFFSET*8)
        self._paged_display.SetCenterPage(
            27,
            line1="Tracks",
            colortype1 = 1,
            color1 = [127, 127, 127],
            line2= bankinf + ' - ' + banksup,
            colortype2 = 1,
            color2 = [127, 127, 127],
            icon = eCenterIcon.ekIconsControls_image
            )



        
    def HintRefresh(self, string) :
              
        if ui.isInPopupMenu() :
            # LABELS = {
                    # "Send to selected channel or focused plugin" : "Replace",
                    # "Open in new channel" : "New Channel",
                    # "Add to plugin database (flag as favorite)" : "Like",
                    # "Open Windows shell menu for this file" : "Windows menu",
                    # "Send file to the trash bin" : "Delete file"
                    # }    

            self._paged_display.SetCenterPage(
                10,
                line1= ui.getHintMsg(),
                colortype1 = 1,
                color1 = [127, 127, 127]
                )

        else :
            self._paged_display.SetCenterPage(
                12,
                line1= string,
                colortype1 = 1,
                color1 = [127, 127, 127],
                line2= PR.BROWSER_TAB,
                colortype2 = 1,
                color2 = [127, 127, 127]
                )
            
            
        self._paged_display.RefreshAllCTXButtons()

            
    def PressRefresh(self) :
        self._paged_display.SetCenterPage(
            9,
            line1= "Select an option"
            )
        
        
    def BackRefresh(self) :
        self._paged_display.SetCenterPage(
            11,
            line1= "Back <-"
            )
        self._paged_display.SetButton(3, 2, "", 2)
        self._paged_display.SetFooterPage()


    def BarRefresh(self) :
        RE.Return(self).SequencerReturn()
        stepinf = str(1 + PR.SEQUENCER_PAGE*8)
        stepsup = str(8 + PR.SEQUENCER_PAGE*8)
        self._paged_display.SetCenterPage(
            27,
            line1="Step Position",
            colortype1 = 1,
            color1 = ANALOG_LAB_BLUE,
            line2= "Step " + stepinf + " - " + stepsup,
            colortype2 = 1,
            color2 = [127, 127, 127],
            icon= eCenterIcon.ekIconsPads_image
        )


        
    
    # def PreviousONRefresh(self) :
    #     self._paged_display.SetButton(3, 0, "", eIcons.eLeftArrowFull)
    #     self._paged_display.SetFooterPage()
    
    # def PreviousOFFRefresh(self) :
    #     self._paged_display.SetButton(3, 0, "", eIcons.eLeftArrow)
    #     self._paged_display.SetFooterPage()

    # def NextONRefresh(self) :
    #     self._paged_display.SetButton(4, 0, "", eIcons.eRightArrowFull)
    #     self._paged_display.SetFooterPage()
    
    # def NextOFFRefresh(self) :
    #     self._paged_display.SetButton(4, 0, "", eIcons.eRightArrow)
    #     self._paged_display.SetFooterPage()




### UTILITY ###

    def CleanCTXButtonRefresh(self) :
        self._paged_display.CleanAllCTXButtons()


    def get_channel_color(self, channel) :
        RGB_color = utils.ColorToRGB(channels.getChannelColor(channel))
        NEW_color = [0, 0, 0]
        if RGB_color == (46, 47, 55) :
            NEW_color = [127, 127, 127]
        else :       
            for i in range(3) :
                NEW_color[i] = RGB_color[i]//2

        return NEW_color

    def get_track_color(self, track) :
        RGB_color = utils.ColorToRGB(mixer.getTrackColor(track))
        NEW_color = [0, 0, 0]
        for i in range(3) :
            NEW_color[i] = RGB_color[i]//2

        return NEW_color

    def get_pattern_color(self, pattern) :
        RGB_color = utils.ColorToRGB(patterns.getPatternColor(pattern))
        NEW_color = [0, 0, 0]
        if RGB_color == (35, 37, 45) :
            NEW_color = [127, 127, 127]
        else :       
            for i in range(3) :
                NEW_color[i] = RGB_color[i]//2

        return NEW_color