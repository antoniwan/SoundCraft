
import device
import plugins
import channels
import ui
import midi
import time

from KL3Dispatch import send_to_device

from IntegrationPatchId import eIntegrationPatchId
from ParamId import eParamId

# Global variable

UNTOUCHED_PARAM = 0
TURNED_PARAM = 1
TOUCHED_PARAM = 2

ABSOLUTE_VALUE = 0
ABSOLUTE_PARAM = 0

PARAM_ID = {
    '91':1,
    '92':2,
    '94':3,
    '95':4,
    '96':5,
    '97':6,
    '102':7,
    '103':8,
    '105':1,
    '106':2,
    '107':3,
    '108':4,
    '109':5,
    '110':6,
    '111':7,
    '112':8
    }

PARAM_TOUCH_MAP = {
    '8':91,
    '9':92,
    '10':94,
    '11':95,
    '12':96,
    '13':97,
    '14':102,
    '15':103,
    '28':105,
    '29':106,
    '30':107,
    '31':108,
    '33':109,
    '34':110,
    '35':111,
    '36':112,
}
            
# KNOB_MAP = {
#     96:1,
#     97:2,
#     98:3,
#     99:4,
#     100:5,
#     101:6,
#     102:7,
#     103:8,
#     104:1,
# }

# FADER_MAP = {
#     105:1,
#     106:2,
#     107:3,
#     108:4,
#     109:5,
#     110:6,
#     111:7,
#     112:8,
#     113:1,
# }

KNOB_MAP = {
    '8':1,
    '91':1,
    '9':2,
    '92':2,
    '10':3,
    '94':3,
    '11':4,
    '95':4,
    '12':5,
    '96':5,
    '13':6,
    '97':6,
    '14':7,
    '102':7,
    '15':8,
    '103':8,
}

FADER_MAP = {
    '28':1,
    '105':1,
    '29':2,
    '106':2,
    '30':3,
    '107':3,
    '31':4,
    '108':4,
    '33':5,
    '109':5,
    '34':6,
    '110':6,
    '35':7,
    '111':7,
    '36':8,
    '112':8
}


NATIVE_PLUGIN_LIST = [
    'FLEX',
    'FPC',
    'FL Keys',
    'Sytrus',
    'GMS',
    'Harmless',
    'Harmor',
    'Morphine',
    '3x Osc',
    'Fruity DX10',
    'BassDrum'
    'Fruit kick'
    'MiniSynth'
    'PoiZone',
    'Sakura',
    'Fruity Envelope Controller',
    'Fruity Keyboard Controller',
    'Ogun',
    'BooBass',
    'SimSynth Live',
    'Autogun',
    'PLUCKED!',
    'BeepMap',
    'Toxic Biohazard',
    'Fruity Dance',
    'Drumaxx',
    'Drumpad',
    'Slicex',
    'SoundFont Player',
    'Fruity granulizer',
    'Sawer',
    'Transistor Bass',
    'Kepler'
]

NATIVE_PRESET_CONTROLLABLE_PLUGIN_LIST = [
    'FLEX',
    'FPC',
    'FL Keys',
    'Sytrus',
    'Harmless',
    'Harmor',
    '3x Osc',
    'Fruity DX10',
    'Fruit kick',
    'Ogun',
    'SimSynth Live',
    'PLUCKED!',
    'BeepMap',
    'Drumpad',
    'Slicex',
    'Fruity granulizer',
    'Transistor Bass',
    'Kepler',
]

