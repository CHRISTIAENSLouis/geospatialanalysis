print("This code was designed to work with Python 3.8.2 and the following packages :\nfeedparser 5.1.3\npandas 0.18.1\nnumpy 1.11.1\nfolium 0.7.0\nmatplotlib 1.5.1\nbranca 0.3.1\njinja2 2.8 ")

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

#------------------------------------------------------------------

#Importing the list of areas recognised by our code/the RSS feed.

areas = pd.read_csv("areas.csv", delimiter = ';',  encoding='latin-1')
#REM ! had to change the "encoding" method => more explication can be found here :
#https://stackoverflow.com/questions/5552555/unicodedecodeerror-invalid-continuation-byte  07/12/2018


selected = []

proceed = True

#As long as the user wants to add areas to his map, this part of the code will loop

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


#-----------------------------------------------------------------------------

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
        df2['Type_magnitude'], df2['Magnitude'] = df2['Magn'].str.split(' ', 1).str 
        del df2['Magn']
        
        #Adding the data related to one area to the main data frame    
        df = df.append(df2, ignore_index = True)

#erase the "f" of the column 'Depth'
i=0;
for p in df['Depth']:
    df['Depth'][i]=re.sub('f','',p)
    i+=1;
           

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

#-------------------------------------------------------------------------

# Creation of the map

#Our map will be composed of 3 differents layers we build separatly



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
    
cmagn.add_child(marker_cluster)


#Depth layer

linear_prof = branca.colormap.LinearColormap(
    ['green', 'yellow','orange', 'red','blue'],
    vmin=min(df['Depth']), vmax=max(df['Depth'])
)
linear_prof.caption = 'Depth'


cprof=folium.FeatureGroup(name='Depth')
marker_cluster2 = MarkerCluster()
for i in range(0,len(df['Depth']),1):
    markers2= folium.CircleMarker([df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
                  popup=str(df.iloc[i]['Depth']),
                  radius=df.iloc[i]['Depth']*2,
                  color=linear_prof(df.iloc[i]['Depth']),
                  fill_color=linear_prof(df.iloc[i]['Depth']))
    marker_cluster2.add_child(markers2)

cprof.add_child(marker_cluster2)


#Date layer


#For this layer we have to define a discreet scale based on time span sinds the earthquake occurs


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


#Defining an empty map, zoom level is adapted to the locations of earthquakes

liste_points=[]
for i in range(0,len(df['Magnitude']),1):
    liste_points.append([df['Latitude'][i],df['Longitude'][i]])
    i+=1
xx=[liste_points]
m.fit_bounds(xx)



# The following part of the code was adapted from the code we found on :
# http://nbviewer.jupyter.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd
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



