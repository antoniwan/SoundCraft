# name=Novation Launch Control XL 3 MIDI
# supportedHardwareIds=00 20 29 48 01 00 00,00 20 29 49 01 00 00,00 20 29 4A 01 00 00,00 20 29 4B 01 00 00,00 20 29 4C 01 00 00,00 20 29 4D 01 00 00,00 20 29 4E 01 00 00,00 20 29 4F 01 00 00
from script.fl import FL
from script.midi_bypass import MidiBypass

fl = FL()
midi_bypass = MidiBypass(fl)


def OnPitchBend(eventData):
    midi_bypass.on_pitch_bend(eventData)
