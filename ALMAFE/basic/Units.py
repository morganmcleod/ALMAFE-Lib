from EnumHelper import EnumHelper

class Units(EnumHelper):
    '''
    Units literals for display.
    '''
    WATTS       = 'W'           # watts
    MW          = 'mW'          # milliwatts
    VOLTS       = 'V'           # volts
    VOLTS_SQ    = 'V²'          # volts squared such as from a square-law detector
    DELTA_GAIN  = 'ΔG/G'        # gain variation
    MV          = 'mV'          # millivolts
    DB          = 'dB'          # dB
    DBM         = 'dBm'         # dBm
    DEG         = 'deg'         # degrees of phase
    SECONDS     = 'seconds'     # time as seconds
    MS          = 'ms'          # time as milliseconds
    FS          = 'fs'          # femtoseconds of phase
    MINUTES     = 'minutes'     # time as minutes
    LOCALTIME   = 'localtime'   # time as datetime
    HZ          = 'Hz'          # X axis of FFT
    AMPLITUDE   = 'amplitude'   # default Y axis units when unknown
    KELVIN      = 'K'           # temperature
    CELCIUS     = 'C'           # temperature