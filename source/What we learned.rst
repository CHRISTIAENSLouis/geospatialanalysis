What we learned
*****

The goal of our project could be summarized by : "Manipulate and display geodata on a map using the python langage".
Given our restrained knowledge in python programming, we had to start by learning some basics of programmation in this particular langage.

We used the following site to gain the first skills required for our project : `<https://developers.google.com/edu/python/>`_


Furthermore, we were asked to create a documentation of our work using *Sphinx*. Sinds it is the first time we had to use such a tool, finding out how to use it effectively was (and is stil) part of the challenge.


Here after, you can find the list of package we discovered during our research so far.

*Rem* : To the point where we are, we did not use all those package during the realisation of our final code, however, getting information on them was part of our learning process.


Shapely
--------

Shapely is a Python package used to define and manipulate plane spatial object.

This package allowed us to create objects such as points, lines and polygons. Furthermore, this package provide several functions dedicated to those type of objects.

For exemple, thanks to Shapely, we can can easily compute areas, distance and plot basic geometries.



Here is the link of the main website we used to discover this package :

`<https://automating-gis-processes.github.io/CSC18/lessons/L1/Geometric-Objects.html>`_


Pandas/Numpy
--------

Pandas library purpose is to organize and manipulate effectively large amount of data, which are stored in DataFrames.

Numpy provide pre made function dedicated to the manipulation of matrices and tables.



Here is the link of the main website we used to discover this package :

`<https://data36.com/pandas-tutorial-1-basics-reading-data-files-dataframes-data-selection/>`_


GeoPandas
--------

GeoPandas is a package that link Pandas and Shapely features and add a geospatial dimension to the data frames created with Pandas.


Here is the link of the main website we used to discover this package :

`<https://automating-gis-processes.github.io/CSC18/lessons/L2/geopandas-basics.html>`_


OSMnx
--------

With this package, we are able to download part of map (with Road, Buildings, Meta Data, etc) from OpenStreetMap. This is really helpfull to easyly construct the "first layer" of any map.

Furthermore, if we combine OSMnx to "geopy", another package, we can do some geocoding (finding coordinates of a point thanks to an adress).



Here is the link of the main website we used to discover this package :

`<https://automating-gis-processes.github.io/CSC18/lessons/L3/overview.html>`_



Folium / Leaflet
--------

This package is used to create simple interactive maps, add indications on them and export them under html type of file.


Here is the link of the main website we used to discover this package :

`<https://pythonhow.com/web-mapping-with-python-and-folium/?fbclid=IwAR1c8mAgceTssp4zzWbzR2UPDFuJw-dlE-60elfiWgNgd8Xzb_Yk7DoIdKM>`_


Fiona
--------

This package enable to associate geographical coordinates to python object and to rapidly switch between every coordinates repair system.


Here is the link of the main website we used to discover this package :

`<https://automating-gis-processes.github.io/CSC18/lessons/L2/projections.html>`_


Matplotlib
--------

Matplotlib is the package used to display all the object we create while coding : Shapely Objects, DataFrames, Maps, etc.


Sphinx/.RST :
---------

Sphinx is the tool we use to create this documentation. It link and transform several .rst file into a network of html pages.


Here is the site we used to discover .rst syntax :

`<https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_





