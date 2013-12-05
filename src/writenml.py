import errors as er
import math
import mixture

def writePolyNamelist(mass, x, z, afe, alpha_mlt, mix,
                      index_n = 1.5, beta = 1., age = 1.e3, 
                      light_elements = 'on', mass_deep = 9.9e-6, 
                      mass_surf = 0.9999):
    """ Write namelist file needed for seed polytrope calculation """
    
    # confirm all values are actually specified
    if None in [mass, x, z, alpha_mlt]:
        er.valErrMissing()
    
    # get solar Z
    z_solar = mixture.getSolar(mix)
    z_solar = z_solar[2]
    
    # determine starting Teff and Luminosity
    adjust_lumi = -0.115*math.log10(z/z_solar)
    adjust_teff = -0.022*math.log10(z/z_solar)
    
    if mass >= 3.9:
        teff       =  3.64
        luminoisty =  0.2*(mass - 5.0) + 2.6
    elif 3.0 <= mass < 3.9:
        teff       = -0.028*mass + 3.785
        luminosity =  0.55*mass + 0.1
    elif 1.5 < mass <= 3.0:
        teff       =  0.039*mass + 3.5765
        luminosity =  1.7
    elif 0.23 < mass <= 1.5:
        teff       =  0.039*mass + 3.5765
        luminosity =  0.85*mass + 0.4
    else:
        teff       =  0.614*mass + 3.3863
        luminosity = -0.16877*mass - 0.117637
        
    teff       += adjust_teff
    luminosity += adjust_lumi
    
    # get heavy element abundances
    z_elements = mixture.getZAbundance(mix)
    z_elements.pop(0)
        
    # write out namelist file
    poly_nml = open('poly.nml', 'w')
    poly_nml.write('! Auto-generated polytrope namelist file \n')
    poly_nml.write('!--------------------------------------- \n')
    poly_nml.write('$data \n\n')
    poly_nml.write(' sumass = {:.4f} \n'.format(mass))
    poly_nml.write(' teffl1 = {:.4f} \n'.format(teff))
    poly_nml.write(' suluml = {:.4f} \n'.format(luminosity))
    poly_nml.write(' x = {:.6e} \n'.format(x))
    poly_nml.write(' z = {:.6e} \n'.format(z))
    poly_nml.write(' elem(1) = {:e} \n'.format(z_elements.pop(0)))
    for i in range(len(z_elements)):
        poly_nml.write(' elem({:.0f}) = {:e} \n'.format(i + 2, z*z_elements[i]))
    poly_nml.write(' cmixl = {:.6f} \n'.format(alpha_mlt))
    poly_nml.write(' beta = {:.3f} \n'.format(beta))
    poly_nml.write(' fmass1 = {:e} \n'.format(mass_deep))
    poly_nml.write(' fmass2 = {:e} \n'.format(mass_surf))
    poly_nml.write(' ddage = {:.2f} \n'.format(age))
    poly_nml.write(' pn = {:4.3f} \n'.format(index_n))
    if light_elements == 'on':
        poly_nml.write(' lexcom = .true. \n')
    else:
        poly_nml.write(' lexcom = .false. \n')
    poly_nml.write('\n$end\n')
    poly_nml.close()
    
    if not poly_nml.closed:
        print "\nWARNING: Polytrope namelist file not closed properly.\n"

