import georinex as gr
import numpy
import math
import datetime
import os
import SNR_orbits
import SNR_filedownloader
import SNR_tools
import sys
###############################################################
#Constants
###############################################################
c = 299792458.0 #speed of light
fL1 = 1575.42e6 #L1 frequency
fL2 = 1227.60e6 #L2 frequency
wL1 = c/fL1 #L1 wavelength
wL2 = c/fL2 #L2 wavelength
###############################################################
#Command line arguments for Site, year, day of year
###############################################################
site = sys.argv[1]
year = sys.argv[2]
doy = sys.argv[3]
###############################################################
#Initialize Folders
###############################################################
if not os.path.exists('output'): #if output folder doesn't exist, make it
	os.makedirs('output')
if not os.path.exists('rinex'): #if rinex folder doesn't exist, make it
        os.makedirs('rinex')
if not os.path.exists('nav'): #if nav folder doesn't exist, make it
        os.makedirs('nav')
###############################################################
#Download Files
###############################################################
SNR_filedownloader.getsp3GFZMGNSSfile(year, doy) #download the SP3 file from GFZ
navfile = 'nav/GBM0MGXRAP_'+year+doy+'0000_01D_05M_ORB.SP3' #name of the nav file

SNR_filedownloader.getrinex3(site,year,doy) #download the rinex3 file 
rinexfile = 'rinex/'+site+'_'+year+'_'+doy+'.rnx' #name of the rinex file
###############################################################
#Read Files
###############################################################
[PRN, gpstsat, xpos, ypos, zpos, satclock] = SNR_orbits.readsp3(navfile) #read the SP3 file, load data to arrays

header=gr.rinexheader(rinexfile) #read the rinex header
(x0,y0,z0)=header['position'] #use the a priori location of the site from the RINEX header

#Load the rinex file, place the values into variables
data = gr.load(rinexfile) 

S1C = data['S1C'].values
S1P = data['S1P'].values
S1W = data['S1W'].values

S2C = data['S2C'].values
S2I = data['S2I'].values
S2L = data['S2L'].values
S2P = data['S2P'].values
S2W = data['S2W'].values

S3Q = data['S3Q'].values

S5Q = data['S5Q'].values

S6C = data['S6C'].values
S6I = data['S6I'].values

S7I = data['S7I'].values
S7Q = data['S7Q'].values

S8Q = data['S8Q'].values


obs_time = data.time.values
nt = len(obs_time)
svs = data.sv
ns = len(svs)

try:
	S1C = data['S1C'].values
except Exception:
	S1C = numpy.nan*numpy.ones((nt,ns))
try:
	S1P = data['S1P'].values
except Exception:
	S1P = numpy.nan*numpy.ones((nt,ns))
try:
	S1W = data['S1W'].values
except Exception:
	S1W = numpy.nan*numpy.ones((nt,ns))
try:
	S2C = data['S2C'].values
except Exception:
	S2C = numpy.nan*numpy.ones((nt,ns))
try:
	S2I = data['S2I'].values
except Exception:
	S2I = numpy.nan*numpy.ones((nt,ns))
try:
	S2L = data['S2L'].values
except Exception:
	S2L = numpy.nan*numpy.ones((nt,ns))
try:
	S2P = data['S2P'].values
except Exception:
	S2P = numpy.nan*numpy.ones((nt,ns))
try:
	S2W = data['S2W'].values
except Exception:
	S2W = numpy.nan*numpy.ones((nt,ns))
try:
	S3Q = data['S3Q'].values
except Exception:
	S3Q = numpy.nan*numpy.ones((nt,ns))
try:
	S5Q = data['S5Q'].values
except Exception:
	S5Q = numpy.nan*numpy.ones((nt,ns))
try:
	S6C = data['S6C'].values
except Exception:
	S6C = numpy.nan*numpy.ones((nt,ns))
try:
	S6I = data['S6I'].values
except Exception:
	S6I = numpy.nan*numpy.ones((nt,ns))
try:
	S7I = data['S7I'].values
except Exception:
	S7I = numpy.nan*numpy.ones((nt,ns))
try:
	S7Q = data['S7Q'].values
except Exception:
	S7Q = numpy.nan*numpy.ones((nt,ns))
try:
	S8Q = data['S8Q'].values
except Exception:
	S8Q = numpy.nan*numpy.ones((nt,ns))
try:
	S5A = data['S5A'].values
except Exception:
	print("No S5A")
	S5A = numpy.nan*numpy.ones((nt,ns))


###############################################################
#loop over time and satellites, compute the orbits, compute the
#azimuth and elevation angles, then write to file
###############################################################
#name of the outfile
outfile = site+'_'+year+'_'+doy+'_SNR.txt'
ffo = open(outfile,'w')

for i in range(0,nt):
	gps_time = (numpy.datetime64(obs_time[i]) - numpy.datetime64('1980-01-06T00:00:00'))/ numpy.timedelta64(1, 's') #compute gps time, seconds from Jan 6, 1980
	for j in range (0, ns):
		SNRvals = numpy.array([[S1C[i,j]],[S1P[i,j]],[S1W[i,j]],[S2C[i,j]],[S2I[i,j]],[S2L[i,j]],[S2P[i,j]],[S2W[i,j]],[S3Q[i,j]],[S5Q[i,j]],[S6C[i,j]],[S6I[i,j]],[S7I[i,j]],[S7Q[i,j]],[S8Q[i,j]]])
		a1 = numpy.where(~numpy.isnan(SNRvals))[0]
		if (len(a1) > 0):
			sv1 = svs.sv[j]
			[xnew,ynew,znew,cpred] = SNR_orbits.sp3interp_LQ(float(gps_time), str(sv1.values), PRN,  gpstsat, xpos*1000, ypos*1000, zpos*1000, satclock*1e-6)
			if (xnew == 999999.9):
				pass
			else:
				[azi,elev] = SNR_tools.azi_elev(float(x0),float(y0),float(z0),xnew,ynew,znew)

				s1c = "{0:.2f}".format(float(S1C[i,j]))
				s1p = "{0:.2f}".format(float(S1P[i,j]))
				s1w = "{0:.2f}".format(float(S1W[i,j]))

				s2c = "{0:.2f}".format(float(S2C[i,j]))
				s2i = "{0:.2f}".format(float(S2I[i,j]))
				s2l = "{0:.2f}".format(float(S2L[i,j]))
				s2p = "{0:.2f}".format(float(S2P[i,j]))
				s2w = "{0:.2f}".format(float(S2W[i,j]))

				s3q = "{0:.2f}".format(float(S3Q[i,j]))
	
				s5q = "{0:.2f}".format(float(S5Q[i,j]))

				s6c = "{0:.2f}".format(float(S6C[i,j]))
				s6i = "{0:.2f}".format(float(S6I[i,j]))

				s7i = "{0:.2f}".format(float(S7I[i,j]))
				s7q = "{0:.2f}".format(float(S7Q[i,j]))

				s8q = "{0:.2f}".format(float(S8Q[i,j]))
				gpst = "{0:.2f}".format(float(gps_time))
				aziout = "{0:.2f}".format(float(azi))
				elevout = "{0:.2f}".format(float(elev))

				ffo.write(str(i)+' '+gpst+' '+str(sv1.values)+' '+aziout+' '+elevout+' '+s1c+' '+s1p+' '+s1w+' '+s2c+' '+s2i+' '+s2l+' '+s2p+' '+s2w+' '+s3q+' '+s5q+' '+s6c+' '+s6i+' '+s7i+' '+s7q+' '+s8q+'\n')

ffo.close()
