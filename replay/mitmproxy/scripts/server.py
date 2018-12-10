# Usage: mitmdump -s "js_injector.py src"
# (this script works best with --anticache)
from bs4 import BeautifulSoup
import mitmproxy
#from mitmproxy.protocol.http import decoded
#from mitmproxy.protocol.http import decoded

def response(flow):
  if "content-type" in flow.response.headers:
    if "javascript" in flow.response.headers["content-type"]:
      flow.response.decode()
      with open("server.txt", "a") as ofile:
        ofile.write("\n-----------------------\n")
        ofile.write(flow.request.pretty_url + "\n")
        ofile.write(flow.response.headers["content-type"] + "\n");
        ofile.write(bytes(flow.response.content).decode("utf-8"));
        ofile.close()
