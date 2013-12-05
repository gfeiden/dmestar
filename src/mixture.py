# A collection of mixture-specific variable definitions, dictionaries, and routines.

solar_calib = {'GS98': [0.70570228, 0.27554077, 0.01875695, 1.88418]}

z_abundance = {'GS98'  : [1.0e22, 3.0e-5, 0.17208, 0.00150, 0.050410, 0.0, 0.468020, 0.0, 0.0],
               'GAS07' : [1.0e22, 3.0e-5, 0.17533, 0.00177, 0.050696, 0.0, 0.439279, 0.0, 0.0],
               'AGSS09': [1.0e22, 3.0e-5, 0.17686, 0.00150, 0.051820, 0.0, 0.428750, 0.0, 0.0]}

def getSolar(mix):
    return solar_calib[mix]
    
def getZAbundance(mix):
    return z_abundance[mix]

def getOpalBinary(mix):
    return 'OPAL_{0}.bin'.format(mix)
    
def getFerg05Data(mix):
    z_vals = [0, 1, 2, 35, 5, 7, 8, 9]
    return ['{:s}.{:.0f}.tron'.format(mix.lower(), z) for z in z_vals]

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