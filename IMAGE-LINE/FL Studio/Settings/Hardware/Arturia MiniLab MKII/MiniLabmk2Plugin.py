import device
import plugins
import channels
import ui
import midi
# Global variable

#ABSOLUTE VALUE
ABSOLUTE_VALUE = 64

def Plugin(event, clef) :

    recognized_plugin = False
    plugin_name = ui.getFocusedPluginName()
    
    global ABSOLUTE_VALUE
    
    if plugin_name == 'FLEX' :
        recognized_plugin = True
        ## FLEX ##
    
        PARAM_MAP = {
                '31':10,
                '32':11,
                '33':12,
                '34':13,
                '35':14,
                '36':15,
                '2':0,
                '3':2,
                '4':4,
                '5':5,
                '6':7,
                '7':9,
                '1':36,
                '224':39
                }
                
    elif plugin_name == 'FPC' :
        recognized_plugin = True
        ## FPC ##
    
        PARAM_MAP = {
                '31':-1,
                '32':4,
                '33':5,
                '34':6,
                '35':7,
                '36':-1,
                '2':-1,
                '3':0,
                '4':1,
                '5':2,
                '6':3,
                '7':-1,
                '1':-1,
                '224':-1
                }
                
    elif plugin_name == 'FL Keys' :
        recognized_plugin = True
        ## FL Keys ##
        
        PARAM_MAP = {
                '31':0,
                '32':1,
                '33':14,
                '34':13,
                '35':5,
                '36':4,
                '2':12,
                '3':7,
                '4':11,
                '5':10,
                '6':3,
                '7':2,
                '1':9,
                '224':8
                }
                
    elif plugin_name == 'Sytrus' :
        recognized_plugin = True
        ## SYTRUS ##
        
        PARAM_MAP = {
                '31':18,
                '32':19,
                '33':1,
                '34':11,
                '35':12,
                '36':13,
                '2':3,
                '3':4,
                '4':6,
                '5':7,
                '6':8,
                '7':10,
                '1':17,
                '224':2
                }
                
                
    elif plugin_name == 'GMS' :
        recognized_plugin = True
        ## GMS ##
        
        PARAM_MAP = {
                '31':32,
                '32':33,
                '33':46,
                '34':45,
                '35':56,
                '36':57,
                '2':24,
                '3':25,
                '4':27,
                '5':40,
                '6':41,
                '7':42,
                '1':65,
                '224':22
                }
                
                
    elif plugin_name == 'Harmless' :
        recognized_plugin = True
        ## HARMLESS ##
        
        PARAM_MAP = {
                '31':54,
                '32':59,
                '33':58,
                '34':89,
                '35':65,
                '36':79,
                '2':26,
                '3':27,
                '4':28,
                '5':48,
                '6':49,
                '7':52,
                '1':69,
                '224':38
                }

                
    elif plugin_name == 'Harmor' :
        recognized_plugin = True
        ## HARMOR ##
        
        PARAM_MAP = {
                '31':52,
                '32':57,
                '33':438,
                '34':443,
                '35':787,
                '36':803,
                '2':103,
                '3':104,
                '4':106,
                '5':127,
                '6':128,
                '7':130,
                '1':45,
                '224':786
                }
    
    elif plugin_name == 'Morphine' :
        recognized_plugin = True
        ## MORPHINE ##
    
        PARAM_MAP = {
                '31':-1,
                '32':-1,
                '33':-1,
                '34':-1,
                '35':-1,
                '36':-1,
                '2':-1,
                '3':-1,
                '4':-1,
                '5':-1,
                '6':-1,
                '7':-1,
                '1':-1,
                '224':-1
                }
                
    elif plugin_name == '3x Osc' :
        recognized_plugin = True
        ## 3X OSC ##
    
        PARAM_MAP = {
                '31':1,
                '32':8,
                '33':15,
                '34':2,
                '35':9,
                '36':16,
                '2':0,
                '3':7,
                '4':14,
                '5':20,
                '6':6,
                '7':13,
                '1':-1,
                '224':5
                }
                
    elif plugin_name == 'Fruity DX10' :
        recognized_plugin = True
        ## FRUITY DX10 ##
        
        PARAM_MAP = {
                '31':11,
                '32':13,
                '33':3,
                '34':14,
                '35':15,
                '36':16,
                '2':0,
                '3':1,
                '4':2,
                '5':4,
                '6':5,
                '7':6,
                '1':10,
                '224':21
                }

    
    elif plugin_name == 'BASSDRUM' :
        recognized_plugin = True
        ## BASSDRUM ##
    
        PARAM_MAP = {
                '31':-1,
                '32':-1,
                '33':-1,
                '34':-1,
                '35':-1,
                '36':-1,
                '2':-1,
                '3':-1,
                '4':-1,
                '5':-1,
                '6':-1,
                '7':-1,
                '1':-1,
                '224':-1
                }
                
    elif plugin_name == 'Fruit kick' :
        recognized_plugin = True
        ## FRUIT KICK ##
        
        PARAM_MAP = {
                '31':-1,
                '32':-1,
                '33':-1,
                '34':-1,
                '35':-1,
                '36':-1,
                '2':0,
                '3':1,
                '4':2,
                '5':3,
                '6':4,
                '7':5,
                '1':-1,
                '224':-1
                }
                
    elif plugin_name == 'MiniSynth' :
        recognized_plugin = True
        ## MINISYNTH ##
    
        PARAM_MAP = {
                '31':8,
                '32':9,
                '33':5,
                '34':2,
                '35':25,
                '36':26,
                '2':12,
                '3':13,
                '4':15,
                '5':21,
                '6':22,
                '7':24,
                '1':4,
                '224':-1
                }
                
    elif plugin_name == 'PoiZone' :
        recognized_plugin = True
        ## POIZONE ##
    
        PARAM_MAP = {
                '31':-1,
                '32':-1,
                '33':-1,
                '34':-1,
                '35':-1,
                '36':-1,
                '2':-1,
                '3':-1,
                '4':-1,
                '5':-1,
                '6':-1,
                '7':-1,
                '1':-1,
                '224':-1
                }
                
    elif plugin_name == 'Sakura' :
        recognized_plugin = True
        ## Sakura ##
    
        PARAM_MAP = {
                '31':-1,
                '32':-1,
                '33':-1,
                '34':-1,
                '35':-1,
                '36':-1,
                '2':-1,
                '3':-1,
                '4':-1,
                '5':-1,
                '6':-1,
                '7':-1,
                '1':-1,
                '224':-1
                }
                
    if recognized_plugin :    
        cle = str(clef)
        PLUGIN_PARAM = PARAM_MAP.get(cle)
        if PLUGIN_PARAM != -1 :
            value = event.data2/127
            plugins.setParamValue(value,PLUGIN_PARAM ,channels.channelNumber())
            event.handled = False
            param = str(plugins.getParamName(PLUGIN_PARAM, channels.channelNumber()))
            value = str(round(100*plugins.getParamValue(PLUGIN_PARAM, channels.channelNumber())))
        else :
            param = ""
            value = "" 
    else :
        param = ""
        value = ""
        
    return param, value
    


    # UTILITY 



# def RelativeToAbsolute(event) :
        # global ABSOLUTE_VALUE
        # if event.data2 < 64 :
            # ABSOLUTE_VALUE += 2*event.data2
        # else :
            # ABSOLUTE_VALUE -= 2*(event.data2-64)
        # if ABSOLUTE_VALUE > 127 :
            # ABSOLUTE_VALUE = 127
        # elif ABSOLUTE_VALUE < 0 :
            # ABSOLUTE_VALUE = 0
        # return ABSOLUTE_VALUE