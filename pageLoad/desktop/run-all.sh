for i in $(cat sites-all.txt) ; do
  ./compare.sh $i
done
