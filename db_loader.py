import requests
from html.parser import HTMLParser
from dbconnection import DBConnection


class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data

html_filter = HTMLFilter()

# Download content from the resource
url = "https://www.cidr-report.org/as2.0/autnums.html"
r = requests.get(url, allow_redirects = True)
html_filter.feed(r.content.decode("utf-8"))

db = DBConnection()
db.create_table()

# Populate the database
lst = html_filter.text.splitlines( )
for i in range(14,len(lst)-8):
    line = lst[i]
    asn, org_info, country_code = int(line[2:8].strip()), line[8:-4].strip(), line[-2:]
    db.insert(asn, org_info, country_code)

db.commit()

db.close()