# Simple example to create a set of models with a range of masses from
# 0.1 solar masses to 1.0 solar masses. Metallicity is taken to be solar
# and the maximum allowed age is 20 Gyr.
#
import dmestar
from numpy import arange

Fe_H = 0.0                                                # declare metallicity
masses = arange(0.1, 1.1, 0.1)                            # create array of masses

for mass in masses:                                       # loop through each mass
    star = dmestar.Model(mass, Fe_H, final_age = 2.0e10)  # new instance of Model
    star.construct()                                      # generate all input files
    star.evolve()                                         # start program
    del star                                              # clear memory for safety
