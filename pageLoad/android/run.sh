#!/bin/bash
set -x

DEVICE=$1
#FLAGS="-s $DEVICE"
FLAGS=""

SITES="sites.txt"

APPNAME2="org.mozilla.klar.debug"
FILENAME2="loadtimes-default.csv"

APPNAME1="org.mozilla.klarSymbolic.debug"
FILENAME1="loadtimes-Bsymbolic.csv"

ITERATIONS=100

adb $FLAGS shell am force-stop ${APPNAME1}
adb $FLAGS shell am force-stop ${APPNAME2}

for i in $(seq 1 $ITERATIONS) ; do
for url in $(cat $SITES) ; do
  echo -n "$url," >> $FILENAME1
  echo -n "$url," >> $FILENAME2
    TIMESTAMP=$(adb $FLAGS shell 'date +"%m-%d %H:%M:%S.00"')

    ################ Run test on APP 1 ##########################
    adb $FLAGS shell am start -n ${APPNAME1}/org.mozilla.focus.activity.IntentReceiverActivity -a android.intent.action.VIEW -d $url

    for j in $(seq 1 4) ; do
      sleep 5
      LOGCAT=`adb $FLAGS shell logcat "-t '$TIMESTAMP'" | grep "LoadTimeObserver: Finished loading" | tail -1`
      echo $LOGCAT
      LOADTIME=$(echo $LOGCAT | awk '{print $11}')
      if [ -z "${LOGCAT}" ]; then
        continue;
      else
        if [ $LOADTIME -gt 700 ]; then
          echo "URL: $url - Loadtime = $LOADTIME"
          echo -n "$LOADTIME" >> $FILENAME1
          break
        fi
      fi
    done
    adb $FLAGS shell am force-stop ${APPNAME1}
    sleep 1

    ################ Run test on APP 2 ##########################
    adb $FLAGS shell am start -n ${APPNAME2}/org.mozilla.focus.activity.IntentReceiverActivity -a android.intent.action.VIEW -d $url

    for j in $(seq 1 4) ; do
      sleep 5
      LOGCAT=`adb $FLAGS shell logcat "-t '$TIMESTAMP'" | grep "LoadTimeObserver: Finished loading" | tail -1`
      echo $LOGCAT
      LOADTIME=$(echo $LOGCAT | awk '{print $11}')
      if [ -z "${LOGCAT}" ]; then
        continue;
      else
        if [ $LOADTIME -gt 700 ]; then
          echo "URL: $url - Loadtime = $LOADTIME"
          echo -n "$LOADTIME" >> $FILENAME2
          break
        fi
      fi
    done
    adb $FLAGS shell am force-stop ${APPNAME2}
    sleep 1

  echo >> $FILENAME1
  echo >> $FILENAME2
done
done



#shutdown
adb $FLAGS shell reboot -p
