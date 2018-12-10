#!/usr/bin/python3
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

parser.add_argument('--iterations', '-i',
                    dest='iterations',
                    nargs=1,
                    type=int,
                    default=0,
                    required=False,
                    help='iterations')

args = parser.parse_args()
url_filename = args.urls[0]
if type(args.duration) is list:
  duration     = args.duration[0]
else:
  duration    = args.duration
if type(args.iterations) is list:
  iterations     = args.iterations[0]
else:
  iterations    = args.iterations
base         = args.base[0]
ref          = args.ref[0]

print("base = " + base)
print("ref  = " + ref)
print("duration = " + str(duration))
print("iterations = " + str(iterations))
print("filename  = " + url_filename)

# open list of urls for testing
with open(url_filename, 'r') as url_file:
    test_urls = url_file.readlines()

opts = Options()
fp_base = R"/mozilla-central/src/trunk/obj-base/tmp/profile-default"
fp_ref  = R"/mozilla-central/src/trunk/obj-opt/tmp/profile-default"
opts.profile = fp_base

counter = 0
startTime   = time.time()
baseloadTestFile = open("base-loadtimes.csv", "w")
refloadTestFile = open("ref-loadtimes.csv", "w")


def saveLoadTime(loadTestFile, driver):
  perfTimings = driver.execute_script("return window.performance.timing")
  loadTime    = perfTimings['loadEventEnd'] - perfTimings['navigationStart']
  loadTestFile.write(str(loadTime)+","+url)

while 1:
  done=False
  for i, url in enumerate(test_urls):
      print("base: ctr = ",counter," url=",url)
      baseDriver = webdriver.Firefox(firefox_options=opts, firefox_binary = base)
      baseDriver.set_page_load_timeout(30)
      baseDriver.maximize_window()
      try:
        baseDriver.get(url)
        saveLoadTime(baseloadTestFile, baseDriver)
      except Exception as e:
        print("..exception: ",e)
      baseDriver.close()

      elapsedTime = time.time() - startTime
      if iterations == 0 and elapsedTime >= duration/2:
        baseloadTestFile.close()
        done=True
        break
  counter = counter+1
  if done or (iterations != 0 and counter >= iterations):
    break

counter = 0
opts.profile = fp_ref
while 1:
  done=False
  for i, url in enumerate(test_urls):
      print("opt: ctr = ",counter," url=",url)
      refDriver = webdriver.Firefox(firefox_options=opts, firefox_binary = ref)
      refDriver.set_page_load_timeout(30)
      refDriver.maximize_window()
      try:
        refDriver.get(url)
        saveLoadTime(refloadTestFile, refDriver)
      except Exception as e:
        print("..exception: ",e)
      refDriver.close()

      elapsedTime = time.time() - startTime
      if iterations == 0 and elapsedTime >= duration:
        refloadTestFile.close()
        done=True
        break
  counter = counter+1
  if done or (iterations != 0 and counter >= iterations):
    break
