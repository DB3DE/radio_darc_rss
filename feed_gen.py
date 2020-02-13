import urllib
import re
import datetime
import yaml
import os
import sys

sPATH_CONFIG_FILE=r"~/.radio_darc_feedgen.yaml"


def read_config():
# reads the config file and returns a dictionary
    sAbs_ConfigFilePath=os.path.abspath(os.path.expanduser(sPATH_CONFIG_FILE))
    if not os.path.exists(sAbs_ConfigFilePath):
        print("Could not find config file %s"%(sAbs_ConfigFilePath))
        sys.exit("-1")

    with open(sAbs_ConfigFilePath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def write_sample_config():
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










def main():
    config = read_config()



if __name__ == '__main__':
    #main()
    read_config()