def writePhysNamelist(mass, atm, eos, turb_diff, nuclear_svals):
    """ Write the physics namelist file """
    import dirstruc as ds
    
    if None in [mass, atm, turb_diff, eos, nuclear_svals]:
        er.valErrMissing()
        
    # define integers for atmosphere toggling
    atm_int = {'edd': 0, 'ks': 1, 'kur': 3, 'phx': 5}
    
    # specify generalized physics namelist
    if mass <= 0.8:
        phys_nml_file = ds.nml + 'phys_low.nml'
    elif 0.8 < mass < 1.8:
        phys_nml_file = ds.nml + 'phys_med.nml'
    else:
        phys_nml_file = ds.nml + 'phys_high.nml'
    
    phys_nml = open('physics.nml', 'w')
    phys_nml.write('! Auto-generated phyiscs namelist file\n')
    phys_nml.write('!-------------------------------------\n')
    phys_nml.write('$physics\n\n')
    phys_nml.write(' kttau = {:1.0f}\n'.format(atm_int[atm]))
    phys_nml.write(' lmatm = .true.\n')
    if turb_diff > 0.0:
        phys_nml.write(' ltdiff = .true.\n')
        phys_nml.write(' turbt = {:2.1f}\n'.format(turb_diff))
    else:
        phys_nml.write(' ltdiff = .false.\n')
    
    phys_nml.write(' ldh = .true.\n')
    if eos == 'std':
        phys_nml.write(' lscv = .false.\n')
        phys_nml.write(' lopale = .false.\n')
        if mass <= 0.8:
            phys_nml.write(' lfree_eos = .true.\n')
        else:
            phys_nml.write(' lfree_eos = .false.\n')
        phys_nml.write(' ieos = 1, 101, 0\n')        # EOS4 configuration
    elif eos == 'feos':
        phys_nml.write(' lscv = .false.\n')
        phys_nml.write(' lopale = .false.\n')
        phys_nml.write(' lfree_eos = .true.\n')
        phys_nml.write(' ieos = 1, 101, 0\n')
    elif eos == 'opal':
        phys_nml.write(' lscv = .false.\n')
        phys_nml.write(' lopale = .true.\n')
        phys_nml.write(' lfree_eos = .false.\n')
    elif eos == 'scvh':
        phys_nml.write(' lscv = .true.\n')
        phys_nml.write(' lopale = .false.\n')
        phys_nml.write(' lfree_eos = .false.\n')
    else:
        phys_nml.write(' lscv = .false.\n')
        phys_nml.write(' lopale = .false.\n')
        phys_nml.write(' lfree_eos = .false.\n')
        
    with open(phys_nml_file, 'r') as nml_in:
        phys_nml.write(nml_in.read())
    phys_nml.close()
    
    if not phys_nml.closed:
        print "WARNING: Physics namelist file was not properly closed."
    

def writeCtrlNamelist(x, y, z, afe, a_mlt, mix, final_age = None, n_models = None):
    """ Write the control namelist file """
    import dirstruc as ds
    import mixture
    from os  import uname, getlogin
    from sys import exit
    
    if (final_age == None and n_models == None):
        exit('\nERROR: Must specify either the number of models or a final age\n')
        
    opalbin = ds.opal + mixture.getOpalBinary(mix)
    fergbin = mixture.getFerg05Data(mix)
    
    diagnostic = uname()
    descrip2 = '"User: {0}, OS Diagnostic: {1} {2} {3}"'.format(getlogin(), diagnostic[0],
                                                              diagnostic[2], diagnostic[4])
    
    ctrl = open('control.nml', 'w')
    ctrl.write('! Auto-generated control namelist file\n')
    ctrl.write('!--------------------------------------\n')
    ctrl.write('$control\n\n')
    ctrl.write(' descrip(1) = "Run autogenerated from within Python."\n')
    ctrl.write(' descrip(2) = {:s}\n'.format(descrip2))
    #ctrl.write(' descrip(3) = " "\n\n')
    ctrl.write(' numrun = 2\n\n') 
    
    # format rescaling run
    ctrl.write(' kindrn(1) = 2\n')
    ctrl.write(' lfirst(1) = .true.\n')
    ctrl.write(' nmodls(1) = 2\n')
    ctrl.write(' rsclx(1)  = {:.12f}\n'.format(x))
    ctrl.write(' rsclz(1)  = {:.12f}\n'.format(z))
    ctrl.write(' cmixla(1) = {:.12f}\n\n'.format(a_mlt))
    
    # format evolution run
    ctrl.write(' kindrn(2) = 1\n')
    ctrl.write(' lfirst(2) = .false.\n')
    ctrl.write(' cmixla(2) = {:.12f}\n'.format(a_mlt))
    if n_models != None:
        ctrl.write(' nmodls(2) = {:.0f}\n'.format(n_models))
    if final_age != None:
        ctrl.write(' endage(2) = {:.4e}\n\n'.format(final_age))
    
    # format mixture information
    ctrl.write(' mix  = "{0}"\n'.format(mix.upper()))
    ctrl.write(' iafe = {:.0f}\n\n'.format(int(afe*10)))
    
    # format opacity information
    ctrl.write(' lalex95 = .true.\n')
    ctrl.write(' zalex   = {:.12f}\n'.format(z))
    ctrl.write(' lopal95 = .true.\n')
    ctrl.write(' fo95cobin = "{0}"\n\n'.format(opalbin))
    for i in range(8):
        ctrl.write(' opecalex({:.0f}) = "{:s}{:s}"\n'.format(i + 1, ds.ferg, fergbin[i]))
    ctrl.write('\n')
    
    # format default logic flags
    ctrl.write(' lzams  = .false.\n')
    ctrl.write(' lhb    = .false.\n')
    ctrl.write(' ltrack = .true.\n')
    ctrl.write(' liso   = .true.\n')
    ctrl.write(' lcorr  = .true.\n')
    ctrl.write(' lrwsh  = .true.\n')
    ctrl.write(' lpulse = .false.\n\n')
    ctrl.write('$end\n')
    ctrl.close()
    
    if not ctrl.closed:
        print "WARNING: Control namelist was not closed properly."

