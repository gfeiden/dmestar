#
#
import os
from .src import writenml as wn


class Model(object):
    
    def __init__(self, mass, feh, x = 'calc', y = 'calc', z = 'calc', y_prim = 0.248, 
                 afe = 0.0, mixture = 'GS98', a_mlt = 'solar', atm = 'phx', 
                 n_models = 10000, final_age = 1.0e11, turb_diff = 6.0, 
                 eos = 'std', nuclear_svals = 'SFII', 
                 b_field = 'off', b_surf = 0.1, b_pert_age = 0.1, 
                 b_gamma = 2.0, chi_f = '1.0', fc_tach = 0.15, 
                 eq_lambda = 0.0, b_rad_prof = 'dipole', dynamo = 'rot', 
                 b_field_ramp = 'no', run_log = True):
        """ Create a new instance of DMESTAR
    
        The base class for initializing a stellar model using DMESTAR. The
        input properties for each instance of DMESTAR will be used to as
        the input configuration for a given series of stellar models.
        
        Required Input:
        ---------------
            mass         ::    final mass (in solar units)

            feh          ::    scaled-solar [Fe/H] 
            
        Optional Input: (default)
        ---------------
            delta_mass   ::    float equal to the requested step size in
                               mass for a series of models. (0.2)
            x            ::    hydrogen mass fraction or an automatic 
                               computation based on Y and Z. ('calc')
            y            ::    helium mass fraction or the method of an
                               automatic linear scaling with Z. ('calc')
                               
                               default 'calc': y = y_prim + dy/dz*z
            
            z            ::    heavy element mass fraction or an automatic
                               computation using [A/Fe] and [Fe/H]. ('calc')
                               
            y_prim       ::    primordial helium mass fraction (0.245)
                      
            afe          ::    [alpha/Fe] abundance (0.0)
                               options --- -0.2, 0.0, 0.2, 0.4, 0.6, 0.8
            
            mixture      ::    solar heavy element composition ('GS98')
                               options --- 'GN93'
                                           'GS98'
                                           'GAS07'
                                           'AGSS09'
            
            a_mlt        ::    convective mixing length in units of pressure
                               scale heights. ('solar') 
                               options --- 'solar' or any real number > 0
                      
            atm          ::    atmosphere model used to define the surface 
                               boundary conditions. ('phx')
                               options --- 'phx' = phoenix model atmosphere
                                           'ks'  = Krishna-Swamy
                                           'edd' = Eddington T-tau 
                                           'kur' = Kurucz '99 atmosphere
            
            n_models     ::    number of model iterations (time steps) to
                               be taken during any given model run. (9000)
            
            final_age    ::    age to terminate a model run. (1.0e11)
            
            turb_diff    ::    logarithm of the reference temperature for 
                               turbulent diffusion. set to 0 to turn off. 
                               (6.0)
                               options --- any real number
            
            eos          ::    equation of state to be used. ('std')
                               options --- 'std'  = FreeEOS / Saha + DH
                                           'saha' = Saha + DH
                                           'opal' = OPAL
                                           'scvh' = SCVH95
                                           'feos' = FreeEOS
            
            nuclear_svals::    nuclear reaction cross-sections, specified
                               by literature compilation. ('SFII')
                               options --- 'SFI'   = Adelberger et al. 1998
                                           'SFII'  = Adelberger et al. 2010
            
            b_field      ::    toggle magnetic field on/off. ('off')
                               options --- 'on'
                                           'off'
                                           
            b_surf       ::    surface magnetic field strength in G. (0.1) 
                               
            b_pert_age   ::    perturbation age for magnetic field in Gyr.
                               (0.1)
                               
            b_gamma      ::    magnetic field geometry parameter, gamma.
                               (2.0)
                               options --- [1.3333, 2.0]
            
            chi_f        ::    magnetic field f parameter. (1.0)
                               options --- [0.0, 1.0]
            
            fc_tach      ::    depth of 'tachocline' in fully convective
                               objects in units of stellar radii. (0.15)
                               options --- (0.0, 1.0)
            
            eq_lambda    ::    equipartition parameter, Lambda, to specify
                               what fraction of the turbulent equipartition
                               magnetic field strength should be used. (0.0)
                               options --- [0.0, 1.0)
            
            b_rad_prof   ::    magnetic field radial profile. ('dipole')
                               options --- 'dipole'
                                           'gauss'
                                           'equip'  
            
            dynamo       ::    magnetic field 'dynamo' type. ('rot')
                               options --- 'rot'
                                           'turb'
            
            b_field_ramp ::    choose whether or not to ramp the magnetic
                               field strength from 0 to maximum value over
                               time. ('no')
                               options --- 'yes'
                                           'no'

           Returns:
           --------
           A model object that can be used to generate a new DMESTAR run.

           Raises:
           -------
        """
        self.mass       = float(mass)
        
        # composition properties
        self.feh        = float(feh)
        self.afe        = float(afe)
        self.x          = x
        self.y          = y
        self.z          = z
        self.y_prim     = float(y_prim)
        
        self.mix        = str(mixture)
        self.atm        = str(atm)
        
        # convective mixing length
        if a_mlt == 'solar':
            from dmestar.src import mixture
            solar = mixture.solar_calib[self.mix]
            self.a_mlt  = solar[3]
        else:
            self.a_mlt  = float(a_mlt)
        
        # other model properties
        self.N_models      = int(n_models)
        self.final_age     = float(final_age)
        self.turb_diff     = float(turb_diff)
        
        self.EOS           = str(eos)
        self.nuclearS      = str(nuclear_svals)
        
        # magnetic field properties
        self.b_field       = str(b_field)
        self.b_surf        = float(b_surf)       
        if self.b_surf < 1.e-4:
            self.b_field   = 'off'
        
        self.b_pert_age    = float(b_pert_age)
        self.b_gamma       = float(b_gamma)
        self.chi_f         = float(chi_f)
        self.fc_tach       = float(fc_tach)
        self.eq_lambda     = float(eq_lambda)
        self.b_rad_prof    = str(b_rad_prof)
        self.dynamo        = str(dynamo)
        self.b_field_ramp  = str(b_field_ramp)
     
    def evolve(self):
        """ Evolve an actual DMESTAR model """
        import subprocess as sp
        from .src import dirstruc as ds
        sp.call('{0}'.format(ds.mach + 'newpoly'))
        sp.call('{0}'.format(ds.binary + 'dmestar'))
        self.cleanup()
        
    def construct(self):
        """ Automatically call all required setup routines """
        self.scratch()
        self.setAbundances()
        self.setAtmosphere()
        self.polyNamelist()
        self.physNamelist()
        self.ctrlNamelist()
        self.magNamelist()
        self.linkInputData()
        self.linkOutputData()
        
    def scratch(self):
        """ Construct a scratch directory using username and 8 digits """
        from .src import dirstruc as ds
        import random
        
        user = os.getlogin()
        random.seed()
        rand = random.random()*1.e8
        self.scratch_dir = ds.base + 'scratch/{:s}_{:.0f}'.format(user, rand)
        try:
            os.chdir(self.scratch_dir)
        except OSError:
            os.mkdir(self.scratch_dir)
            os.chdir(self.scratch_dir)
        
    def linkInputData(self):
        """ Redirect input files to Fortran unit files """
        from .src import dirstruc as ds
        
        # check if old files exist
        try:
            os.remove('./fort.15')
            self.cleanup()
            import sys
            sys.exit('ERROR: Previous instance of DMESTAR was found and cleaned up.')
        except OSError:
            pass
        
        # Generate name for OPAL 95 opacity tables
        if self.afe == 0.0:
            opal95_tab = '{0}hz'.format(self.mix.upper())
        else:
            pass # EDIT for non-zero alpha/Fe
        
        # DO NOT TOUCH: opacity files
        print '\nLinking Library Files:'
        print '----------------------'
        self.link(ds.opac, 'FERMI.TAB', 'fort.15')
        self.link(ds.opac, 'thecond_07.d', 'fort.35')
        self.link(ds.opal, opal95_tab, 'fort.48')
        
        # Equation of state tables
        self.link(ds.eos, 'opal01/opaleos01.z0188', 'fort.49')
        self.link(ds.eos, 'scvh/h_tab_i.dat', 'fort.72')
        self.link(ds.eos, 'scvh/he_tab_i.dat', 'fort.73')
        
        # Atmosphere files
        self.link(ds.kur, self.kur_f, 'fort.38')
        for i in range(5): 
            os.symlink(self.phx_f[i], 'fort.{:.0f}'.format(95 + i))
            print 'Linked: {:s} ---> fort.{:.0f}'.format(self.phx_f[i], 95 + i)
        
        # Namelist files
        self.link('./', 'physics.nml',  'fort.13')
        self.link('./', 'control.nml',  'fort.14')
        self.link('./', 'magnetic.nml', 'fort.75')
        print ''
    
    def linkOutputData(self):
        """ Redirect output to permanent files """
        from .src.atmosphere import plusMinus as pM
        
        # create output file name
        fout = 'm{:04.0f}_{:s}_{:s}{:03.0f}_{:s}{:01.0f}_mlt{:4.3f}'.format(
                self.mass*1000., self.mix, pM(self.feh), abs(self.feh)*100.,
                pM(self.afe), abs(self.afe)*10., self.a_mlt)
        if self.b_field == 'on':
            fout += 'mag{:02.0f}kG'.format(self.b_surf/100.)
        
        self.fout = fout
        
        tmp = './'
        print 'Linking Output Files:'
        print '---------------------'
        # primary output files
        self.link(tmp, '{0}.trk'.format(fout),   'fort.37')
        self.link(tmp, '{0}.dtrk'.format(fout),  'fort.19')
        self.link(tmp, '{0}.short'.format(fout), 'fort.20')
        self.link(tmp, '{0}.last'.format(fout),  'fort.11')
        
        # secondary output files (uncomment to include in final file transfer)
        #
        #self.link(tmp, '{0}.grad'.format(fout), 'fort.8')
        #self.link(tmp, '{0}.env'.format(fout),  'fort.22')
        #self.link(tmp, '{0}.del'.format(fout),  'fort.41')
        #self.link(tmp, '{0}.isc'.format(fout),  'fort.77')
        if self.b_field == 'on':
            self.link(tmp, '{0}.mag'.format(fout),  'fort.76')
            self.link(tmp, '{0}.menv'.format(fout), 'fort.80')
    
    def link(self, directory, file1, file2):
        """ Generate symbolic link to fortran input file. """
        filepath1 = directory + file1
        try:
            os.symlink(filepath1, file2)
            print "Linked: {0} ---> {1}".format(filepath1, file2)
        except OSError:
            print "WARNING: Failed to link {0} ---> {1}".format(filepath1, file2)
            
        
    def polyNamelist(self):
        """ Write the polytrope namelist """
        wn.writePolyNamelist(self.mass, self.x, self.z, self.afe, 
                             self.a_mlt, self.mix)
        
    def physNamelist(self):
        """ Write the physics namelist """
        wn.writePhysNamelist(self.mass, self.atm, self.EOS, self.turb_diff,
                             self.nuclearS)
        
    def ctrlNamelist(self):
        """ Write the control namelist """
        wn.writeCtrlNamelist(self.x, self.y, self.z, self.afe, self.a_mlt, 
                             self.mix, final_age = self.final_age, 
                             n_models = self.N_models)
        
    def magNamelist(self):
        """ Write the magnetic namelist file """
        wn.writeMagNamelist(self.b_field, self.b_surf, self.b_pert_age,
                            self.b_gamma, self.chi_f,  self.fc_tach, 
                            self.eq_lambda, self.b_rad_prof, self.dynamo,
                            self.b_field_ramp)
        
    def setAtmosphere(self):
        """ Select correct atmosphere files """
        from .src import atmosphere as atm
        self.kur_f, self.phx_f = atm.select(self.feh, self.afe)
    
    def setAbundances(self):
        from .src import mixture
        self.x, self.y, self.z = mixture.setAbundances(self.x, self.y, self.z, 
                                                       self.mix, self.feh, 
                                                       self.afe, self.y_prim)
    
    def cleanup(self):
        """ Clean up after model run """
        from .src import dirstruc as ds  
        try:
            os.system('mv {0}/{1}.* {2}/'.format(os.getcwd(), self.fout, ds.outdir))
        except:
            pass
        os.system('rm fort.*')
        os.system('rm *.nml')
        os.rmdir(self.scratch_dir)
