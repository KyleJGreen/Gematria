import IOFunctions

def scrape(previous, url):
    import urllib
    import lxml.html
    connection = urllib.urlopen('https://www.crowndiamond.org/cd/Dict/a/ab/abd.html')
    prev = ""
    current = ""

    dom =  lxml.html.fromstring(connection.read())

    for link in dom.xpath('//a/@href'): # select the url in href for all a tags(links)
        if prev == previous:
            text = IOFunctions.getBookFromUrl(url)
            with open('Dictionary/' + link, 'w') as f:
                f.write(text.encode('utf-8'))
        prev = link