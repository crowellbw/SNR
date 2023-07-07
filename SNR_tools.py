#!/usr/bin/env python
import numpy
import datetime
import calendar
import math
import georinex as gr
#####################################################################################
#SNR_tools.py
#Written by Brendan Crowell, University of Washington
#Last edited July 7, 2023
#####################################################################################
c = 299792458.0 #speed of light
fL1 = 1575.42e6 #L1 frequency
fL2 = 1227.60e6 #L2 frequency

#Convert months into an index
def month_converter(month):
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    return months.index(month) + 1

#Find the month from the day of the year
def doy2month(doy,year):
    isleap = calendar.isleap(year)
    if str(isleap) == 'True':
        dom = [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        dom = [31,28,31,30,31,30,31,31,30,31,30,31]

    dayind = int(dom[0])
    monind=1
    for i in range (1, 12):
        if (int(doy) < dayind):
            month = monind
        else:
            dayind = dayind+dom[i]
            monind=monind+1
            
    return(month)

#Compute the day of the year from year, month, day
def doy_calc(year,month,day):
    isleap = calendar.isleap(year)
    if str(isleap) == 'True':
        dom = [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        dom = [31,28,31,30,31,30,31,31,30,31,30,31]
    doy = int(numpy.sum(dom[:(month-1)])+day)
    return(doy)

#compute the GPS week and day of week from year and day of year
def gpsweekdow(year,doy):
    date = datetime.datetime(year, 1, 1) + datetime.timedelta(doy - 1)
    gpstime = (numpy.datetime64(date) - numpy.datetime64('1980-01-06T00:00:00'))/ numpy.timedelta64(1, 's')
    gpsweek = int(gpstime/604800)
    gpsdow = math.floor((gpstime-gpsweek*604800)/86400)                   
    return(gpsweek, gpsdow)


#Determine the number of leap seconds between GPS time and UTC
def gpsleapsec(gpssec):
    leaptimes = numpy.array([46828800, 78364801, 109900802, 173059203, 252028804, 315187205, 346723206, 393984007, 425520008, 457056009, 504489610, 551750411, 599184012, 820108813, 914803214, 1025136015, 1119744016, 1167264017])
    leapseconds = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    a1 = numpy.where(gpssec > leaptimes)[0]
    leapsec = len(a1)
    return(leapsec)


#Convert lat, lon, alt into ITRF XYZ
def lla2ecef(lat,lon,alt):
    lat = lat*math.pi/180
    lon = lon*math.pi/180
    a = 6378137
    e = 8.1819190842622e-2

    N = a/numpy.sqrt(1-numpy.power(e,2)*numpy.power(numpy.sin(lat),2))

    x = (N+alt)*numpy.cos(lat)*numpy.cos(lon)
    y = (N+alt)*numpy.cos(lat)*numpy.sin(lon)
    z = ((1-numpy.power(e,2))*N+alt)*numpy.sin(lat)

    return (x, y, z)

#Convert ITRF XYZ into lat, lon, alt
def ecef2lla(x,y,z):
    a = 6378137
    e = 8.1819190842622e-2

    b = math.sqrt(math.pow(a,2)*(1-math.pow(e,2)))
    ep = math.sqrt((math.pow(a,2)-math.pow(b,2))/math.pow(b,2))
    p = math.sqrt(math.pow(x,2)+math.pow(y,2))
    th = math.atan2(a*z,b*p)
    lon = math.atan2(y,x)
    lat = math.atan2((z+math.pow(ep,2)*b*math.pow(math.sin(th),3)),(p-math.pow(e,2)*a*math.pow(math.cos(th),3)))
    N = a/math.sqrt(1-math.pow(e,2)*math.pow(math.sin(lat),2))
    alt = p/math.cos(lat)-N

    return (lat,lon,alt)

#compute the azimuth and elevation angle between satellite to receiver
def azi_elev(xsta,ysta,zsta,xsat,ysat,zsat):
    [latsta,lonsta,altsta]=ecef2lla(xsta,ysta,zsta)
    [latsat,lonsat,altsat]=ecef2lla(xsat,ysat,zsat)
    re = math.sqrt(math.pow(xsta,2)+math.pow(ysta,2)+math.pow(zsta,2))
    rs = math.sqrt(math.pow(xsat,2)+math.pow(ysat,2)+math.pow(zsat,2))
    gamma = math.acos(math.cos(latsta)*math.cos(latsat)*math.cos(lonsat-lonsta) + math.sin(latsta)*math.sin(latsat))
    elev = math.acos(math.sin(gamma)/math.sqrt(1 + math.pow(re/rs,2) - 2*re/rs*math.cos(gamma)))

    deltalon = lonsat-lonsta

    azi = math.atan2(math.sin(deltalon)*math.cos(latsat),math.cos(latsta)*math.sin(latsat)-math.sin(latsta)*math.cos(latsat)*math.cos(deltalon))

    azi = azi*180/math.pi

    if (azi < 0):
        azi = azi+360
    elev = elev*180/math.pi
    return(azi,elev)

#takes in a pandas array from georinex, outputs the observables available
#def obs_available(data):
#    print('test')
#data = gr.load('col2262s.22o')
#print(data['obs'])
