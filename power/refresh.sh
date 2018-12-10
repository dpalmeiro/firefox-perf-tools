wget https://www.alexa.com/topsites/category/News
grep -Po "^<a href=\"/siteinfo/\K.*(?=\">)" News > alexa-top50.txt
rm News
