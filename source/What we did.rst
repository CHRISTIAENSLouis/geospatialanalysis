What we did
------

In this section, we present the code that we have implemented.

Goal of the project
*********


The goal of our project was to manipulate and display geospatial data using the python programming langage.

Therefore, we aimed to implement a code that would display the lastest earthquakes that occured all around the world.

The data we use comes from different RSS feeds provided by the EMSC: `<https://www.emsc-csem.org/>`_

Here is an example of the kind of map our code is able to create :

.. raw:: html

    <iframe src="_static/BelgiumCorsicaNSCFranceGermanymap.html" marginwidth="10" marginheight="10" scrolling="no" style="width:600px; height:375px; border:0; overflow:hidden;">
    </iframe>


In this case, the user decided to display the last 50 earthquakes that occured in Belgium, South of France, Corsica and Germany.



Data provider : EMSC
*********

The data we use is provided by the EMSC website `<https://www.emsc-csem.org/>`_.

The EMSC (Abbreviation for : *Euro-Mediterranean seismological center*) is a non gonvernmental organization composed by 85 members distributed in 55 countries.
Among the missions of this organization, the one we are interested in is the continuous collection of earthquakes related data.

On their website they provide RSS feeds related to each Flinn–Engdahl regions ( `<https://en.wikipedia.org/wiki/Flinn%E2%80%93Engdahl_regions>`_ ) and those RSS are the way we gather the information our code requires.

Here is an example of the RSSfeed related to Belgium : `<https://www.emsc-csem.org/service/rss/rss.php?filter=yes&region=BELGIUM&min_intens=0&max_intens=8>`_

.. figure:: /_static/RSSfeed.PNG
    :width: 400px
    :align: center
    :height: 200px
    :alt: alternate text
    :figclass: align-center
    
    RSSfeed related to Belgium

**REM :** On the previous picture, if we take a look at the third line of the RSS, we can see that only the **last 50** earthquakes that occured are covered.

The data we recover from those RSS is :

* The location of the earthquake in WGS84
* The magnitude of the earthquake
* The depth at wich the earthquake occurend
* The date of the earthquake



Code flow
*********

From the moment we compile the code, a sequence of operations starts. Here is a summary of the how the code flows :

* 1) The user is asked to define roughly the area he is interested in (For example, the name of the country)
* 2) Since flinn engdahl regions are not used by most of the people, a dropdown list (as shown below) appears to help the user selecting the areas he wants to display
* 3) After closing the dropdownlist window, the user chooses if he wants to add more areas to his selection
* 4) When the selection phase is over, the data is retrieved from RSS feeds
* 5) Finally, the code use the data to create the map




Area selection
*********

The first step is to import the packages our code need as well as the static data required. 

::

	print("This code was designed to work with Python 3.8.2 and the following packages :\nfeedparser 5.1.3\npandas 0.18.1\nnumpy 1.11.1\nfolium 0.7.0\nmatplotlib 1.5.1\nbranca 0.3.1\njinja2 2.8\ndatetime ")

	#Importing all the packages

	import feedparser #5.1.3
	import pandas as pd #0.18.1
	import numpy as np #1.11.1
	import folium #0.7.0
	import matplotlib #1.5.1
	
	from folium import branca #0.3.1
	from folium.plugins import MarkerCluster
	import folium.plugins 
	
	import tkinter as tk #8.6
	
	from branca.element import MacroElement #0.3.1
	
	from jinja2 import Template  #2.8
	
	from datetime import datetime, timedelta
	import dateutil.relativedelta
	
	import tkinter as tk
	import re
	import webbrowser



In this case, we need to import the areas.csv file.

::

	#Importing the list of areas recognised by our code/the RSS feed.

	areas = pd.read_csv("areas.csv", delimiter = ';',  encoding='latin-1')
	#REM ! had to change the "encoding" method => more explication can be found here :
	#https://stackoverflow.com/questions/5552555/unicodedecodeerror-invalid-continuation-byte  07/12/2018

**Rem :** The areas.csv file contains the full name of all the flinn engdahl regions as well as their short form wich is used by the RSS feeds.


.. figure:: /_static/area.PNG
    :width: 400px
    :align: center
    :height: 200px
    :alt: alternate text
    :figclass: align-center

    areas.csv file structure


The next step is to define the list of areas the user wants to display.


