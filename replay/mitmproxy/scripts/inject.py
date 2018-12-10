import time
import os
from bs4 import BeautifulSoup
from mitmproxy import http
from mitmproxy import ctx

htmlctr = 0;
jsctr   = 0;
injectctr=0;

def load(l):
    ctx.log.info("Registering option 'siteurl'")
    l.add_option("siteurl", str, "ERROR", "Website being visited.")

    ctx.log.info("Registering option 'savecontent'")
    l.add_option("savecontent", bool, False, "save all js and html content.")

def configure(updated):
    if "siteurl" in updated:
      ctx.log.info("siteurl value: %s" % ctx.options.siteurl)
    if "savecontent" in updated:
      ctx.log.info("savecontent value: %s" % ctx.options.savecontent)

def response(flow):
  global htmlctr, jsctr, injectctr
  millis = int(round(time.time() * 1000))

  #---------Inject into HTML----------#
  #if ctx.options.siteurl == flow.request.pretty_url:
  if "content-type" in flow.response.headers:
    if 'text/html' in flow.response.headers["content-type"]:
      if injectctr == 0:
        flow.response.decode()

        html = BeautifulSoup(flow.response.content)
        firstScript = html.find("script")

        with open("scripts/deterministic.js", "r") as jsfile:
          js = jsfile.read().replace("REPLACE_LOAD_TIMESTAMP",str(millis));
          script = html.new_tag("script")
          script.append(js);
          firstScript.insert_before(script)
          flow.response.content = bytes(str(html), "utf-8")
      injectctr=injectctr+1


  if ctx.options.savecontent == True:
    if "content-type" in flow.response.headers:
      #---------Save all HTML----------#
      if 'text/html' in flow.response.headers["content-type"]:
        filename = "content/html" + str(htmlctr) + ".txt";
        with open(filename, "a") as ofile:
          try:
            htmlctr = htmlctr + 1
            ofile.write(flow.request.pretty_url + "\n")
            ofile.write(flow.response.headers["content-type"] + "\n");
            ofile.write("----------------------------------------\n");
            ofile.write(bytes(flow.response.content).decode("utf-8"));
          except:
            ofile.write("error");
          ofile.close()



      #---------Save all JS----------#
      if "javascript" in flow.response.headers["content-type"]:
        filename = "content/js" + str(jsctr) + ".txt";
        with open(filename, "a") as ofile:
          try:
            jsctr = jsctr+1
            ofile.write(flow.request.pretty_url + "\n")
            ofile.write(flow.response.headers["content-type"] + "\n");
            ofile.write("----------------------------------------\n");
            ofile.write(bytes(flow.response.content).decode("utf-8"));
          except:
            ofile.write("error");
          ofile.close()
