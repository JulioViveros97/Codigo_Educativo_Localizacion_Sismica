#!/bin/bash
#--------------------------------------------------------------------
#input start and end days (yyyy.jdy) for a certain station
echo 'Ingrese fecha INICIO (yyyy.jdy)'
read start
echo 'Ingrese fecha TERMINO (yyyy.jdy)'
read end 

echo '¿Cada cuantas horas guardamos la data?' 
read horas
sec=3600
add_time=$(($horas * $sec )) 

#start=2019.360 # finicio
#end=2020.001 # ftermino
#-------------------------------------------------------------------
#define start year and start day 
#I AM AN IDIOT FOR THIS +0, but it does force awk to convert a string such as 001 to a number 1 which the date command needs
syear=`echo ${start} | awk -F"." '{print $1 + 0}'`
sday=`echo ${start} | awk -F"." '{print $2 + 0}'`
#define start unix time, the number of seconds after 1970-01-01 if I recall correctly
sunix=`date -d "$syear-01-01 + $sday days -1 day" "+%s"`

#define end year and end day
eyear=`echo ${end} | awk -F"." '{print $1 + 0}'`
eday=`echo ${end} | awk -F"." '{print $2 + 0}'`
#define end unix time
eunix=`date -d "$eyear-01-01 + $eday days" "+%s"`

#start at the beginning!
time=$sunix


#loop hour by hour while the time is less than the end unix time
while [ $time -lt $eunix ]; do
sdate=`date -d @${time} "+%Y-%m-%dT%H:%M:%S"`  #format the time in the required format using the date command
time=`echo $time $add_time | awk '{print $1 + $2}'` #add 3600 seconds to the time
edate=`date -d @${time} "+%Y-%m-%dT%H:%M:%S"`  #this is the end date

#once the start date and end date are defined, can loop over the operation times for a certain station, channel etc. and generate the miniseed files
#echo "fetchdata more loops needed -s ${sdate} -e ${edate} output ..."

printf "%s %s\n" ${sdate} ${edate}
#end the while loop
done >> fecha.txt  
echo -e '##################\e[5mFECHAS\e[0m#\e[5mLISTAS\e[0m##########################'