::

	selected = []
	
	proceed = True #As long as the user wants to add areas to his map, this part of the code will loop
	
	while (proceed == True):
	
	    # Asking to the user a part of the name of the area he wants to display
	
	    area = input('Give a region (Care capital form for the fisrt letter) : ')
	    
	    # Recovering all the areas that could match user's request
	    matching = [s for s in areas['Region'] if area in s]
	
	    # Displaying a basic dropdown list to confirm user's choice
	    def select():
	        global selected
	        selected.append(var.get())
	        root.title(selected[-1])
	    
	    root = tk.Tk()
	    # use width x height + x_offset + y_offset (no spaces!)
	    root.geometry("%dx%d+%d+%d" % (400, 50, 200, 150))
	    root.title("tk.Optionmenu as combobox")
	    var = tk.StringVar(root)
	
	    # initial value
	    var.set(matching[0])
	    choices = matching
	    option = tk.OptionMenu(root, var, *choices)
	    option.pack(side='left', padx=10, pady=10)
	    button = tk.Button(root, text="check value selected", command=select)
	    button.pack(side='left', padx=20, pady=10)
	    
	    root.mainloop()
	    
	    #Asking the user if he wants to select another area
	    print("Do u want to display areas from another country yes/no?")
	    answer = input()
	    if ( 'yes' in answer):
	        proceed = True
	    else :
	        proceed = False

Here is an example of the kind dropdown list proposed to the user.
In this case, the user asked to display an area located in Alaska.

.. figure:: /_static/selectionarea.PNG
    :width: 600px
    :align: center
    :height: 375px
    :alt: alternate text
    :figclass: align-center

    Dropdown list




Since the list of selected areas is defined, we substitute them by their short form and transform them in a shape the RSS feeds will understand.


::

	#Substituting the selected areas by a list of elements the EMSC's RSSfeed understand
	#Storing the elements in the "RSSentry" list
	j=0
	RSSentry =[]
	for q in selected :
	    i=0;
	    for p in areas['Region'] :
	
	        if selected[j] == p : 
	            index = i;
	        else :
	            i+=1;       
	    j+=1;
	    RSSentry.append(areas['RSS'][index])
	#CHANGE TO CAPITAL LETTERS + REPLACE ' ' by a +
	i=0
	for p in RSSentry :
	    RSSentry[i]=RSSentry[i].upper()
	    RSSentry[i]=RSSentry[i].replace(" ","+")
	    i+=1;


Here is an example of how the list of areas is modified :


.. figure:: /_static/changingshape.PNG
    :width: 800px
    :align: center
    :height: 100px
    :alt: alternate text
    :figclass: align-center

    Mofications to the list of areas



Data frame creation
*********

Now that we have a list of areas understood by the RSS, we can gather the data and store it in a data frame.

::


	#Defining the data frame we will use

	df=pd.DataFrame(columns=['Longitude', 'Latitude', 'Magnitude','Depth'])
	
	#For each area selected previously, we retrieve the data from a RSSfeed
	
	for p in RSSentry :
	    area = p
	    
	    rss_url = "https://www.emsc-csem.org/service/rss/rss.php?filter=yes&region={}&min_intens=0&max_intens=8".format(area)
	
	    feed = feedparser.parse(rss_url)   #Recovery of RSS data
	    
	    # Checking if any earthquake as been reported in this area
	    if len(feed.entries)== 0 : 
	        print("No events reported in this area :{}".format(area))
	    
	    else :
	    	# If at least one earthquakes occured in the area, we retrieve all the data we need frome the RSSfeed and store into 
	        
		#Double list to extract data
	        x=[[i.geo_long, i.geo_lat, i.emsc_magnitude, i.emsc_depth, i.emsc_time] for i in feed.entries]
		#Creating a dataframe with columns(names)
	        df2=pd.DataFrame(x, columns=['Longitude', 'Latitude', 'Magn', 'Depth', 'date'])
	        #Columns separation to optimize the dataframe
		#The magnitude is accompanied by information on how it was measured
		#We split the information into two distinct columns
	        df2['Type_magnitude'], df2['Magnitude'] = df2['Magn'].str.split(' ', 1).str 
	        del df2['Magn']
	        
	        #Adding the data related to one area to the main data frame    
	        df = df.append(df2, ignore_index = True)
	

At this point, all the data we need has been recovered. However, we still need to transform the shape of some elements.

For exemple, for some events the depth information is accompanied by a "f" that stand for "focal depth".
Since we don't use this information and in order to standardize our set of data, we erase this part of information from our data frame.

::


	#erase the "f" of the column 'Depth'
	i=0;
	for p in df['Depth']:
	    df['Depth'][i]=re.sub('f','',p)
	    i+=1;
           
On another side, since they are all considered as strings, we have to define the type of our variable.

