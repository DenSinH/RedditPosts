import json
import datetime as dt
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)

# november 1st 2018 00:00:00 : 1540944000
# november 1st 2017 00:00:00 : 1509408000

"""
spook data from from:
https://api.pushshift.io/reddit/submission/search/?subreddit=dankmemes&before=1540944000&title=spook&size=1000

This puts the newest 1000 posts with spook in the title in a json format before the given timestamp

doot data from:
data from https://api.pushshift.io/reddit/search/submission/?subreddit=dankmemes&title=doot&size=1000

This does the same, but for doot. Unfortunately, there were too many posts with doot in the title in 2018 to get all
of them in one search query, so I had to look up the oldest posts (at the bottom) and use the same link, but with
the timestamp of the oldest post as new 'before' argument.

The results of these queries are in the .json files.
"""

# change to 2017 if desired
year = 2018

# sep 15
startdate = dt.datetime(year, 9, 25)

# read json files
"""Remove 2017 if you are trying to plot the data for 2018"""
with open("searchspook2017.json") as f:
    data_spook = json.load(f)

with open("searchdoot2017.json") as f:
    data_doot = json.load(f)

with open("searchdoot2.json") as f:
    data_doot2 = json.load(f)


# calculate time difference since startdate
def t_since_start(ts):
    # example ts : data["data"][0]["created_utc"]
    inpdate = dt.datetime.utcfromtimestamp(ts)
    delta = inpdate - startdate
    return delta.days


# values for dates in figure
oct1 = (dt.datetime(year, 10, 1) - startdate).days
oct15 = (dt.datetime(year, 10, 15) - startdate).days
oct31 = (dt.datetime(year, 10, 31) - startdate).days

# data in lists
delta_data_spook = np.array([t_since_start(data_spook["data"][i]["created_utc"]) for i in range(len(data_spook["data"]))])
delta_data_doot = [t_since_start(data_doot["data"][i]["created_utc"]) for i in range(len(data_doot["data"]))]
if year == 2018:
    delta_data_doot = np.array(delta_data_doot + [t_since_start(data_doot2["data"][i]["created_utc"]) for i in range(len(data_doot2["data"]))])

# figure
fig = plt.figure()

# histogram plotting
plt.hist(delta_data_doot, bins=oct31 + 1, range=(0, oct31 + 1), edgecolor='k', color="white")
plt.hist(delta_data_spook, bins=oct31 + 1, range=(0, oct31 + 1), edgecolor='k', color="white")

plt.hist(delta_data_doot, bins=oct31 + 1, range=(0, oct31 + 1), edgecolor='k', alpha=0.5, label="Doot")
plt.hist(delta_data_spook, bins=oct31 + 1, range=(0, oct31 + 1), edgecolor='k', alpha=0.5, label="Spook")

# looks
plt.xlim(0, oct31 + 1)
plt.xticks([0.5, oct1 + 0.5, oct15 + 0.5, oct31 + 0.5], ["Sep 25", "Oct 1 ", "Oct 15", "Oct 31"])
plt.xlabel("Date")
plt.axes().xaxis.set_label_coords(0.99, -0.08)

plt.ylim(0, 60)
plt.ylabel("# Posts")

plt.title("Popularity of the words 'Doot' and 'Spook'\nin r/dankmemes post titles in 2017")
plt.legend()

# doot doot image
fn = get_sample_data("D:\PyProjects\PokerAI\DankmemesAnalysis\doot.png", asfileobj=False)
arr_img = plt.imread(fn, format="png")

imagebox = OffsetImage(arr_img, zoom=0.2)
imagebox.image.axes = fig

imagebox.image.axes = fig

ab = AnnotationBbox(imagebox, [0.7, 0.55],
                    xybox=(298., 175.),
                    xycoords='data',
                    boxcoords="offset points",
                    pad=0.5
                    )

plt.axes().add_artist(ab)

plt.savefig("Popularity.png", dpi=800)
plt.show()
