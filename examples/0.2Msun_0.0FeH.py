# Simple example to construct and evolve an 0.2 solar mass model with
# solar metallicity, [Fe/H] = 0.0, to an age of 20 Gyr.
#
import dmestar

# specify stellar properties
mass = 0.2
Fe_H = 0.0

star = dmestar.Model(mass, Fe_H, final_age = 2.0e10)  # new instance of Model
star.construct()                                      # construct all required input files
star.evolve()                                         # start the program 
