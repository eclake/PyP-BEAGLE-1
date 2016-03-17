import os
import argparse
import logging
from matplotlib import rc
from astropy.io import ascii
from astropy.io import fits

from bangs_spectra import Spectrum
from bangs_pdf import PDF
from bangs_utils import BangsDirectories, find_file

# 
parser = argparse.ArgumentParser()

parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG,
    default=logging.WARNING,
)

parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    action="store_const", dest="loglevel", const=logging.INFO,
)
args = parser.parse_args()    
logging.basicConfig(level=args.loglevel)

suffix = "BANGS.fits.gz"

# Global font size
font = {'size': 16}
rc('font', **font)

version = "Jan_2016"

redshiftStr = 'z9'
mStr = "m10"
iterStr = "iter10"
objID = "5"

# Initialize an instance of the main "Photometry" class
data_dir = "/Users/jchevall/JWST/Simulations/March_2016"
results_dir = "/Users/jchevall/Coding/BEAGLE/files/results/JWST/March_2016"
BangsDirectories.results_dir = results_dir

# Consider all files in the results directory
file_list = list()
file_IDs = list()
for file in os.listdir(results_dir):
    if file.endswith(suffix):
        file_list.append(file)
        file = file[0:file.find(suffix)-1]
        file_IDs.append(file)

my_spectrum = Spectrum()

my_PDF = PDF(os.path.join(results_dir, "params_names.json"))

for ID in file_IDs:

    # Plot the "triangle plot"
    print "ID: ", ID
    my_PDF.plot_triangle(ID)

# ********** Load observed spectrum *****************
    file_name = find_file(ID+'.fits', data_dir)
    my_spectrum.observed_spectrum.load(file_name)

    # ********** Plotting of the marginal photometry *****************
    my_spectrum.plot_marginal(ID)

#my_photometry.plot_replicated_data(ID)
stop

# *****************************************************
# *********** "BANGS summary catalogue" ****************
# *****************************************************

file_name = "BANGS_summary_catalogue.fits"

# ********* Load ***************
#my_photometry.summary_catalogue.load(file_name)

# ********* Compute ***************
#file_list = ("1021_BANGS.fits.gz", "5866_BANGS.fits.gz")
#for file in os.listdir(results_dir):
#    if file.endswith("BANGS.fits.gz"):
#        file_list.append(file)

#my_photometry.summary_catalogue.compute(file_list, file_name)

# *****************************************************
# *********** "BANGS MultiNest catalogue" ****************
# *****************************************************

file_name = "UVUDF_MultiNest.cat"

# ********* Load ***************
my_photometry.multinest_catalogue.load(file_name)

# ********* Compute ***************
#file_list = list()
#for file in os.listdir(results_dir):
#    if file.endswith("MNstats.dat"):
#        file_list.append(file)

#n_par = 6
#my_photometry.multinest_catalogue.compute( n_par, file_list, file_name)

# *****************************************************
# *********** Posterior Predictive Checks  ****************
# *****************************************************

file_name = "PPC.fits"

# ********* Load ***************
my_photometry.PPC.load( file_name) 

# ********* Compute ***************
#my_photometry.PPC.compute(my_photometry.observed_catalogue, 
#        my_photometry.filters, 
#        file_name=file_name)

# ********* Plot ***************

#my_photometry.PPC.plot_chi2()

my_photometry.PPC.plot_p_value(broken_axis=True)

stop

# *****************************************************
# *********** Residual Photometry  ****************
# *****************************************************

my_photometry.residual.compute(my_photometry.observed_catalogue,
        my_photometry.summary_catalogue, my_photometry.filters)

# *****************************************************
# *********** PDF  ****************
# *****************************************************