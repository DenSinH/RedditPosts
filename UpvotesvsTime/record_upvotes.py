import urllib2
import json
import time

url = "https://www.reddit.com/r/dataisbeautiful/comments/9t8saj/oc_popularity_of_the_words_doot_and_spook_in/.json"

while True:
    try:
        # trying to open the url might raise an HTML error
        request = urllib2.Request(url)
        """Do NOT use my username when running this script, it might get you shadowbanned"""
        request.add_header("User-Agent", "D3NN152000, using this for a post")
        post = urllib2.urlopen(request)
        # read the json file
        dic = json.loads(str(post.read()))

        # write the amount of upvotes and report it
        with open("upvotes.txt", "a+") as f:
            print time.time(), dic[0]["data"]["children"][0]["data"]["score"]
            f.write(str(time.time()) + "\t\t" + str(dic[0]["data"]["children"][0]["data"]["score"]) + "\n")

        # wait 60 seconds before trying again
        time.sleep(60)
    except urllib2.HTTPError:
        # if reading the url failed, try again in 1 second
        print "attempt failed"
        time.sleep(1)
