# name=SSL 360 UF8/UF1
# url=
# supportedDevices=
# version 2025.2

import patterns
import mixer
import device
import transport
import arrangement
import general
import launchMapPages
import playlist
import ui
import channels

import midi
import utils
import time

MackieCU_KnobOffOnT = [(midi.MIDI_CONTROLCHANGE + (1 << 6)) << 16, midi.MIDI_CONTROLCHANGE + ((0xB + (2 << 4) + (1 << 6)) << 16)];
MackieCU_nFreeTracks = 64

#const
MackieCUNote_Undo = 0x3C
MackieCUNote_Pat = 0x3E
MackieCUNote_Mix = 0x3F
MackieCUNote_Chan = 0x40
MackieCUNote_Tempo = 0x41
MackieCUNote_Free1 = 0x42
MackieCUNote_Free2 = 0x43
MackieCUNote_Free3 = 0x44
MackieCUNote_Free4 = 0x45
MackieCUNote_Marker = 0x48
MackieCUNote_Zoom = 0x64
MackieCUNote_Move = 0x46
MackieCUNote_Window = 0x4C
# Mackie CU pages
MackieCUPage_Pan = 0
MackieCUPage_Stereo = 1
MackieCUPage_Sends = 2
MackieCUPage_FX = 3
MackieCUPage_EQ = 4
MackieCUPage_Free = 5

ExtenderLeft = 0
ExtenderRight = 1

OffOnStr = ('off', 'on')

class TMackieCol:
	def __init__(self):
		self.TrackNum = 0
		self.BaseEventID = 0
		self.KnobEventID = 0 
		self.KnobPressEventID = 0
		self.KnobResetEventID = 0
		self.KnobResetValue = 0
		self.KnobMode = 0
		self.KnobCenter = 0
		self.SliderEventID = 0
		self.Peak = 0
		self.Tag = 0
		self.SliderName = ""
		self.KnobName = ""
		self.LastValueIndex = 0
		self.ZPeak = False
		self.Dirty = False
		self.KnobHeld = False


