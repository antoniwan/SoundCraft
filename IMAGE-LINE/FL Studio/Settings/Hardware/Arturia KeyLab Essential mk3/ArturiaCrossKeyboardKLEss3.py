import midi
import channels
import mixer

# This script contains big fonctions that can be shared with other scripts

PART_OFFSET = 0

def SetVolumeTrack(event):
    value = event.data2/127
    if event.midiId == midi.MIDI_CONTROLCHANGE  :
        event.handled = False
        if event.data1 == 105 :
            mixer.setTrackVolume(1 + (8*PART_OFFSET),value)
        elif event.data1 == 106 :
            mixer.setTrackVolume(2 + (8*PART_OFFSET),value)
        elif event.data1 == 107 :
            mixer.setTrackVolume(3 + (8*PART_OFFSET),value)
        elif event.data1 == 108 :
            mixer.setTrackVolume(4 + (8*PART_OFFSET),value)
        elif event.data1 == 109 :
            mixer.setTrackVolume(5 + (8*PART_OFFSET),value)
        elif event.data1 == 110 :
            mixer.setTrackVolume(6 + (8*PART_OFFSET),value)
        elif event.data1 == 111 :
            mixer.setTrackVolume(7 + (8*PART_OFFSET),value)
        elif event.data1 == 112 :
            mixer.setTrackVolume(8 + (8*PART_OFFSET),value)


 
def SetPanTrack(event):
    event.handled = False
    if event.data1 == 96 :
        mixer.setTrackPan(1 + (8*PART_OFFSET), (event.data2/64)-1)
    elif event.data1 == 97 :
        mixer.setTrackPan(2 + (8*PART_OFFSET), (event.data2/64)-1)
    elif event.data1 == 98 :
        mixer.setTrackPan(3 + (8*PART_OFFSET), (event.data2/64)-1)
    elif event.data1 == 99 :
        mixer.setTrackPan(4 + (8*PART_OFFSET), (event.data2/64)-1)
    elif event.data1 == 100 :
        mixer.setTrackPan(5 + (8*PART_OFFSET), (event.data2/64)-1)
    elif event.data1 == 101 :
        mixer.setTrackPan(6 + (8*PART_OFFSET), (event.data2/64)-1)
    elif event.data1 == 102 :
        mixer.setTrackPan(7 + (8*PART_OFFSET), (event.data2/64)-1)
    elif event.data1 == 103 :
        mixer.setTrackPan(8 + (8*PART_OFFSET), (event.data2/64)-1)