:: 



	#Transformation of the values into floats
	i=0
	for p in df['Magnitude']:
	    df['Magnitude'][i]= float(df['Magnitude'][i])
	    df['Longitude'][i]= float(df['Longitude'][i])
	    df['Latitude'][i]= float(df['Latitude'][i])
	    df['Depth'][i]= float(df['Depth'][i])
	    i+=1

	
	#Adjusting the shape of date column data + Transforming the strings into datetime objects
	i=0
	for p in df['date']:
	    df['date'][i]=df['date'][i].replace(' UTC','')
	    df['date'][i]=datetime.strptime( df['date'][i],'%Y-%m-%d %H:%M:%S')
	    i+=1
	

Here is an example of the kind of DataFrame we should get at this point :

.. figure:: /_static/dataframe.PNG
    :width: 600px
    :align: center
    :height: 300px
    :alt: alternate text
    :figclass: align-center

    Final data frame

	
Map creation and display
*********

Now that all the data is stored in the same data frame, we can finally approach the creation of the map.

The map we want to display will be composed of four layers :

* 1) One bottom layer, wich is in fact a simple and empty world map
* 2) One superficial layer that displays the earthquakes ranked by magnitude
* 3) One superficial layer that displays the earthquakes ranked by detph
* 4) One superficial layer that displays the earthquakes ranked by date

Each superficial layer is associated to a specific color scale.


The layers related to depth and magnitude are very similar. Therefore, we will only detail the creation of one of these layers in this documention.

