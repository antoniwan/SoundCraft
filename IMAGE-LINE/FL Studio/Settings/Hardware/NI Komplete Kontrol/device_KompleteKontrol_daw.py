# name=Native Instruments Komplete Kontrol DAW
# url=https://forum.image-line.com/viewtopic.php?f=1994&t=233461
# supportedDevices=Komplete Kontrol DAW - 1,KONTROL S49 MK3 DAW,KONTROL S61 MK3 DAW,KONTROL S88 MK3 DAW,MIDIIN2 (KONTROL S49 MK3),MIDIIN2 (KONTROL S61 MK3),MIDIIN2 (KONTROL S88 MK3),Komplete Kontrol A DAW,Komplete Kontrol M DAW

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

import device

import midi
import utils

# Imports Native Instruments Host Integration Agent library
import nihia
from nihia import *

import midi_setup_check
import controller_definition

######################################################################################################################
# Script logic
######################################################################################################################

if midi_setup_check.settingsCheck() == 0:
    print("Detected device: ", midi_setup_check.supportedDevices.get(device.getName())[1])
    keyboard = controller_definition.S_Series()

elif midi_setup_check.settingsCheck() == 1:
    print("Detected device: ", midi_setup_check.supportedDevices.get(device.getName())[1])
    keyboard = controller_definition.A_Series()

def OnInit():
    keyboard.OnInit()

def OnDeInit():
    keyboard.OnDeInit()

def OnMidiMsg(event):
    keyboard.OnMidiMsg(event)

def OnIdle():
    keyboard.OnIdle()

def OnRefresh(flag):
    keyboard.OnRefresh(flag)

def OnDirtyMixerTrack(index):
    keyboard.OnDirtyMixerTrack(index)

def OnUpdateMeters():
    # Fix OnUpdateMeters getting called regardless of device.setHasMeters() being called
    # by the script in FL Studio 20.9
    if type(keyboard) == type(controller_definition.S_Series()):
        keyboard.OnUpdateMeters()
