#
#

class RunLog(object):
    
    def __init__(self, filename):
        """ Initialize new instance of RunLog """
        self.filename = filename
        self.log = open(filename, 'w')

    def warning(self, message = ''):
        """ Add warning to log file """
        self.log.write('WARNING: ' + message)

    def error(self, message = ''):
        """ Add error to log file """
        self.log.write('ERROR: ' + message)

    def close(self):
        """ Close and save log file """
        self.log.close()
