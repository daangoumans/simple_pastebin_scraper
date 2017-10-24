#!/usr/bin/env python
import sys
import os
import re
import time
import json
import urllib
import urllib2
import requests

default_url = "https://pastebin.com/"

word_list_file = "word_list.txt"
save_path = "./saves/"

word_list = []
pastebin_keys = []


def setup_word_list():
    global word_list
    try:
        with open(word_list_file, "r") as words:
            word_list = words.read().split()
        if not word_list:
            raise Exception
    except:
        print "----------------------------------------"
        print "------------- PLEASE READ! -------------"
        print "----------------------------------------"
        print "Add your words in a line separated txt file"
        print "and include it in the top of the code"
        print "----------------------------------------"
        print "----------------------------------------"
        exit()


def writeout(item, path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(path, "a+") as datafile:
        datafile.write(item)
        datafile.write("\n")
        datafile.close()


def read_paste(key):
    try:
        scrape = requests.get(default_url + "/api_scrape_item.php?i=" + key)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    if any(word in scrape.content for word in word_list):
        save_location = save_path + key + ".txt"
        print "[+] Data found in %s -- saving to %s" % (key, save_location)
        writeout(scrape.content, save_location)


def get_keys(limit):
        global pastebin_keys

        url = default_url + "api_scraping.php?limit="
        full_url = url + str(limit)

        try:
            response = requests.get(full_url)
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

        try:
            data = json.loads(response.content)
        except ValueError:
            # decode failed
            return False

        pastebin_keys = pastebin_keys[:limit]

        # TODO: store in database
        for paste in data:
            if paste['key'] in pastebin_keys:
                continue
            read_paste(paste['key'])
            pastebin_keys.insert(0, paste['key'])


def main():
    global pastebin_keys
    print ("Starting scraper - " + time.ctime())
    print ""
    setup_word_list()
    print ("Scanning for the following tags: " + str(word_list))
    print "--------------------------------------------"
    while True:
        get_keys(250)  # TODO: CLI setting
        time.sleep(60)  # TODO: CLI setting

if __name__ == "__main__":
    main()
