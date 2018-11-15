import time
import csv
import json
import os
import random
import datetime
import argparse

from subprocess import Popen
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

parser = argparse.ArgumentParser(description='Invoke the selenium driver.')

parser.add_argument('--base', '-b',
                    dest='base',
                    nargs=1,
                    required=True,
                    help='base browser to test')

parser.add_argument('--ref', '-r',
                    dest='ref',
                    nargs=1,
                    required=True,
                    help='reference browser to test')

parser.add_argument('--file', '-f',
                    dest='urls',
                    nargs=1,
                    required=True,
                    help='file with list of urls')

parser.add_argument('--duration', '-d',
                    dest='duration',
                    nargs=1,
                    type=int,
                    default=3600,
                    required=False,
                    help='run duration')

args = parser.parse_args()
url_filename = args.urls[0]
duration     = args.duration[0]
base         = args.base[0]
ref          = args.ref[0]

# open list of urls for testing
with open(url_filename, 'r') as url_file:
    test_urls = url_file.readlines()

opts = Options()
#fp = <path to profile>
#opts.profile = fp

pageCounter = 0
startTime   = time.time()

baseloadTestFile = open("base-loadtimes.csv", "a")
refloadTestFile = open("ref-loadtimes.csv", "a")

def saveLoadTime(loadTestFile, driver):
  perfTimings = driver.execute_script("return window.performance.timing")
  loadTime    = perfTimings['loadEventEnd'] - perfTimings['navigationStart']
  loadTestFile.write(str(loadTime)+","+url)

while 1:
  for i, url in enumerate(test_urls):
      print("i = ",i," url=",url)
      baseDriver = webdriver.Firefox(firefox_options=opts, firefox_binary = base)
      baseDriver.set_page_load_timeout(30)
      baseDriver.maximize_window()
      try:
        baseDriver.get(url)
        saveLoadTime(baseloadTestFile, baseDriver)
      except Exception as e:
        print("..exception: ",e)
      baseDriver.close()

      refDriver = webdriver.Firefox(firefox_options=opts, firefox_binary = ref)
      refDriver.set_page_load_timeout(30)
      refDriver.maximize_window()
      try:
        refDriver.get(url)
        saveLoadTime(refloadTestFile, refDriver)
      except Exception as e:
        print("..exception: ",e)
      refDriver.close()

      pageCounter = pageCounter + 1

      elapsedTime = time.time() - startTime
      if elapsedTime >= duration :
        baseloadTestFile.close()
        refloadTestFile.close()
        baseDriver.quit()
        refDriver.quit()
        exit()
