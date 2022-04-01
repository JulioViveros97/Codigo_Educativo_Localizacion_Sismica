#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# FUNCION PICK MANUAL DE ONDAS P Y S PARA ESTACIONES DE EVENTOS FILTRADOS.
#%%
import os
import matplotlib.image as img 
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor, Button
import numpy as np
from obspy.core import read,Trace,Stream,UTCDateTime
from pathlib import Path
import time
###############################################################################
#%% 1) CARGA ARCHIVO DE EVENTOS A PICKEAR
path: str ="/home/julito/Descargas/2020-1/topico-matt/"
#
# (*) Creamos un archivo copia de los eventos para borrar lineas a medida que avancemos.
filee:str = path + "EVENTOS_copia_pick.txt"
if not os.path.isfile(filee):
        os.system("cp "+path+"EVENTOS.txt "+path+"EVENTOS_copia_pick.txt")
# (*) Cargamos el archivo de eventos y columnas.       
ff=open(filee,"r") ; liness=ff.readlines()
eve_prof=[];eve_lon=[];eve_lat=[]; eve_dir=[]; eve_unixt=[];
conta=0
for xx in liness:   # cargamos dir,unix,lon,lat y prof estimadas para c/evento como variables STRING en python
    eve_dir.append(xx.split(' ')[0]) # NOMBRE-FECHA CARPETA
    eve_unixt.append(xx.split(' ')[1]) # FECHA UNIX EVENTO
    eve_lat.append(xx.split(' ')[2]) # LATITUD ESTIMADA (1INV) EVENTO
    eve_lon.append(xx.split(' ')[3]) # LONGITUD ESTIMADA(1INV) EVENTO
    eve_prof.append(xx.split(' ')[4]) # PROFUNDIDAD ESTIMADA (1INV) EVENTO
    print('evento a pickear n°:'+str(conta+1)+' leido')
    conta=conta+1
ff.close() ; del conta, ff, liness, xx
print("###########################################################")
# (*) Modificamos columna de fecha-carpeta para acceder a la descarga original en /data/
eve_dirc=[]
for xx in eve_dir:
    eve_dirc.append(path+'data/'+'Descarga_'+xx+'/')
del xx
#
# (*) Cargamos el archivo de los nombres de estaciones
f_namestat: str=path + "estaciones_taltal_serena.txt"
fff=open(f_namestat,"r") ; lin=fff.readlines()
namestat=[];chanstat=[]; conta=0
for xxx in lin:
    namestat.append(xxx.split(' ')[0]) # NOMBRE ESTACIONES
    chanstat.append(xxx.split(' ')[3]) # NOMBRE CANAL(ES)
    print('estacion n°: '+str(conta+1)+' a evaluar: '+ ('\033[1m {}\033[00m' .format(namestat[conta])) +' de canales '+('\033[1m {}\033[00m' .format(chanstat[conta])))
    conta=conta+1
fff.close; del fff, lin, xxx, conta
# (*) Construir la keyword para entrar a c/archivo.
#
# Matriz: 
# Keyword -> componentes
# |
# v
# estaciones
#
#
keychan=[]
for chan in chanstat:
    keychan.append(chan.split(',',3)) # separar columnas por las comas, 3 columnas
#
keyword=[];conta=0;
for stat in namestat:
    keyword.append([stat+'_'+ x for x in keychan[conta] ]) # añadir prefijo estacion correspondiente, a cada columna
    conta=conta+1
del keychan,conta,chan,stat
#
print("###########################################################"); 
print("###########################################################")
##################################################################################################################
#%% 2) CICLO PICKEADO P + S
#def MANUAL_PICK_PS():


