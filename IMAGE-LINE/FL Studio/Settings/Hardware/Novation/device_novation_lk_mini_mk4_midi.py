# name=Novation Launchkey Mini MK4 MIDI
# supportedHardwareIds=00 20 29 42 01 00 00,00 20 29 41 01 00 00
from script.fl import FL
from script.midi_bypass import MidiBypass

fl = FL()
midi_bypass = MidiBypass(fl)


def OnPitchBend(eventData):
    midi_bypass.on_pitch_bend(eventData)
