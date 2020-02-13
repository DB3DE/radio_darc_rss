import urllib
import re
import datetime
import yaml
import os
import sys
import re
import datetime

from lib.rfeed import *

sPATH_CONFIG_FILE=r"~/.radio_darc_feedgen.yaml"
config = None
PodElements = list()

class PodElement():
    """ Represents an object that can be host to other extensions.
    """
    def __init__(self, sRawline):
        self.__sRasline = sRawline

        self.title = None   #Title of this podcast issue
        self.filename = None
        self.url = None     #url of ths podcast issue
        self.description = None
        self.pubDate = None

    def ExtractData(self):
        #print(self.__sRasline)
        rem = re.search('.*<a href=\"(.*.mp3).*/(.*)/(.*)</a>.*', self.__sRasline)

        #filename and url
        self.filename = rem.group(1).strip()
        self.url = config["url"] + self.filename

        # extract the date
        date_str = rem.group(3).strip()
        date_dy, date_mon, date_yr = date_str.split(".")
        self.pubDate = datetime.datetime(int(date_yr), int(date_mon), int(date_dy))

        transmission = rem.group(2).strip()
        self.title = "Radio DARC "+transmission
        self.description = "Radio DARC " + transmission + " from " + date_str

    def GetFeedItem(self):
        return Item(
            title=self.title,
            link=self.url,
            description=self.description,
            pubDate=self.pubDate)



def read_config():  # reads the config file and set the global variable
    global config
    sAbs_ConfigFilePath=os.path.abspath(os.path.expanduser(sPATH_CONFIG_FILE))
    if not os.path.exists(sAbs_ConfigFilePath):
        print("Could not find config file %s"%(sAbs_ConfigFilePath))
        sys.exit("-1")

    with open(sAbs_ConfigFilePath, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def write_sample_config():
    global config
    config = dict()
    config["url"]="http://www.alximedia.de/radio/"
    config["feedfile"]="~/radio_darc_feed.rss"
    config["download"]=False
    config["url_feed"]="localhost"
    sAbs_sPATH_CONFIG_FILE = os.path.abspath(os.path.expanduser(sPATH_CONFIG_FILE))

    with open("sample_config.yaml", 'w') as file:
        documents = yaml.dump(config, file, default_flow_style=False)
        print("Config written to %s"%(sAbs_sPATH_CONFIG_FILE))
        #print(yaml.dump(config, default_flow_style=False))


def CreateElements():
    global config
    global PodElements
    #read the webside
    print("Reading website %s" % (config["url"]))
    try:
        f = urllib.request.urlopen(config["url"])
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("Opening the webside failed with the following code: %s" % (e.code))
        if hasattr(e,"reason"):
            print("Error reason: %s" % (e.reason))
        sys.exit(2)

    website = str(f.read())
    f.close()

    for line in str(website).split("<br>"):
        if str(line).find(".mp3\">RADIO DARC") != -1:
            PodElements.append(PodElement(line))
            PodElements[-1].ExtractData()


def CreateFeed():
    global config
    global PodElements

    podcastitems = list()

    for elem in PodElements:
        podcastitems.append(elem.GetFeedItem())



def main():
    read_config()
    CreateElements()
    CreateFeed()


if __name__ == '__main__':
    main()
