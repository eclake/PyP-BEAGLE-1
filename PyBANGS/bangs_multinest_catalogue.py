import numpy as np
import os
import cPickle

class MultiNestMode:

    def __init__(self, logEvidence, post_mean, max_likelihood, max_a_post):
        self.logEvidence = logEvidence
        self.post_mean = np.array(post_mean)
        self.max_likelihood = max_likelihood
        self.max_a_post = max_a_post

class MultiNestObject:

    def __init__(self, ID, logEvidence):
        self.ID = ID
        self.logEvidence = logEvidence
        self.mode = list()

    def add_mode(self, logEvidence, post_mean, max_likelihood, max_a_post):
        newMode = MultiNestMode( logEvidence, post_mean, max_likelihood, max_a_post )
        self.mode.append(newMode)

class MultiNestCatalogue:

    def __init__(self, n_par, catalogueName):

        self.catalogueName = catalogueName
        self.n_par = n_par

    def load_catalogue(self, filename):

        try:
            file = open(filename, 'rb')
            self.MNObjects = cPickle.load(file)
            file.close()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

        # You then access the data for each object and each mode as
        # self.MNObjects[0].mode[0].post_mean  ---> posterior mean values for
        # the different parameters for object 0 and mode 0

        # self.MNObjects[2].mode[1].max_likelihood ---> max_likelihood likelihood values for
        # the different parameters for object 2 and mode 1

    def make_catalogue(self, filelist, filename):

        self.MNObjects = list()

        # Open file for writing
        fOut = open(filename, 'w')

        # Loop over all files containing BANGS results
        for j, file in enumerate(filelist):

            # Object ID is what comes before the suffix (excluding the
            # directory tree!)
            end = file.find('_BANGS')
            objID = os.path.basename(file[:end]) 

            # Open the MultiNest "stats" file
            # Read the global evidence and total number of modes
            f = open(file, 'r')
            for i, line in enumerate(f):
                if i == 0:
                    logEvidence = float(line.split()[5])
                if i == 5:
                    n_modes = int(line.split()[3])
            f.close()

            # This number include the posterior mean, maximum likelihood and
            # maximum a posteriori for each parameter + the headers
            n_lines_per_mode = 8 + self.n_par*3

            # Useful information for the first mode start at line 11 (in Python
            # we count from 0)
            first_line = 10

            post_mean = list()
            max_likelihood = list()
            max_a_post = list()
            mode = list()
            
            # This object will contain the parameters (post mean, ecc...) for
            # each mode found by MultiNest
            MNObj = MultiNestObject(objID, logEvidence)

            # Now we read the evidence, post mean, maximum likelihood and map for each mode
            f = open(file, 'r')
            for i, line in enumerate(f):
                
                # Evidence
                if i == first_line:
                    logEv = float(line.split()[2])
                # Posterior mean for each parameter 
                elif( (i >= first_line+3) and (i < first_line+3+self.n_par) ):
                    post_mean.append( float(line.split()[1]) ) 
                # Maximum likelihood for each parameter 
                elif( (i >= first_line+6+self.n_par) and (i < first_line+6+2*self.n_par ) ):
                    max_likelihood.append( float(line.split()[1]) ) 
                # Maximum a posteriori for each parameter 
                elif( (i >= first_line+9+2*self.n_par) and (i < first_line+9+3*self.n_par ) ):
                    max_a_post.append( float(line.split()[1]) ) 

                # Once you've read the data for the first mode, put them into
                # the MultiNestObject!
                if i == (first_line + n_lines_per_mode):
                    MNObj.add_mode( logEv, post_mean, max_likelihood, max_a_post )
                    post_mean = list()
                    max_likelihood = list()
                    max_a_post = list()
                    first_line += n_lines_per_mode + 5

            f.close()

            # Finally append the MultiNestObject corresponding to the current
            # object to the catalogue
            self.MNObjects.append(MNObj)

        # Print to a file the data read from the different *stats* files, and
        # saved into self.MNObjects  
        cPickle.dump(self.MNObjects, fOut, cPickle.HIGHEST_PROTOCOL)

        # You then access the data for each object and each mode as
        # self.MNObjects[0].mode[0].post_mean  ---> posterior mean values for
        # the different parameters for object 0 and mode 0

        # self.MNObjects[2].mode[1].max_likelihood ---> max_likelihood likelihood values for
        # the different parameters for object 2 and mode 1

        # Close the output file containing the cataogue
        fOut.close()