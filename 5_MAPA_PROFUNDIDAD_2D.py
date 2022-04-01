#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################ MAPA VERTICAL-SUBTERRANEO 2D EVENTOS #################
import matplotlib.pyplot as plt
import numpy as np

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
for xxx in range(len(eve_lon)):    # Traspaso de variables a datos FLOAT.#
	eve_long.append(float(eve_lon[xxx]))
	eve_profu.append(float(eve_prof[xxx]))
	eve_lati.append(float(eve_lat[xxx]))

plt.plot(eve_long,eve_profu,'.')
plt.xlabel('Lon [°]')
plt.ylabel('Profundidad [km]')
plt.grid(color='grey', linestyle='--', linewidth=0.5)
plt.show()