class TMackieCU():
	def __init__(self):
		self.LastMsgLen =  0x37
		self.TempMsgT = ["", ""]
		self.LastTimeMsg = bytearray(10)

		self.Shift = False
		self.TempMsgDirty = False
		self.JogSource = 0
		self.TempMsgCount = 0
		self.SliderHoldCount = 0
		self.FirstTrack = 0
		self.FirstTrackT = [0, 0]
		self.ColT = [0 for x in range(9)]
		for x in range(0, 9):
			self.ColT[x] = TMackieCol()
			
		self.ColTP = [0 for x in range(9)]
		for x in range(0, 9):
			self.ColTP[x] = TMackieCol()

		self.FreeCtrlT = [0 for x in range(MackieCU_nFreeTracks - 1 + 2)]  # 64+1 sliders
		self.Clicking = False
		self.Scrub = False
		self.Flip = False
		self.MeterMode = 0
		self.CurMeterMode = 0
		self.Page = 0
		self.SmoothSpeed = 0
		self.MeterMax = 0
		self.ActivityMax = 0

		self.MackieCU_PageNameT = ('Panning (press to     reset)', 'Stereo separ. (press to     reset)',  'Sends  for    select.track (press  to     enable)', 'Effects for selected track (press to enable)', 'EQ for select.track (press  to     reset)',  'Lotsa  free   ctrls')
		self.MackieCU_MeterModeNameT = ('Horizontal meters mode', 'Vertical meters mode', 'Disabled meters mode')
		self.MackieCU_ExtenderPosT = ('left', 'right')

		self.FreeEventID = 400
		self.ArrowsStr = chr(0x7F) + chr(0x7E) + chr(0x32)
		self.AlphaTrack_SliderMax = round(13072 * 16000 / 12800)
		self.ExtenderPos = ExtenderRight

	def OnInit(self):

		self.FirstTrackT[0] = 1
		self.FirstTrack = 0
		self.SmoothSpeed = 469
		self.Clicking = True

		device.setHasMeters()
		self.LastTimeMsg = bytearray(10)

		for m in range (0, len(self.FreeCtrlT)):
			self.FreeCtrlT[m] = 8192 # default free faders to center
		if device.isAssigned():
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x0C, 1, 0xF7]))

		self.SetBackLight(2) # backlight timeout to 2 minutes
		self.UpdateClicking()
		self.UpdateMeterMode()

		self.SetPage(self.Page)
		self.UpdateExtender()
		self.OnSendTempMsg('Linked to ' + ui.getProgTitle() + ' (' + ui.getVersion() + ')', 2000);
		print('OnInit ready')
		
	def OnInitAll(self):
		self.UpdateExtender()

	def OnDeInit(self):

		if device.isAssigned():

			for m in range(0, 8):
				device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x20, m, 0, 0xF7]))

			if ui.isClosing():
				self.SendMsg(ui.getProgTitle() + ' session closed at ' + time.ctime(time.time()), 0)
			else:
				self.SendMsg('')

			self.SendMsg('', 1)
			self.SendTimeMsg('')
			self.SendAssignmentMsg('  ')

		print('OnDeInit ready')

	def OnDirtyMixerTrack(self, SetTrackNum):

		for m in range(0, len(self.ColT)):
			if (self.ColT[m].TrackNum == SetTrackNum) | (SetTrackNum == -1):
				self.ColT[m].Dirty = True

	def OnRefresh(self, flags):

		if flags & midi.HW_Dirty_Mixer_Sel:
			self.UpdateMixer_Sel()

		if flags & midi.HW_Dirty_Mixer_Display:
			self.UpdateTextDisplay()
			self.UpdateColT()

		if flags & midi.HW_Dirty_Mixer_Controls:
			for n in range(0, len(self.ColT)):
				if self.ColT[n].Dirty:
					self.UpdateCol(n)

		# LEDs
		if flags & midi.HW_Dirty_LEDs:
			self.UpdateLEDs()

	def TrackSel(self, Index, Step):

		Index = 2 - Index
		device.baseTrackSelect(Index, Step)
		if Index == 0:
			s = channels.getChannelName(channels.channelNumber())
			self.OnSendTempMsg(self.ArrowsStr + 'Channel: ' + s, 500);
		elif Index == 1:
			self.OnSendTempMsg(self.ArrowsStr + 'Mixer track: ' + mixer.getTrackName(mixer.trackNumber()), 500);
		elif Index == 2:
			s = patterns.getPatternName(patterns.patternNumber())
			self.OnSendTempMsg(self.ArrowsStr + 'Pattern: ' + s, 500);

	def Jog(self, event):

		if self.JogSource == 0:
			transport.globalTransport(midi.FPT_Jog + int(self.Shift ^ self.Scrub), event.outEv, event.pmeFlags) # relocate
		elif self.JogSource == MackieCUNote_Move:
			transport.globalTransport(midi.FPT_MoveJog, event.outEv, event.pmeFlags)
		elif self.JogSource == MackieCUNote_Marker:
			if self.Shift:
				s = 'Marker selection'
			else:
				s = 'Marker jump'
			if event.outEv != 0:
				if transport.globalTransport(midi.FPT_MarkerJumpJog + int(self.Shift), event.outEv, event.pmeFlags) == midi.GT_Global:
					s = ui.getHintMsg()
			self.OnSendTempMsg(self.ArrowsStr + s, 500)

		elif self.JogSource == MackieCUNote_Undo:
			if event.outEv == 0:
				s = 'Undo history'
			elif transport.globalTransport(midi.FPT_UndoJog, event.outEv, event.pmeFlags) == midi.GT_Global:
				s = ui.GetHintMsg()
			self.OnSendTempMsg(self.ArrowsStr + s + ' (level ' + general.getUndoLevelHint() + ')', 500)

		elif self.JogSource == MackieCUNote_Zoom:
			if event.outEv != 0:
				transport.globalTransport(midi.FPT_HZoomJog + int(self.Shift), event.outEv, event.pmeFlags)

		elif self.JogSource == MackieCUNote_Window:

			if event.outEv != 0:
				transport.globalTransport(midi.FPT_WindowJog, event.outEv, event.pmeFlags)
			s = ui.getFocusedFormCaption()
			if s != "":
				self.OnSendTempMsg(self.ArrowsStr + 'Current window: ' + s, 500)

		elif (self.JogSource == MackieCUNote_Pat) | (self.JogSource == MackieCUNote_Mix) | (self.JogSource == MackieCUNote_Chan):
			self.TrackSel(self.JogSource - MackieCUNote_Pat, event.outEv)

		elif self.JogSource == MackieCUNote_Tempo:
			if event.outEv != 0:
				channels.processRECEvent(midi.REC_Tempo, channels.incEventValue(midi.REC_Tempo, event.outEv, midi.EKRes), midi.PME_RECFlagsT[int(event.pmeFlags & midi.PME_LiveInput != 0)] - midi.REC_FromMIDI)
			self.OnSendTempMsg(self.ArrowsStr + 'Tempo: ' + mixer.getEventIDValueString(midi.REC_Tempo, mixer.getCurrentTempo()), 500)

		elif self.JogSource in [MackieCUNote_Free1, MackieCUNote_Free2, MackieCUNote_Free3, MackieCUNote_Free4]:
			# CC
			event.data1 = 390 + self.JogSource - MackieCUNote_Free1

			if event.outEv != 0:
				event.isIncrement = 1
				s = chr(0x7E + int(event.outEv < 0))
				self.OnSendTempMsg(self.ArrowsStr + 'Free jog ' + str(event.data1) + ': ' + s, 500)
				device.processMIDICC(event)
				return
			else:
				self.OnSendTempMsg(self.ArrowsStr + 'Free jog ' + str(event.data1), 500)


	def OnMidiMsg(self, event):

		ArrowStepT = [2, -2, -1, 1]
		CutCopyMsgT = ('Cut', 'Copy', 'Paste', 'Insert', 'Delete')  #FPT_Cut..FPT_Delete

		if (event.midiId == midi.MIDI_CONTROLCHANGE):
			if (event.midiChan == 0):
				event.inEv = event.data2
				if event.inEv >= 0x40:
					event.outEv = -(event.inEv - 0x40)
				else:
					event.outEv = event.inEv

				if event.data1 == 0x3C:
					self.Jog(event)
					event.handled = True
					# knobs
				elif event.data1 in [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17]:
					r = utils.KnobAccelToRes2(event.outEv)  #todo outev signof
					Res = r * (1 / (40 * 2.5))
					if self.Page == MackieCUPage_Free:
						i = event.data1 - 0x10
						self.ColT[i].Peak = self.ActivityMax
						event.data1 = self.ColT[i].BaseEventID + int(self.ColT[i].KnobHeld)
						event.isIncrement = 1
						s = 'Free' + str(event.data1)
						BaseID = midi.EncodeRemoteControlID(device.getPortNumber(), 0, 0)
						eventId = device.findEventID(BaseID + event.data1, 0)
						if utils.Limited(eventId, 0, midi.MaxInt):
							s = device.getLinkedValueString(eventId)
						self.SendTrackMsg(self.ColT[i].TrackNum, s) 
						device.processMIDICC(event)
						device.hardwareRefreshMixerTrack(self.ColT[i].TrackNum)
					else:
						self.SetKnobValue(event.data1 - 0x10, event.outEv, Res)
						event.handled = True
				else:
					event.handled = False # for extra CCs in emulators
			else:
				event.handled = False # for extra CCs in emulators

		elif event.midiId == midi.MIDI_PITCHBEND: # pitch bend (faders)

			if event.midiChan <= 8:
				event.inEv = event.data1 + (event.data2 << 7)
				event.outEv = int(event.inEv / 16383 * midi.FromMIDI_Max);
				event.inEv -= 0x2000

				if self.Page == MackieCUPage_Free:
					self.ColT[event.midiChan].Peak = self.ActivityMax
					self.FreeCtrlT[self.ColT[event.midiChan].TrackNum] = event.data1 + (event.data2 << 7)
					device.hardwareRefreshMixerTrack(self.ColT[event.midiChan].TrackNum)
					event.data1 = self.ColT[event.midiChan].BaseEventID + 7
					track = event.midiChan
					event.midiChan = 0
					event.midiChanEx = event.midiChanEx & (not 0xF)
					s = 'Free' + str(event.data1)
					BaseID = midi.EncodeRemoteControlID(device.getPortNumber(), 0, 0)
					eventId = device.findEventID(event.data1, 0)
					if utils.Limited(eventId, 0, midi.MaxInt):
						s = device.getLinkedValueString(eventId)
					self.SendTrackMsg(track, s)

					device.processMIDICC(event)
				elif self.ColT[event.midiChan].SliderEventID >= 0:
					# slider (mixer track volume)
					event.handled = True
					mixer.automateEvent(self.ColT[event.midiChan].SliderEventID, self.AlphaTrack_SliderToLevel(event.inEv + 0x2000), midi.REC_MIDIController, self.SmoothSpeed)
					# hint
					#n = mixer.getAutoSmoothEventValue(self.ColT[event.midiChan].SliderEventID)
					#s = mixer.getEventIDValueString(self.ColT[event.midiChan].SliderEventID, n)
					#if s != '':
					#	s = ': ' + s
					#self.OnSendTempMsg(self.ColT[event.midiChan].SliderName + s, 500)
                    

		elif (event.midiId == midi.MIDI_NOTEON) | (event.midiId == midi.MIDI_NOTEOFF):  # NOTE
			if event.midiId == midi.MIDI_NOTEON:
				# slider hold
				if event.data1 in [0x68, 0x69, 0x70]:
					self.SliderHoldCount += -1 + (int(event.data2 > 0) * 2)

				if (event.pmeFlags & midi.PME_System != 0):
					# F1..F8
					if self.Shift & (event.data1 in [0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D]):
						transport.globalTransport(midi.FPT_F1 - 0x36 + event.data1, int(event.data2 > 0) * 2, event.pmeFlags)
						event.data1 = 0xFF

					if event.data1 == 0x34: # display mode
						if event.data2 > 0:
							if self.Shift:
								self.ExtenderPos = abs(self.ExtenderPos - 1)
								self.FirstTrackT[self.FirstTrack] = 1
								self.UpdateExtender()
								self.OnSendTempMsg('Extender on ' + self.MackieCU_ExtenderPosT[self.ExtenderPos], 1500)
							else:
								self.MeterMode = (self.MeterMode + 1) % 3
								self.OnSendTempMsg(self.MackieCU_MeterModeNameT[self.MeterMode])
								self.UpdateMeterMode()
								device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16) )
					elif event.data1 == 0x35: # time format
						if event.data2 > 0:
							ui.setTimeDispMin()
					elif (event.data1 == 0x2E) | (event.data1 == 0x2F): # mixer bank
						if event.data2 > 0:
							track = utils.Limited(self.FirstTrackT[self.FirstTrack] - 8 + int(event.data1 == 0x2F) * 16, 0, 500) 
							self.SetFirstTrack(track)
							mixer.setTrackNumber(track, 1)
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16))
							self.UpdateExtender()
					elif (event.data1 == 0x30) | (event.data1 == 0x31):
						if event.data2 > 0:
							self.SetFirstTrack(self.FirstTrackT[self.FirstTrack] - 1 + int(event.data1 == 0x31) * 2)
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16) )
							self.UpdateExtender()
					elif event.data1 == 0x32: # self.Flip
						if event.data2 > 0:
							self.Flip = not self.Flip
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16))
							self.UpdateColT()
							self.UpdateLEDs()
					elif event.data1 == 0x33: # smoothing
						if event.data2 > 0:
							self.SmoothSpeed = int(self.SmoothSpeed == 0) * 469
							self.UpdateLEDs()
							self.OnSendTempMsg('Control smoothing ' + OffOnStr[int(self.SmoothSpeed > 0)])
					elif event.data1 == 0x65: # self.Scrub
						if event.data2 > 0:
							self.Scrub = not self.Scrub
							self.UpdateLEDs()
							# jog sources
					elif event.data1 in [MackieCUNote_Undo, MackieCUNote_Pat, MackieCUNote_Mix, MackieCUNote_Chan, MackieCUNote_Tempo, MackieCUNote_Free1, MackieCUNote_Free2, MackieCUNote_Free3, MackieCUNote_Free4, MackieCUNote_Marker, MackieCUNote_Zoom, MackieCUNote_Move, MackieCUNote_Window]:
						# update jog source
						self.SliderHoldCount +=  -1 + (int(event.data2 > 0) * 2)
						if event.data1 in [MackieCUNote_Zoom, MackieCUNote_Window]:
							device.directFeedback(event)
						if event.data2 == 0:
							if self.JogSource == event.data1:
								self.SetJogSource(0)
						else:
							self.SetJogSource(event.data1)
							event.outEv = 0
							self.Jog(event) # for visual feedback

					elif event.data1 in [0x60, 0x61, 0x62, 0x63]: # arrows
						if self.JogSource == 0:
							transport.globalTransport(midi.FPT_Up - 0x60 + event.data1, int(event.data2 > 0) * 2, event.pmeFlags)
						else:
							if event.data2 > 0:
								event.inEv = ArrowStepT[event.data1 - 0x60]
								event.outEv = event.inEv
								self.Jog(event)

					elif event.data1 in [0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D]: # self.Page
						self.SliderHoldCount +=  -1 + (int(event.data2 > 0) * 2)
						if event.data2 > 0:
							n = event.data1 - 0x28
							self.OnSendTempMsg(self.MackieCU_PageNameT[n], 500)
							self.SetPage(n)
							device.dispatch(0, midi.MIDI_NOTEON + (event.data1 << 8) + (event.data2 << 16) )

					elif event.data1 == 0x54: # self.Shift
						self.Shift = event.data2 > 0
						device.directFeedback(event)

					elif event.data1 == 0x55: # open audio editor in current mixer track
						device.directFeedback(event)
						if event.data2 > 0:
							ui.launchAudioEditor(False, '', mixer.trackNumber(), 'AudioLoggerTrack.fst', '')
							self.OnSendTempMsg('Audio  editor ready')

					elif event.data1 == 0x57: # metronome/button self.Clicking
						if event.data2 > 0:
							if self.Shift:
								self.Clicking = not self.Clicking
								self.UpdateClicking()
								self.OnSendTempMsg('self.Clicking ' + OffOnStr[self.Clicking])
							else:
								transport.globalTransport(midi.FPT_Metronome, 1, event.pmeFlags)

					elif event.data1 == 0x58: # precount
						if event.data2 > 0:
							transport.globalTransport(midi.FPT_CountDown, 1, event.pmeFlags)

					elif event.data1 in [0x36, 0x37, 0x38, 0x39, 0x3A]: # cut/copy/paste/insert/delete
						transport.globalTransport(midi.FPT_Cut + event.data1 - 0x36, int(event.data2 > 0) * 2, event.pmeFlags)
						if event.data2 > 0:
							self.OnSendTempMsg(CutCopyMsgT[midi.FPT_Cut + event.data1 - 0x36 - 50])

					elif (event.data1 == 0x5B) | (event.data1 == 0x5c) : # << >>
						if self.Shift:
							if event.data2 == 0:
								v2 = 1
							elif event.data1 == 0x5B:
								v2 = 0.5
							else:
								v2 = 2
							transport.setPlaybackSpeed(v2)
						else:
							transport.globalTransport(midi.FPT_Rewind + int(event.data1 == 0x5C), int(event.data2 > 0) * 2, event.pmeFlags)
						device.directFeedback(event)

					elif event.data1 == 0x5D: # stop
						transport.globalTransport(midi.FPT_Stop, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x5E: # play
						transport.globalTransport(midi.FPT_Play, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x5F: # record
						transport.globalTransport(midi.FPT_Record, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x5A: # song/loop
						transport.globalTransport(midi.FPT_Loop, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x59: # mode
						transport.globalTransport(midi.FPT_Mode, int(event.data2 > 0) * 2, event.pmeFlags)
						device.directFeedback(event)

					elif event.data1 == 0x56: # snap
						if self.Shift:
							if event.data2 > 0:
								transport.globalTransport(midi.FPT_SnapMode, 1, event.pmeFlags)
						else:
							transport.globalTransport(midi.FPT_Snap, int(event.data2 > 0) * 2, event.pmeFlags)

					elif event.data1 == 0x52: # ESC
						transport.globalTransport(midi.FPT_Escape + int(self.Shift) * 2, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 == 0x53: # ENTER
						transport.globalTransport(midi.FPT_Enter + int(self.Shift) * 2, int(event.data2 > 0) * 2, event.pmeFlags)
					elif event.data1 in [0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]: # knob reset
						if self.Page == MackieCUPage_Free:
							i = event.data1 - 0x20
							self.ColT[i].KnobHeld = event.data2 > 0
							if event.data2 > 0:
								self.ColT[i].Peak = self.ActivityMax
								event.data1 = self.ColT[i].BaseEventID + 2
								event.outEv = 0
								event.isIncrement = 2
								self.OnSendTempMsg('Free knob switch ' + str(event.data1), 500)
								device.processMIDICC(event)
							device.hardwareRefreshMixerTrack(self.ColT[i].TrackNum)
							return
						elif event.data2 > 0:
							n = event.data1 - 0x20
							if self.Page == MackieCUPage_Sends:
								if mixer.setRouteTo(mixer.trackNumber(), self.ColT[n].TrackNum, -1) < 0:
									self.OnSendTempMsg('Cannot send to this track')
								else:
									mixer.afterRoutingChanged()
							else:
								self.SetKnobValue(n, midi.MaxInt)

					elif (event.data1 >= 0) & (event.data1 <= 0x1F): # free hold buttons
						if self.Page == MackieCUPage_Free:
							i = event.data1 % 8
							self.ColT[i].Peak = self.ActivityMax
							event.data1 = self.ColT[i].BaseEventID + 3 + event.data1 // 8
							event.inEv = event.data2
							event.outEv = int(event.inEv > 0) * midi.FromMIDI_Max
							BaseID = midi.EncodeRemoteControlID(device.getPortNumber(), 0, 0)
							eventId = device.findEventID(BaseID + event.data1, 0)
							s = 'Free' + str(event.data1)
							if eventId != 2147483647:
								s = device.getLinkedValueString(eventId)
							self.SendTrackMsg(self.ColT[i].TrackNum, s) 
							#self.OnSendTempMsg('Free button ' + str(event.data1) + ': ' + OffOnStr[event.outEv > 0], 500)
							device.processMIDICC(event)
							device.hardwareRefreshMixerTrack(self.ColT[i].TrackNum)
							return

					if (event.pmeFlags & midi.PME_System_Safe != 0):
						if event.data1 == 0x47: # link selected channels to current mixer track
							if event.data2 > 0:
								if self.Shift:
									mixer.linkTrackToChannel(midi.ROUTE_StartingFromThis)
								else:
									mixer.linkTrackToChannel(midi.ROUTE_ToThis)
						elif event.data1 == 0x4A: # focus browser
							if event.data2 > 0:
								ui.showWindow(midi.widBrowser)

						elif event.data1 == 0x4B: # focus step seq
							if event.data2 > 0:
								ui.showWindow(midi.widChannelRack)

						elif event.data1 == 0x51: # menu
							transport.globalTransport(midi.FPT_Menu, int(event.data2 > 0) * 2, event.pmeFlags)
							if event.data2 > 0:
								self.OnSendTempMsg('Menu', 10)

						elif event.data1 == 0x3B: # tools
							transport.globalTransport(midi.FPT_ItemMenu, int(event.data2 > 0) * 2, event.pmeFlags)
							if event.data2 > 0:
								self.OnSendTempMsg('Tools', 10)

						elif event.data1 == 0x3D: # undo/redo
							if (transport.globalTransport(midi.FPT_Undo, int(event.data2 > 0) * 2, event.pmeFlags) == midi.GT_Global) & (event.data2 > 0):
								self.OnSendTempMsg(ui.getHintMsg() + ' (level ' + general.getUndoLevelHint() + ')')

						elif event.data1 in [0x4D, 0x4E, 0x4F]: # punch in/punch out/punch
							if event.data1 == 0x4F:
								n = midi.FPT_Punch
							else:
								n = midi.FPT_PunchIn + event.data1 - 0x4D
							if event.data1 >= 0x4E:
								self.SliderHoldCount +=  -1 + (int(event.data2 > 0) * 2)
							if not ((event.data1 == 0x4D) & (event.data2 == 0)):
								device.directFeedback(event)
							if (event.data1 >= 0x4E) & (event.data2 >= int(event.data1 == 0x4E)):
								if device.isAssigned():
									device.midiOutMsg((0x4D << 8) + midi.TranzPort_OffOnT[False])
							if transport.globalTransport(n, int(event.data2 > 0) * 2, event.pmeFlags) == midi.GT_Global:
								t = -1
								if n == midi.FPT_Punch:
									if event.data2 != 1:
										t = int(event.data2 != 2)
								elif event.data2 > 0:
									t = int(n == midi.FPT_PunchOut)
								if t >= 0:
									self.OnSendTempMsg(ui.getHintMsg())

						elif event.data1 == 0x49: # marker add
							if (transport.globalTransport(midi.FPT_AddMarker + int(self.Shift), int(event.data2 > 0) * 2, event.pmeFlags) == midi.GT_Global) & (event.data2 > 0):
								self.OnSendTempMsg(ui.getHintMsg())
						elif (event.data1 >= 0x18) & (event.data1 <= 0x1F): # select mixer track
							if event.data2 > 0:
								i = event.data1 - 0x18

								ui.showWindow(midi.widMixer)
								mixer.setTrackNumber(self.ColT[i].TrackNum, midi.curfxScrollToMakeVisible | midi.curfxMinimalLatencyUpdate)

						elif (event.data1 >= 0x8) & (event.data1 <= 0xF): # solo
							if event.data2 > 0:
								i = event.data1 - 0x8
								self.ColT[i].solomode = midi.fxSoloModeWithDestTracks
								if self.Shift:
									Include(self.ColT[i].solomode, midi.fxSoloModeWithSourceTracks)
								mixer.soloTrack(self.ColT[i].TrackNum, midi.fxSoloToggle, self.ColT[i].solomode)
								mixer.setTrackNumber(self.ColT[i].TrackNum, midi.curfxScrollToMakeVisible)

						elif (event.data1 >= 0x10) & (event.data1 <= 0x17): # mute
							if event.data2 > 0:
								mixer.enableTrack(self.ColT[event.data1 - 0x10].TrackNum)

						elif (event.data1 >= 0x0) & (event.data1 <= 0x7): # arm
							if event.data2 > 0:
								mixer.armTrack(self.ColT[event.data1].TrackNum)
								if mixer.isTrackArmed(self.ColT[event.data1].TrackNum):
									self.OnSendTempMsg(mixer.getTrackName(self.ColT[event.data1].TrackNum) + ' recording to ' + mixer.getTrackRecordingFileName(self.ColT[event.data1].TrackNum), 2500)
								else:
									self.OnSendTempMsg(mixer.getTrackName(self.ColT[event.data1].TrackNum) + ' unarmed')

						elif event.data1 == 0x50: # save/save new
							transport.globalTransport(midi.FPT_Save + int(self.Shift), int(event.data2 > 0) * 2, event.pmeFlags)

						event.handled = True
				else:
					event.handled = False
			else:
				event.handled = False

	def SendMsg(self, Msg, Row = 0):
		sysex = bytearray([0xF0, 0x00, 0x00, 0x66, 0x14, 0x12, (self.LastMsgLen + 1) * Row]) + bytearray(Msg.ljust(self.LastMsgLen + 1, ' '), 'utf-8')
		sysex.append(0xF7)
		device.midiOutSysex(bytes(sysex))

	# update the CU time display
	def SendTimeMsg(self, Msg):

		TempMsg = bytearray(10)
		for n in range(0, len(Msg)):
			TempMsg[n] = ord(Msg[n])

		if device.isAssigned():
			#send chars that have changed
			for m in range(0, min(len(self.LastTimeMsg), len(TempMsg))):
				#if self.LastTimeMsg[m] != TempMsg[m]:
				device.midiOutMsg(midi.MIDI_CONTROLCHANGE + ((0x49 - m) << 8) + ((TempMsg[m]) << 16))

		self.LastTimeMsg = TempMsg

	def SendAssignmentMsg(self, Msg):

		s_ansi = Msg + chr(0) #AnsiString(Msg);
		if device.isAssigned():
			for m in range(1, 3):
				device.midiOutMsg(midi.MIDI_CONTROLCHANGE + ((0x4C - m) << 8) + (ord(s_ansi[m]) << 16))

	def UpdateTempMsg(self):
		self.SendMsg(self.TempMsgT[int(self.TempMsgCount != 0)], 1)

	def OnSendTempMsg(self, Msg, Duration = 1000):

		if self.CurMeterMode == 0:
			self.TempMsgCount = (Duration // 48) + 1
		self.TempMsgT[1] = Msg
		self.TempMsgDirty = True

	def OnUpdateBeatIndicator(self, Value):

		SyncLEDMsg = [ midi.MIDI_NOTEON + (0x5E << 8), midi.MIDI_NOTEON + (0x5E << 8) + (0x7F << 16), midi.MIDI_NOTEON + (0x5E << 8) + (0x7F << 16)]

		if device.isAssigned():
			device.midiOutNewMsg(SyncLEDMsg[Value], 128)

	def UpdateTextDisplay(self):

		s1 = ''
		for m in range(0, len(self.ColT) - 1):
			s = ''
			if self.Page == MackieCUPage_Free:
				s = '  ' + utils.Zeros(self.ColT[m].TrackNum + 1, 2, ' ')
			else:
				s = mixer.getTrackName(self.ColT[m].TrackNum, 6)
			for n in range(1, 7 - len(s) + 1):
				s = s + ' '
			s1 = s1 + s

		self.SendMsg(s1, 0)

	def GetSplitMarks(self):
		s2 = '';
		for m in range(0, len(self.ColT) - 1):
			s2 = s2 + '      .'
		return s2

	def UpdateMeterMode(self):

		# force vertical (activity) meter mode for free controls self.Page
		if self.Page == MackieCUPage_Free:
			self.CurMeterMode = 1
		else:
			self.CurMeterMode = self.MeterMode

		if device.isAssigned():
			#clear peak indicators
			for m in range(0, len(self.ColT) - 1):
				device.midiOutMsg(midi.MIDI_CHANAFTERTOUCH + (0xF << 8) + (m << 12))
			# disable all meters
			for m in range (0, 8):
				device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x20, m, 0, 0xF7]))

		# reset stuff
		if self.CurMeterMode > 0:
			self.TempMsgCount = -1
		else:
			self.TempMsgCount = 500 // 48 + 1

		self.MeterMax = 0xD + int(self.CurMeterMode == 1) # $D for horizontal, $E for vertical meters
		self.ActivityMax = 0xD - int(self.CurMeterMode == 1) * 6

		# meter split marks
		if self.CurMeterMode == 0:
			self.SendMsg(self.GetSplitMarks(), 1)
		else:
			self.UpdateTextDisplay()

		if device.isAssigned():
			# horizontal/vertical meter mode
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x21, int(self.CurMeterMode > 0), 0xF7]))

			# enable all meters
			if self.CurMeterMode == 2:
				n = 1
			else:
				n = 1 + 2;
			for m  in range(0, 8):
				device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x20, m, n, 0xF7]))

	def SetPage(self, Value):

		oldPage = self.Page
		self.Page = Value

		self.FirstTrack = int(self.Page == MackieCUPage_Free)
		receiverCount = device.dispatchReceiverCount()
		if receiverCount == 0:
			self.SetFirstTrack(self.FirstTrackT[self.FirstTrack])

		if self.Page == MackieCUPage_Free:
			BaseID = midi.EncodeRemoteControlID(device.getPortNumber(), 0, self.FreeEventID + 7)
			for n in range(0, len(self.FreeCtrlT)):
				d = mixer.remoteFindEventValue(BaseID + n * 8, 1)
				if d >= 0:
					self.FreeCtrlT[n] = min(round(d * 16384), 16384)

		if (oldPage == MackieCUPage_Free) | (self.Page == MackieCUPage_Free):
			self.UpdateMeterMode()
		self.UpdateColT()
		self.UpdateLEDs()
		self.UpdateTextDisplay()
		
	def UpdateExtender(self):
		
		receiverCount = device.dispatchReceiverCount()
		if receiverCount > 0:
			if self.ExtenderPos == ExtenderLeft:
				for n in range(0, receiverCount):
					device.dispatch(n, midi.MIDI_NOTEON + (0x7F << 8) + (self.FirstTrackT[self.FirstTrack] + (n * 8) << 16))
				self.SetFirstTrack(self.FirstTrackT[self.FirstTrack] + receiverCount * 8)
			elif self.ExtenderPos == ExtenderRight:
				self.SetFirstTrack(self.FirstTrackT[self.FirstTrack])
				for n in range(0, receiverCount):
					device.dispatch(n, midi.MIDI_NOTEON + (0x7F << 8) + (self.FirstTrackT[self.FirstTrack] + ((n + 1) * 8) << 16))	

	def UpdateMixer_Sel(self):

		if self.Page !=  MackieCUPage_Free:
			if device.isAssigned():
				for m in range(0, len(self.ColT) - 1):
					device.midiOutNewMsg(((0x18 + m) << 8) + midi.TranzPort_OffOnT[self.ColT[m].TrackNum == mixer.trackNumber()], self.ColT[m].LastValueIndex + 4)

			if self.Page in [MackieCUPage_Sends, MackieCUPage_FX]:
				self.UpdateColT()

	def UpdateCol(self, Num):

		data1 = 0
		data2 = 0
		baseID = 0
		center = 0
		b = False

		if device.isAssigned():
			if self.Page == MackieCUPage_Free:
				baseID = midi.EncodeRemoteControlID(device.getPortNumber(), 0, self.ColT[Num].BaseEventID)
				# slider
				m = self.FreeCtrlT[self.ColT[Num].TrackNum]
				device.midiOutNewMsg(midi.MIDI_PITCHBEND + Num + ((m & 0x7F) << 8) + ((m >> 7) << 16), self.ColT[Num].LastValueIndex + 5)
				if Num < 8:
					# ring
					d = mixer.remoteFindEventValue(baseID + int(self.ColT[Num].KnobHeld))
					if d >= 0:
						m = 1 + round(d * 10)
					else:
						m = int(self.ColT[Num].KnobHeld) * (11 + (2 << 4))
					device.midiOutNewMsg(midi.MIDI_CONTROLCHANGE + ((0x30 + Num) << 8) + (m << 16), self.ColT[Num].LastValueIndex)
					# buttons
					for n in range(0, 4)            :
						d = mixer.remoteFindEventValue(baseID + 3 + n)
						if d >= 0:
							b = d >= 0.5
						else:
							b = False

						device.midiOutNewMsg(((n * 8 + Num) << 8) + midi.TranzPort_OffOnT[b], self.ColT[Num].LastValueIndex + 1 + n)
			else:
				sv = mixer.getEventValue(self.ColT[Num].SliderEventID)

				if Num < 8:
					# V-Pot
					center = self.ColT[Num].KnobCenter
					if self.ColT[Num].KnobEventID >= 0:
						m = mixer.getEventValue(self.ColT[Num].KnobEventID, midi.MaxInt, False)
						if center < 0:
							if self.ColT[Num].KnobResetEventID == self.ColT[Num].KnobEventID:
								center = int(m !=  self.ColT[Num].KnobResetValue)
							else:
								center = int(sv !=  self.ColT[Num].KnobResetValue)

						if self.ColT[Num].KnobMode < 2:
							data1 = 1 + round(m * (10 / midi.FromMIDI_Max))
						else:
							data1 = round(m * (11 / midi.FromMIDI_Max))
						if self.ColT[Num].KnobMode > 3:
							data1 = (center << 6)
						else:
							data1 = data1 + (self.ColT[Num].KnobMode << 4) + (center << 6)
					else:
						Data1 = 0

					device.midiOutNewMsg(midi.MIDI_CONTROLCHANGE + ((0x30 + Num) << 8) + (data1 << 16), self.ColT[Num].LastValueIndex)

					# arm, solo, mute
					device.midiOutNewMsg( ((0x00 + Num) << 8) + midi.TranzPort_OffOnBlinkT[int(mixer.isTrackArmed(self.ColT[Num].TrackNum)) * (1 + int(transport.isRecording()))], self.ColT[Num].LastValueIndex + 1)
					device.midiOutNewMsg( ((0x08 + Num) << 8) + midi.TranzPort_OffOnT[mixer.isTrackSolo(self.ColT[Num].TrackNum)], self.ColT[Num].LastValueIndex + 2)
					device.midiOutNewMsg( ((0x10 + Num) << 8) + midi.TranzPort_OffOnT[not mixer.isTrackEnabled(self.ColT[Num].TrackNum)], self.ColT[Num].LastValueIndex + 3)

				# slider
				data1 = self.AlphaTrack_LevelToSlider(sv)
				data2 = data1 & 127
				data1 = data1 >> 7
				device.midiOutNewMsg(midi.MIDI_PITCHBEND + Num + (data2 << 8) + (data1 << 16), self.ColT[Num].LastValueIndex + 5)

			Dirty = False

	def AlphaTrack_LevelToSlider(self, Value, Max = midi.FromMIDI_Max):

		return round(Value / Max * self.AlphaTrack_SliderMax)

	def AlphaTrack_SliderToLevel(self, Value, Max = midi.FromMIDI_Max):

		return min(round(Value / self.AlphaTrack_SliderMax * Max), Max)

	def UpdateColT(self):

		f = self.FirstTrackT[self.FirstTrack]
		CurID = mixer.getTrackPluginId(mixer.trackNumber(), 0)

		for m in range(0, len(self.ColT)):
			if self.Page == MackieCUPage_Free:
				# free controls
				if m == 8:
					self.ColT[m].TrackNum = MackieCU_nFreeTracks
				else:
					self.ColT[m].TrackNum = (f + m) % MackieCU_nFreeTracks

				self.ColT[m].KnobName = 'Knob ' + str(self.ColT[m].TrackNum + 1)
				self.ColT[m].SliderName = 'Slider ' + str(self.ColT[m].TrackNum + 1)

				self.ColT[m].BaseEventID = self.FreeEventID + self.ColT[m].TrackNum * 8 # first virtual CC
			else:
				self.ColT[m].KnobPressEventID = -1

				# mixer
				if m == 8:
					self.ColT[m].TrackNum = -2
					self.ColT[m].BaseEventID = midi.REC_MainVol
					self.ColT[m].SliderEventID = self.ColT[m].BaseEventID
					self.ColT[m].SliderName = 'Master Vol'
				else:
					self.ColT[m].TrackNum = midi.TrackNum_Master + ((f + m) % mixer.trackCount())
					self.ColT[m].BaseEventID = mixer.getTrackPluginId(self.ColT[m].TrackNum, 0)
					self.ColT[m].SliderEventID = self.ColT[m].BaseEventID + midi.REC_Mixer_Vol
					s = mixer.getTrackName(self.ColT[m].TrackNum)
					self.ColT[m].SliderName = s + ' - Vol'

					self.ColT[m].KnobEventID = -1
					self.ColT[m].KnobResetEventID = -1
					self.ColT[m].KnobResetValue = midi.FromMIDI_Max >> 1
					self.ColT[m].KnobName = ''
					self.ColT[m].KnobMode = 1 # parameter, pan, volume, off
					self.ColT[m].KnobCenter = -1

					if self.Page == MackieCUPage_Pan:
						self.ColT[m].KnobEventID = self.ColT[m].BaseEventID + midi.REC_Mixer_Pan
						self.ColT[m].KnobResetEventID = self.ColT[m].KnobEventID
						self.ColT[m].KnobName = ''
					elif self.Page == MackieCUPage_Stereo:
						self.ColT[m].KnobEventID = self.ColT[m].BaseEventID + midi.REC_Mixer_SS
						self.ColT[m].KnobResetEventID = self.ColT[m].KnobEventID
						self.ColT[m].KnobName = ''
					elif self.Page == MackieCUPage_Sends:
						self.ColT[m].KnobEventID = CurID + midi.REC_Mixer_Send_First + self.ColT[m].TrackNum
						s = mixer.getEventIDName(self.ColT[m].KnobEventID)
						self.ColT[m].KnobName = s
						self.ColT[m].KnobResetValue = round(12800 * midi.FromMIDI_Max / 16000)
						self.ColT[m].KnobCenter = mixer.getRouteSendActive(mixer.trackNumber(),self.ColT[m].TrackNum)
						if self.ColT[m].KnobCenter == 0:
							self.ColT[m].KnobMode = 4
						else:
							self.ColT[m].KnobMode = 2
					elif self.Page == MackieCUPage_FX:
						CurID = mixer.getTrackPluginId(mixer.trackNumber(), m)
						self.ColT[m].KnobEventID = CurID + midi.REC_Plug_MixLevel
						self.ColT[m].KnobName = mixer.getEventIDName(self.ColT[m].KnobEventID)
						self.ColT[m].KnobResetValue = midi.FromMIDI_Max

						IsValid = mixer.isTrackPluginValid(mixer.trackNumber(), m)
						IsEnabledAuto = mixer.isTrackAutomationEnabled(mixer.trackNumber(), m)
						if IsValid:
							self.ColT[m].KnobMode = 2
							self.ColT[m].KnobPressEventID = CurID + midi.REC_Plug_Mute
						else:
							self.ColT[m].KnobMode = 4
						self.ColT[m].KnobCenter = int(IsValid & IsEnabledAuto)
					elif self.Page == MackieCUPage_EQ:
						match m:
							case 0 | 3 | 6: #gain
								n = int(m / 3)
								self.ColT[m].KnobEventID = CurID + midi.REC_Mixer_EQ_Gain + n
								self.ColT[m].KnobResetEventID = self.ColT[m].KnobEventID
								self.ColT[m].KnobName = ''
								self.ColT[m].KnobResetValue = midi.FromMIDI_Max >> 1
								self.ColT[m].KnobCenter = -2
								self.ColT[m].KnobMode = 0
							case 1 | 4 | 7:  #freq
								n = int((m - 1) / 3)
								self.ColT[m].KnobEventID = CurID + midi.REC_Mixer_EQ_Freq + n
								self.ColT[m].KnobName = ''
								self.ColT[m].KnobResetValue = midi.FromMIDI_Max >> 1
								self.ColT[m].KnobCenter = -2
								self.ColT[m].KnobMode = 0
								self.ColT[m].KnobPressEventID = -2  #swap on press
								self.ColTP[m].KnobEventID = CurID + midi.REC_Mixer_EQ_Q + n
								self.ColTP[m].KnobName = ''
								self.ColTP[m].KnobResetValue = 17500
								self.ColTP[m].KnobCenter = -1
								self.ColTP[m].KnobMode = 2
							case _:
								#self.ColT[m].SliderEventID = -1
								self.ColT[m].KnobEventID = -1
								self.ColT[m].KnobMode = 4

					# self.Flip knob & slider
					if self.Flip:
						self.ColT[m].KnobEventID, self.ColT[m].SliderEventID = utils.SwapInt(self.ColT[m].KnobEventID, self.ColT[m].SliderEventID)
						s = self.ColT[m].SliderName
						self.ColT[m].SliderName = self.ColT[m].KnobName
						self.ColT[m].KnobName = s
						self.ColT[m].KnobMode = 2
						if not (self.Page in [MackieCUPage_Sends, MackieCUPage_FX, MackieCUPage_EQ]):
							self.ColT[m].KnobCenter = -1
							self.ColT[m].KnobResetValue = round(12800 * midi.FromMIDI_Max / 16000)
							self.ColT[m].KnobResetEventID = self.ColT[m].KnobEventID

			self.ColT[m].LastValueIndex = 48 + m * 6
			self.ColT[m].Peak = 0
			self.ColT[m].ZPeak = False
			self.UpdateCol(m)

	def SetKnobValue(self, Num, Value, Res = midi.EKRes):
		if (self.ColT[Num].KnobEventID >= 0) & (self.ColT[Num].KnobMode < 4):
			if Value == midi.MaxInt:
				if self.Page == MackieCUPage_FX:
					if self.ColT[Num].KnobPressEventID >= 0:

						Value = channels.incEventValue(self.ColT[Num].KnobPressEventID, 0, midi.EKRes)
						channels.processRECEvent(self.ColT[Num].KnobPressEventID, Value, midi.REC_Controller)
						s = mixer.getEventIDName(self.ColT[Num].KnobPressEventID)
						self.OnSendTempMsg(s)
					return
				elif (self.Page == MackieCUPage_EQ) & (self.ColT[Num].KnobPressEventID == -2):
					self.ColT[Num].KnobEventID, self.ColTP[Num].KnobEventID = utils.SwapInt(self.ColT[Num].KnobEventID, self.ColTP[Num].KnobEventID)
					self.ColT[Num].KnobResetValue, self.ColTP[Num].KnobResetValue = utils.SwapInt(self.ColT[Num].KnobResetValue, self.ColTP[Num].KnobResetValue)
					self.ColT[Num].KnobMode, self.ColTP[Num].KnobMode = utils.SwapInt(self.ColT[Num].KnobMode, self.ColTP[Num].KnobMode)
					return
				else:
					mixer.automateEvent(self.ColT[Num].KnobResetEventID, self.ColT[Num].KnobResetValue, midi.REC_MIDIController, self.SmoothSpeed)
			else:
				mixer.automateEvent(self.ColT[Num].KnobEventID, Value, midi.REC_Controller, self.SmoothSpeed, 1, Res)

			# hint
			n = mixer.getAutoSmoothEventValue(self.ColT[Num].KnobEventID)
			s = mixer.getEventIDValueString(self.ColT[Num].KnobEventID, n)
			#s = str(n)
			#self.OnSendTempMsg(self.ColT[Num].KnobName + s)
			self.SendTrackMsg(Num, s + ' ' + self.ColT[Num].KnobName) 
            
	def SendTrackMsg(self, Track, Value):    	
		s1 = ''
		for m in range(0, len(self.ColT) - 1):
			s = ''
			if m == Track:
				s = Value
			else:
				s = '  '
			for n in range(1, 7 - len(s) + 1):
				s = s + ' '
			s1 = s1 + s
                
		self.OnSendTempMsg(s1)                

	def SetFirstTrack(self, Value):

		if self.Page == MackieCUPage_Free:
			self.FirstTrackT[self.FirstTrack] = (Value + MackieCU_nFreeTracks) % MackieCU_nFreeTracks
			s = utils.Zeros(self.FirstTrackT[self.FirstTrack] + 1, 2, ' ')
		else:
			self.FirstTrackT[self.FirstTrack] = (Value + mixer.trackCount()) % mixer.trackCount()
			s = utils.Zeros(self.FirstTrackT[self.FirstTrack], 2, ' ')
		self.UpdateColT()
		self.SendAssignmentMsg(s)
		device.hardwareRefreshMixerTrack(-1)

	def OnUpdateMeters(self):

		if self.Page != MackieCUPage_Free:
			for m in range(0, len(self.ColT) - 1):
				self.ColT[m].Peak = max(self.ColT[m].Peak, round(mixer.getTrackPeaks(self.ColT[m].TrackNum, midi.PEAK_LR_INV)	* self.MeterMax))

	def OnIdle(self):

		# refresh meters
		if device.isAssigned():
			f = self.Page == MackieCUPage_Free
			for m in range(0,  len(self.ColT) - 1):
				self.ColT[m].Tag = utils.Limited(self.ColT[m].Peak, 0, self.MeterMax)
				self.ColT[m].Peak = 0
				if self.ColT[m].Tag == 0:
					if self.ColT[m].ZPeak:
						continue
					else:
						self.ColT[m].ZPeak = True
				else:
					self.ColT[m].ZPeak = f
				device.midiOutMsg(midi.MIDI_CHANAFTERTOUCH + (self.ColT[m].Tag << 8) + (m << 12))
		# time display
		if ui.getTimeDispMin():
			# MM.SS.CC_
			if playlist.getVisTimeBar() == -midi.MaxInt:
				s = '-   0'
			else:

				s = utils.Zeros_Strict(playlist.getVisTimeBar(), 3, ' ') 

			s = s + '.' + utils.Zeros_Strict(abs(playlist.getVisTimeStep()), 2) + '.' + utils.Zeros_Strict(playlist.getVisTimeTick(), 2)
		else:
			# BBB.BB.__.TTT
			s = utils.Zeros_Strict(playlist.getVisTimeBar(), 3, ' ') + '.' + utils.Zeros_Strict(abs(playlist.getVisTimeStep()), 2) + '.' + utils.Zeros_Strict(playlist.getVisTimeTick(), 2)
		self.SendTimeMsg(s)

		# temp message
		if self.TempMsgDirty:
			self.UpdateTempMsg()
			self.TempMsgDirty = False

		if (self.TempMsgCount > 0) & (self.SliderHoldCount <= 0)  & (not ui.isInPopupMenu()):
			self.TempMsgCount -= 1
			if self.TempMsgCount == 0:
				self.UpdateTempMsg()
				if self.CurMeterMode == 0:
					self.SendMsg(self.GetSplitMarks(), 1)

	def UpdateLEDs(self):

		if device.isAssigned():
			# stop
			device.midiOutNewMsg((0x5D << 8) + midi.TranzPort_OffOnT[transport.isPlaying() == midi.PM_Stopped], 0)
			# loop
			device.midiOutNewMsg((0x5A << 8) + midi.TranzPort_OffOnT[transport.getLoopMode() == midi.SM_Pat], 1)
			# record
			r = transport.isRecording()
			device.midiOutNewMsg((0x5F << 8) + midi.TranzPort_OffOnT[r], 2)
			# SMPTE/BEATS
			device.midiOutNewMsg((0x71 << 8) + midi.TranzPort_OffOnT[ui.getTimeDispMin()], 3)
			device.midiOutNewMsg((0x72 << 8) + midi.TranzPort_OffOnT[not ui.getTimeDispMin()], 4)
			# self.Page
			for m in range(0,  6):
			  device.midiOutNewMsg(((0x28 + m) << 8) + midi.TranzPort_OffOnT[m == self.Page], 5 + m)
			# changed flag
			device.midiOutNewMsg((0x50 << 8) + midi.TranzPort_OffOnT[general.getChangedFlag() > 0], 11)
			# metronome
			device.midiOutNewMsg((0x57 << 8) + midi.TranzPort_OffOnT[general.getUseMetronome()], 12)
			# rec precount
			device.midiOutNewMsg((0x58 << 8) + midi.TranzPort_OffOnT[general.getPrecount()], 13)
			# self.Scrub
			device.midiOutNewMsg((0x65 << 8) + midi.TranzPort_OffOnT[self.Scrub], 15)
			# use RUDE SOLO to show if any track is armed for recording
			b = 0
			for m in range(0,  mixer.trackCount()):
			  if mixer.isTrackArmed(m):
			    b = 1 + int(r)
			    break

			device.midiOutNewMsg((0x73 << 8) + midi.TranzPort_OffOnBlinkT[b], 16)
			# smoothing
			device.midiOutNewMsg((0x33 << 8) + midi.TranzPort_OffOnT[self.SmoothSpeed > 0], 17)
			# self.Flip
			device.midiOutNewMsg((0x32 << 8) + midi.TranzPort_OffOnT[self.Flip], 18)
			# snap
			device.midiOutNewMsg((0x56 << 8) + midi.TranzPort_OffOnT[ui.getSnapMode() !=  3], 19)
			# focused windows
			device.midiOutNewMsg((0x4A << 8) + midi.TranzPort_OffOnT[ui.getFocused(midi.widBrowser)], 20)
			device.midiOutNewMsg((0x4B << 8) + midi.TranzPort_OffOnT[ui.getFocused(midi.widChannelRack)], 21)


	def SetJogSource(self, Value):
		self.JogSource = Value

	def OnWaitingForInput(self):

	  self.SendTimeMsg('..........')

	def UpdateClicking(self): # switch self.Clicking for transport buttons

		if device.isAssigned():
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x0A, int(self.Clicking), 0xF7]))

	def SetBackLight(self, Minutes): # set backlight timeout (0 should switch off immediately, but doesn't really work well)

		if device.isAssigned():
			device.midiOutSysex(bytes([0xF0, 0x00, 0x00, 0x66, 0x14, 0x0B, Minutes, 0xF7]))

MackieCU = TMackieCU()

def OnInit():
	MackieCU.OnInit()
	
def OnInitAll():
	MackieCU.OnInitAll()

def OnDeInit():
	MackieCU.OnDeInit()

def OnDirtyMixerTrack(SetTrackNum):
	MackieCU.OnDirtyMixerTrack(SetTrackNum)

def OnRefresh(Flags):
	MackieCU.OnRefresh(Flags)

def OnMidiMsg(event):
	MackieCU.OnMidiMsg(event)

def OnSendTempMsg(Msg, Duration = 1000):
	MackieCU.OnSendTempMsg(Msg, Duration)

def OnUpdateBeatIndicator(Value):
	MackieCU.OnUpdateBeatIndicator(Value)

def OnUpdateMeters():
	MackieCU.OnUpdateMeters()

def OnIdle():
	MackieCU.OnIdle()

def OnWaitingForInput():
	MackieCU.OnWaitingForInput()





