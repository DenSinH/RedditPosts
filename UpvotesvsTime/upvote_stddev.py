import urllib2
import json
import time
import numpy as np

u_list = []
# low upvote post:
#url = "https://www.reddit.com/r/dankmemes/comments/8s9idh/trying_to_capture_this_month_in_one_image/.json"
# high upvote post:
url = "https://www.reddit.com/r/announcements/comments/4oedco/lets_all_have_a_town_hall_about_rall/.json"

# using a "dead" post to observe the fluctuations in the amount of upvotes

while True:
    try:
        # trying to open the url might raise an HTML error
        request = urllib2.Request(url)
        request.add_header("User-Agent", "D3NN152000, using this for a post")
        post = urllib2.urlopen(request)
        # read the json file
        dic = json.loads(str(post.read()))

        # record the value
        u_list.append(dic[0]["data"]["children"][0]["data"]["score"])
        with open("stddev.txt", "a") as f:
            f.write(str(dic[0]["data"]["children"][0]["data"]["score"]) + "\n")
        # report it and the standard deviation
        print time.time(), dic[0]["data"]["children"][0]["data"]["score"]
        print np.std(u_list)

        # try again 1 second later
        time.sleep(1)

    except urllib2.HTTPError:
        # if an error occured, report this and try again
        print "attempt failed"