::


	#Magnitude layer
	
	
	#Defining a linear color scale based on the most extremes magnitude we have to display
	
	linear_magn = branca.colormap.LinearColormap(
	    ['green', 'yellow','orange', 'red','blue'],
	    vmin=min(df['Magnitude']), vmax=max(df['Magnitude'])
	)
	linear_magn.caption = 'Magnitude'
	
	
	cmagn=folium.FeatureGroup(name='Magnitude')   #Creation of a new layer
	m = folium.Map(control_scale=True)            #Creation of a map
	marker_cluster = MarkerCluster()              #Creation of Marker Cluster
	for i in range(0,len(df['Magnitude']),1):
		    markers= folium.CircleMarker([df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
	                  popup=str(df.iloc[i]['Magnitude']),
	                  radius=df.iloc[i]['Magnitude']*5,
	                  color=linear_magn(df.iloc[i]['Magnitude']),
	                  fill_color=linear_magn(df.iloc[i]['Magnitude']))   #Creation of Marker with color depending of the Magnitude value
	    marker_cluster.add_child(markers)
	    
	cmagn.add_child(marker_cluster) #Adding the Marker Cluster to the cmagn layer.


The layer related to the date is a bit different because, unlike the other two, it is associated to a non-linear color scale.

::

	
	#Date layer
	
	#For this layer we have to define a discreet scale based on time span since the earthquake occurs
	
	
	#Defining the color in function of date
	now=datetime.now()
	def colortest(date):
	    yesterday = datetime.now() - timedelta(days = 1)
	    week=  datetime.now() - timedelta(days = 7)
	    month=  now + dateutil.relativedelta.relativedelta(months=-1)
	    year=   now + dateutil.relativedelta.relativedelta(years=-1)
	    if (date<year):
	        col='gray'
	    elif (date>year and date<month):
	        col='green'
	    elif (date>month and date<week):
	        col='yellow'
	    elif (date>week and date<yesterday):
	        col='blue'
	    else :
	        col='red'
	    return col
	
	cdate=folium.FeatureGroup(name='date')
	marker_cluster3 = MarkerCluster()
	for i in range(0,len(df['date']),1):
	    markers3= folium.CircleMarker([df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
	                  popup=str(df.iloc[i]['date']),
	                  radius=df.iloc[i]['Magnitude']*5,
	                  color=colortest(df.iloc[i]['date']),
		          fill_color=colortest(df.iloc[i]['date']))
	    marker_cluster3.add_child(markers3)

	cdate.add_child(marker_cluster3)



After the creation of the superficial layers, we create an empty map of the world.

::


	#Defining an empty map, zoom level is adapted to the locations of earthquakes
	
	liste_points=[]
	for i in range(0,len(df['Magnitude']),1):
	    liste_points.append([df['Latitude'][i],df['Longitude'][i]])
	    i+=1
	xx=[liste_points]
	m.fit_bounds(xx)
   


The final step of this project is to associate a color scale to each layer and bound them to the main map.
Since this part of the code caused us more problems, we ended up adapting existing two parts of code we found on the internet.

The first part of code is in html langage, we use to display a draggable scale to our map.

::


	# The following part of the code was adapted from the code we found on :
	# https://nbviewer.jupyter.org/gist/BibMartin/f153aa957ddc5fadc64929abdee9ff2e
	# It allows to display the legend related to the "date layer"
	
	template = """
	{% macro html(this, kwargs) %}
	
	<!doctype html>
	<html lang="en">
	<head>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	  <title>jQuery UI Draggable - Default functionality</title>
	  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
	
	  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
	  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
	  
	  <script>
	  $( function() {
    $( "#maplegend" ).draggable({
	                    start: function (event, ui) {
	                        $(this).css({
	                            right: "auto",
	                            top: "auto",
	                            bottom: "auto"
	                        });
	                    }
	                });
	});



	
	  </script>
	</head>
	<body>
	
	 
	<div id='maplegend' class='maplegend' 
	    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
	     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
	     
	<div class='legend-title'>Date legend </div>
	<div class='legend-scale'>
	  <ul class='legend-labels'>
	    <li><span style='background:red;opacity:0.7;'></span>Last day</li>
	    <li><span style='background:blue;opacity:0.7;'></span>Last week</li>
	    <li><span style='background:yellow;opacity:0.7;'></span>Last month</li>
	    <li><span style='background:green;opacity:0.7;'></span>Last year</li>
	    <li><span style='background:gray;opacity:0.7;'></span>Over 1 years ago</li>
	
	  </ul>
	</div>
	</div>
	 
	</body>
	</html>
	
	<style type='text/css'>
	  .maplegend .legend-title {
	    text-align: left;
	    margin-bottom: 5px;
	    font-weight: bold;
    font-size: 90%;
	    }
	  .maplegend .legend-scale ul {
	    margin: 0;
	    margin-bottom: 5px;
	    padding: 0;
	    float: left;
	    list-style: none;
	    }
	  .maplegend .legend-scale ul li {
    font-size: 80%;
	    list-style: none;
	    margin-left: 0;
	    line-height: 18px;
	    margin-bottom: 2px;
	    }
	  .maplegend ul.legend-labels li span {
	    display: block;
	    float: left;
	    height: 16px;
	    width: 30px;
	    margin-right: 5px;
	    margin-left: 0;
    border: 1px solid #999;
	    }
	  .maplegend .legend-source {
	    font-size: 80%;
	    color: #777;
	    clear: both;
	    }
	  .maplegend a {
	    color: #777;
	    }
	</style>
		{% endmacro %}"""
	
	macro = MacroElement()
	macro._template = Template(template)



The seconde part of code is used to bind togheter a map layer and a linear color scale. 
This is implemented in java script and we use jinja2 to compile it with python.


::


	#The following part of code define a funtion used to bind a colormap to a given layer
	#Source : http://nbviewer.jupyter.org/gist/BibMartin/f153aa957ddc5fadc64929abdee9ff2e 07/12/2018
	
	
	class BindColormap(MacroElement):
	    """Binds a colormap to a given layer.
	
	    Parameters
	    ----------
	    colormap : branca.colormap.ColorMap
	        The colormap to bind.
	    """
	    def __init__(self, layer, colormap):
	        super(BindColormap, self).__init__()
	        self.layer = layer
	        self.colormap = colormap
	        self._template = Template(u"""
	        {% macro script(this, kwargs) %}
	            {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
	            {{this._parent.get_name()}}.on('overlayadd', function (eventLayer) {
	                if (eventLayer.layer == {{this.layer.get_name()}}) {
	                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
                }});
	            {{this._parent.get_name()}}.on('overlayremove', function (eventLayer) {
	                if (eventLayer.layer == {{this.layer.get_name()}}) {
	                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'none';
	                }});
	        {% endmacro %}
	        """)  # noqa
	
	
	
Finally, we can add all the layers to the final map, save it and display it inside a webbrowser.

::


	#Adding all the layers to the map
	m.add_child(cmagn).add_child(cprof).add_child(cdate)
	m.add_child(folium.map.LayerControl())
	m.add_child(linear_magn).add_child(linear_prof).add_child(macro)
	
	#Binding colormaps and layers using the "BlindColormap" function defined above
	                             
	m.add_child(BindColormap(cmagn,linear_magn)).add_child(BindColormap(cprof, linear_prof)).add_child(BindColormap(cdate, macro))
	
	#Save the map
	outf = "map.html"
	m.save(outf)
	
	#Open the map into a browser
	webbrowser.open(outf) 
			


Here is another example of the kind of map we obtain thanks to this code :

.. raw:: html

    <iframe src="_static/Greece.html" marginwidth="10" marginheight="10" scrolling="no" style="width:800px; height:375px; border:0; overflow:hidden;">
    </iframe>

