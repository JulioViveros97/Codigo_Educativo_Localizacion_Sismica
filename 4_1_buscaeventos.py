#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################# SCRIPT CAPTURA EVENTOS  #########
# ABRIMOS CADA CARPETA POSEEDORA DE UN ARCHIVO DE EVENTOS (CALCULADO POR BINDER), TOMAMOS EL EVENTO Y LO ALMACENAMOS EN UN .TXT
# EL ARCHIVO DE SALIDA SERA UTIL PARA QUITAR FALSOS POSITIVOS, ENTREGAR RESULTADOS, RELOCALIZAR ,ETC.
import os
path: str ="/home/julito/Descargas/2020-1/topico-matt/"
d: str="data_procesada/" # carpeta actual contenedora de datos sismologicos
path2=os.path.join(path,d)
dhoras=os.listdir(path2) # entramos a la carpeta de datos
dhoras.sort()
#
os.chdir(path2)
#####################################################
#
for hfile in dhoras:
    path3=path2 + hfile; os.chdir(path3)
    os.system('''cat events.txt | sed '/P/d' | sed '/No events/d' | awk -v dir=${PWD##*/} '{ printf "%s %10.2f %-3.2f %-3.2f %.2f\\n",dir,$1,$8,$9,$10}' >>''' + path + '''/EVENTOS.txt''')    
    print(str(hfile))
    print('#')
    os.chdir(path2)
print('EVENTOS DENTRO DE LA VENTANA REAGRUPADOS EN ARCHIVO EVENTOS.TXT')










