#
# Spotify dashboard production
#

import datetime
import json
import sys

#
# Read.py -
# -- read a full.json file
# -- generate the pandas.csv (CSV) file
# -- generate the frequency file used for colors
#

#
#
# Each JSON quad looks like thislooks sort of like this:
#  {
#    "endTime" : "2019-12-23 03:34",
#    "artistName" : "Ahmad Jamal",
#    "trackName" : "Feeling Good",
#    "msPlayed" : 98545
#  },

#
# Read the full.json file into a list
#
print("read the full.json file")
input_str = open('full.json', 'r').read()
slist  = json.loads(input_str)
pre = []
for s in slist:
    aname = s["master_metadata_album_artist_name"]
    if aname == "null" or aname == None:
        continue
    track = s["master_metadata_track_name"].replace('"', '\'')
    # track = s["master_metadata_track_name"]

    d = datetime.datetime.strptime(s["ts"], "%Y-%m-%dT%H:%M:%SZ")
    d = d.replace(tzinfo=datetime.timezone.utc)
    d = d.astimezone()
    endtime = d.strftime("%Y-%m-%d %H:%M:%S")

    # endtime = s["endTime"]
    seconds = int(s["ms_played"]) / 1000
    pre.append((aname,track,endtime,int(seconds)))

# sort the list
s_pre = sorted(pre)

#
# write (generate) the pandas.csv file to be used in the next step
#
print("generate pandas.csv file")
sdict = {}
ofile = "pandas.csv"
with open(ofile, 'w') as outf:
    # header for the CSV file
    outf.write("name,date,date2,track,duration\n")
    # input is 4 fields
    for s in s_pre:
        aname = s[0]       # Author Name
        track = s[1]       # Track
        endtime = s[2]     # End Time
        seconds = s[3]     # Total Seconds
        if aname not in sdict:
            sdict[aname] = []
        sdict[aname].append(endtime)

        d,t = endtime.split(' ')
        h,m,s = t.split(':')
        H = int(h)
        M = int(m) / 60
        T = H + M
        buf = "\"%s\",%s, 2000-01-01 %s,\"%s\",%d" % (aname, d, t, track, seconds)
        outf.write(buf + "\n")

colorlist = []
print("generate color map")
for k in sdict.keys():
    colorlist.append((len(sdict[k]), k))
    #for t in sdict[k]:
    #    sys.stdout.write(t)
    #    sys.stdout.write(',')
    #sys.stdout.write('\n')

slist = sorted(colorlist, reverse=True)
r1=0
freq = "freqlist.txt"
with open(freq, 'w') as fs:
    for s in slist:
        fs.write(s[1]+"\n")
