#!/usr/bin/env python3
#from IPython import get_ipython
#get_ipython().magic('reset -sf')
import os
import subprocess
#########################################################################
# SCRIPT USO BINDER_NOSC
################### CREAR EL PATH DE LA DATA PROCESADA + PARAMETROS BINDER ##################   
path: str ="/home/julito/Descargas/2020-1/topico-matt"
path_binder_param: str = path + "/binder_param/param.txt"
#
#path_binder_unused : str= path + "/binder_param/unused.txt"
#path_binder_events : str= path + "/binder_param/events.txt"
path_binder_info : str= path + "/binder_param/info.dat"
path_binder_velmod : str= path + "/binder_param/velmod.hdr"
################### Listar carpetas ##################################
d: str="data_procesada" # carpeta actual contenedora de datos procesados legibles por binder_nosc
path2=os.path.join(path,d)
dhoras=os.listdir(path2) 
dhoras.sort()
os.chdir(path2)
####################### CARGAMOS LOS PICKS ##################')
for hfile in dhoras:#[9:10]: # seleccionamos una hora-carpeta
    path0: str=path+"/data_procesada/"+hfile
    os.chdir(path0) # entramos a la hora-carpeta
    d=os.listdir() # se abren todos los archivos de c/hora
    for f in d: # seleccionamos un archivo
        ###################   Abrir    ####################################
        if  f.endswith(".txt"):  # TRABAJAMOS PARA .txt, DATOS PICKS
            f_pick=os.path.join(path0,f)
            os.system("cp " + path_binder_info +" " + path0); os.system("cp " + path_binder_velmod +" " + path0)
            os.system("binder_nosc_AR " + f_pick + " " + path_binder_param) # lanzamos bindes_nosc 
            print("binder_nosc_AR aplicado para picks del "+ hfile ) 
            os.system("rm info.dat" );os.system("rm velmod.hdr" ); os.system("rm latency_error.txt"); os.system("rm hypo71.log"); os.system("rm loc.debug")
print("DETECCION AUTOMATICA LISTA")
subprocess.call(["python3", "/home/julito/Descargas/2020-1/topico-matt/correo_control.py"])
os.system('say "BINDER APLICADO "')
