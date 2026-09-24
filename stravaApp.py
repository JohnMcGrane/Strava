import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.lines import Line2D
import matplotlib
import streamlit as st

st.set_page_config(layout="wide")

@st.cache_data()# suppress_st_warning=True)
def import_data():
	full = pd.read_csv('out.csv')
	full['Miles'] = full['distance']*0.000621371
	full['Hours_Total'] = full['elapsed_time']/3600
	full['Hours_Moving'] = full['moving_time']/3600
	full['Elevation_Gain_Feet'] = full['total_elevation_gain']*3.28084
	time, date = [], []
	for i in full['start_date_local']:
	    time.append(i.split('T')[1])
	    date.append(i.split('T')[0])
	full['Date'] = date
	full['Time'] = time
	full['Activity Date'] = list(map(lambda x: datetime.strptime(x,'%Y-%m-%d'),full['Date']))
	full['Year'] = list(map(lambda x: x.year, full['Activity Date']))
	full['Weekday'] = list(map(lambda x: x.weekday(), full['Activity Date'])) # weekdays labeled 0-6 meaning Monday-Sunday
	daylist = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	full['weekday'] = list(map(lambda x: daylist[x], full['Weekday'])) # weekdays labeled Monday-Sunday
	years = np.unique(np.array(full['Year']))
	array = np.zeros((years.size,7,53))
	montharray = np.zeros((years.size,7,53))
	df = full
	yearcount = 0
	for i in range(1,df['Activity Date'].size):
	    lastdate = df['Activity Date'][i-1]
	    date = df['Activity Date'][i]
	    x = (date.weekday(),date.week,date.year)
	    if date.year != lastdate.year:
	        yearcount+=1
	    if df['type'][i] == 'Run':
	        array[yearcount,date.weekday(),date.week%53] = 1
	    if df['type'][i] == 'Ride' or df['type'][i] == 'VirtualRide':
	        array[yearcount,date.weekday(),date.week%53] = 2
	    if df['type'][i] == 'NordicSki':
	        array[yearcount,date.weekday(),date.week%53] = 3
	    if df['type'][i] == 'Hike':
	        array[yearcount,date.weekday(),date.week%53] = 4
	    if df['type'][i] == 'AlpineSki':
	        array[yearcount,date.weekday(),date.week%53] = 5
	    if df['type'][i] == 'Walk':
	        array[yearcount,date.weekday(),date.week%53] = 6
	return array, yearcount, years

array1, yearcount, years = import_data()

st.title("Strava")

opt1 = st.selectbox('Select Sport to Display History',
   ('All', 'Run', 'Bike Ride', 'Nordic Ski', 'Hike', 'Alpine Ski', 'Walk'), index=0)

optsdict = {'All': 0, 'Run': 1,'Bike Ride': 2, 'Nordic Ski': 3, 'Hike': 4, 'Alpine Ski': 5, 'Walk': 6}

if optsdict[opt1] == 0:
	array = array1
else:
	num = optsdict[opt1]
	array = np.where(array1==num, array1, 0)

#@st.cache_data(hash_funcs={matplotlib.figure.Figure: hash},suppress_st_warning=True)
@st.cache_data() #allow_output_mutation=True,suppress_st_warning=True)
def make_visualization(yearcount, array, years):
	plt.rcParams['figure.facecolor'] = 'black'
	none = 'black'
	run = 'maroon'
	ride = 'darkorange'
	nordicski = 'darkcyan'
	hike = 'yellow'
	alpineski = 'azure'
	walk = 'midnightblue'
	plt.style.use('fivethirtyeight')
	#fig, axs = plt.subplots(yearcount+1,figsize=(3*yearcount-3,5*yearcount))
	fig, axs = plt.subplots(yearcount+1, figsize=(16, 2*(yearcount+1)))
	plt.subplots_adjust(hspace=0.1)
	for j in range(0,years.size):
	    if j == years.size-1:
	        axs[j].set_xlabel('Week of the Year',fontsize=18, color = 'w')
	    if j == 0:
	        axs[j].set_title('Strava Activities',fontsize=26, color = 'w') 
	    axs[j].set_facecolor('black')
	    axs[j].grid(False)
	    axs[j].set_ylabel(f"{years[j]}",fontsize=18, color = 'w')
	    fig.patch.set_facecolor('black')
	    activities = array[j]
	    X,Y = np.meshgrid(np.arange(activities.shape[1]), np.arange(activities.shape[0]))
	    colors = {0.0:none,1.0:run, 2.0:ride, 3.0:nordicski, 
	              4.0:hike, 5.0:alpineski, 6.0:walk}
	    
	    axs[j].scatter(X.flatten(), abs(Y.flatten()-6), c=pd.Series(activities.flatten()).map(colors), s = 195)
	    axs[j].set_xlim(-1,53)
	    axs[j].set_ylim(-1,7)
	    axs[j].set_aspect('equal', adjustable='box')
	    axs[j].set_yticks(ticks = [6,5,4,3,2,1,0])
	    axs[j].set_yticklabels(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
	                           fontsize=16, color = 'w')
	    axs[j].spines['top'].set_visible(False)
	    axs[j].spines['right'].set_visible(False)
	    axs[j].spines['bottom'].set_visible(False)
	    axs[j].spines['left'].set_visible(False)
	    axs[j].set_xticks([0, 4, 8, 13, 17, 21, 26, 30, 34, 39, 43, 47])
	    axs[j].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                           fontsize=12, color='w')
	    axs[j].tick_params(axis='x', pad=-1)

	    custom_markers = [Line2D([0], [0], marker="o", ms=17, color=c, lw=0) for c in [run, ride, hike, alpineski, nordicski, walk]]

	# custom_markers = [Line2D([0], [0], marker = "o", ms=22 , color=run, lw=0),
	#                 Line2D([0], [0], marker = "o", ms=22 , color=ride, lw=0),
	#                 Line2D([0], [0], marker = "o", ms=22 , color=hike, lw=0),
	#                 Line2D([0], [0], marker = "o", ms=22 , color=alpineski, lw=0),
	#                 Line2D([0], [0], marker = "o", ms=22 , color=nordicski, lw=0),
	#                 Line2D([0], [0], marker = "o", ms=22 , color=walk, lw=0)]
	axs[0].legend(
    custom_markers,
    ['Run', 'Ride', 'Hike', 'Alpine Ski', 'Nordic Ski', 'Walk'],
    loc='upper left',
    bbox_to_anchor=(0, 1.25),
    ncol=1,
    fontsize=16,
    labelcolor='w',
    facecolor='black',
    labelspacing=0.2,
    frameon=True
)

# 	fig.legend(
#     custom_markers,
#     ['Run', 'Ride', 'Hike', 'Alpine Ski', 'Nordic Ski', 'Walk'],
#     loc='lower center',
#     ncol=6,
#     fontsize=15,
#     labelcolor='w',
#     facecolor='black',
#     bbox_to_anchor=(0.5, 0.98)
# )
	plt.subplots_adjust(hspace=0.1, top=0.965)
	return fig
fig1 = make_visualization(yearcount, array, years) 
st.pyplot(fig1, facecolor='black')















