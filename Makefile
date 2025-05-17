#
# Spotify dashboard production
#

all: pandas.csv figure_spotify.html

pandas.csv:
	python read.py

figure_spotify.html:
	python spotify.py

clean::
	-rm -rf *~ pandas.csv figure_spotify.html freqlist.txt




