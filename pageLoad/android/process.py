#!/usr/bin/python
import glob
from statistics import mean
from statistics import stdev

files = glob.glob("*.csv")

baseUrls = {}
refUrls = {}

for filename in files:
  i = 0;
  with open(filename) as f:
    for line in f:
      fields  = line.split(",")

      url = fields[0]
      try:
        loadTime = float(fields[1])
      except:
        continue

      if url not in baseUrls.keys():
        baseUrls[url] = []
        refUrls[url] = []

      if (filename == 'loadtimes-default.csv'):
        baseUrls[url].append(loadTime)
      else:
        refUrls[url].append(loadTime)


geomean = 1
for url in baseUrls:
  loadTimes1 = baseUrls[url]
  loadTimes2 = refUrls[url]
  if len(loadTimes1) == 0 or len(loadTimes2) == 0:
    continue

  avg1 = mean(loadTimes1)
  avg2 = mean(loadTimes2)
  len1 = len(loadTimes1)
  len2 = len(loadTimes2)
  speedup=(avg1-avg2)/avg1*100

  std1 = stdev(loadTimes1)
  std1per = std1/avg1*100
  std2 = stdev(loadTimes2)
  std2per = std2/avg2*100

  print("%-30s"% url + " " + "%12.3f"% avg1 + " (+-%02.1f"% + std1per + "%, " + str(len1)  + ") " + "%12.3f"% avg2 + " (+-%02.1f"% + std2per + "%, " + str(len2) + ") " + "%5.2f"% speedup + "%")
