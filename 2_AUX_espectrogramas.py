#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 16:08:42 2020

@author: julito
"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf')
import os
#import time
#import glob
from obspy.core import read
import matplotlib.pyplot as plt
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
dhoras_MODIFICADO=(dhoras[8:11])
#print('######################   RED/ESTACIONES/CANAL/ HORA ##################')
for hfile in dhoras_MODIFICADO:   #:len(dhoras) # seleccionamos una hora-carpeta
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
        path1: str=path0 + enz[T] + "/" ;savepath1=os.mkdir(path1)
        cont=0; TRAZ=aa[T]
        for x in range(len(TRAZ)):
           trza=TRAZ[x]; 
           # PROCESADO DEL SISMOGRAMA
           trez=trza[0].detrend('linear')
           trez.detrend('demean')
           trez.taper(0.05,type='hann')
           # PLOTEAMOS CADA ESTACION Y SU ESPECTROGRAMA
           statname= trez.stats.station; channame= trez.stats.channel;#nombre y canal de la traza
           titulo=(statname + "_" + "_" + enz[T] + "___" + hfile[9:])
           t=np.arange(0,trez.stats.npts / trez.stats.sampling_rate, trez.stats.delta)
           fig1=plt.figure("espectrograma_"+ titulo )
           fig1.suptitle(titulo ,fontsize=24,fontweight="bold")
           plt.subplot(211)
           plt.specgram(trez, NFFT=2**6, Fs=50 , noverlap=2**5)
           plt.xticks(size = 20)
           plt.yticks(size = 20)
           plt.subplot(212)
           plt.plot(t,trez.data,'k')
           plt.xlabel('Time [s]')
           plt.xticks(size = 20)
           plt.yticks(size = 20)
           manager = plt.get_current_fig_manager()
           manager.window.showMaximized()
           #
           figure = plt.gcf()
           figure.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
           fign=path1 + statname  + '_' + channame + ".png" ; figname=os.path.join(fign)
           plt.savefig(figname, bbox_inches='tight'); plt.close(figure); plt.close(fig1)
           del fig1,figure,fign,figname
           print('Espectrograma de estacion ',statname,'/',channame,' cargado') 
        ###################### SI UD. QUIERE EL GIF DE LOS ESPECTROGRAMAS DE C/HORA: DESCOMENTE ###############
        # bashCD = "cd " + path1 
        # bashCommand = ("convert -delay 100 -loop 0 *.png "+path0+"espectrograma_" + enz[T] + "_"+ hfile[9:] +".gif" )
        # os.system(bashCD +";"+ bashCommand)
        ######################################################################
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
