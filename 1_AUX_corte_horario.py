#!/usr/bin/env python3
import os
from obspy.core import read
from obspy.core import UTCDateTime
################ SCRIPT SEPARADOR ARCHIVOS DIARIOS A HORARIOS #################
#%%########################################################################
################### CREAR EL PATH DE LA DATA PROCESADA ##################   
path: str ="/home/julito/Descargas/2020-1/topico-matt/"
################### LISTAR CARPETAS ##################################
d: str="data" # carpeta actual contenedora de datos sismologicos
path2=os.path.join(path,d)
dhoras=os.listdir(path2) # entramos a la carpeta de datos
dhoras.sort()
#
guardapath: str =path+"data_trozada/"
if not os.path.exists(guardapath):
    os.mkdir(guardapath) # Creamos la carpeta contenedora de los cortes horarios
#
os.chdir(path2)
#
for hfile in dhoras:#seleccionamos un día-carpeta//[9:10] para experimento// 
    dia=os.listdir(hfile); dia.sort() # listamos todos los archivos de c/dia-carpeta
    hh=00
    #
    print("#");print("#");print("#");print("#")
    print("// ABRIMOS EL DÍA "+ str(hfile) + " //"); print("#");print("#");print("#");print("#")
    for h in range(24): # fabricamos una carpeta  
        path_hora: str =guardapath +"Descarga_2019-"+hfile[14:16]+"-"+hfile[17:19]+"T"+(str(hh+h).zfill(2))+":00:00/" 
        os.mkdir(path_hora)
        #
        print("#");print("#")
        print("// CREAMOS LA HORA   2019-"+hfile[14:16]+"-"+hfile[17:19]+"T"+(str(hh+h).zfill(2))+":00:00   //")
        print("#");print("#")
        #
        try:
            dti=UTCDateTime("2019-"+hfile[14:16]+"-"+hfile[17:19]+"T"+(str(hh+h).zfill(2))+":00:00")
            dtf=UTCDateTime("2019-"+hfile[14:16]+"-"+hfile[17:19]+"T"+(str(hh+h+1).zfill(2))+":00:00")
        except Exception:
            dti=UTCDateTime("2019-"+hfile[14:16]+"-"+hfile[17:19]+"T"+(str(hh+h).zfill(2))+":00:00")
            dtf=UTCDateTime("2019-"+hfile[14:16]+"-"+hfile[17:19]+"T"+(str(hh+h).zfill(2))+":59:59")
        #
        for f in dia: # seleccionamos un archivo-canal-estacion
            if f.endswith(".mseed"):
                try:
                    #print("CORTAMOS EL ARCHIVO   / "+ str(f)+" /" )
                    file=os.path.join(hfile,f)
                    traz=read(file,format='mseed')
                    #CORTAR MSEED,UNA HORA(h); CORTAR METADARA,UNA HORA(h)  
                    cont=0
                    for x in range(len(traz)):
                        traz.merge()
                        trza=traz[cont].copy()
                        tt=trza.slice(dti,dtf)
                        #print(traz)
                        #print(tt)
                        #GUARDAR CORTES EN path_hora
                        ss: str= f[0:36]+(str(hh+h).zfill(2))+":00:00"+".mseed"
                        save=os.path.join(path_hora,ss) 
                        tt.write(save, format="MSEED") 
                        del traz,trza,tt,ss,save
                except Exception:
                    pass
    del dia    

                
