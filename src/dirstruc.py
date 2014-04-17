# directory locations for dmestar

# output file directory
outdir  = '/Users/grefe950/evolve/models/tmp'

# base directories
base    = '/Users/grefe950/evolve/'
data    = '/usr/local/dmestar/data/'
mach    = '/usr/local/dmestar/bin/'

# top level directories
binary  = base + 'mDsepX/'

# local data directories
nml     = base + 'nml/'
zams    = base + 'zams/'
poly    = base + 'poly/'
prems   = base + 'prems/'

# data level directories
atm     = data + 'atm/'
eos     = data + 'eos/'
opac    = data + 'opac/'

# first level directories
phx     = atm  + 'phx/'
kur     = atm  + 'kur/'
ferg    = opac + 'ferg04/'
opal    = opac + 'opal/'

# second level directories
phxnorm = phx + 'GS98/t010/'
phxteff = phx + 'AGSS09/teff/'
phxt100 = phx + 'GS98/t100/'
