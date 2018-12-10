import re
import time
import os


def parseBatteryReport():
  with open('battery-report.html', 'r') as html_file:
    html_lines = html_file.readlines()

  reportLineFound = False
  percentageFound = False

  percentage = 0

  for i, line in enumerate(html_lines):

    if reportLineFound == False:
      matchObj = re.match( r'.*Report generated.*', line)
      if matchObj:
        reportLineFound = True
        continue

    if reportLineFound:
      matchObj = re.match( r'.*"percent">(\d+).*', line)
      if matchObj:
        percentageFound = True
        percentage = matchObj.group(1)
        continue

    if percentageFound:
      matchObj = re.match (r'.*"mw">(.*) mWh.*', line)
      if matchObj:
        capacity = matchObj.group(1)
        capacity = re.sub (r',','', capacity)
        html_file.close()
        return {"battery" : int(percentage), "capacity" : int(capacity)}


def parseGadgetLog():
  while not os.path.exists("power-log.txt"):
    time.sleep(1)
  time.sleep(5)

  with open('power-log.txt', 'r') as html_file:
    html_lines = html_file.readlines()

  cpuPower   = 0
  iaPower    = 0
  dramPower  = 0
  gtPower    = 0

  for i, line in enumerate(html_lines):

    if cpuPower == 0:
      matchObj = re.match( r'^Cumulative Processor Energy_0 \(mWh\) = (.+)$', line)
      if matchObj:
        cpuPower = matchObj.group(1)
        continue

    if iaPower == 0:
      matchObj = re.match( r'^Cumulative IA Energy_0 \(mWh\) = (.+)$', line)
      if matchObj:
        iaPower = matchObj.group(1)
        continue

    if dramPower == 0:
      matchObj = re.match (r'^Cumulative DRAM Energy_0 \(mWh\) = (.+)$', line)
      if matchObj:
        dramPower = matchObj.group(1)
        continue

    if gtPower == 0:
      matchObj = re.match( r'^Cumulative GT Energy_0 \(mWh\) = (.+)$', line)
      if matchObj:
        gtPower = matchObj.group(1)
        continue


  return {"cpu" : float(cpuPower), "ia" : float(iaPower), "dram" : float(dramPower), "gt" : float(gtPower)}

if os.path.exists("battery-report.html") :
    print(parseBatteryReport())

if os.path.exists("power-log.txt") :
    print(parseGadgetLog())
