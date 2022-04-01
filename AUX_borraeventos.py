#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################# SCRIPT BORRA ARCHIVOS  #########
# EN CASO DE NECESITAR LIMPIAR EL CATALOGO (DE RESULTADOS) DE CUALQUIER EVENTO HALLADO POR BINDER Y POSTERIORES, APLIQUE ESTE SCRIPT
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
    #
    os.system(''' ls | grep -E "events|MINI|unused" | xargs rm ''') 
    print(str(hfile))
    print('#')
    os.chdir(path2)
print('ARCHIVOS events.txt, unused.txt y MINIS DENTRO DE LA VENTANA: BORRADOS')



