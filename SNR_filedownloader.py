#!/usr/bin/env python
import wget
import os
import urllib
import SNR_tools
from ftplib import FTP_TLS
import sys
#####################################################################################
#SNR_filedownloader.py
#Written by Brendan Crowell, University of Washington
#Last edited July 7, 2023
#VARIABLES
#year - 4 digit string of year
#doy - 3 digit string of day of year
#site - 7 digit string of site id, rinex3 convention
#Rinex3 files are renamed to SITE_YEAR_DOY.rnx
#####################################################################################
#This subroutine downloads the any sp3 file for a given day from CDDIS
def getsp3file(year, doy):
    if not os.path.exists('nav'): #if nav folder doesn't exist, make it
        os.makedirs('nav')
    [gpsweek,gpsdow]=SNR_tools.gpsweekdow(int(year),int(doy))
    week = str(int(gpsweek))
    dow = str(int(gpsdow))
    fname = 'nav/igs' + week + dow + '.sp3.Z'
    fname2 = 'nav/igs' + week + dow + '.sp3'
    fname3 = 'nav/GBM0MGXRAP_' + year + doy + '0000_01D_05M_ORB.SP3'
    if (os.path.isfile(fname2) == True):
        print ('Final orbit file ' + fname2 + ' already exists')
    else:
        try:
            ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
            ftps.login(user='anonymous', passwd='snivel@uw.edu')
            ftps.prot_p()
            ftps.cwd('gnss/products/' + week + '/')
            ftps.retrbinary("RETR " + 'igs' + week + dow + '.sp3.Z', open('igs'+ week + dow + '.sp3.Z', 'wb').write)
            #url = 'ftp://cddis.gsfc.nasa.gov/gnss/products/' + week + '/igs' + week + dow + '.sp3.Z'
            print('Downloading final orbit file '+fname2)
            os.system('mv igs'+ week + dow + '.sp3.Z nav')
            os.system('gunzip' + ' ' + fname)
            os.system('cp' + ' ' + fname2 + ' ' + fname3 )
        except Exception:
            print ('Final orbit not available, trying rapid orbits')
            
#This subroutine downloads the multi-GNSS SP3 file from GFZ
def getsp3GFZMGNSSfile(year, doy):
    if not os.path.exists('nav'): #if nav folder doesn't exist, make it
        os.makedirs('nav')
    [gpsweek,gpsdow]=SNR_tools.gpsweekdow(int(year),int(doy))
    week = str(int(gpsweek))
    dow = str(int(gpsdow))
    fname = 'nav/GBM0MGXRAP_' + year + doy + '0000_01D_05M_ORB.SP3.gz' 
    fname2 = 'nav/GBM0MGXRAP_' + year + doy + '0000_01D_05M_ORB.SP3'

    if (os.path.isfile(fname2) == True):
        print ('GFZ Orbit File ' + fname2 + ' already exists')
    else:
        url = 'ftp://ftp.gfz-potsdam.de/GNSS/products/mgnss//' + week + '/GBM0MGXRAP_' + year + doy + '0000_01D_05M_ORB.SP3.gz' 
        print('Downloading orbit file '+fname2)
        wget.download(url, out='nav/')
        os.system('gunzip' + ' ' + fname)        

