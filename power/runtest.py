#!/mnt/c/Python27/python.exe
import time
import csv
import json
import os
import random
import datetime
import argparse

from subprocess import Popen
from selenium import webdriver
from parse    import  parseBatteryReport, parseGadgetLog
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options

parser = argparse.ArgumentParser(description='Invoke the selenium driver.')

parser.add_argument('--browser', '-b',
                    dest='browser',
                    nargs=1,
                    required=True,
                    choices=['firefox','chrome','edge'],
                    help='which browser to invoke')

parser.add_argument('--events', '-e',
                    dest='events',
                    nargs='+',
                    required=True,
                    choices=['load','power','battery', 'all'],
                    help='what to measure')

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

parser.add_argument('--binary',
                    dest='binary',
                    nargs=1,
                    required=False,
                    help='browser executable location')

args = parser.parse_args()


url_filename = args.urls[0]
duration     = args.duration[0]
browser      = args.browser[0]


batteryTest = False
powerTest   = False
loadTimeTest= False
for value in args.events:
  if value == "load":
    loadTimeTest = True
  if value == "power":
    powerTest = True
  if value == "battery":
    batteryTest = True
  if value == "all":
    batteryTest = True
    loadTimeTest = True
    powerTest = True


if os.path.exists("power-log.txt"):
    os.remove("power-log.txt")
if os.path.exists("battery-report.1.html"):
    os.remove("battery-report.1.html")
if os.path.exists("battery-report.2.html"):
    os.remove("battery-report.2.html")

# open list of urls for testing
with open(url_filename, 'r') as url_file:
    test_urls = url_file.readlines()

# start chromedriver using the previously defined options
if browser == "chrome" :
  options = ChromeOptions()
  options.binary_location = "C:\\Users\\mozilla\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe"
  driver = webdriver.Chrome(chrome_options = options)
  csvFilename = "chrome_log.txt"

if browser == "firefox" :
  binary = (r'C:\Program Files\Firefox Nightly\firefox.exe')
  fp = (r'C:\Users\mozilla\AppData\Roaming\Mozilla\Firefox\Profiles\19c2m00s.power_tests')
  opts = Options()
  opts.profile = fp
  driver = webdriver.Firefox(firefox_options=opts, firefox_binary = binary)
  #binary_location = "C:\\Program Files\\Firefox Nightly\\firefox.exe"
  #driver = webdriver.Firefox(firefox_binary=binary_location)
  csvFilename = "firefox_log.txt"

if browser == "edge" :
  driver = webdriver.Edge()
  csvFilename = "edge_log.txt"

# set page load time out to 60 seconds
driver.set_page_load_timeout(30)

driver.maximize_window()

pageCounter = 0
startTime   = time.time()

if powerTest:
  cmd  = ["C:\\Program Files\\Intel\\Power Gadget 3.5\\PowerLog3.0.exe", "-resolution", "50", "-duration", str(duration), "-file", "power-log.txt"]
  Popen(cmd)

if batteryTest:
  os.system("powercfg.exe /batteryreport")
  reportStart = parseBatteryReport()
  os.rename("battery-report.html","battery-report.1.html")

averageLoadTime    = 0
averageNetworkTime = 0

loadTestFile = open(browser+"-loadtimes.csv", "a")

while 1:
  for i, url in enumerate(test_urls):
      print("i = ",i," url=",url)
      try:
        driver.get(url)
      except Exception as e:
        print("..exception: ",e)
        # reset session and continue
        if browser == "chrome" :
          driver.close()
          driver = webdriver.Chrome(chrome_options = options)
          driver.set_page_load_timeout(30)
          driver.maximize_window()
        #elif browser == "firefox" :
        #  driver = webdriver.Firefox(firefox_binary = binary_location)
        #elif browser == "edge" :
        #  driver = webdriver.Edge()
        continue;

      pageCounter = pageCounter + 1
      if loadTimeTest:
        perfTimings = driver.execute_script("return window.performance.timing")
        loadTime    = perfTimings['loadEventEnd'] - perfTimings['navigationStart']
        averageLoadTime    += loadTime
        averageNetworkTime += perfTimings['responseEnd'] - perfTimings['fetchStart']
        loadTestFile.write(str(loadTime/float(1000))+","+url)

      elapsedTime = time.time() - startTime
      if elapsedTime >= duration :
        averageLoadTime = float(averageLoadTime) / float(pageCounter)
        averageNetworkTime = float(averageNetworkTime) / float(pageCounter)

        dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")
        filename   = "report-" + browser + "-" + dateString + ".txt"

        reportFile = open(filename, "w")
        reportFile.write("elapsed time: " + str(elapsedTime) + "\n")
        reportFile.write("pages loaded: " + str(pageCounter) + "\n")

        csvFile = open(csvFilename, "a")
        csvFile.write(str(elapsedTime))
        csvFile.write("," + str(pageCounter))

        if batteryTest:
          os.system("powercfg.exe /batteryreport")
          reportEnd = parseBatteryReport()
          os.rename("battery-report.html","battery-report.2.html")
          batteryConsumed  = reportStart['battery']    - reportEnd['battery']
          cumulativeEnergy = reportStart['capacity']  - reportEnd['capacity']
          reportFile.write("Battery Report:\n")
          reportFile.write("      battery consumed (%)   : " + str(batteryConsumed) + "\n")
          reportFile.write("      cumulative Energy (mWh): " + str(cumulativeEnergy) + "\n")
          csvFile.write("," + str(batteryConsumed) + "," + str(cumulativeEnergy))
        else:
          csvFile.write(",,")

        if powerTest:
          powerReport = parseGadgetLog()
          reportFile.write("Intel Gadget Report:\n")
          reportFile.write("      cpu   Cumulative Energy (mWh):  " + str(powerReport['cpu']) + "\n")
          reportFile.write("      ia    Cumulative Energy (mWh):  " + str(powerReport['ia']) + "\n")
          reportFile.write("      dram  Cumulative Energy (mWh):  " + str(powerReport['dram']) + "\n")
          reportFile.write("      gt    Cumulative Energy (mWh):  " + str(powerReport['gt']) + "\n")
          totalPower = powerReport['cpu'] + powerReport['dram'] + powerReport['gt'];
          reportFile.write("      total Cumulative Energy (mWh):  " + str(totalPower) + "\n")
          csvFile.write("," + str(totalPower) + "," + str(powerReport['cpu']) + "," + str(powerReport['ia']) + "," + str(powerReport['dram']) + "," + str(powerReport['gt']))
        else:
          csvFile.write(",,,,,")


        if loadTimeTest:
          reportFile.write("Load Times:\n")
          reportFile.write("Average Load Time  (s): " + str(averageLoadTime/float(1000)) + "\n")
          reportFile.write("Average Net  Time (ms): " + str(averageNetworkTime) + "\n")
          csvFile.write("," + str(averageLoadTime/float(1000)) + "," + str(averageNetworkTime) + "\n")
        else:
          csvFile.write(",,\n")


        loadTestFile.close()
        csvFile.close()
        reportFile.close()
        driver.quit()
        exit()


driver.quit()