print('\033[1m {}\033[00m' .format("FUNCION PICK MANUAL LLEGADAS P Y S PARA EVENTOS FILTRADOS DE FALSOS POSITIVOS")); print(" ")
# CICLO: CARGA ESTACION C/CARPETA DE eve_dir  
contaevento=0; keyword2=".mseed"
for dd in eve_dirc[0:1]: #(*) ///Evento///  Abrimos un carpeta-hora de datos originales 
    try:
        #
        # #                
        # #
        d=os.listdir(dd)
        print(('\033[1m {}\033[00m' .format("Evento N°    "+str(contaevento+1)) +": ") + ('\033[92m {}\033[00m' .format(eve_unixt[contaevento]))  ) 
        print( ('\033[1m {}\033[00m' .format("Dentro de Hora: "))+ ('\033[92m {}\033[00m' .format(eve_dir[contaevento])) )
        print(" ")
        #
        eve_date_unix = float(eve_unixt[contaevento])
        eve_date_utc = UTCDateTime(eve_date_unix)
        #
        txt_final=[]
        #
        F_TRAZA=[]
        # LEER ESTACIONES QUE TENGAN LA KEYWORD + .MSEED, leer-> por fila(estacion),luego columna(canal).
        for est in range(len(keyword)): # (*) ///Estacion///
            print('\033[1m {}\033[00m' .format("Estacion ") + '\033[92m {}\033[00m' .format(str(namestat[est])) )
            for can in range(len(keyword[0])): #(*) ///Canal///
                print('Pickeamos la traza: '+str(keyword[est][can]))
                # CARGAR LA TRAZA COMPLETA DE STAT_CHAN(X) SEGUN KEYWORD #
                for file in d:
                    if ((keyword[est][can] in file) and file.endswith(".mseed")) and ((Path(dd+file).stat().st_size) != 0):
                        print(str(file) + " encontrado")
                        ff=read(dd+file, format='mseed')
                        # RECORTAR LA TRAZA SEGUN FECHA EVENTO (1° estimacion Binder.sh)
                        #finicio_nuevo=(eve_date_utc-10)
                        ff.trim(eve_date_utc, eve_date_utc+120)
                        #
                        #OPCIONAL: abrir un espectrograma, click para cerrar e ingresar los extremos del filtro pasabanda.
                        #ff.spectrogram()
                        #
                        #PROCESADO
                        trez=ff[0].detrend('linear');trez.detrend('demean');trez.filter('bandpass', freqmin=5, freqmax=19,corners=1, zerophase=True);#trez.taper(0.05,type='hann')
                        #PLOT
                        #fig = trez.plot(color='gray',handle=True)
                        fig,ax= plt.subplots()
                        #
                        # pasamos el eje x desde muestras a segundos.
                        df = trez.stats.sampling_rate
                        npts = trez.stats.npts
                        t = np.arange(npts, dtype=np.float32) / df
                        # plot
                        ax.plot(t,trez,color='gray')
                        #
                        # PICK MANUAL P Y S, otro boton para cerrar
                        cursor=Cursor(ax,horizOn=False,vertOn=True,color='green',linewidth=2.0)
                        plt.draw(); plt.waitforbuttonpress(0)
                        PICKS=[]; conta_pic=0;te=[];fase=["P","S"]
                
                        def onclick(event):
                            tt=time.time(); te.append(tt)#;print(tt)
                        #    
                        def onrelease(event):
                            global conta_pic
                            x_pic = event.xdata
                            ttt = time.time()
                            #
                            if ((ttt-te[conta_pic]) <= 0.1) and (len(PICKS)<2): # click largo, no se condiera pick(ej.zoom)
                                print(  '\033[1m {}\033[00m' .format('pick n°'+str(conta_pic+1)+' en el segundo: ') + str( eve_date_utc + x_pic ) );
                                PICKS.append(x_pic)
                            elif len(PICKS) == 2: #(mas de dos picks: P,S; cierran el plot)
                                plt.close()
                            elif len(PICKS)>2:
                                plt.close()
                            else:
                                pass
                            conta_pic=conta_pic+1
                        #
                        def evento_o_ruido():
                            ask=input('¿La traza tiene P-S visibles? [s/n]')
                            if ask =="s":
                                return True
                            if ask =="n":
                                return False
                        ###
                        if evento_o_ruido()== True:        
                            while len(PICKS)<len(fase):
                                fig.canvas.mpl_connect('button_press_event',onclick)
                                fig.canvas.mpl_connect('button_release_event', onrelease)
                                plt.show()                               
                        else:
                            plt.close()
                        #
                        #
                        for i in range(len(PICKS)):
                            pick_unix= eve_date_unix + PICKS[i]
                            pick_utc=  eve_date_utc + PICKS[i]
                            txt: str= str(keyword[est][can]) +' '+ str(eve_date_utc) + ' ' + str(eve_date_unix) + ' ' + str(fase[i]) 
                            txt_final.append(txt)
                            #print(txt)      
                        # GUARDAR LOS PICKS, COLUMNA P Y COL S
                        # GUARDADO EN FORMATO LEGIBLE DENTRO DE data_procesada PARA REPICKS CADA EVENTO
                        # : 
                        # RENOMBRAR COMO repicks_manual_PS_MINI_X.txt
                        # (LINEA:"BINDER_VIEJO" unixt_evento tiempo_YYYMMDDMMSS lat lon prof N°est )
                        # (NLINEAS): nombre_est unixtP ? ? ? P _ REPICK_MANUAL
                        # (NLINEAS): nombre_est unixtP ? ? ? S _ REPICK_MANUAL
                        # :
                    else:
                        pass
                # 
            print("####");print("####")
        # GUARDAR LA LISTA DE PICKS DE LA CARPETA/EVENTO
        #endfor FIN ciclo carga traza con keyword 
        #txt_final=np.stack(txt_final)
        with open(path+"data_procesada/"+str(eve_dir[contaevento])+"/repick_manual_"+str(eve_date_unix)+".txt","+ab") as ff:
            np.savetxt(ff, txt_final, fmt='%s',delimiter=' ', newline='\n')
        ff.close()
    except Exception:
        # ANOTAR EN TXT CUANDO HAYAN ERRORES/no estaciones
        pass
    contaevento=contaevento+1
#endfor FIN ciclo carpeta-hora    
# 


