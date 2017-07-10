import urllib.request

BASE_URL="https://www.google.com/search?sclient=psy-ab&hl=en&site=webhp&source=hp&btnG=Search&q="
headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
req = urllib.request.Request(BASE_URL+'crisis+text+line', headers=headers)

response = urllib.request.urlopen(req)
print(response.read())