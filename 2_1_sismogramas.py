#!/usr/bin/env python3
# RECUERDE ACTIVAR UN PAQUETE DE ANACONDA CON OBSPY CONTENIDO
#from IPython import get_ipython
#get_ipython().magic('reset -sf')
import subprocess
import os
import matplotlib
matplotlib.use('Agg') # Graficos no aparecen en pantalla
import matplotlib.pyplot as plt
import numpy as np
#import datetime
from obspy.core import UTCDateTime 
from obspy.core import read # Leer datos sismicos mseed
# paquetes trigger
from obspy.signal.trigger import trigger_onset
from obspy.signal.trigger import recursive_sta_lta
#from   obspy.signal.tf_misfit   import   cwt
#from obspy import Stream
#%%########################################################################
################### CREAR EL PATH DE LA DATA PROCESADA ##################   
path: str ="/home/julito/Descargas/2020-1/topico-matt/"
guardapath: str =path+"/data_procesada"
if not os.path.exists(guardapath):
    os.mkdir(guardapath) # Creamos la carpeta contenedora de los sismogramas
#
################### LISTAR CARPETAS ##################################
d: str="data" # carpeta actual contenedora de datos sismologicos
path2=os.path.join(path,d)
dhoras=os.listdir(path2) # entramos a la carpeta de datos
dhoras.sort()
################### LISTAR HORAS  ####################################
#horas=[]
#for line in dhoras:
#   type= line.split("_")
#   x= type[0]
#   y=type[1]
#   horas.append(y)  
#del x,y
#%%###############################################################
#                                                                #   
#                      CARGA DE DATOS                            #
#                                                                #   
##################################################################  
############# Tomar data HHE,HHN,HHZ de cada hora/carpeta ########
keyword1="HHE" ; keyword11="BHE"
keyword2="HHN" ; keyword22="BHN"
keyword3="HHZ" ; keyword33="BHZ"
os.chdir(path2)
#
contador=1
for hfile in dhoras: #HORAS VACIAS:2660/4989:5030/5050:5100/6113:6130/
    d=os.listdir(hfile) # listamos todos los archivos de c/hora-carpeta
    f_HHE=[]; f_HHN=[];E=[]; N=[]
    Z=[];f_HHZ=[]
    for f in d: # seleccionamos un archivo
              #################   HHE   ##############################
        if (keyword1 in f or keyword11 in f) and f.endswith(".mseed"):  # HHE
            f_hhe=os.path.join(hfile,f)
            f_HHE.append(f_hhe) # guardamos los hhe en una variable
              #################   HHN    ###############################      
        elif (keyword2 in f or keyword22 in f) and f.endswith(".mseed"): # HHN
            f_hhn=os.path.join(hfile,f)
            f_HHN.append(f_hhn)            
            #################    HHZ    ################################        
        elif (keyword3 in f or keyword33 in f) and f.endswith(".mseed"): # HHZ
            f_hhz=os.path.join(hfile,f)
            f_HHZ.append(f_hhz)
    ########################   LECTURA TRAZAS OBSPY  #######################
    for tre in range(len(f_HHE)): # cargamos c/variable HHE en OBSPY
        try:
            trhhe=read(f_HHE[tre], format='mseed')
            E.append(trhhe)
        except Exception:
            pass
    #endfor HHE
    for trn in range(len(f_HHN)): # cargamos c/variable HHN en OBSPY
        try:
            trhhn=read(f_HHN[trn],format='mseed')
            N.append(trhhn)
        except Exception:
            pass
    #endfor HHN    
    for trz in range(len(f_HHZ)): # cargamos c/variable HHZ en OBSPY
        try:
            trhhz=read(f_HHZ[trz],format='mseed')
            Z.append(trhhz)
        except Exception:
            pass
    #endfor HHZ    
    print('HORA:  ',hfile[9:])
    print(len(f_HHE),' Archivos HHE presentes')
    print('> ',len(E),' Trazas HHE con datos')
    print(len(f_HHN),' Archivos HHN presentes')
    print('> ',len(N),' Trazas HHN con datos')
    print(len(f_HHZ),' Archivos HHZ presentes')
    print('> ',len(Z),' Trazas HHZ con datos')
    print('#')            
    #%%######################## PLOTEAR CADA CARPETA/HORA COMPLETA  ######## 
    trza=[];trez=[]; aa=[E,N,Z]; enz=["E","N","Z"]
    path0: str=path+"data_procesada/"+hfile[9:]+"/"
    if not os.path.exists(path0): # Crear la carpeta-hora de los resultados
        os.mkdir(path0)
    plt.ioff() # NO abrir los graficos en la pantalla
    PICKS2=[]
    for T in range(3):
        cont=0; TRAZ=aa[T];
        for x in range(len(TRAZ)): # A veces cada canal tiene varias trazas, sobre todo cuando hay sismos
            trza=TRAZ[cont]; 
            # PROCESADO DEL SISMOGRAMA            
            trez=trza[0].detrend('linear');trez.detrend('demean');trez.filter('bandpass', freqmin=5, freqmax=19,corners=1, zerophase=True);#trez.taper(0.05,type='hann')
            # PLOTEAMOS
            statname= trez.stats.station;   channame= trez.stats.channel;#nombre y canal de la traza
            titulo=(enz[T] + "___" + hfile[9:])
            fig1=plt.figure(titulo); fig1.suptitle(titulo, fontsize=12,fontweight="bold")
            #########  PLOT TRIGGER  #####
            ax1 =fig1.add_subplot(len(TRAZ),1,x+1)
            fig1.subplots_adjust(hspace=0)
            #%% TRIGGER STA/LTA
            STA=1;LTA=10 # //PARAMETRO 1//
            df = trez.stats.sampling_rate # frecuencia de muestreo
            cft = recursive_sta_lta(trez.data, int(STA * df), int(LTA * df)) # Funcion caracteristica de promedios. 
            thr_on=5 ;thr_off= 2 #   //PARAMETRO 2//
            npts = trez.stats.npts; t = np.arange(npts, dtype=np.float32) / df 
            #
            ax1.plot(t, trez.data, 'grey');fig1.subplots_adjust(hspace=0)
            # GATILLADO
            on_off = np.array(trigger_onset(abs(cft), thr_on, thr_off,max_len= (df*30),max_len_delete=False)) # GATILLADO
            #
            #%%############## GUARDAMOS TIEMPOS GATILLADOS COMO SISMOS ###############################
            on_off1=[row[0] for row in on_off] # extraemos on's de picks
            on_off2=[row[1] for row in on_off] # extraemos off's de picks
            #
            samp_rate=trez.stats.sampling_rate ;
            ########################################################## ON_picks
            pick_t = []
            for number in on_off1:
                pick_t.append(number / samp_rate)
            str_t=trez.stats.starttime; str_t_unix=str_t.timestamp
            #
            pickt_unix = []
            for num in pick_t:
                pickt_unix.append(num + str_t_unix)
            ######################################################### OFF_picks
            off_pick_t = []
            for nu in on_off2:
                off_pick_t.append(nu / samp_rate)
            #
            off_pickt_unix = []
            for n in pick_t:
                off_pickt_unix.append(n + str_t_unix)
            ##
            del pick_t,off_pick_t    
            ##
            # APLICAMOS DEADTIME
            min_len=30; pickt_unixx=[]; on_offx=[]
            for pck in range(len(pickt_unix)):
                deadtime = pickt_unix[pck] - off_pickt_unix[pck-1] # Diferencia pic_ON actual vs pic_OFF anterior 
                #
                if (deadtime > min_len):
                    pickt_unixx.append(pickt_unix[pck])
                    on_offx.append(on_off[pck])
                    #print(str(deadtime)+"   SI");print(str(pickt_unixx)); print(str(on_offx))
                elif (deadtime == 0.0):
                    pickt_unixx.append(pickt_unix[pck])
                    on_offx.append(on_off[pck])
                    #print(str(deadtime)+"   CERO");print(str(pickt_unixx)); print(str(on_offx))
                elif (deadtime < 0.0):
                    pickt_unixx.append(pickt_unix[pck])
                    on_offx.append(on_off[pck])
                    #print(str(deadtime)+"  PRIMERO")
                elif (deadtime < min_len):
                    #pickt_unixx.append(pickt_unix[pck])
                    #on_offx.append(on_off[pck])
                    #print(str(deadtime)+"   NO"); print(str(pickt_unixx)); print(str(on_offx))
                    pass
                else:
                    pickt_unixx.append(pickt_unix[pck])
                    on_offx.append(on_off[pck])
                    #print(str(deadtime)+ "    ELSE");print(str(pickt_unixx)); print(str(on_offx)) 
            #endfor  
            pickt_utc = []; pickt_UTC=[]
            for numb in pickt_unixx:
                pickt_utc=UTCDateTime(numb)
                pickt_UTC.append(pickt_utc)
            #
            P=['P'] *len(pickt_unixx); cero=['0']*len(pickt_unixx); bajo=['_']*len(pickt_unixx)
            chachan = [channame[2]] * len(pickt_unixx); statss = [statname] * len(pickt_unixx);     
            #
            PICKS=np.column_stack((pickt_unixx ,statss, chachan, P , cero , bajo))
            PICKS2.append(PICKS)
            #%%###################################################################
            # PLOT PICKS
            i, j = ax1.get_ylim(); on_offxx=np.array(on_offx)
            try:
                ax1.vlines(on_offxx[:, 0] / df, i, j, color='r', lw=2,label="Trigger On")
                ax1.vlines(on_offxx[:, 1] / df, i, j, color='b', lw=2,label="Trigger Off")
            except IndexError:
                pass
            ############### DETALLES PLOTEO SISMOGRAMA ###############
            ax1.get_shared_x_axes().join(ax1)
            ax1.set_ylabel((statname + '.' + channame), fontdict=dict(weight='bold'),labelpad=30, rotation=0, color='red') #size='large'
            ax1.yaxis.tick_right()
            fig1.subplots_adjust(left=0.15, top=0.95)
            #manager = plt.get_current_fig_manager()
            #manager.window.showMaximized()
            #ax.set_xticklabels([])
            #manager = plt.get_current_fig_manager()
            #manager.window.showMaximized()
            print('estacion ',statname,'/',channame,' cargada')     
            cont=cont+1
       ###### GUARDADO CADA PLOTEO CANAL/HORA ######################
        figure = plt.gcf()
        figure.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
        fign=path0 + enz[T] + '_' + hfile[9:] + ".png" ; figname=os.path.join(fign)
        plt.savefig(figname, bbox_inches='tight'); plt.close(figure); plt.close(fig1)
        #plt.show
        del fig1,figure,fign,figname,ax1
    #    
    #endfor Ploteo 3 canales
    ############# GUARDADO FECHA DE PICKS DE TODAS ESTACIONES, TODO CANAL/HORA ##############3
    f = open(path0 + 'picks__' + hfile[9:] + '.txt', "a")
    i = 0
    sizeofList = len(PICKS2)    
    while i < sizeofList :   
        for dd in PICKS2[i]:   
            print(*dd,' ',file=f)
        i += 1
    f.close()
    ff : str = ("picks__"+hfile[9:]+".txt"); fff : str = ("ORDEN_picks__"+hfile[9:]+".txt")
      
    del f_HHE,f_HHN,f_HHZ,E, N, Z
    #
    os.chdir(path0)
    os.system('''cat '''+ff+''' |awk '{printf "%.2f %s %s %s %s %s\\n",$1, $2, $3, $4, $5, $6}' '''+ff+''' | sort -k1 -n > '''+ fff)
    print('#####  HORA ',contador ,' COMPLETA   ##################')    
    os.system('say "HORAA COMPLETAA" ')
    contador=contador+1  
    os.system("rm "+ff)
    os.chdir(path2)
    del ff,fff    
###############################################################
###############################################################
del contador, d, dhoras, f_hhz , hfile #,f_hhe, f_hhn,f 
del keyword1, keyword2, keyword3, keyword11, keyword22, keyword33
del path, path2, trz, tre, trn#line
del trez, trza, aa, enz,cont 
print('#################################################')
print('############## DATA COMPLETA ####################')
subprocess.call(["python3", "/home/julito/Descargas/2020-1/topico-matt/correo_control.py"])
os.system('say "DESCAARRGAA COMPLETAA"')
os.system('say "DESCAARRGAA COMPLETAA"')
os.system('say "DESCAARRGAA COMPLETAA"')
os.system('say "DESCAARRGAA COMPLETAA"')