def writeMagNamelist(b_field = 'off', b_surf = 0.1, b_pert_age = 0.1, 
                     b_gamma = 2.0, chi_f = 1.0, fc_tach = 0.15,
                     eq_lambda = 0.0, b_rad_prof = 'dipole', dynamo = 'rot', 
                     b_field_ramp = 'no'):
    """ Write the magnetic namelist file """
       
    # ensure that b_gamma is in [4/3, 2]
    if b_gamma < 4./3.:
        b_gamma  = er.valWarnBelow('b_gamma', 4./3.)
    elif b_gamma > 2.:
        b_gamma  = er.valWarnAbove('b_gamma', 2.)
    else:
        pass
       
    # ensure that chi_f is in [0, 1]
    if chi_f < 0.:
        chi_f    = er.valWarnBelow('chi_f', 0.)
    elif chi_f > 1.:
        chi_f    = er.valWarnAbove('chi_f', 1.)
    else:
        pass
       
    # ensure that fc_tach is in (0, 1)
    if fc_tach <= 0.:
        fc_tach  = er.valWarnBelow('fc_tach', 0.01)
    elif fc_tach >= 1.:
        fc_tach  = er.valWarnAbove('fc_tach', 0.99)
    else:
        pass
      
    # confirm eq_lambda is in [0, 1)
    if eq_lambda >= 1.:
        eq_lambda = er.valWarnAbove('eq_lambda', 0.99)
    elif eq_lambda < 0.:
        eq_lambda = er.valWarnBelow('eq_lambda', 0.0)
    else:
        pass
        
    # write the file
    mag_nml = open('magnetic.nml', 'w')
    mag_nml.write('! Auto-generated magnetic namelist file\n')
    mag_nml.write('!--------------------------------------\n')
    mag_nml.write('$magnetic\n\n')
    if (b_field == 'off'):
        mag_nml.write(' lmag = .false.\n')
    else:
        mag_nml.write(' lmag = .true.\n')
    mag_nml.write(' b_pert_age = {:5.4e}\n'.format(b_pert_age))
    mag_nml.write(' b_surf = {:5.4e}\n'.format(b_surf))
    mag_nml.write(' gammag = {:4.2f}\n'.format(b_gamma))
    mag_nml.write(' chi_f = {:4.2f}\n'.format(chi_f))
    mag_nml.write(' fc_tach = {:5.4e}\n'.format(fc_tach))
    mag_nml.write(' eq_lambda = {:e}\n'.format(eq_lambda))
    mag_nml.write(' b_rad_prof = \'{:s}\'\n'.format(b_rad_prof))
    mag_nml.write(' dynamo = \'{:s}\'\n'.format(dynamo))
    if (b_field_ramp == 'no'):
        mag_nml.write(' ramp_b_field = .false.\n')
    else:
        mag_nml.write(' ramp_b_field = .true.\n')
    mag_nml.write('\n$end\n')
    mag_nml.close()
    
    if not mag_nml.closed:
        print "WARNING: Magnetic field namelist file not closed properly."

    

