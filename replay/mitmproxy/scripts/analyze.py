import time
import os
from bs4 import BeautifulSoup
from mitmproxy import http

htmlctr = 0;
jsctr   = 0;
millis  = 0;

def start():
  millis = int(round(time.time() * 1000))


def response(flow):
  global htmlctr, jsctr, millis
  if "content-type" in flow.response.headers:
    if 'text/html' in flow.response.headers["content-type"]:
      flow.response.decode()
      html = BeautifulSoup(flow.response.content)
      if html.body:
        with open("scripts/deterministic.js", "r") as jsfile:
          js = jsfile.read().replace("REPLACE_LOAD_TIMESTAMP",str(millis));
          script = html.new_tag("script")
          #script.append(jsfile.read());
          script.append(js);
          html.html.insert(0, script)
          flow.response.content = bytes(str(html), "utf-8")

        filename = "content/html" + str(htmlctr) + ".txt";
        with open(filename, "a") as ofile:
          htmlctr = htmlctr + 1
          ofile.write(flow.request.pretty_url + "\n")
          ofile.write(flow.response.headers["content-type"] + "\n");
          ofile.write("----------------------------------------\n");
          ofile.write(bytes(flow.response.content).decode("utf-8"));
          ofile.close()

    #if "javascript" in flow.response.headers["content-type"]:
    #  flow.response.decode()
    #  with open("scripts/deterministic.js", "rb") as jsfile:
    #    js = jsfile.read().decode("utf-8");
    #    js.replace("REPLACE_LOAD_TIMESTAMP",str(millis));
    #    flow.response.content = bytes(js,"utf-8") + flow.response.content

    #  filename = "content/js" + str(jsctr) + ".txt";
    #  with open(filename, "a") as ofile:
    #    jsctr = jsctr+1
    #    ofile.write(flow.request.pretty_url + "\n")
    #    ofile.write(flow.response.headers["content-type"] + "\n");
    #    ofile.write("----------------------------------------\n");
    #    ofile.write(bytes(flow.response.content).decode("utf-8"));
    #    ofile.close()
      #os.system("/usr/local/bin/js-beautify " + filename + " -o " + filename + "_new");