#This subroutine will download RINEX3 files given the station, year and day of year from the IGS.
def getrinex3IGS(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
            ftps.login(user='anonymous', passwd='snivel@uw.edu')
            ftps.prot_p()
            ftps.cwd('gnss/data/daily/' + year + '/' + doy + '/' + year[-2:] + 'd/')
            ftps.retrbinary("RETR " + fnameZ2, open(fnameZ2, 'wb').write)
            os.system('mv '+ fnameZ2 + '  rinex')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
                ftps.login(user='anonymous', passwd='snivel@uw.edu')
                ftps.prot_p()
                ftps.cwd('gnss/data/daily/' + year + '/' + doy + '/' + year[-2:] + 'd/')
                ftps.retrbinary("RETR " + fnameZ2S, open(fnameZ2S, 'wb').write)
                os.system('mv '+ fnameZ2S + '  rinex')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print('RINEX file '+ fnamefinal + ' not at IGS')


def getrinex3EPN(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://epncb.eu/ftp/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://epncb.eu/ftp/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print ('Rinex not at EPN')

def getrinex3BKG_EUREF(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://igs.bkg.bund.de/root_ftp/EUREF/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://igs.bkg.bund.de/root_ftp/EUREF/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print('Rinex not at BKG_EUREF')

def getrinex3BKG_GREF(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://igs.bkg.bund.de/root_ftp/GREF/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://igs.bkg.bund.de/root_ftp/GREF/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print('Rinex not at BKG_GREF')

def getrinex3BKG_IGS(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://igs.bkg.bund.de/root_ftp/IGS/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://igs.bkg.bund.de/root_ftp/IGS/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print('Rinex not at BKG_IGS')

def getrinex3BKG_MGEX(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://igs.bkg.bund.de/root_ftp/MGEX/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://igs.bkg.bund.de/root_ftp/MGEX/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print('Rinex not at BKG_MGEX')

def getrinex3BEV(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'


    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://gnss.bev.gv.at/at.gv.bev.dc/data/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://gnss.bev.gv.at/at.gv.bev.dc/data/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print('Rinex not at BEV')

def getrinex3APREF(site, year, doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)        
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print('Rinex not at APREF')


def getrinex3(site,year,doy):
    fnameZ = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamed = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx'
    fnameo = 'rinex/'+site+'_R_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2 = site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnameZS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
    fnamedS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx'
    fnameoS = 'rinex/'+site+'_S_'+year+doy+'0000_01D_30S_MO.rnx'
    fnameZ2S = site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'

    fnamefinal = 'rinex/'+site+'_'+year+'_'+doy+'.rnx'

    if not os.path.exists('rinex'): #if rinex folder doesn't exist, make it
        os.makedirs('rinex')
    
    if (os.path.isfile(fnamefinal) == True):
        print ('RINEX file '+ fnamefinal + ' already exists')
    else:
        try:
            url = 'https://epncb.eu/ftp/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
            wget.download(url, out='rinex/')
            os.system('gunzip' + ' ' + fnameZ)
            os.system('./CRX2RNX ' + fnamed)
            os.system('mv '+ fnameo + ' ' + fnamefinal)
        except Exception:
            try:
                url = 'https://epncb.eu/ftp/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                wget.download(url, out='rinex/')
                os.system('gunzip' + ' ' + fnameZS)
                os.system('./CRX2RNX ' + fnamedS)
                os.system('mv '+ fnameoS + ' ' + fnamefinal)
            except Exception:
                print ('Rinex not at EPN')
                try:
                    url = 'https://gnss.bev.gv.at/at.gv.bev.dc/data/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
                    wget.download(url, out='rinex/')
                    os.system('gunzip' + ' ' + fnameZ)
                    os.system('./CRX2RNX ' + fnamed)
                    os.system('mv '+ fnameo + ' ' + fnamefinal)
                except Exception:
                    try:
                        url = 'https://gnss.bev.gv.at/at.gv.bev.dc/data/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                        wget.download(url, out='rinex/')
                        os.system('gunzip' + ' ' + fnameZS)
                        os.system('./CRX2RNX ' + fnamedS)
                        os.system('mv '+ fnameoS + ' ' + fnamefinal)
                    except Exception:
                        print('Rinex not at BEV')
                        try:
                            url = 'https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
                            wget.download(url, out='rinex/')
                            os.system('gunzip' + ' ' + fnameZ)
                            os.system('./CRX2RNX ' + fnamed)
                            os.system('mv '+ fnameo + ' ' + fnamefinal)
                        except Exception:
                            try:
                                url = 'https://ga-gnss-data-rinex-v1.s3.amazonaws.com/public/daily/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                wget.download(url, out='rinex/')
                                os.system('gunzip' + ' ' + fnameZS)
                                os.system('./CRX2RNX ' + fnamedS)
                                os.system('mv '+ fnameoS + ' ' + fnamefinal)
                            except Exception:
                                print('Rinex not at APREF')
                                try:
                                    url = 'https://igs.bkg.bund.de/root_ftp/EUREF/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                    wget.download(url, out='rinex/')
                                    os.system('gunzip' + ' ' + fnameZ)
                                    os.system('./CRX2RNX ' + fnamed)
                                    os.system('mv '+ fnameo + ' ' + fnamefinal)
                                except Exception:
                                    try:
                                        url = 'https://igs.bkg.bund.de/root_ftp/EUREF/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                        wget.download(url, out='rinex/')
                                        os.system('gunzip' + ' ' + fnameZS)
                                        os.system('./CRX2RNX ' + fnamedS)
                                        os.system('mv '+ fnameoS + ' ' + fnamefinal)
                                    except Exception:
                                        print('Rinex not at BKG_EUREF')
                                        try:
                                            url = 'https://igs.bkg.bund.de/root_ftp/GREF/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                            wget.download(url, out='rinex/')
                                            os.system('gunzip' + ' ' + fnameZ)
                                            os.system('./CRX2RNX ' + fnamed)
                                            os.system('mv '+ fnameo + ' ' + fnamefinal)
                                        except Exception:
                                            try:
                                                url = 'https://igs.bkg.bund.de/root_ftp/GREF/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                                wget.download(url, out='rinex/')
                                                os.system('gunzip' + ' ' + fnameZS)
                                                os.system('./CRX2RNX ' + fnamedS)
                                                os.system('mv '+ fnameoS + ' ' + fnamefinal)
                                            except Exception:
                                                print('Rinex not at BKG_GREF')
                                                try:
                                                    url = 'https://igs.bkg.bund.de/root_ftp/IGS/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                                    wget.download(url, out='rinex/')
                                                    os.system('gunzip' + ' ' + fnameZ)
                                                    os.system('./CRX2RNX ' + fnamed)
                                                    os.system('mv '+ fnameo + ' ' + fnamefinal)
                                                except Exception:
                                                    try:
                                                        url = 'https://igs.bkg.bund.de/root_ftp/IGS/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                                        wget.download(url, out='rinex/')
                                                        os.system('gunzip' + ' ' + fnameZS)
                                                        os.system('./CRX2RNX ' + fnamedS)
                                                        os.system('mv '+ fnameoS + ' ' + fnamefinal)
                                                    except Exception:
                                                        print('Rinex not at BKG_IGS')
                                                        try:
                                                            url = 'https://igs.bkg.bund.de/root_ftp/MGEX/obs/'+year+'/'+doy+'/'+site+'_R_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                                            wget.download(url, out='rinex/')
                                                            os.system('gunzip' + ' ' + fnameZ)
                                                            os.system('./CRX2RNX ' + fnamed)
                                                            os.system('mv '+ fnameo + ' ' + fnamefinal)
                                                        except Exception:
                                                            try:
                                                                url = 'https://igs.bkg.bund.de/root_ftp/MGEX/obs/'+year+'/'+doy+'/'+site+'_S_'+year+doy+'0000_01D_30S_MO.crx.gz'
                                                                wget.download(url, out='rinex/')
                                                                os.system('gunzip' + ' ' + fnameZS)
                                                                os.system('./CRX2RNX ' + fnamedS)
                                                                os.system('mv '+ fnameoS + ' ' + fnamefinal)
                                                            except Exception:
                                                                print('Rinex not at BKG_MGEX')
                                                                try:
                                                                    ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
                                                                    ftps.login(user='anonymous', passwd='snivel@uw.edu')
                                                                    ftps.prot_p()
                                                                    ftps.cwd('gnss/data/daily/' + year + '/' + doy + '/' + year[-2:] + 'd/')
                                                                    ftps.retrbinary("RETR " + fnameZ2, open(fnameZ2, 'wb').write)
                                                                    os.system('mv '+ fnameZ2 + '  rinex')
                                                                    os.system('gunzip' + ' ' + fnameZ)
                                                                    os.system('./CRX2RNX ' + fnamed)
                                                                    os.system('mv '+ fnameo + ' ' + fnamefinal)
                                                                except Exception:
                                                                    try:
                                                                        ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
                                                                        ftps.login(user='anonymous', passwd='snivel@uw.edu')
                                                                        ftps.prot_p()
                                                                        ftps.cwd('gnss/data/daily/' + year + '/' + doy + '/' + year[-2:] + 'd/')
                                                                        ftps.retrbinary("RETR " + fnameZ2S, open(fnameZ2S, 'wb').write)
                                                                        os.system('mv '+ fnameZ2S + '  rinex')
                                                                        os.system('gunzip' + ' ' + fnameZS)
                                                                        os.system('./CRX2RNX ' + fnamedS)
                                                                        os.system('mv '+ fnameoS + ' ' + fnamefinal)
                                                                    except Exception:
                                                                        print('RINEX file '+ fnamefinal + ' not available')


#Examples
##getrinexhr('lwck','2018','002')
#getrinex3('TONG','2022','015')
##getbcorbit('2018','002')
##gettseries('p494')
##
#getsp3file('2018','002')

#getsp3GFZMGNSSfile('2022', '015')

#getrinex3('TONG00TON','2022','001')
