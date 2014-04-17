#
#
def plusMinus(value):
    """ Convert sign to character """
    if value < 0.0:
        value = 'm'
    else:
        value = 'p'
    return value

def select(feh, afe, atm_tau = 10):
    """ Select appropriate atmosphere files """
    import os
    from sys import exit
    from . import dirstruc as ds
    
    fort_files = ['fort.{:.0f}'.format(x) for x in range(95, 100)]
    if (feh < -1.0 or feh > 0.5):
        exit("\nERROR: Invalid [Fe/H] in atmosphere selection.\n")
    if afe not in [0.0, 0.2, 0.4]:
        exit("\nERROR: Invalid [a/Fe] in atmosphere selection.\n")
    for f in fort_files:
        try:
            os.remove(f)
        except OSError:
            pass
    
    # generate Kurucz atmosphere file name
    kur_file = 'atmk1990{0}{1}{2}.tab'.format(plusMinus(feh), 
                                              str(abs(round(feh, 1)))[0],
                                              str(abs(round(feh, 1)))[2])
    
    #--- NOTE, add other mixtures later
    # GS98 specific 
    # protect against issues at edge of grid
    if feh < -0.3:
        feh = -0.3
    elif feh > 0.3:
        feh = 0.3
    else:
        pass
    feh  = round(feh, 1)
    
    # generate atmosphere file names
    feh_list  = [round(feh + float(x)/10., 1) for x in range(-2, 3)]
    if atm_tau == 10:
        phx_files = ["{0}Z{1}{2}d{3}.a{4}{5}d{6}_t010.dat".format(ds.phxnorm, 
                      plusMinus(x), str(abs(x))[0], str(abs(x))[2], plusMinus(afe), 
                      str(abs(afe))[0], str(abs(afe))[2]) for x in feh_list]
    elif atm_tau == 100:
        phx_files = ["{0}Z{1}{2}d{3}.a{4}{5}d{6}_t100.dat".format(ds.phxt100, 
                      plusMinus(x), str(abs(x))[0], str(abs(x))[2], plusMinus(afe), 
                      str(abs(afe))[0], str(abs(afe))[2]) for x in feh_list]
    else:
        phx_files = ["{0}z_{1}{2}d{3}.afe_{4}{5}d{6}.dat".format(ds.phxteff, 
                      plusMinus(x), str(abs(x))[0], str(abs(x))[2], plusMinus(afe), 
                      str(abs(afe))[0], str(abs(afe))[2]) for x in feh_list]
        
    if len(phx_files) != len(fort_files):
        exit("\nERROR: Length discrepancy in atmosphere selection routine.\n")
    
    return kur_file, phx_files
    
