# USAGE:
#   1. Copy this script into your working directory
#   2. Adjust the dict below where "request url" => "local file path"
#   3. Run mitmproxy with `mitmproxy -z --anticache -s local_file_replace.py`
#      (-z disables gzip compression, --anticache disables 304 responses)
#   4. Profit!

# NOTE for Python 2.7 users:
# Please replace the function signature with `def response(self, flow)`

_S1 = 'Math.random\(\)'
_R1 = "0.3425253151"

_S2 = "new Date\(\)"
_R2 = "new Date('November 1, 2018 14:04:00')"

REPLACEMENTS_URL = {
    "http://example.com/example/assets/jquery.min.js": "empty.js",
    "https://cdn.example.com/foo/compressed.js": "empty.js"
}

def response(flow):
    flow.response.replace(_S1, _R1)
    flow.response.replace(_S2, _R2)

    #if flow.request.url in REPLACEMENTS:
    #    file = open(REPLACEMENTS[flow.request.url], "rb")
    #    flow.response.content = file.read()
    #    file.close()
