#!/usr/bin/python3
import glob
from statistics import mean
from statistics import stdev
from scipy import stats
from operator import itemgetter
import os.path

#files = glob.glob("*.csv")
basefile = "base-loadtimes.csv"
reffile  = "ref-loadtimes.csv"

baseUrls = {}
refUrls = {}


if os.path.exists(basefile):
  with open(basefile) as f:
    for line in f:
      line = line.rstrip()
      fields  = line.split(",")

      url = fields[1]
      try:
        loadTime = float(fields[0])
      except:
        continue

      if url not in baseUrls.keys():
        baseUrls[url] = []
      baseUrls[url].append(loadTime)

if os.path.exists(reffile):
  with open(reffile) as f:
    for line in f:
      line = line.rstrip()
      fields  = line.split(",")

      url = fields[1]
      try:
        loadTime = float(fields[0])
      except:
        continue

      if url not in refUrls.keys():
        refUrls[url] = []
      refUrls[url].append(loadTime)


# Eliminate outliers by removing any values with
# a z-score of > 3.
MULTIPLIER=1
if baseUrls:
  for url in baseUrls:
    std  = stdev(baseUrls[url])
    avg  = mean(baseUrls[url])
    for i,val in enumerate(baseUrls[url]):
      diff = val - avg
      if diff > MULTIPLIER*std or diff < -MULTIPLIER*std:
        del baseUrls[url][i]

if refUrls:
  for url in refUrls:
    std  = stdev(refUrls[url])
    avg  = mean(refUrls[url])
    for i,val in enumerate(refUrls[url]):
      diff = val - avg
      if diff > MULTIPLIER*std or diff < -MULTIPLIER*std:
        del refUrls[url][i]


results=[]
for url in baseUrls:
  loadTimes1 = baseUrls[url]
  if len(loadTimes1) == 0:
    continue

  loadTimes2 = []
  if refUrls and refUrls[url]:
    loadTimes2 = refUrls[url]
    if len(loadTimes2) == 0:
      continue

  mean1 = mean(loadTimes1)
  std1  = stdev(loadTimes1)/mean1*100

  mean2 = 0
  std2  = 0
  if refUrls and refUrls[url]:
    mean2 = mean(loadTimes2)
    std2  = stdev(loadTimes2)/mean2*100

  entry = {
      "url"  : url,
      "avg1" : mean1,
      "avg2" : mean2,
      "len1" : len(loadTimes1),
      "len2" : len(loadTimes2),
      "std1" : std1,
      "std2" : std2,
      }
  results.append(entry)

sortedResults = sorted(results, key=itemgetter('std1'))

speedups = []
#url  mean1  (stdev1,count1)  mean2  (stdev2,count2)  improvement
print("%-50s"%  "url" + " "  , end="")
print("%8s"%  "avg"  + " "  , end="")
print("(%4s"% "std"  + ", %3s"% "count" + ")", end="")
print("%12s"% "avg"  + " "  , end="")
print("(%4s"% "std"  + ", %3s"% "count" + ")", end="")
print("%10s"% "speedup")
print("-" * 150)
for entry in sortedResults:
  speedup=(entry["avg1"]-entry["avg2"])/entry["avg1"]*100
  speedups.append(entry["avg1"]/entry["avg2"])
  print("%-50s"%  entry["url"]     + " "  , end="")
  print("%8.2f"%  entry["avg1"]    + " "  , end="")
  print("(%3.0f"% entry["std1"]    + "%, " + "%5d"% entry["len1"] + ")", end="")
  if entry["avg2"] != 0:
    print("%12.2f"% entry["avg2"]    + " "  , end="")
    print("(%3.0f"% entry["std2"]    + "%, " + "%5d"% entry["len2"] + ")", end="")
    print("%10.2f"% speedup + "%")
  else:
    print("")

print("geomean = " + str(stats.gmean(speedups)))

