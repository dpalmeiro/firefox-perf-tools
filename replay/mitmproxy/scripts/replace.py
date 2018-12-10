from bs4 import BeautifulSoup

_S1 = 'Math.random\(\)'
_R1 = "0.3425253151"

_S2 = "new Date\(\)"
_R2 = "new Date('November 1, 2018 14:04:00')"

_S3 = "\(new Date\)"
_R3 = "(new Date('November 1, 2018 14:04:00'))"

def response(flow):
    flow.response.replace(_S1, _R1)
    flow.response.replace(_S2, _R2)
    flow.response.replace(_S3, _R3)

#    with decoded(flow.response):
#    html = BeautifulSoup(flow.response.content)
#    if html.body and ('text/html' in flow.response.headers["content-type"][0]):
#      with open("file_to_write_data_to.txt", "a") as ofile:
#        ofile.write("-----------------------\n")
#        ofile.write(flow.request.pretty_url)
#        ofile.write(str(html))
#        ofile.close()