def Plugin(hw_param, hw_value, is_bypassed) :
    
    recognized_plugin = False
    plugin_name = None
    
    if channels.selectedChannel(1) != -1 :
        if plugins.isValid(channels.selectedChannel()) : 
            plugin_name = plugins.getPluginName(channels.selectedChannel()) # Modify parameters without opening the instrument
    


    if plugin_name == 'FLEX' :
        recognized_plugin = True
        ## FLEX ##
    
        PARAM_MAP = {
                '91':21,
                '92':22,
                '94':25,
                '95':30,
                '96':0,
                '97':2,
                '102':3,
                '103':4,
                '105':10,
                '106':11,
                '107':12,
                '108':13,
                '109':14,
                '110':15,
                '111':16,
                '112':17,
                '1':-1
                }
                
    elif plugin_name == 'FPC' :
        recognized_plugin = True
        ## FPC ##
    
        PARAM_MAP = {
                '91':8,
                '92':9,
                '94':10,
                '95':11,
                '96':12,
                '97':13,
                '102':14,
                '103':15,
                '105':0,
                '106':1,
                '107':2,
                '108':3,
                '109':4,
                '110':5,
                '111':6,
                '112':7,
                '1':-1
                }
                
    elif plugin_name == 'FL Keys' :
        recognized_plugin = True
        ## FL Keys ##
        
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':14,
                '95':13,
                '96':5,
                '97':4,
                '102':-1,
                '103':8,
                '105':12,
                '106':7,
                '107':11,
                '108':10,
                '109':3,
                '110':2,
                '111':6,
                '112':9,
                '1':-1
                }
                
    elif plugin_name == 'Sytrus' :
        recognized_plugin = True
        ## SYTRUS ##
        
        PARAM_MAP = {
                '91':18,
                '92':19,
                '94':1,
                '95':11,
                '96':12,
                '97':13,
                '102':14,
                '103':15,
                '105':3,
                '106':4,
                '107':5,
                '108':6,
                '109':7,
                '110':8,
                '111':9,
                '112':10,
                '1':-1
                }
                
                
    elif plugin_name == 'GMS' :
        recognized_plugin = True
        ## GMS ##
              
        PARAM_MAP = {
                '91':32,
                '92':33,
                '94':46,
                '95':45,
                '96':56,
                '97':57,
                '102':58,
                '103':65,
                '105':24,
                '106':25,
                '107':26,
                '108':27,
                '109':40,
                '110':41,
                '111':42,
                '112':39,
                '1':65
                }
                
                
    elif plugin_name == 'Harmless' :
        recognized_plugin = True
        ## HARMLESS ##
        
        PARAM_MAP = {
                '91':54,
                '92':59,
                '94':58,
                '95':89,
                '96':65,
                '97':79,
                '102':97,
                '103':91,
                '105':26,
                '106':27,
                '107':31,
                '108':28,
                '109':48,
                '110':49,
                '111':52,
                '112':2,
                '1':-1
                }

                
    elif plugin_name == 'Harmor' :
        recognized_plugin = True
        ## HARMOR ##
                
        PARAM_MAP = {
                '91':52,
                '92':57,
                '94':438,
                '95':443,
                '96':787,
                '97':791,
                '102':803,
                '103':810,
                '105':103,
                '106':104,
                '107':105,
                '108':106,
                '109':127,
                '110':128,
                '111':129,
                '112':130,
                '1':-1
                }
    
    elif plugin_name == 'Morphine' :
        recognized_plugin = True
        ## MORPHINE ##
    
        PARAM_MAP = {
                '91':1,
                '92':2,
                '94':30,
                '95':31,
                '96':32,
                '97':33,
                '102':6,
                '103':0,
                '105':21,
                '106':22,
                '107':23,
                '108':24,
                '109':25,
                '110':26,
                '111':27,
                '112':28,
                '1':-1
                }
                
    elif plugin_name == '3x Osc' :
        recognized_plugin = True
        ## 3X OSC ##
    
        PARAM_MAP = {
                '91':1,
                '92':2,
                '94':8,
                '95':9,
                '96':7,
                '97':15,
                '102':16,
                '103':14,
                '105':4,
                '106':5,
                '107':11,
                '108':12,
                '109':18,
                '110':19,
                '111':6,
                '112':13,
                '1':-1
                }
                
    elif plugin_name == 'Fruity DX10' :
        recognized_plugin = True
        ## FRUITY DX10 ##
        
                
        PARAM_MAP = {
                '91':11,
                '92':21,
                '94':13,
                '95':10,
                '96':3,
                '97':4,
                '102':14,
                '103':15,
                '105':0,
                '106':1,
                '107':2,
                '108':5,
                '109':6,
                '110':7,
                '111':8,
                '112':12,
                '1':-1
                }

    
    elif plugin_name == 'BassDrum' :
        recognized_plugin = True
        ## BASSDRUM ##
    
        PARAM_MAP = {
                '91':8,
                '92':7,
                '94':6,
                '95':0,
                '96':4,
                '97':3,
                '102':5,
                '103':2,
                '105':9,
                '106':10,
                '107':11,
                '108':12,
                '109':14,
                '110':13,
                '111':15,
                '112':1,
                '1':-1
                }
                
    elif plugin_name == 'Fruit kick' :
        recognized_plugin = True
        ## FRUIT KICK ##
        
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':3,
                '96':4,
                '97':5,
                '102':-1,
                '103':-1,
                '105':-1,
                '106':1,
                '107':2,
                '108':3,
                '109':4,
                '110':5,
                '111':-1,
                '112':-1,
                '1':-1
                }
                
    elif plugin_name == 'MiniSynth' :
        recognized_plugin = True
        ## MINISYNTH ##
    
        PARAM_MAP = {
                '91':8,
                '92':9,
                '94':20,
                '95':19,
                '96':5,
                '97':2,
                '102':25,
                '103':26,
                '105':12,
                '106':13,
                '107':14,
                '108':15,
                '109':21,
                '110':22,
                '111':23,
                '112':24,
                '1':1
                }
                
    elif plugin_name == 'PoiZone' :
        recognized_plugin = True
        ## POIZONE ##
    
        PARAM_MAP = {
                '91':18,
                '92':19,
                '94':26,
                '95':28,
                '96':29,
                '97':30,
                '102':15,
                '103':46,
                '105':11,
                '106':12,
                '107':13,
                '108':14,
                '109':22,
                '110':23,
                '111':24,
                '112':25,
                '1':43
                }
                
    elif plugin_name == 'Sakura' :
        recognized_plugin = True
        ## Sakura ##
    
        PARAM_MAP = {
                '91':29,
                '92':30,
                '94':33,
                '95':31,
                '96':24,
                '97':25,
                '102':9,
                '103':14,
                '105':34,
                '106':35,
                '107':36,
                '108':37,
                '109':2,
                '110':3,
                '111':4,
                '112':5,
                '1':43
                }
                
    elif plugin_name == 'Fruity Envelope Controller' :
        recognized_plugin = True
        ## Fruity Envelope Controller ##
    
        PARAM_MAP = {
                '91':3,
                '92':4,
                '94':5,
                '95':6,
                '96':88,
                '97':89,
                '102':7,
                '103':2,
                '105':0,
                '106':1,
                '107':8,
                '108':9,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
                            
    elif plugin_name == 'Fruity Keyboard Controller' :
        recognized_plugin = True
        ## Fruity Keyoard Controller ##
    
        PARAM_MAP = {
                '91':-1,
                '92':-1,
                '94':-1,
                '95':-1,
                '96':-1,
                '97':-1,
                '102':-1,
                '103':-1,
                '105':0,
                '106':1,
                '107':-1,
                '108':-1,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
                
    
    elif plugin_name == 'Ogun' :
        recognized_plugin = True
        ## Ogun ##
    
        PARAM_MAP = {
                '91':17,
                '92':18,
                '94':25,
                '95':39,
                '96':5,
                '97':6,
                '102':7,
                '103':8,
                '105':13,
                '106':14,
                '107':15,
                '108':16,
                '109':26,
                '110':27,
                '111':28,
                '112':29,
                '1':-1
                }
    
    elif plugin_name == 'BooBass' :
        recognized_plugin = True
        ## BooBass ##
    
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':-1,
                '96':-1,
                '97':-1,
                '102':-1,
                '103':-1,
                '105':-1,
                '106':-1,
                '107':-1,
                '108':-1,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
    
    elif plugin_name == 'SimSynth Live' :
        recognized_plugin = True
        ## SimSynth ##
    
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':3,
                '96':4,
                '97':5,
                '102':6,
                '103':7,
                '105':22,
                '106':23,
                '107':24,
                '108':25,
                '109':17,
                '110':18,
                '111':19,
                '112':20,
                '1':-1
                }
    
    elif plugin_name == 'Autogun' :
        recognized_plugin = True
        ## Autogun ##
    
        PARAM_MAP = {
                '91':0,
                '92':-1,
                '94':-1,
                '95':-1,
                '96':-1,
                '97':-1,
                '102':-1,
                '103':-1,
                '105':-1,
                '106':-1,
                '107':-1,
                '108':-1,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
    
    elif plugin_name == 'PLUCKED!' :
        recognized_plugin = True
        ## Plucked! ##
    
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':3,
                '96':4,
                '97':-1,
                '102':-1,
                '103':-1,
                '105':-1,
                '106':-1,
                '107':-1,
                '108':-1,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
    
    elif plugin_name == 'BeepMap' :
        recognized_plugin = True
        ## BeepMap ##
    
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':3,
                '96':4,
                '97':5,
                '102':6,
                '103':-1,
                '105':-1,
                '106':-1,
                '107':-1,
                '108':-1,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
                
    elif plugin_name == 'Toxic Biohazard' :
        recognized_plugin = True
        ## Toxic Biohazard ##
    
        PARAM_MAP = {
                '91':15,
                '92':16,
                '94':17,
                '95':18,
                '96':8,
                '97':10,
                '102':0,
                '103':1,
                '105':19,
                '106':20,
                '107':21,
                '108':22,
                '109':3,
                '110':4,
                '111':5,
                '112':6,
                '1':-1
                }
    
    elif plugin_name == 'Fruity Dance' :
        recognized_plugin = True
        ## Fruity Dance ##
    
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':3,
                '96':4,
                '97':5,
                '102':6,
                '103':-1,
                '105':-1,
                '106':-1,
                '107':-1,
                '108':-1,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
    
    elif plugin_name == 'Drumaxx' :
        recognized_plugin = True
        ## Drumaxx ##
    
        PARAM_MAP = {
                '91':352,
                '92':396,
                '94':440,
                '95':484,
                '96':528,
                '97':572,
                '102':616,
                '103':660,
                '105':0,
                '106':44,
                '107':88,
                '108':132,
                '109':176,
                '110':220,
                '111':264,
                '112':308,
                '1':-1
                }
    
    elif plugin_name == 'Drumpad' :
        recognized_plugin = True
        ## Drumpad ##
    
        PARAM_MAP = {
                '91':2,
                '92':3,
                '94':6,
                '95':7,
                '96':13,
                '97':15,
                '102':18,
                '103':21,
                '105':4,
                '106':5,
                '107':8,
                '108':9,
                '109':14,
                '110':16,
                '111':19,
                '112':22,
                '1':-1
                }
                
    elif plugin_name == 'Slicex' :
        recognized_plugin = True
        ## Slicex ##
    
        PARAM_MAP = {
                '91':6,
                '92':7,
                '94':-1,
                '95':-1,
                '96':-1,
                '97':-1,
                '102':-1,
                '103':-1,
                '105':2,
                '106':3,
                '107':4,
                '108':5,
                '109':5-1,
                '110':6-1,
                '111':7-1,
                '112':8-1,
                '1':-1
                }
                
    elif plugin_name == 'SoundFont Player' :
        recognized_plugin = True
        ## SoundFont Player ##
    
        PARAM_MAP = {
                '91':2,
                '92':3,
                '94':9,
                '95':10,
                '96':11,
                '97':12,
                '102':4,
                '103':-1,
                '105':5,
                '106':6,
                '107':7,
                '108':8,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
                
    elif plugin_name == 'Fruity granulizer' :
        recognized_plugin = True
        ## Fruity granulizer ##
    
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':3,
                '96':7,
                '97':4,
                '102':5,
                '103':6,
                '105':8,
                '106':9,
                '107':10,
                '108':11,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
    
    elif plugin_name == 'Sawer' :
        recognized_plugin = True
        ## Sawer ##
    
        PARAM_MAP = {
                '91':27,
                '92':28,
                '94':39,
                '95':45,
                '96':11,
                '97':18,
                '102':19,
                '103':26,
                '105':32,
                '106':33,
                '107':34,
                '108':35,
                '109':2,
                '110':3,
                '111':4,
                '112':5,
                '1':-1
                }
                
    elif plugin_name == 'Transistor Bass' :
        recognized_plugin = True
        ## Transistor Bass ##
    
        PARAM_MAP = {
                '91':0,
                '92':1,
                '94':2,
                '95':4,
                '96':5,
                '97':6,
                '102':7,
                '103':8,
                '105':9,
                '106':10,
                '107':11,
                '108':27,
                '109':28,
                '110':29,
                '111':30,
                '112':31,
                '1':-1
                }
        
    elif plugin_name == 'Kepler' :
        recognized_plugin = True
        ## Transistor Bass ##
    
        PARAM_MAP = {
                '91':19,
                '92':20,
                '94':21,
                '95':22,
                '96':23,
                '97':24,
                '102':5,
                '103':3,
                '105':26,
                '106':27,
                '107':28,
                '108':29,
                '109':16,
                '110':17,
                '111':10,
                '112':18,
                '1':-1
                }
                
    else :
        
        PARAM_MAP = {
                '91':-1,
                '92':-1,
                '94':-1,
                '95':-1,
                '96':-1,
                '97':-1,
                '102':-1,
                '103':-1,
                '105':-1,
                '106':-1,
                '107':-1,
                '108':-1,
                '109':-1,
                '110':-1,
                '111':-1,
                '112':-1,
                '1':-1
                }
      

    if is_bypassed : recognized_plugin=False
    #This enables default feedback values for Arturia plugins

    str_cle = str(hw_param)
    
    
    if str_cle in PARAM_TOUCH_MAP.keys() :
        PLUGIN_PARAM = PARAM_MAP.get(str(PARAM_TOUCH_MAP[str_cle]))
    else :
        PLUGIN_PARAM = PARAM_MAP.get(str_cle)       

    
    str_parameter, str_value_disp, widget_value, is_mapped, is_released = get_param_display_values(str_cle, hw_value, PLUGIN_PARAM, recognized_plugin)

    return str_parameter, str_value_disp, widget_value, is_mapped, is_released
    


def get_param_display_values(str_cle, hw_value, PLUGIN_PARAM, recognized_plugin) :
    #Large functions that handles the output param for feedbacks


    if str_cle in KNOB_MAP.keys() :
        item = KNOB_MAP.get(str_cle) - 1 # Select the right encoder/fader to connect/release
    else :
        item = FADER_MAP.get(str_cle) - 1 # Select the right fader to connect/release


    if not recognized_plugin :
        # The plugin is not a stock plugin
        str_parameter, str_value_disp, widget_value, is_mapped, is_released = get_default_param_display_values(str_cle)

        return str_parameter, str_value_disp, widget_value, is_mapped, is_released

    else :
        # The plugin is a stock plugin

        if PLUGIN_PARAM == -1 :
            #Parameter is not mapped to a control, we have to display the default widget

            str_parameter, str_value_disp, widget_value, is_mapped, is_released = get_default_param_display_values(str_cle)

            return str_parameter, str_value_disp, widget_value, is_mapped, is_released
        
        else :
            #Parameter is mapped to a control   

            is_mapped = 1
            is_released = 0                 

            if str_cle not in PARAM_TOUCH_MAP :
            # If we turn the encoder, we set the value before getting it
            
                if str_cle in KNOB_MAP.keys() :
                    #Param is calculated using relative value for knobs
                
                    next_value = get_plugin_next_value(hw_value, PLUGIN_PARAM)
                    plugins.setParamValue(next_value,PLUGIN_PARAM ,channels.selectedChannel())
                    
                else :                              
                    #Param is calculated using absolute value for faders
                    
                    next_value = hw_value/127
                    plugins.setParamValue(next_value,PLUGIN_PARAM ,channels.selectedChannel(), -1, 2)

            else :
                # If we touch the encoder, we set the ABSOLUTE VALUE to the current plugin value
                
                global ABSOLUTE_VALUE
                ABSOLUTE_VALUE = plugins.getParamValue(PLUGIN_PARAM ,channels.selectedChannel())
                send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eProperties, item, 0x02, 0x01, 0x00])) # Reconnects the item on touch


            str_parameter = str(plugins.getParamName(PLUGIN_PARAM, channels.selectedChannel()))
            str_value_disp = plugins.getParamValueString(PLUGIN_PARAM, channels.selectedChannel())
            widget_value = round(127*plugins.getParamValue(PLUGIN_PARAM, channels.selectedChannel()))

            return str_parameter, str_value_disp, widget_value, is_mapped, is_released
        

    


