#!/bin/bash
# archivo para descargar datos IRIS automaticamente desde red c1
#----------------------------------------------------------------------
#	1)INGRESO DATOS:
#echo 'Ingrese red sismologica'
#read red
#echo 'Ingrese estacion'
#read estaciones
#echo 'Ingrese canales'
#read canales
#echo 'Ingrese fecha INICIO (yyy-mm-dd hh:mm:ss)'
#read finicio
#finicio=${finicio// /T}
#echo 'Ingrese fecha TERMINO (yyy-mm-dd hh:mm:ss)'
#read ftermino
#ftermino=${ftermino// /T}
#
path=./
echo -e "\e[5mRECUERDE CORRER ESTE SCRIPT EN EL DIRECTORIO QUE CONTENGA LOS ARCHIVOS fetch_dayloop.sh y estaciones_$\e[0m"
echo "¿Desea apagar el equipo luego de descargar los datos? (si/no)"
read sino
#--------------------------------------------------------------------
#	2)EXTRACCION HORAS  
/bin/bash ./1_fetch_dayloop.sh
#--------------------------------------------------------------------
#	3) FETCHDATA 
estredcan=$(awk '{print $1,$3,$4,$5}' ${path}/estaciones_taltal_serena.txt)
estredcan=$(printf '%s %s\n' "$estredcan")
mkdir ${path}/data

# Ciclo que descarga para c/hora-intervalo, todas las estaciones
while IFS=" " read -r finicio ftermino
do 
# Crear carpeta para la descarga
#hoy=$(date +"%F_%T")
mkdir ${path}/data/Descarga_${finicio}
path2=${path}/data/Descarga_${finicio}

# Ejecutar fetchdata en hora seleccionada, para c/estacion.
	while IFS=" " read -r estaciones red can loc
	do 
		can1=${can//,/ }
		for canales in $can1
		do
	echo -e "\e[34m${finicio} ${ftermino}\e[0m \e[1m${red}\e[0m \e[1m${estaciones}\e[0m \e[33m${canales}\e[0m"
	fetchdata -F -N ${red} -S ${estaciones} -C ${canales} -L ${loc} -s ${finicio} -e ${ftermino} -o ${path2}/data_${red}_${estaciones}_${canales}_${finicio}.mseed -m ${path2}/meta_${red}_${estaciones}_${canales}_${finicio}.metadata -sd ${path2}
		done
	done <<< "${estredcan}"
echo " "
echo -e "\e[1mUna hora de datos descargados para todas las estaciones en los canales \e[31m$can\e[0m"
echo "################################################################ "
done <fecha.txt
rm fecha.txt
#----------------------------------------------------------------------
#	4)APAGADO OPCIONAL 
#if [ $sino = si ];then
#echo "#"
#echo "#"
#echo -e "\e[5mDescarga lista\e[0m"
#echo    "Apagando el equipo"
#echo "227984bbl" | sudo -S shutdown  -P  -t 20 
#
#elif [ $sino = no ];then
#echo "#"
#echo "#"
#echo -e "\e[5mDescarga lista\e[0m"
#fi
date > 1_tiempo_op.txt






