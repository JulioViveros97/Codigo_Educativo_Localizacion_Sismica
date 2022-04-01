#!/usr/bin/env python3
#from IPython import get_ipython
#get_ipython().magic('reset -sf') # Limpiamos las variables almacenadas en caso de usar un interpretador(como Spyder)
#################################### SCRIPT MAPA VERTICAL 2D CON CARTOPY ##############
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patheffects import Stroke
import shapely.geometry as sgeom
import cartopy.io.img_tiles as cimgt
from matplotlib.transforms import offset_copy
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy

###############################################################################
extent = [-72.4044, -67.3506,-31.279, -26.000] # LIMITES VENTANA
#fig=plt.figure("Mapa eventos ventana tiempo")
#ax = plt.axes(projection = ccrs.Mercator())
#ax.set_extent(extent)
# 
# USAR TOPOGRAFIA 
stamen_terrain = cimgt.Stamen('terrain-background')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
ax.set_extent([-74, -67.3506,-31.279, -24.1272], crs=ccrs.Geodetic())
ax.add_image(stamen_terrain, 8)
#
#
# plotear la serena
ax.plot(-71.252,-29.9027, marker='o', color='red', markersize=5,alpha=0.3, transform=ccrs.Geodetic())
geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
text_transform = offset_copy(geodetic_transform, units='dots', x=-15)
ax.text(-71.252,-29.9027, u'La Serena',verticalalignment='center', horizontalalignment='right',transform=text_transform,bbox=dict(facecolor='sandybrown', alpha=0.5, boxstyle='round'))
# plotear tal tal
ax.plot(-70.489397, -25.403414, marker='o', color='red', markersize=5,alpha=0.3, transform=ccrs.Geodetic())
geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
text_transform = offset_copy(geodetic_transform, units='dots', x=-15)
ax.text(-70.489397,-25.403414, u'Tal-Tal',verticalalignment='center', horizontalalignment='right',transform=text_transform,bbox=dict(facecolor='sandybrown', alpha=0.5, boxstyle='round'))
# plotear copiapo 
ax.plot(-70.322040, -27.370250, marker='o', color='red', markersize=5,alpha=0.3, transform=ccrs.Geodetic())
geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
text_transform = offset_copy(geodetic_transform, units='dots', x=-15)
ax.text(-70.322040,-27.370250, u'Copiapo',verticalalignment='center', horizontalalignment='right',transform=text_transform,bbox=dict(facecolor='sandybrown', alpha=0.5, boxstyle='round'))
#
#
#ax.add_feature(cf.COASTLINE,edgecolor='white')#ax.coastlines(resolution='50m')
axx=ax.gridlines(draw_labels=True,dms=True, color='grey',alpha=0.5,linestyle='dotted',linewidth=2)
axx.top_labels = False
axx.left_labels = False
#axx.
#ax.stock_img()
#
ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.LAND, edgecolor='white', alpha=0.3)
ax.add_feature(cartopy.feature.LAKES, edgecolor='white',alpha=0.3)
rivers_50m = cf.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m')
ax.add_feature(rivers_50m, facecolor='None', edgecolor='b',alpha=0.3)
ax.set_title("2019",fontdict=dict(weight='bold'))
#
# AÑADIR LOS BORDES DE PLACAS TECTONICAS: USO DE SHAPEFILES(¡buscar forma de usar .txt en vez de .shp!)
fname1='plate_boundaries/ridge.shp'
shape_feature1 = ShapelyFeature(Reader(fname1).geometries(),ccrs.PlateCarree(), facecolor='none',edgecolor='red')
ax.add_feature(shape_feature1)
fname2='plate_boundaries/transform.shp'
shape_feature2 = ShapelyFeature(Reader(fname2).geometries(),ccrs.PlateCarree(), facecolor='none',edgecolor='red')
ax.add_feature(shape_feature2)
fname3='plate_boundaries/trench.shp'
shape_feature3 = ShapelyFeature(Reader(fname3).geometries(),ccrs.PlateCarree(), facecolor='none',edgecolor='red')
ax.add_feature(shape_feature3)
##
##
##
##

# CARGAR TXT DE ESTACIONES
file="estaciones_taltal_serena.txt"
f=open(file,"r")
lines=f.readlines()
stat_nombre=[];stat_lat=[];stat_lon=[]
for x in lines:
    stat_nombre.append(x.split(' ')[0])
    stat_lat.append(x.split(' ')[5])
    stat_lon.append(x.split(' ')[6])
f.close()

cont=0
for nombre in stat_nombre:
    print(str(nombre))
    ax.plot(float(stat_lon[cont]),float(stat_lat[cont]),color='black',alpha=1.5, linewidth=1, marker='.',transform=ccrs.Geodetic())
    geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units='dots', x=15)
    ax.text(float(stat_lon[cont]),float(stat_lat[cont]), ('u'+nombre),verticalalignment='center', horizontalalignment='left',transform=text_transform,bbox=dict(facecolor='grey', alpha=0.3, boxstyle='round',linewidth=0.5))
    cont=cont+1
#end for
#
#    
#
# CARGAR TXT DE EVENTOS   
# LEER UN ARCHIVO DE EVENTOS ( recopilados del archivo de datos procesados con "buscaeventos.py" )
filee="EVENTOS.txt"
ff=open(filee,"r")
liness=ff.readlines()
eve_lat=[];eve_lon=[]
for xx in liness:
    eve_lat.append(xx.split(' ')[2])#[2]
    eve_lon.append(xx.split(' ')[3])#[3]
ff.close()
#
#
conta=0
for ee in range(len(eve_lat)):
	try:
	    print('evento n°:'+str(conta)+' mapeado')
	    ax.plot(float(eve_lon[conta]),float(eve_lat[conta]),color='green',alpha=0.5, linewidth=0.01, marker='.',transform=ccrs.Geodetic())
	    geodetic_transform1 = ccrs.Geodetic()._as_mpl_transform(ax)
	    text_transform = offset_copy(geodetic_transform, units='dots', x=15)
	    ax.text(float(eve_lon[cont]),float(eve_lat[cont]), ('u'+nombre),verticalalignment='center', horizontalalignment='left',transform=text_transform,bbox=dict(facecolor='grey', alpha=0.3, boxstyle='round',linewidth=0.5))
	    conta=conta+1
	except Exception:
		conta=conta+1
		pass
#end for 
##    
##
##
##  
##
##    
# SUBMAPA MUNDIAL 
sub_ax = fig.add_axes([0.18, 0.675, 0.2, 0.2],projection=ccrs.NearsidePerspective(central_longitude=-70.0, central_latitude=-37.0, satellite_height=5785831, false_easting=0, false_northing=0, globe=None))
##sub_ax.set_extent([-85, -50, -55, -10])
#
effect = Stroke(linewidth=4, foreground='wheat', alpha=0.5)
sub_ax.spines['geo'].set_path_effects([effect])
#
sub_ax.gridlines(color='grey',alpha=0.5,linewidth=0.5)
sub_ax.add_feature(cf.LAND)
sub_ax.coastlines(resolution='110m')
#
extent_box = sgeom.box(extent[0], extent[2], extent[1], extent[3])
sub_ax.add_geometries([extent_box], ccrs.PlateCarree(), facecolor='none',edgecolor='blue', linewidth=1)
#
sub_ax.add_feature(shape_feature1,linewidth=0.5)
sub_ax.add_feature(shape_feature2,linewidth=0.5)
sub_ax.add_feature(shape_feature3,linewidth=0.5)
#
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()