def get_plugin_next_value(hw_value, PLUGIN_PARAM) : 
    # Functions that gets the next value of the plugin when an encoder is turned
    # Absolute value exists because it is currently not possible to handle discrete parameters using relative. This is a little trick to make it work
    # We have to store a global variable that contains an absolute value. This is updated everytime an encoder is touched

    global ABSOLUTE_VALUE
    global ABSOLUTE_PARAM

    if PLUGIN_PARAM != ABSOLUTE_PARAM :
        ABSOLUTE_VALUE = plugins.getParamValue(PLUGIN_PARAM ,channels.selectedChannel())
        ABSOLUTE_PARAM = PLUGIN_PARAM
    
    delta_value = (hw_value-64)/100 #Relative precision
    current_value = ABSOLUTE_VALUE
    next_value = current_value + delta_value

    if next_value < 0 : #Avoid going beyond limit 0%
        next_value = 0
    elif next_value > 1 : #Avoid going beyond limit 100%
        next_value = 1

    ABSOLUTE_VALUE = next_value

    return next_value


def get_default_param_display_values(str_cle) :

    if str_cle in KNOB_MAP.keys() :
        item = KNOB_MAP.get(str_cle) - 1 # Select the right encoder/fader to release
    else :
        item = FADER_MAP.get(str_cle) - 1 # Select the right fader to release
        
    send_to_device(bytes([0x00, eIntegrationPatchId.eDaw, eParamId.eProperties, item, 0x02, 0x00, 0x00])) # Release

    str_parameter = ""
    str_value_disp = 0
    widget_value = 0
    is_mapped = 0
    is_released = 1

    return str_parameter, str_value_disp, widget_value, is_mapped, is_released



    # UTILITY 



def RelativeToAbsolute(event) :
        global ABSOLUTE_VALUE
        if event.data2 < 64 :
            ABSOLUTE_VALUE += 2*event.data2
        else :
            ABSOLUTE_VALUE -= 2*(event.data2-64)
        if ABSOLUTE_VALUE > 127 :
            ABSOLUTE_VALUE = 127
        elif ABSOLUTE_VALUE < 0 :
            ABSOLUTE_VALUE = 0
        return ABSOLUTE_VALUE