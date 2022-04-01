#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################ MAPA VERTICAL-SUBTERRANEO 3D EVENTOS #################
#
########### PROCESADO DE DATOS ########################################
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d

filee="EVENTOS.txt" # Leemos el archivo con los eventos: [unixt. lat lon prof]
ff=open(filee,"r")
liness=ff.readlines()
eve_prof=[];eve_lon=[];eve_lat=[]
conta=0
for xx in liness:   # cargamos lat,lon y prof estimadas para c/evento como variables STRING en python
    eve_lat.append(xx.split(' ')[2])
    eve_lon.append(xx.split(' ')[3])
    eve_prof.append(xx.split(' ')[4])
    print('evento n°:'+str(conta)+' leido')
    conta=conta+1
ff.close()

eve_profu=[];eve_long=[];eve_lati=[]
for xxx in range(len(eve_lon)):    # Traspaso de variables a datos FLOAT, paquete axes3d no admite graficos de datos str#
	eve_long.append(float(eve_lon[xxx]))
	eve_profu.append(float(eve_prof[xxx]))
	eve_lati.append(float(eve_lat[xxx]))


############### MAPEO PROPIAMENTE TAL ##########################
import itertools
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
import cartopy.feature as cf
from cartopy.mpl.patch import geos_to_path
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

fig = plt.figure()
ax = Axes3D(fig,xlim=[-180, 180],ylim=[-90, 90])

ax.set_zlim([-110,0])
ax.set_xlim([-75.0, -67.3506])
ax.set_ylim([-31.279, -24.1272])

feature = cf.NaturalEarthFeature('physical', 'coastline', '50m')
borde=[-50.666,-20.555,-60.55,-20]
feature = cf.NaturalEarthFeature('physical', 'coastline', '50m')
geoms = feature.intersecting_geometries(borde)
lc = LineCollection(geoms, edgecolor='black')
ax.add_collection3d(lc)
ax.scatter(eve_long, eve_lati,eve_profu, s=20, c='b')

plt.xlabel('Longitud');plt.ylabel('Latitud'); ax.set_zlabel('Profundidad')
plt.title(' 2019 ')
plt.show()
