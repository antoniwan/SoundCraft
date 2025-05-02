# MIT License

# Copyright (c) 2021 Pablo Peral

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import mixer_definition
import nihia
from nihia import *
import config

import mixer
import transport
import general
import ui
import device
import midi
import plugins
import channels
import math

class Core:
    """ Common controller definition across all Komplete Kontrol keyboards. """
    def __init__(self):
        # Initialize mixer cache
        self.mixer = mixer_definition.Mixer()

        # Button light states
        self.PLAY           = None
        self.STOP           = None
        self.REC            = None
        self.COUNT_IN       = None
        self.CLEAR          = None
        self.LOOP           = None
        self.METRO          = None

        self.UNDO           = None
        self.REDO           = None
        self.QUANTIZE       = None
        self.AUTO           = None

        self.MUTE_SELECTED  = None
        self.SOLO_SELECTED  = None

    def OnInit(self):
        # Activates the deep integration mode
        nihia.handShake()

        # Update LEDs
        self.OnRefresh(midi.HW_Dirty_LEDs)
        self.OnRefresh(260)

        nihia.buttons.setLight("QUANTIZE", 1)
        nihia.buttons.setLight("AUTO", 0)

        # Update mixer
        self.mixer.setGroupToCurrentTrack()
        self.mixer.update()

    def OnDeInit(self):
        # Deactivates the deep integration mode
        nihia.goodBye()

    def OnMidiMsg(self, event):

        # Play button
        if event.data1 == nihia.buttons.button_list.get("PLAY"):
            event.handled = True
            transport.start()

        # Restart button
        elif event.data1 == nihia.buttons.button_list.get("RESTART"):
            event.handled = True
            transport.stop()
            transport.setSongPos(0)
            transport.start()

        # Record button
        elif event.data1 == nihia.buttons.button_list.get("REC"):
            event.handled = True
            transport.record()
        
        # Count-In button
        elif event.data1 == nihia.buttons.button_list.get("COUNT_IN"):
            event.handled = True
            
            # Defines the standard behavior (just to toggle "Countdown before recording" on/off)
            if config.COUNT_IN_BEHAVIOR == 0:
                transport.globalTransport(midi.FPT_CountDown, 1)
            
            # Defines behavior of the button if the user chooses the Maschine-alike behavior
            if config.COUNT_IN_BEHAVIOR == 1:
        
                # Toggles recording on if it isn't enabled already
                if transport.isRecording() == 0:
                    transport.record()
                
                # Toggles countdown before recording on if it isn't enabled already
                if ui.isPrecountEnabled() == 0:
                    transport.globalTransport(midi.FPT_CountDown, 1)
                
                # Stops playback if FL Studio is playing
                if transport.isPlaying() == True:
                    transport.stop()
                
                # Then turns playback on again. This time record and countdown before recording will be activated
                transport.start()

        # Stop button
        elif event.data1 == nihia.buttons.button_list.get("STOP"):
            event.handled = True
            transport.stop()

        # Clear button
        # This one in other DAWs (in Maschine, specifically) this button is meant to clear the MIDI clip you're
        # on so you can record again on it without having to use a mouse to delete all of the notes on the clip before
        # recording again
        #
        # However, since the MIDI API on FL Studio doesn't allow control over the piano roll specifically, for now it will only just
        # emulate the delete button (which does the same)
        elif event.data1 == nihia.buttons.button_list.get("CLEAR"):
            event.handled = True
            ui.delete()
        
        # Loop button (toggles loop recording on/off)
        elif event.data1 == nihia.buttons.button_list.get("LOOP"):
            event.handled = True
            transport.globalTransport(midi.FPT_LoopRecord, 1)

        # Metronome button
        elif event.data1 == nihia.buttons.button_list.get("METRO"):
            event.handled = True
            transport.globalTransport(midi.FPT_Metronome, 1)
        
        # Tempo button
        elif event.data1 == nihia.buttons.button_list.get("TEMPO"):
            event.handled = True
            transport.globalTransport(midi.FPT_TapTempo, 1)

        # Undo button
        elif event.data1 == nihia.buttons.button_list.get("UNDO"):
            event.handled = True
            general.undoUp()
        
        # Redo button
        elif event.data1 == nihia.buttons.button_list.get("REDO"):
            event.handled = True
            general.undoDown()
   
        # Quantize button
        elif (event.data1 == nihia.buttons.button_list.get("QUANTIZE")):
            event.handled = True
            channels.quickQuantize(channels.selectedChannel(), config.QUANTIZE_MODE)

        # 4D Encoder +/-
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_GENERAL"):
            event.handled = True
            
            # Playback jogging
            transport.setSongPos(transport.getSongPos(midi.SONGLENGTH_S) + nihia.convertMidiValueToSignedInteger(event.data2), midi.SONGLENGTH_S)
        
        # 4D Encoder +/- (selected track volume)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_VOLUME_SELECTED"):
            event.handled = True
            value = nihia.convertMidiValueToNormalizedFloat(event.data2) * config.ENCODER_INCREMENTS_VOL
            mixer.setTrackVolume(mixer.trackNumber(), mixer.getTrackVolume(mixer.trackNumber()) + value)
        
        # 4D Encoder +/- (selected track pan)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_PAN_SELECTED"):
            event.handled = True
            value = nihia.convertMidiValueToNormalizedFloat(event.data2) * config.ENCODER_INCREMENTS_PAN
            mixer.setTrackPan(mixer.trackNumber(), mixer.getTrackPan(mixer.trackNumber()) + value)
        
        # 4D Encoder button
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON"):
            event.handled = True

            # Open and close plugin window for the currently selected plugin on the channel rack
            if ui.getFocused(midi.widChannelRack) == True:
                channels.showEditor(channels.selectedChannel(), 1)
            elif ui.getFocused(5) == True:
                channels.showEditor(channels.selectedChannel(), 0)
            else:
                ui.enter()
        
        # 4D Encoder button (shifted)
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_BUTTON_SHIFTED"):
            event.handled = True
            transport.globalTransport(midi.FPT_Menu, 1)

        # Knobs
        # Normal knobs (volume adjustment)
        elif nihia.mixer.knobs[0][0] <= event.data1 <= nihia.mixer.knobs[0][7]:
            event.handled = True
            value = nihia.convertMidiValueToNormalizedFloat(event.data2) * config.KNOB_INCREMENTS_VOL 
            self.adjustMixer(event.data1 - nihia.mixer.knobs[0][0], "VOLUME", value)
        
        # Shifted knobs (pan adjustment)
        elif nihia.mixer.knobs[1][0] <= event.data1 <= nihia.mixer.knobs[1][7]:
            event.handled = True
            value = nihia.convertMidiValueToNormalizedFloat(event.data2) * config.KNOB_INCREMENTS_PAN
            self.adjustMixer(event.data1 - nihia.mixer.knobs[1][0], "PAN", value)

    def OnIdle(self):
        # Updates the LED of the CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)
        if ui.getFocused(midi.widPianoRoll) != self.CLEAR:
            self.CLEAR = ui.getFocused(midi.widPianoRoll)
            nihia.buttons.setLight("CLEAR", ui.getFocused(midi.widPianoRoll))

    def OnRefresh(self, flag):
        # LEDs update
        if flag == midi.HW_Dirty_LEDs:
            # PLAY button
            if transport.isPlaying() != self.PLAY:
                self.PLAY = transport.isPlaying()

                # Handle transport.isPlaying() exception returning 2 when recording countdown is happening
                if transport.isPlaying() == 2:
                    nihia.buttons.setLight("PLAY", 0)
                else:
                    nihia.buttons.setLight("PLAY", transport.isPlaying())

            # STOP button
            if (not transport.isPlaying()) != self.STOP:
                self.STOP =  (not transport.isPlaying())

                # Handle transport.isPlaying() exception returning 2 when recording countdown is happening
                if transport.isPlaying() == 2:
                    nihia.buttons.setLight("STOP", 0)
                else:
                    nihia.buttons.setLight("STOP", (not transport.isPlaying()))

            # COUNT-IN button
            if ui.isPrecountEnabled() != self.COUNT_IN:
                self.COUNT_IN = ui.isPrecountEnabled()
                nihia.buttons.setLight("COUNT_IN", ui.isPrecountEnabled())
            
            # CLEAR button (moved to OnIdle, since OnRefresh isn't called when focused window changes)

            # LOOP button
            if ui.isLoopRecEnabled() != self.LOOP:
                self.LOOP = ui.isLoopRecEnabled()
                nihia.buttons.setLight("LOOP", ui.isLoopRecEnabled())

            # METRO button
            if ui.isMetronomeEnabled() != self.METRO:
                self.METRO = ui.isMetronomeEnabled()
                nihia.buttons.setLight("METRO", ui.isMetronomeEnabled())

            # UNDO button
            if self.getUndoStatus() != self.UNDO:
                self.UNDO = self.getUndoStatus()
                nihia.buttons.setLight("UNDO", self.getUndoStatus())

            # REDO button
            if self.getRedoStatus() != self.REDO:
                self.REDO = self.getRedoStatus()
                nihia.buttons.setLight("REDO", self.getRedoStatus())

            # QUANTIZE button is set on init and permanently on

            # AUTO button is set on init and permanently on

            # MUTE button
            if mixer.isTrackMuted(mixer.trackNumber()) != self.MUTE_SELECTED:
                self.MUTE_SELECTED = mixer.isTrackMuted(mixer.trackNumber())
                nihia.buttons.setLight("MUTE_SELECTED", mixer.isTrackMuted(mixer.trackNumber()))
            
            # SOLO button
            if mixer.isTrackSolo(mixer.trackNumber()) != self.SOLO_SELECTED:
                self.SOLO_SELECTED = mixer.isTrackSolo(mixer.trackNumber())
                nihia.buttons.setLight("SOLO_SELECTED", mixer.isTrackSolo(mixer.trackNumber()))

        # Undocumented flag for recording state changes
        elif flag == 260:
            # REC button
            if transport.isRecording() != self.REC:
                self.REC = transport.isRecording()
                nihia.buttons.setLight("REC", transport.isRecording())

        else:
            self.mixer.update()

    def OnDirtyMixerTrack(self, index):
        if index == -1:
            self.mixer.need_full_refresh = True

        # Queue an update for a specific track
        elif self.mixer.trackFirst <= index < self.mixer.trackFirst + self.mixer.trackLimit:
            self.mixer.need_refresh += [index - self.mixer.trackFirst]

    def OnUpdateMeters(self):           # Intended to be declared by child
        raise NotImplementedError()

    def adjustMixer(self, knob: int, dataType: str, value: int):
        """ Dynamically maps the physical knob to the right mixer track depending on the track group the selected track belongs to, and adjusts the parameter.
        ### Parameters

        - knob: From 0 to 7. Number of the physical knob you are mapping.
        
        - dataType: The parameter you are going to adjust. Can be PAN or VOLUME.

        """

        if (self.mixer.trackGroup == 15) and (knob == 6 or knob == 7): # Control 15th group exception
            return

        else:
            track = self.mixer.getTrackFromTrackOffset(knob)
            if dataType == "VOLUME":
                    mixer.setTrackVolume(track, mixer.getTrackVolume(track) + value)

            elif dataType == "PAN":
                    mixer.setTrackPan(track, mixer.getTrackPan(track) + value)

    def getUndoStatus(self):
        """ Helper function to set the light on the UNDO button. """

        # general.getUndoHistoryPos() is broken, returning always the same result
        # as general.getUndoHistoryCount()
        # Function is a stub
        """
        undoLength = general.getUndoHistoryCount()
        undoPosition = general.getUndoHistoryPos()

        # In FL Studio, the first (most ancient) undo point in the history seems to have
        # the greatest number and the entire history as an index of 1
        if undoPosition == undoLength:
            status = 0
        else:
            status = 1

        return status
        """

        return 1

    def getRedoStatus(self):
        """ Helper function to set the light on the REDO button. """

        # general.getUndoHistoryPos() is broken, returning always the same result
        # as general.getUndoHistoryCount()
        # Function is a stub
        """
        undoLength = general.getUndoHistoryCount()
        undoPosition = general.getUndoHistoryPos()

        # In FL Studio, the first (most ancient) undo point in the history seems to have
        # the greatest number and the entire history as an index of 1
        if general.getUndoHistoryPos() == 1:
            status = 0
        else:
            status = 1
        
        return status
        """

        return 1

