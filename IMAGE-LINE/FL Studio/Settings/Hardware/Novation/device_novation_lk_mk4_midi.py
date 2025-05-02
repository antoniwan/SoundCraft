# name=Novation Launchkey MK4 MIDI
# supportedHardwareIds=00 20 29 46 01 00 00,00 20 29 45 01 00 00,00 20 29 44 01 00 00,00 20 29 43 01 00 00
from script.fl import FL
from script.midi_bypass import MidiBypass

fl = FL()
midi_bypass = MidiBypass(fl)


def OnPitchBend(eventData):
    midi_bypass.on_pitch_bend(eventData)
