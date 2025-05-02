
import device
import plugins
import channels
import ui
import midi

from KLEss3Dispatch import send_to_device

# Global variable

PARAM_ID = {
            '96':1,
            '97':2,
            '98':3,
            '99':4,
            '100':5,
            '101':6,
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
            
KNOB_ID = (
            96,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            )

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
                    'BASSDRUM'
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
]

def Plugin(hw_param, hw_value, moved_param) :

    recognized_plugin = False
    # plugin_name = ui.getFocusedPluginName() Like that before
    plugin_name = plugins.getPluginName(channels.selectedChannel()) # Modify parameters without opening the instrument
    
    global ABSOLUTE_VALUE
    
    if plugin_name == 'FLEX' :
        recognized_plugin = True
        ## FLEX ##
    
        PARAM_MAP = {
                '96':21,
                '97':22,
                '98':25,
                '99':30,
                '100':0,
                '101':2,
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
                '96':8,
                '97':9,
                '98':10,
                '99':11,
                '100':12,
                '101':13,
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
                '96':0,
                '97':1,
                '98':14,
                '99':13,
                '100':5,
                '101':4,
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
                '96':18,
                '97':19,
                '98':1,
                '99':11,
                '100':12,
                '101':13,
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
                '96':32,
                '97':33,
                '98':46,
                '99':45,
                '100':56,
                '101':57,
                '102':58,
                '103':65,
                '105':24,
                '106':25,
                '107':26,
                '108':27,
                '109':40,
                '110':41,
                '111':42,
                '112':38,
                '1':65
                }
                
                
    elif plugin_name == 'Harmless' :
        recognized_plugin = True
        ## HARMLESS ##
        
        PARAM_MAP = {
                '96':54,
                '97':59,
                '98':58,
                '99':89,
                '100':65,
                '101':79,
                '102':97,
                '103':91,
                '105':26,
                '106':27,
                '107':31,
                '108':28,
                '109':48,
                '110':49,
                '111':52,
                '112':58,
                '1':-1
                }

                
    elif plugin_name == 'Harmor' :
        recognized_plugin = True
        ## HARMOR ##
                
        PARAM_MAP = {
                '96':52,
                '97':57,
                '98':438,
                '99':443,
                '100':787,
                '101':791,
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
                '96':40,
                '97':41,
                '98':1,
                '99':6,
                '100':30,
                '101':31,
                '102':32,
                '103':33,
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
                '96':1,
                '97':2,
                '98':8,
                '99':9,
                '100':7,
                '101':15,
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
                '96':11,
                '97':21,
                '98':13,
                '99':10,
                '100':3,
                '101':4,
                '102':14,
                '103':15,
                '105':0,
                '106':1,
                '107':2,
                '108':4,
                '109':5,
                '110':6,
                '111':7,
                '112':8,
                '1':-1
                }

    
    elif plugin_name == 'BASSDRUM' :
        recognized_plugin = True
        ## BASSDRUM ##
    
        PARAM_MAP = {
                '96':8,
                '97':7,
                '98':6,
                '99':0,
                '100':4,
                '101':3,
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
                '96':-1,
                '97':-1,
                '98':-1,
                '99':-1,
                '100':-1,
                '101':-1,
                '102':-1,
                '103':-1,
                '105':0,
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
                '96':8,
                '97':9,
                '98':20,
                '99':19,
                '100':5,
                '101':2,
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
                '96':18,
                '97':19,
                '98':26,
                '99':28,
                '100':29,
                '101':30,
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
                '96':29,
                '97':30,
                '98':33,
                '99':31,
                '100':24,
                '101':25,
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
                '96':3,
                '97':4,
                '98':5,
                '99':6,
                '100':88,
                '101':89,
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
                '96':-1,
                '97':-1,
                '98':-1,
                '99':-1,
                '100':-1,
                '101':-1,
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
                '96':17,
                '97':18,
                '98':25,
                '99':39,
                '100':5,
                '101':6,
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
                '96':0,
                '97':1,
                '98':2,
                '99':-1,
                '100':-1,
                '101':-1,
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
                '96':0,
                '97':1,
                '98':2,
                '99':3,
                '100':4,
                '101':5,
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
                '96':0,
                '97':-1,
                '98':-1,
                '99':-1,
                '100':-1,
                '101':-1,
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
                '96':0,
                '97':1,
                '98':2,
                '99':3,
                '100':4,
                '101':-1,
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
                '96':0,
                '97':1,
                '98':2,
                '99':3,
                '100':4,
                '101':5,
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
                '96':15,
                '97':16,
                '98':17,
                '99':18,
                '100':8,
                '101':10,
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
                '96':0,
                '97':1,
                '98':2,
                '99':3,
                '100':4,
                '101':5,
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
                '96':352,
                '97':396,
                '98':440,
                '99':484,
                '100':528,
                '101':572,
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
                '96':2,
                '97':3,
                '98':6,
                '99':7,
                '100':13,
                '101':15,
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
                '96':6,
                '97':7,
                '98':-1,
                '99':-1,
                '100':-1,
                '101':-1,
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
                '96':2,
                '97':3,
                '98':9,
                '99':10,
                '100':11,
                '101':12,
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
                '96':0,
                '97':1,
                '98':2,
                '99':3,
                '100':7,
                '101':4,
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
                '96':27,
                '97':28,
                '98':39,
                '99':45,
                '100':11,
                '101':18,
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
                '96':1,
                '97':2,
                '98':3,
                '99':4,
                '100':5,
                '101':6,
                '102':7,
                '103':8,
                '105':1,
                '106':2,
                '107':3,
                '108':4,
                '109':5,
                '110':6,
                '111':7,
                '112':8,
                '1':-1
                }
                
    else :
        
        PARAM_MAP = {
                '96':-1,
                '97':-1,
                '98':-1,
                '99':-1,
                '100':-1,
                '101':-1,
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
      
    # We see if the plugin is a stock plugin            
    if recognized_plugin :

        # If a parameter has been touched 
        if moved_param : 

            cle = str(hw_param)
            PLUGIN_PARAM = PARAM_MAP.get(cle)
            if PLUGIN_PARAM != -1 :
                mapped = 1
                value = hw_value/127
                plugins.setParamValue(value,PLUGIN_PARAM ,channels.selectedChannel())
                #event.handled = False
                parameter = str(plugins.getParamName(PLUGIN_PARAM, channels.selectedChannel()))
                value = str(round(100*plugins.getParamValue(PLUGIN_PARAM, channels.selectedChannel())))
            else :
                mapped = 0
                if hw_param in KNOB_ID :
                    parameter = "Encoder "
                else :
                    parameter = "Fader "
                
                parameter = parameter + str(PARAM_ID.get(cle))
                value = str(hw_value)
 

        # If no parameter has been touched
        else :
            #print(PARAM_MAP)
            index = 0
            param_value = []
            for i in PARAM_MAP.values():
                param_value.append(i)
            for i in range(len(param_value)):
                if param_value[i] != -1 :
                    parameter = None
                    mapped = None
                    value = round(127*plugins.getParamValue(param_value[i], channels.selectedChannel()))
                    #print(i, value)
                    SetParamValue(i, value)


    else :

        mapped = 0
        cle = str(hw_param)
        if hw_param in KNOB_ID :
            parameter = "Encoder "
        else :
            parameter = "Fader "
            
        parameter = parameter + str(PARAM_ID.get(cle))
        value = str(hw_value)


    return parameter, value, mapped
    

def SetParamValue(param, value):
    
    send_to_device(bytes([0x02, 0x0F, 0x40, 3 + param, value]))
    





    # UTILITY 



# def RelativeToAbsolute(event) :
#         global ABSOLUTE_VALUE
#         if event.data2 < 64 :
#             ABSOLUTE_VALUE += 2*event.data2
#         else :
#             ABSOLUTE_VALUE -= 2*(event.data2-64)
#         if ABSOLUTE_VALUE > 127 :
#             ABSOLUTE_VALUE = 127
#         elif ABSOLUTE_VALUE < 0 :
#             ABSOLUTE_VALUE = 0
#         return ABSOLUTE_VALUE