# name=KORG Keystage DAW
# supportedHardwareIds=42 69 01 01 00, 42 69 01 09 00


import midi
import ui
import transport
import device
import general
import mixer
import channels

CcIdPlay = 0x29
CcIdStop = 0x2A
CcIdRec = 0x2D
CcIdLoop = 0x2E
CcIdTempo = 0x2F
CcIdMetro = 0x30
CcIdUndo = 0x31
CcIdTrkN = 0x3A
CcIdTrkP = 0x3B
CcIdRew = 0x2B
CcIdFwd = 0x2C

MemberId49 = 0x01
MemberId61 = 0x09
MMID = MemberId49
GlobalMidiCh = 0xff

DevInqReply = bytes([0xF0, 0x7E, 0x00, 0x06, 0x02, 0x42, 0x69, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF7])

CurTrackName = mixer.getTrackName(mixer.trackNumber())

def IsDevInqRep(sysex):
    for i in [0, 1, 3, 4, 5, 6, 7, 14]:
        if sysex[i] != DevInqReply[i]:
            return False
    if sysex[8] != MemberId49 and sysex[8] != MemberId61:
        return False
    return True

def SetDevInfo(sysex):
    # if not IsDevInqRep(sysex):
    #     return
    global GlobalMidiCh
    global MMID
    GlobalMidiCh = sysex[2]
    MMID = sysex[8]
    print('g midi ch '+''.join([r'{:02x} '.format(GlobalMidiCh)]))
    print('member id '+''.join([r'{:02x} '.format(MMID)]))

def SendCtrlModeReq():
    print('SendCtrlModeReq')
    global GlobalMidiCh
    if (0x0f < GlobalMidiCh):
        return
    msg = bytes([0xF0, 0x42, 0x40|GlobalMidiCh, 0x00, 0x01, 0x69, MMID, 0x02, 0x00, 0x00, 0x49, 0x05, 0xF7])
    print(''.join([r'{:02x} '.format(x) for x in msg]))
    device.midiOutSysex(msg)

def SendDispMsg(trackname):
    global GlobalMidiCh
    encoded = trackname.encode('ascii', errors='ignore')
    l = len(encoded)
    if 16 < l:
        l = 16
        encoded = encoded[0:l]
    sysex = bytes([0xF0, 0x42, 0x40|GlobalMidiCh, 0x00, 0x01, 0x69, MMID, 3 + l, 0x00, 0x00, 0x28, 0, 0])
    sysex += encoded
    sysex += bytes([0xF7])
    print(''.join([r'{:02x} '.format(x) for x in sysex]))
    device.midiOutSysex(sysex)



# Function called when FL Studio is starting
def OnInit():
    print('Script for KORG Keystage')
    device.midiOutSysex(bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7]))


def OnDeInit():
    print('end: keystage')

def OnSysEx(event):
    print('onsysex')
    print(''.join([r'{:02x} '.format(x) for x in event.sysex]))
    if IsDevInqRep(event.sysex):
        SetDevInfo(event.sysex)
        SendCtrlModeReq()

def OnFirstConnect():
    print('Keystage is connected for the first time')

def OnControlChange(event):
    event.handled = False
    # print(event.data1)
    if event.data2 >= 0x40:
        if event.data1 == CcIdPlay:
            transport.start()
            event.handled = True
        elif event.data1 == CcIdStop:
            transport.stop()
            event.handled = True
        elif event.data1 == CcIdRec:
            transport.record()
            event.handled = True
        elif event.data1 == CcIdLoop:
            transport.setLoopMode()
            event.handled = True
        elif event.data1 == CcIdTempo:
            event.handled = True
        elif event.data1 == CcIdMetro:
            transport.globalTransport(midi.FPT_Metronome, 1)
            event.handled = True
        elif event.data1 == CcIdUndo:
            general.undo()
            event.handled = True
        elif event.data1 == CcIdTrkN:
            t = channels.selectedChannel()
            t = (t + 1) % (channels.channelCount(0))
            channels.selectOneChannel(t)
            print(t, channels.channelCount(0))
            event.handled = True
        elif event.data1 == CcIdTrkP:
            t = channels.selectedChannel()
            t = (t - 1) % (channels.channelCount(0))
            channels.selectOneChannel(t)
            print(t, channels.channelCount(0))
            event.handled = True
        elif event.data1 == CcIdRew:
            # print("rew")
            ui.setFocused(midi.widPlaylist)
            ui.jog(-1)
            event.handled = True
        elif event.data1 == CcIdFwd:
            # print("fwd")
            ui.setFocused(midi.widPlaylist)
            ui.jog(1)
            event.handled = True

def OnRefresh(flags):
    # print(flags)
    if flags & midi.HW_Dirty_LEDs:
        p = 0x00 # play
        s = 0x00 # stop
        r = 0x00 # rec
        l = 0x00 # loop
        str_pr = ""
        if transport.isPlaying():
            # print('playing')
            str_pr += 'playing / '
            p = 0x7F
        else :
            # print('stopped')
            str_pr += 'stopped / '
            s = 0x7F
        if transport.isRecording():
            # print('rec')
            str_pr += 'rec / '
            r = 0x7F
        else :
            # print('not rec')
            str_pr += 'not rec / '
        if transport.getLoopMode():
            # print('loop song')
            str_pr += 'loop s'
            l = 0x7F
        else :
            # print('loop pat')
            str_pr += 'loop p'
        print(str_pr)
        device.midiOutMsg(0xB0, 0, CcIdPlay, p)
        device.midiOutMsg(0xB0, 0, CcIdStop, s)
        device.midiOutMsg(0xB0, 0, CcIdRec, r)
        device.midiOutMsg(0xB0, 0, CcIdLoop, l)
        global CurTrackName
        chname = channels.getChannelName(channels.selectedChannel())
        if CurTrackName != chname:
            CurTrackName = chname
            SendDispMsg(CurTrackName)


PrevBeat = 0
def OnUpdateBeatIndicator(value):
    global PrevBeat
    if PrevBeat == 0:
        if PrevBeat != value:
            # bar/beat off -> on
            print("b on")
            device.midiOutMsg(0xB0, 0, CcIdTempo, 0x7F)
            PrevBeat = value
    else:
        if PrevBeat != value:
            if value == 0:
                #bar/beat on -> off
                print("b off")
                device.midiOutMsg(0xB0, 0, CcIdTempo, 0x00)
            PrevBeat = value
