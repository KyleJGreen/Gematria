# import statements
import urllib
from bs4 import BeautifulSoup

## copies book from html file on crowndiamond.org to new file in Books/
import sys


def copyBook(book):
    url = 'https://www.crowndiamond.org/cd/' + book + '.html' # the url from which we are copying
    text = getBookFromUrl(url)
    lines = getLines(getBookFromUrl(url))

    with open('Books/' + book + '.txt', 'w') as f:
        f.write(text.encode('utf-8'))

## returns a string of text for a given url
def getBookFromUrl(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text  # return the text

## returns a string of text for a given book name from a text file
def getBookFromText(book):
    path = 'Books/' + book + '.txt' # build the path
    # write file to memory, replacing newline characters, v's and footer with empty string
    with open(path, 'r') as f:
        text = f.read().replace('\n', '').replace('v', '')
        text = text.replace('Leiticus', 'Leviticus')
    return text

def getLines(text):
    line = ""
    lines = []

    # iterate through text in reverse order, parsing on digits and adding to list of lines
    for char in reversed(text):
        # omit newline characters
        if char == '\n' or char == 'v':
            continue
        # parse on digits
        if char.isdigit():
            if line is not "":
                lines.insert(0, line.replace('Leiticus', 'Leviticus'))  # insert line to beginning of list
                line = ""  # reset line
        else:
            line = char + line

    return lines  # return the lines