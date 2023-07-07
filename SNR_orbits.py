import numpy
import math
from scipy import optimize
from scipy.interpolate import lagrange
####################################################
#Constants
####################################################
omeg_E = 7.2921151467e-5 #Earth's rotation rate
c = 299792458.0 #Speed of light
mu = 3.986004418e14 #G*Mearth
####################################################
#Precise orbits - reader and interpolator
####################################################
#This code reads in an sp3 file and outputs matrices of the satellite positions, times, and
#PRN numbers
def readsp3(sp3file):
    k=0
    with open(sp3file, 'rt') as g:
        rows = (line.split() for line in g)
        for grow in rows:
            if (k == 0):
                nt =  int(grow[6])
            if (k == 2):
                numsat = int(grow[1])
            k=k+1

    xpos = numpy.nan*numpy.ones([nt,numsat])
    ypos = numpy.nan*numpy.ones([nt,numsat])
    zpos = numpy.nan*numpy.ones([nt,numsat])
    satclock = numpy.nan*numpy.ones([nt,numsat])
    gpst = numpy.nan*numpy.ones([nt,1])
    PRN = list()
    k=0
    n=0
    t=0
    with open(sp3file, 'rt') as g:
        rows = (line.split() for line in g)
        for grow in rows:
            if (k == 0):
                if (grow[0] == "*"):
                    year = grow[1]
                    month = grow[2]
                    day = grow[3]
                    hour = grow[4]
                    minute = grow[5]
                    second = grow[6]
                    dtime64 = year + '-' + month.zfill(2) + '-' + day.zfill(2) + 'T' + hour.zfill(2) + ':' + minute.zfill(2) + ':' + "{0:011.8f}".format(float(second))
                    gps_time = (numpy.datetime64(dtime64) - numpy.datetime64('1980-01-06T00:00:00'))/ numpy.timedelta64(1, 's')
                    gps_week = int(gps_time/604800)
                    gps_sow = gps_time - gps_week*604800
                    gpst[t,0] = gps_time
                    k = 1
                    t=t+1
            else:
                if (n < numsat-1):
                    sat = grow[0]
                    if (len(PRN) < numsat):
                        PRN.append(sat[1:])
                    xpos[t-1,n] = grow[1]
                    ypos[t-1,n] = grow[2]
                    zpos[t-1,n] = grow[3]
                    satclock[t-1,n] = grow[4]
                    n=n+1
                elif (n == numsat-1):
                    sat = grow[0]
                    if (len(PRN) < numsat):
                        PRN.append(sat[1:])
                    xpos[t-1,n] = grow[1]
                    ypos[t-1,n] = grow[2]
                    zpos[t-1,n] = grow[3]
                    satclock[t-1,n] = grow[4]
                    n=0
                    k=0
    return(PRN, gpst, xpos, ypos, zpos, satclock)



#Interpolate the precise orbits using 11-point Lagrangian interpolation
#this is the low quality version to obtain a crude estimate of azimuth and elevation angle

def sp3interp_LQ(tt, satnum, PRN,  gpst, xpos, ypos, zpos, satclock):
    a1 = numpy.argmin(abs(tt-gpst))
    b1 = numpy.where(satnum == numpy.asarray(PRN))[0]
    [lent,lensat] = numpy.shape(gpst)
    if (len(b1) > 0):
        if ((a1 >= 5) & (a1 < lent-6)): 
            xinput = xpos[a1-5:a1+6,b1]
            yinput = ypos[a1-5:a1+6,b1]
            zinput = zpos[a1-5:a1+6,b1]
            cinput = satclock[a1-5:a1+6,b1]
            aclock = numpy.amax(cinput/1e-6)
            tinput = gpst[a1-5:a1+6,0]-tt
        elif ((a1 < 5) & (a1 < lent-6)):
            xinput = xpos[0:11,b1]
            yinput = ypos[0:11,b1]
            zinput = zpos[0:11,b1]
            cinput = satclock[0:11,b1]
            aclock = numpy.amax(cinput/1e-6)
            tinput = gpst[0:11,0]-tt
        else:
            xinput = xpos[lent-11:lent,b1]
            yinput = ypos[lent-11:lent,b1]
            zinput = zpos[lent-11:lent,b1]
            cinput = satclock[lent-11:lent,b1]
            aclock = numpy.amax(cinput/1e-6)
            tinput = gpst[lent-11:lent,0]-tt
        if (aclock > 99999):
            xnew = 999999.9
            ynew = 999999.9
            zpred = 999999.9
            cpred = 999999.9
            rclock = 999999.9
            rpath = 999999.9
            rho = 999999.9
        else:
            pc = lagrange(tinput,cinput)
            cpred = numpy.polyval(pc,0)
            tinput = tinput-cpred
            px = lagrange(tinput,xinput)
            py = lagrange(tinput,yinput)
            pz = lagrange(tinput,zinput)
            xpred = numpy.polyval(px,0)
            ypred = numpy.polyval(py,0)
            zpred = numpy.polyval(pz,0)
            r = math.sqrt(math.pow(xpred,2)+math.pow(ypred,2)+math.pow(zpred,2))
            phi = -omeg_E*r/c
            xnew = math.cos(phi)*xpred-math.sin(phi)*ypred
            ynew = math.sin(phi)*xpred+math.cos(phi)*ypred
    else:
        xnew = 999999.9
        ynew = 999999.9
        zpred = 999999.9
        cpred = 999999.9
        rclock = 999999.9
        rpath = 999999.9
        rho = 999999.9
        

    return(xnew, ynew, zpred, cpred)


#[PRN, gpst, xpos, ypos, zpos, satclock] = readsp3('nav/GBM0MGXRAP_20220150000_01D_05M_ORB.SP3')
#[xnew,ynew,znew,cpred] = sp3interp_LQ(1326067200.00, 'J01', PRN,  gpst, xpos*1000, ypos*1000, zpos*1000, satclock*1e-6)
