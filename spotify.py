#
# spotify.py - generate the ifram
#

import pandas
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot


print("read the pandas.csv file")
data=pandas.read_csv("pandas.csv", delim_whitespace=False)

print("invoke plotly scatter plot")
fig = px.scatter(title="Spotify Visualization for 2023: Keoni Bolding",
    		 x=data["date"],
                 y=data["date2"],
                 color=data["name"],
                 hover_name=data["name"] + "<br>" + data["track"] + "<br> (duration: " +
                    pandas.Series(data["duration"], dtype="string") + " s.)"
                 )

print("generate the figure_spotify.html file")
plot(fig, filename='figure_spotify.html', auto_open=False)

