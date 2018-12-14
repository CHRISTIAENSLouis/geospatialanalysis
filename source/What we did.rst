What we did
------

In this section, we present the code that we have implemented so far.

The goal of our project was to manipulate and display Data that comes from : `<https://www.emsc-csem.org/>`_


For the exemple, the following code will display the earthquakes that occured in Belgium for the past 11 years.
Altough this version of the code is suitable to areas with few sismic events, it can be used for every area on earth.


1) Import packages and Data
*********

Here are the packages that we used for this short code :

::
	
	import numpy as np
	import pandas as pd
	import folium


And here is how we imported the data into a data frame with pandas.
The data comes from EMSC and has been downloaded into a *.csv* file. The final goal is to implement in our code a way to retrieve data from a RSS feed. Then, the code would be automatically updated if another earthquakes occurs in the area.

::

	#Récupération des données :
	data = pd.read_csv('/home/gfa/Documents/Projettest/Belgium.csv', delimiter =';')
	data.head()


FIND HOW TO ADD PICTURE




2) Create the empty map with center and zoom that fit the data
*********

The next step is to create an "empty" map with an initial center and zoom level that fit the data we imported.


To define the coordinates of the center, we use the two most distant points in longitude and then latitude.

*Rem :* In most of python's package, the classic schema for the coordinates of a point is (x=longitude, y=latitude). With Leaflet/Folium functions, this convention is inverted. Therefore, we use the latitude as the first coordinates and the longitude as the second.


::
	
	#Détermination du centre de la carte ATTENTION LEAFLET INVERSER LON LAT => LAT LON
	x =(max(data['Latitude'])+min(data['Latitude']))/2
	y =(max(data['Longitude'])+min(data['Longitude']))/2
	Centre = (x,y)
	print(Centre)


Then, we need to define the initial zoom-level of the map. The goal is to ensure that all the elements are visible when the map is launched.

To archieve this, we follow this list of opérations :

1. Define the maximum gap between the longitude for 2 points in our data frame
2. Define the width of the map screen in degrees for the highest zoom-level
3. Confront the width of each zoom-level with the maximum gap between the longitudes and STOP when the gap can fit in the map
4. Reproduce the point 1->3 for latitudes and heigth of the map screen

Select the zoom-level that fit the gap of longitudes AND the gap of latitudes.

::

	#Détermination du niveau de zoom de la carte

	#En utilisant .bounds pour une map avec zoom de 18, nous pouvons trouver la taille de celle-ci
	Ecartminilongitude = 0.005112290382385254;
	#Correspond à l'écart en degré entre le la gauche et la droite de la carte, zoomlevel =18
	Ecartminilatitude = 0.0013547231035460072; 
	#Correspond à l'écart en degré entre le haut et le bas de la carte, zoomlevel = 18

	zoomlon = 18;
	zoomlat = 18;

	#Pour les longitudes

	#Ecart maximum en degrés entre les différents points
	Ecart = max(data['Longitude'])-min(data['Longitude'])

	continuer = True;
	# Par défaut, le zoom est à fond
	zoom = 18;
	#Temps que l'écartmax est supérieur à l'écart toléré par le niveau de zoom, on diminue de 1 le niveau de zoom
	while continuer == True :
	    if Ecart < Ecartminilongitude :
		continuer = False;
		zoomlon = zoom;

	    else :
		Ecartminilongitude = Ecartminilongitude *2;
		zoom -= 1;


	#Pour les latitudes
	Ecart = max(data['Latitude'])-min(data['Latitude'])

	continuer = True;
	zoom = 18;
	while continuer == True :
	    if Ecart < Ecartminilatitude :
		continuer = False;
		zoomlat = zoom;

	    else :
		Ecartminilatitude = Ecartminilatitude *2;
		zoom -= 1;
		
	zoom = min([zoomlon, zoomlat])

Now that the center and the zoom-level have been defined, we can create the map.
::

	#Création de la map en utilisant le centre et le zoom que nous avons déterminé
	m = folium.Map(
	    Centre,
	    zoom_start=zoom)
	m



3) Displays markers
*********

The folowing step is to add markers on the map at the location of each earthquake.



First, we create a function that will return a color (green, orange, red) according to the magnitude of one earthquake.
In this case, the range of magnitude hold in the data frame is cut into three parts.
According to the part in wich the event's magnitude fits, the color of the event will be defined.


::

	# Cette fonction détermine la couleur du marqueur en fonction de l'intensité du tremblement de terre
	def color(magn):
	    minimum=float(min(data['Magnitude']))
	    step= float((max(data['Magnitude'])-min(data['Magnitude']))/3)
	    if magn < (minimum+step):
		col='green'
	    elif magn < (minimum+step*2):
		col='orange'
	    else:
		col='red'
	    return col



Finally, we can add markers to the map.
In this case, there is one marker for each event, the color of the marker is defined using the "color" function and the date of the event will be displayed on top of each marker.

::

	fg=folium.FeatureGroup(name="Earthquake Location")

	for lat,lon,date,magn in zip(data['Latitude'],data['Longitude'],data['Date'],data['Magnitude']):
	    fg.add_child(folium.Marker(location=[lat,lon],popup=(folium.Popup(date)),icon=folium.Icon(color=color(magn),icon_color='green')))
	m.add_child(fg)



4) Save the map
*********

The final step is to save the map into a .html file wich can be open with any internet browser.

::

	#sauvegarde de la carte :
	outfp = r'/home/gfa/Documents/Projettest/map.html'
	m.save(outfp)




retfshogire
	.. image:: /_static/carte1exemple.PNG

    
    
