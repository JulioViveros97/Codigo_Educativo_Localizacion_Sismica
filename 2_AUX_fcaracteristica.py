#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 12:39:56 2020

@author: julito
"""

#!/usr/bin/env python3
from IPython import get_ipython
get_ipython().magic('reset -sf')
import os
#import time
#import glob
from obspy.core import read
import matplotlib.pyplot as plt
# paquetes trigger
from obspy.core import read
from obspy.signal.trigger import trigger_onset
from obspy.signal.trigger import recursive_sta_lta
import numpy as np
#from   obspy.signal.tf_misfit   import   cwt
#from obspy import Stream
#########################################################################
###### Cargamos la columna de nombres-estaciones########## 
path: str ="/home/julito/Descargas/2020-1/topico-matt/"
guardapath: str =path+"/data_procesada"
if not os.path.exists(guardapath):
    os.mkdir(path) # Creamos la carpeta contenedora de los sismogramas
fname: str ="estaciones_taltal_serena.txt"
file=os.path.join(path,fname)
f= open(file, "r")
data= f.read()
datta=data.strip().split()
est=[]
for count, line in enumerate(datta, start=0):
    if count % 5 == 0:
        est.append(line) # est = nombres estaciónes en juego
del fname,count,data,datta,f,file,line
######################################################################
################### Listar carpetas ##################################
d: str="data" # carpeta contenedora de datos sismologicos
path2=os.path.join(path,d)
dhoras=os.listdir(path2) # entramos a la carpeta de datos
dhoras.sort()
################### Listar horas  ####################################
horas=[]
for line in dhoras:
   type= line.split("_")
   x= type[0]
   y=type[1]
   horas.append(y)  
del x,y
#################################################################
############# Tomar data HHE,HHN,HHZ de cada hora/carpeta ########
keyword1="HHE" ; keyword11="BHE"
keyword2="HHN" ; keyword22="BHN"
keyword3="HHZ" ; keyword33="BHZ"
os.chdir(path2)
#
contador=1
#print('######################   RED/ESTACIONES/CANAL/ HORA ##################')
for hfile in dhoras:#[9:10]: # seleccionamos una hora-carpeta
    d=os.listdir(hfile) # se abren todos los archivos de c/hora
    f_HHE=[]; f_HHN=[]; f_HHZ=[];E=[]; N=[]; Z=[];
    for f in d: # seleccionamos un archivo
        ###################   HHE   ####################################
        if (keyword1 in f or keyword11 in f) and f.endswith(".mseed"):  # TRABAJAMOS PARA HHE
            f_hhe=os.path.join(hfile,f)
            f_HHE.append(f_hhe) # guardamos los hhe en una variable
            #print('dato:',f_hhe[42:53], '___Hora :',hfile[9:])
              #################   HHN    ###################################      
        elif (keyword2 in f or keyword22 in f) and f.endswith(".mseed"):
            f_hhn=os.path.join(hfile,f)
            f_HHN.append(f_hhn)            
            #print('dato:',f_hhn[42:53], '___Hora :',hfile[9:])
            #################    HHZ    #################################       
        elif (keyword3 in f or keyword33 in f) and f.endswith(".mseed"):
            f_hhz=os.path.join(hfile,f)
            f_HHZ.append(f_hhz)
            #print('dato:',f_hhz[42:53], '___Hora :',hfile[9:])
    ########################   LECTURA OBSPY TRAZAS  #######################
    for tre in range(len(f_HHE)): # cargamos c/variable HHE en OBSPY
        try:
            trhhe=read(f_HHE[tre], format='mseed')
            E.append(trhhe)
        except Exception:
            pass
    for trn in range(len(f_HHN)): # cargamos c/variable HHN en OBSPY
        try:
            trhhn=read(f_HHN[trn],format='mseed')
            N.append(trhhn)
        except Exception:
            pass 
    for trz in range(len(f_HHZ)): # cargamos c/variable HHZ en OBSPY
        try:
            trhhz=read(f_HHZ[trz],format='mseed')
            Z.append(trhhz)
        except Exception:
            pass    
    print('HORA:  ',hfile[9:])
    print(len(f_HHE),' Archivos HHE presentes')
    print('> ',len(E),' Trazas HHE con datos')
    print(len(f_HHN),' Archivos HHN presentes')
    print('> ',len(N),' Trazas HHN con datos')
    print(len(f_HHZ),' Archivos HHZ presentes')
    print('> ',len(Z),' Trazas HHZ con datos')
    print('#')            
############################ PLOTEAR CADA CARPETA/HORA COMPLETA  ######## 
    trza=[];trez=[]; aa=[E,N,Z] ; enz=["E","N","Z"]
    path0: str=path+"data_procesada/"+hfile[9:]+"/"
    if not os.path.exists(path0):
        os.mkdir(path0)
    plt.ioff()
    for T in range(3):
        cont=0; TRAZ=aa[T];
        for x in range(len(TRAZ)):
            trza=TRAZ[cont]; 
            # PROCESADO DEL SISMOGRAMA
            trez=trza[0].detrend('linear')
            trez.detrend('demean')
            #trez.taper(0.05,type='hann')
            trez.filter('bandpass', freqmin=5, freqmax=19,corners=1, zerophase=True)
            # PLOTEAMOS
            statname= trez.stats.station; channame= trez.stats.channel;#nombre y canal de la traza
            titulo=("funcion_caracteristica__"+enz[T] + "___" + hfile[9:])
            fig1=plt.figure(titulo)
            fig1.suptitle(titulo, fontsize=12,fontweight="bold")
            #########  PLOT ESPECTROGRAMAS Y TRIGGER  #####
            # trigger
            STA=1;LTA=10
            df = trez.stats.sampling_rate
            cft = recursive_sta_lta(trez.data, int(STA * df), int(LTA * df))
            thr_on=5  ;thr_off= 2
            npts = trez.stats.npts
            t = np.arange(npts, dtype=np.float32) / df
            on_off = np.array(trigger_onset(cft, thr_on, thr_off,max_len= (df*30),max_len_delete=False))
            #ax.set_xticklabels([])
            #
            ###### PLOT FUNCION  CARACTERISTICA
            ax2 =fig1.add_subplot(len(TRAZ),2,x+1)
            fig1.subplots_adjust(hspace=0)
            ax2.plot(t,abs(cft), 'grey')
            fig1.subplots_adjust(hspace=0)
            ax2.axhline(thr_on, color='red', lw=1, ls='--')
            ax2.axhline(thr_off, color='blue', lw=1, ls='--')
            ax2.get_shared_x_axes().join(ax2)
             #
            fig1.subplots_adjust(left=0.15, top=0.95)
            ax2.set_ylabel((statname + '.' + channame), fontdict=dict(weight='bold'),labelpad=30, rotation=0, color='red') #size='large'
            ax2.yaxis.tick_right()
            manager = plt.get_current_fig_manager()
            manager.window.showMaximized()
            print('f.caracteristica ',statname,'/',channame,' cargada')     
            cont=cont+1
       ###### GUARDADO CADA PLOTEO CANAL/HORA ######################
        figure = plt.gcf()
        figure.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
        fign=path0 + "fcaracteristica_"+enz[T] + '_' + hfile[9:] + ".png" ; figname=os.path.join(fign)
        plt.savefig(figname, bbox_inches='tight'); plt.close(figure); plt.close(fig1)
        #plt.show
        del fig1,figure,fign,figname,ax2
    print('#####  HORA ',contador ,' COMPLETA   ##################')    
    contador=contador+1    
    del f_HHE,f_HHN,f_HHZ,E, N, Z
###############################################################
###############################################################
del contador, d, dhoras, f , f_hhe, f_hhn, f_hhz , hfile
del keyword1, keyword2, keyword3, keyword11, keyword22, keyword33
del line, path, path2, tre, trn, trz,
del trez, trza, aa, enz,cont 
print('#################################################')
print('############## DATA COMPLETA ####################')
