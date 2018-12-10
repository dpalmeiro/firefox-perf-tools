# USAGE:
#   1. Copy this script into your working directory
#   2. Adjust the dict below where "request url" => "local file path"
#   3. Run mitmproxy with `mitmproxy -z --anticache -s local_file_replace.py`
#      (-z disables gzip compression, --anticache disables 304 responses)
#   4. Profit!

REPLACEMENTS = {
    "https://secure.quantserve.com/aquant\.js\?a=p-xLEyC0FLYFXAH": "empty.js"
}

# NOTE for Python 2.7 users:
# Please replace the function signature with `def response(self, flow)`
def response(flow):
    if flow.request.url in REPLACEMENTS:
        file = open(REPLACEMENTS[flow.request.url], "rb")
        flow.response.content = file.read()
        file.close()
