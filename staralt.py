# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:31:39 2015

@author: Inaki Ordonez-Etxeberria

Script to show the altitude of an astronomical target during a specific night.
It is possible to change the position of observation (lat, lon), as well the date and the coordinates of the target. 

"""

import ephem
from math import degrees
import matplotlib.pyplot as plt


#Variables
fecha = '2015/12/29' #date 
lat = '42.7167' #Latitude and Longitude for the point of observation. Guirguillano (MPC: J81): lat = '42.7167'; lon =  '-1.8667'
lon =  '-1.8667'
#Coordinates of the target 
AR = ephem.hours('5:14:32') #Right Ascension in hour
DEC = ephem.degrees('-8:12:05.9') #Declination in degrees


#definition of the observatory
observatory = ephem.Observer()
observatory.lon = str(lon)
observatory.lat = str(lat)

# Definition of the target
target = ephem.Equatorial(AR, DEC, epoch = ephem.J2000)
body = ephem.FixedBody()
body._ra = target.ra
body._dec = target.dec
body._epoch = target.epoch

altitude = []
tablehours=[]
sec2days=1.157408e-05
interval = 450 #seconds between each calculation.
portion = int(3600 / interval) #portion of hours, used to split the plot. 

#determining the date and hours
sun = ephem.Sun() 
observatory.date = ephem.Date(fecha) 
h0 = ' ' + str(observatory.previous_setting(sun).tuple()[3]) + ':' + str(observatory.previous_setting(sun).tuple()[4]) 
nightduration = (observatory.next_rising(sun).tuple()[3]) - (observatory.previous_setting(sun).tuple()[3]) + 25 #is not the real night duration, but the hours to plot

for i in range(0,nightduration * int(portion)):
    observatory.date = ephem.Date(fecha + h0) + (i * interval * sec2days)
    body.compute(observatory)
    altitude.append(degrees(body.alt))
    tablehours.append(observatory.date.tuple()[3])

# tables with values to show in the x axe. 
tablehours2 = tablehours[::portion]
tablesticks = list(range(0,len(tablehours2)*portion,portion))

# calculation of the sunset and sunrise
sunset = ((observatory.previous_setting(sun).tuple()[4])/60.)
sunrise = ((observatory.next_rising(sun).tuple()[3]))+ ((observatory.next_rising(sun).tuple()[4])/60.) - ((observatory.previous_setting(sun).tuple()[3])) + 24

plt.title(fecha)
plt.grid()
plt.xticks(tablesticks ,tablehours2)
plt.xlabel('Time UTC')
plt.ylabel('Altitude')
plt.ylim(0,90)
plt.plot(altitude, label = 'RA: %s; DEC: %s' % (ephem.hours(target.ra), ephem.degrees(target.dec)))
plt.plot([sunset * portion,sunset * portion], [90,0], '--')
plt.plot([sunrise * portion,sunrise * portion], [90,0], '--')
plt.plot([sunset * portion + portion * 1.2,sunset * portion + portion * 1.2], [90,0], '-.')
plt.plot([sunrise * portion - portion * 1.2,sunrise * portion - portion * 1.2], [90,0], '-.')

#Text of sunset, sunrise, twilight, ...
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 8,
        }
plt.text(sunset * portion + portion * 0.2, 85, 'sunset: ' +  str(observatory.previous_setting(sun).tuple()[3]) + ':' + str('%02d' % observatory.previous_setting(sun).tuple()[4]), fontdict=font, rotation='vertical')
plt.text(sunset * portion + portion * 1.4, 85, 'twilight night', fontdict=font, rotation='vertical')
plt.text(sunrise * portion - portion * 0.4, 85, 'sunrise: ' + str('%02d' % observatory.previous_rising(sun).tuple()[3]) + ':' + str('%02d' % observatory.previous_rising(sun).tuple()[4]), fontdict=font, rotation='vertical')
plt.text(sunrise * portion - portion * 1.6, 85, 'twilight day', fontdict=font, rotation='vertical')

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
