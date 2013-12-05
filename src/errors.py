
def valWarnBelow(var, val_min):
    """ Issues a value warning if value is below the accepted minimum """
    print "WARNING: {:s} value is below {:-2.1f}. Setting {:s} to {:-2.1f}".format( \
          str(var), val_min, str(var), val_min)
    return val_min

def valWarnAbove(var, val_max):
    print "WARNING: {:s} value is above {:-2.1f}. Setting {:s} to {:-2.1f}".format( \
          str(var), val_max, str(var), val_max)
    return val_max
    
def valErrMissing():
    print "ERROR: Missing a required input value."
    
