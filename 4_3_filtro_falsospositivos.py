#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################### CODIGO FILTRO MANUAL FALSOS POSITIVOS #####
import matplotlib.image as img 
from matplotlib import pyplot as plt
import numpy as np
import os
from datetime import datetime
#
path: str ="/home/julito/Descargas/2020-1/topico-matt/"
d: str="data_procesada/" # carpeta actual contenedora de datos sismologicos
path2=os.path.join(path,d)
dhoras=os.listdir(path2) # entramos a la carpeta de datos
dhoras.sort()
#
# LECTURA DEL ARCHIVO GUARDA POSIBLES EVENTOS
filee= path + "EVENTOS_copia.txt" # Leemos el archivo con los eventos: [dir unixt. lat lon prof]
if not os.path.isfile(filee):
        os.system("cp EVENTOS.txt EVENTOS_copia.txt")
#
ff=open(filee,"r")
liness=ff.readlines()
eve_prof=[];eve_lon=[];eve_lat=[]; eve_dir=[]; eve_unixt=[];
conta=0
for xx in liness:   # cargamos dir,unix,lon,lat y prof estimadas para c/evento como variables STRING en python
    eve_dir.append(xx.split(' ')[0])
    eve_unixt.append(xx.split(' ')[1])
    eve_lat.append(xx.split(' ')[2])
    eve_lon.append(xx.split(' ')[3])
    eve_prof.append(xx.split(' ')[4])
    print('posible evento n°:'+str(conta)+' leido')
    conta=conta+1
ff.close()
#
true_eve_dir=[];true_eve_unixt=[];true_eve_lat=[];true_eve_lon=[];true_eve_prof=[]
###################################################
os.chdir(path2) ; c=0;cc=0; keyword1="MINI"; keyword2=".png"
###################### INICIO CICLO ###############
#
for hfile in eve_dir: # entramos a carpeta evento
    path3=path2 + hfile; os.chdir(path3);  hh=os.listdir(path3); keyword3=eve_unixt[c]
    #
    if hfile == eve_dir[c-1]: # Para multiples eventos dentro de una hora.
        try:
            cc=cc+1
        except IndexError:
            cc=0
    else:
        cc=0
    #### ABRIR PNG'S CON KEYWORD "MINI" SI CORRESPONDE A N° EVENTO CORRECTO ###
    print("#########################################")
    print( '\033[01m {}\033[00m' .format("Verifique el posible evento   N°")   + '\033[92m {}\033[00m' .format(str(c)))
    print('\033[01m {}\033[00m' .format("            CARPETA  ///  FECHA "))
    print('\033[92m {}\033[00m' .format(str(hfile)) +'\033[01m {}\033[00m' .format("///") + '\033[92m {}\033[00m' .format(str(eve_unixt[c])));
    imagen=[]
    for h in hh: # listamos la carpeta donde puede haber un evento
        if (str(keyword1+"_"+str(cc)+keyword2) in h): # Abrir el .png del supuesto evento
            print(str(h));imagen.append(h) 
        #endif    
    #endfor            
    #
    #### PLOT SUPUESTO EVENTO: tricomponente.####
    titulo=str(hfile) + "///" + str(eve_unixt[c] + "///" +keyword1+" "+str(cc))        
    fig=plt.figure(titulo,constrained_layout=False,figsize=(11,8) )
    fig.text(0.5, 0.005, '[s]', ha='center',fontweight='bold')
    #gs = fig.add_gridspec( 1,3, wspace=0)
    axs = fig.subplots(1,3,sharey='row'); fig.subplots_adjust(wspace=0)  
    ccc=1
    for ax in axs:
        plt.subplot(1,3,ccc)
        plt.xlim(170,2500); plt.ylim(50,1570)
        labels=['0','20','40','60','80','100','120']
        plt.xticks(np.arange(170,2500,step=332.857),labels) 
        plt.grid(axis='x',color='g',linestyle='--',linewidth=0.5)
        plt.yticks([]); plt.title(str(imagen[ccc-1]))
        i=img.imread(imagen[ccc-1])
        plt.imshow(i,interpolation='nearest',aspect='auto',alpha=0.8)
        ccc=ccc+1   
    plt.tight_layout(); fig.subplots_adjust(wspace=0)
    plt.draw()
    #
    # 
    plt.waitforbuttonpress(0);plt.close(fig)  
    ####### ALMACENAR EVENTO SI  NO  ES UN FALSO POSITIVO 
    def evento_o_falso():
        event = input("¿Es el evento real o un falso positivo? [s/n]")
        if event == "s":
            return True
        if event == "n":
            return False
    #    
    if evento_o_falso() == True:
        true_eve_dir.append(eve_dir[c])
        true_eve_unixt.append(eve_unixt[c])
        true_eve_lat.append(eve_lat[c])
        true_eve_lon.append(eve_lon[c])
        true_eve_prof.append(eve_prof[c])
        #        
        PICKS=np.column_stack((true_eve_dir,true_eve_unixt,true_eve_lat,true_eve_lon,true_eve_prof))    
        #datedate=datetime.today().strftime('%d-%m-%y')
        with open(path+"EVENTOS_nofalsosP.txt", 'ab+') as ff:
            np.savetxt(ff, PICKS, fmt='%s',delimiter=' ', newline='\n')
        ff.close()
        true_eve_dir=[]; true_eve_unixt=[]; true_eve_lat=[]; true_eve_lon=[]; true_eve_prof=[];PICKS=[]
        #
        #
    else:
        pass        
    ############### 
    print('#');print('#');print('#')
    os.system("sed -i '/"+ str(eve_unixt[c]) +"/d' "+path+"EVENTOS_copia.txt")
    os.chdir(path2); c=c+1
#enfor(revision data_procesada)
##    
##   
##    
os.system("sed -i '/^$/d' EVENTOS_nofalsosP.txt");os.system("rm EVENTOS_copia.txt")
print('EVENTOS DENTRO DE LA VENTANA REAGRUPADOS EN ARCHIVO EVENTOS_nofalsosP.txt')

