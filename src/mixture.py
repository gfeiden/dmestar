# A collection of mixture-specific variable definitions, dictionaries, and routines.

solar_calib = {'GS98'  : [0.70570228, 0.27554077, 0.01875695, 1.88418],
               'AGSS09': [0.71777587, 0.26727,    0.01495323, 2.17936]}

z_abundance = {'GS98'  : [3.0e-5, 0.17208, 0.00150, 0.050410, 0.0,    0.468020, 0.0, 0.0],
               'GS98a2': [3.0e-5, 0.12329, 0.00150, 0.036110, 0.0,    0.531430, 0.0, 0.0],
               'GS98a3': [3.0E-5, 0.10400, 0.00150, 0.030490, 0.0,    0.555730, 0.0, 0.0],
               'GS98a4': [3.0E-5, 0.08490, 0.00150, 0.024870, 0.0,    0.580030, 0.0, 0.0],
               'GS98a6': [3.0E-5, 0.05685, 0.00150, 0.016650, 0.0,    0.615540, 0.0, 0.0],
               'GS98a8': [3.0E-5, 0.03731, 0.00150, 0.010930, 0.0,    0.640270, 0.0, 0.0],
               'GAS07' : [3.0e-5, 0.17533, 0.00177, 0.050696, 0.0,    0.439279, 0.0, 0.0],
               'AGSS09': [3.0e-5, 0.17647, 0.00214, 0.052174, 1.3e-4, 0.431654, 0.0, 0.0]}

def getSolar(mix):
    return solar_calib[mix]
    
def getZAbundance(mix):
    return z_abundance[mix]

def getOpalBinary(mix, afe):
    if afe in [0.2, 0.3, 0.4]:
        afe_ext = '_AFE{:.0f}'.format(afe*10.)
    else:
        afe_ext = ''
    return 'OPAL_{0}{1}.bin'.format(mix, afe_ext)
    
def getFerg05Data(mix, afe):
    z_vals = [0, 1, 2, 35, 5, 7, 8, 9]
    if afe in [0.2, 0.3, 0.4]:
        afe_ext = '+.{:.0f}'.format(afe*10.)
    else:
        afe_ext = ''   
    return ['{:s}{:s}.{:.0f}.tron'.format(mix.lower(), afe_ext, z) for z in z_vals]

def setAbundances(x, y, z, mix, feh, afe, y_prim):
    """ Set mass fractions X, Y, and Z """
    from math import log10
    
    # get solar X, Y, and Z
    solar = solar_calib[mix]
    
    # readjust total metallicity for alpha enhancement (Salaris & Cassisi 2005)
    meh = feh + log10(0.694*10.**afe + 0.306)
    
    # calculate dy/dz based on defined primordial Y
    dydz   = (solar[1] - y_prim)/solar[2]
    ZoverX = log10(solar[2]/solar[0])
    
    if z == 'calc':
        z = (1.0 - y_prim)/(1.0 + dydz + 10.0**(-1.0*meh - ZoverX))
    else:
        pass
    
    if y == 'calc':
        y = y_prim + dydz*z
    else:
        pass
    
    if x == 'calc':
        x = 1.0 - y - z
    else:
        pass
    
    return x, y, z