class A_Series(Core):
    """ Controller code specific to A/M-Series keyboards. """
    def OnMidiMsg(self, event):
        super().OnMidiMsg(event)
        # Mute button - A-Series
        if event.data1 == nihia.buttons.button_list.get("MUTE_SELECTED"):
            event.handled = True
            mixer.muteTrack(mixer.trackNumber())

        # Solo button - A-Series
        elif event.data1 == nihia.buttons.button_list.get("SOLO_SELECTED"):
            event.handled = True
            mixer.soloTrack(mixer.trackNumber())
        
        # 4D Encoder up/down
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_Y_A"):
            event.handled = True
            channels.selectOneChannel(channels.selectedChannel() + nihia.convertMidiValueToSignedInteger(event.data2))

        # 4D Encoder left/right
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_X_A"):
            event.handled = True
            mixer.setTrackNumber(mixer.trackNumber() + nihia.convertMidiValueToSignedInteger(event.data2))
            ui.scrollWindow(midi.widMixer, mixer.trackNumber())
            self.mixer.setGroupToCurrentTrack()

class S_Series(Core):
    """ Controller code specific to S-Series MK2/MK3 keyboards. """

    def OnInit(self):
        super().OnInit()
        # Tells to FL Studio the device has peak meters
        device.setHasMeters()

        # Sets the lights of the 4D Encoder and navigation buttons on S-Series keyboards
        self.update4DEncoderNavigation()
        self.updateGroupNavigation()

    def OnMidiMsg(self, event):
        super().OnMidiMsg(event)
        # Mute button - S-Series
        if event.data1 == nihia.buttons.button_list.get("MUTE"):
            event.handled = True
            self.mixerMuteSoloHandler("MUTE", event.data2)

        # Solo button - S-Series
        elif event.data1 == nihia.buttons.button_list.get("SOLO"):
            event.handled = True
            self.mixerMuteSoloHandler("SOLO", event.data2)
        
        # 4D Encoder up/down
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_Y_S"):
            event.handled = True
            channels.selectOneChannel(channels.selectedChannel() + nihia.convertMidiValueToSignedInteger(event.data2))
            self.update4DEncoderNavigation()

        # 4D Encoder left/right
        elif event.data1 == nihia.buttons.button_list.get("ENCODER_X_S"):
            event.handled = True
            mixer.setTrackNumber(mixer.trackNumber() + nihia.convertMidiValueToSignedInteger(event.data2))
            ui.scrollWindow(midi.widMixer, mixer.trackNumber())
            self.mixer.setGroupToCurrentTrack()
            self.update4DEncoderNavigation()
            self.updateGroupNavigation()

        elif event.data1 == nihia.buttons.button_list.get("NAVIGATE_BANKS"):
            event.handled = True
            self.mixer.moveGroup(nihia.convertMidiValueToSignedInteger(event.data2))
            trackOffset = 0 if nihia.convertMidiValueToSignedInteger(event.data2) < 0 else 7
            scrollTrack = self.mixer.getTrackFromTrackOffset(trackOffset)
            scrollTrack = max(1, scrollTrack) #exclude Master (index 0) as it is always visible
            ui.scrollWindow(midi.widMixer, scrollTrack)
            self.updateGroupNavigation()

    def OnUpdateMeters(self):
        self.mixer.sendPeakInfo()

    def updateGroupNavigation(self):
        prevGroupAvailable = self.mixer.trackGroup > 0
        nextGroupAvailable = self.mixer.trackGroup < 15
        groupNav = prevGroupAvailable | (nextGroupAvailable << 1)
        nihia.buttons.setLight("NAVIGATE_BANKS", groupNav)

    def update4DEncoderNavigation(self):
        prevTrackAvailable = mixer.trackNumber() > 0
        nextTrackAvailable = mixer.trackNumber() < (mixer.trackCount() - 2)
        trackNav = prevTrackAvailable | (nextTrackAvailable << 1)

        prevChannelAvailable = channels.selectedChannel() > 0
        nextChannelAvailable = channels.selectedChannel() < (channels.channelCount() - 1)
        channelNav = prevChannelAvailable | (nextChannelAvailable << 1)

        nihia.buttons.setLight("ENCODER_X_S", trackNav)
        nihia.buttons.setLight("ENCODER_Y_S", channelNav)

    def mixerMuteSoloHandler(self, action: str, targetTrack: int):
        """ Handles the way mixer and solo commands are sent from S-Series keyboards. 
        ### Parameters
        
        - action: MUTE or SOLO.
        - targetTrack: From 0 to 7, the track that the user is trying to mute or solo from the ones showing on the device's mixer.
        - selectedTrack: The currently selected track that is used to calculate the track group.
        """

        track = self.mixer.getTrackFromTrackOffset(targetTrack)

        # Adjusts the correct property of the right track
        if action == "MUTE":
            mixer.muteTrack(track)

        elif action == "SOLO":
            mixer.soloTrack(track)
