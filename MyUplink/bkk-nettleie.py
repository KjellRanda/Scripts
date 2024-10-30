from html.parser import HTMLParser
import datetime
import sys
import requests
import bs4

class HTMLFilter(HTMLParser):
    text = ''
    def handle_data(self, data):
        self.text += f'{data}\n'

def html2text(html):
    filter = HTMLFilter()
    filter.feed(html)
    return filter.text

url = "https://www.bkk.no/alt-om-nettleie/nettleiepriser"

req = requests.get(url, timeout=60)
if req.status_code == 200:
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    table = soup.find_all('table')[1]
    text = html2text(str(table))
    line = text.split("\n")
    print(f"Data scraped from {url} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{line[0]}\t{line[1]}\t{line[2]}")
    print(f"{line[3]}\t\t{float(line[4].replace(',', '.'))}\t\t{float(line[5].replace(',', '.'))}")
    print(f"{line[6]}\t{float(line[7].replace(',', '.'))}\t\t{float(line[8].replace(',', '.'))}")
else:
    print(f"Failed to scrape data from {url}  Response code: {req.status_code}")
    sys.exit(2)