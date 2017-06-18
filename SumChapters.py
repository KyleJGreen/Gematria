# import statements
import urllib
from bs4 import BeautifulSoup

## returns a string of text for a given url
def getPage(url):
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

# parses text into lines
def getLines(text):
    line = ""
    lines = []

    # iterate throuh text in reverse order, parsing on digits and adding to list of lines
    for char in reversed(text):
        # ommit newline characters
        if char == '\n' or char == 'v':
            continue
        # parse on digits
        if char.isdigit():
            if line is not "":
                lines.insert(0, line)  # insert line to beginning of list
                line = ""  # reset line
        else:
            line = char + line

    return lines  # return the lines


## for a given Book of the Torah, generate a dictionary with the chapters as keys and a list of their paragraphs as values
def fillBookDict(lines, BOOK, BOOK_HEBREW):
    chapter_lines = []  # list of lines for each chapter
    bookDict = {}  # the dictionary for this Book of the Torah
    count = 1  # loop counter variable

    # add every line to a list that gets added as the value to the chapter key in the book dictionary,
    # ommitting the chapter titles and paragraph break colons from the final result
    for line in lines:
        chapter = BOOK + str(count)  # create the name/key for each chapter by concatenating count to the book name
        chapter_lines.append(line.replace(':', '').replace(BOOK, '').replace(BOOK_HEBREW,
                                                                             ''))  # add line to list of lines for this chapter
        # use the name of the book to parse chapters
        if BOOK in line:
            # ommit empty lines
            if (line[:-8].replace(':', '') != ''):
                chapter_lines.append(line.replace(':', '').replace(BOOK, '').replace(BOOK_HEBREW,
                                                                                     ''))  # add line to list of lines for this chapter
            bookDict[chapter] = chapter_lines  # set lines for this chapter as the value of this chapter key
            count += 1  # increment count
            chapter_lines = []  # reset lines for next chapter
        # use the Hebrew name of the book to parse chapters
        elif BOOK_HEBREW in line:
            if (line[:-8].replace(':', '') != ''):
                chapter_lines.append(line.replace(':', '').replace(BOOK, '').replace(BOOK_HEBREW,
                                                                                     ''))  # add line to list of lines for this chapter
            bookDict[chapter] = chapter_lines  # set lines for this chapter as the value of this chapter key
            count += 1  # increment count
            chapter_lines = []  # reset lines for next chapter
    bookDict[chapter] = chapter_lines  # set lines for the final chapter

    return bookDict  # return the dictionary


## generates a new dictionary which contains a list of each word in a paragraph for each paragraph in a chapter
def parseWords(bookDict):
    bookDictList = {}  # new dictionary

    # go through each chapter in original dictionary and parse the paragraphs
    for chapter in bookDict:
        chapter_lines = []
        # iterate over each paragraph and parse on whitespace, adding list of strings to new list for new dictionary
        for par in bookDict[chapter]:
            chapter_lines.insert(len(chapter_lines), par.split())
        bookDictList[chapter] = chapter_lines

    return bookDictList  # return new dictionary


## remove footer text from dictionary
# TODO: rewrite algorithmically so that this can be applied to other pages/books
def removeFooter(bookDictList):
    lines = []  # for storing the lines for the chapter with the footer

    # for each paragraph in the chapter, see if the footer is contained in it and remove it if so
    for paragraph in bookDictList["Genesis50"]:
        parLine = []
        for word in paragraph:
            if 'mainmenu[Exodus][Leiticus][Numbers][Deuteronomy]bookmenu' in word:
                parLine.append(
                    word.replace('mainmenu[Exodus][Leiticus][Numbers][Deuteronomy]bookmenu', ''))  # remove footer
            else:
                parLine.append(word)
        else:
            lines.insert(len(lines), parLine)
    bookDictList["Genesis50"] = lines  # replace the chapter

    return bookDictList  # return dictionary without the footer


# apply Qabalistic correspondences to words in dictionary
def convertToNumeric(bookDictList, numCorrDict):
    bookDictNumeric = {}  # new dictionary for storing words within paragraphs of chapters as numerical scores

    # for each paragraph in each chapter, convert each word to a numerical score give the Table of pg. 4 in Aleister Crowley's 777
    for chapter in bookDictList:
        chapter_lines = []  # to contain list of lines with scores for each word
        for par in bookDictList[chapter]:
            par_lines = []
            for word in par:
                wordNumeric = 0
                # for each character in a word, compute its score and add it to the total for the word
                for char in word:
                    wordNumeric += numCorrDict[char.lower()]  # add char score to word total
                par_lines.insert(len(par_lines), wordNumeric)  # insert word total to new list
            chapter_lines.insert(len(chapter_lines), par_lines)  # add new list to chapter lines
        bookDictNumeric[chapter] = chapter_lines  # populate dictionary

    return bookDictNumeric  # return the new dictionary


# sum the word totals for each paragraph
def sumParagraphs(bookDictNumeric):
    bookDictParSums = {}  # new dictionary to contain sums of word scores for each paragraph in a chapter
    sums = []  # paragraph sums

    # for each paragraph in each chapter, sum the numeric scores for each word and add to new dictionary
    for chapter in bookDictNumeric:
        sums = [] # reset sums
        for par in bookDictNumeric[chapter]:
            sum = 0
            # for each word, add to the sum
            for word in par:
                sum += word
            sums.insert(len(sums), sum)
        bookDictParSums[chapter] = sums  # populate new dictionary

    return bookDictParSums  # return new dictionary


# sum the paragraph totals for each chapter
def sumChapters(bookDictParSums):
    bookDictChpSums = {}
    # for each chapter, generate a sum of all paragraph sums
    for chapter in bookDictParSums:
        sum = 0
        for parTotal in bookDictParSums[chapter]:
            sum += parTotal
        bookDictChpSums[chapter] = sum  # populate new dictionary

    return bookDictChpSums


def main():
    # variables
    BOOK = "Genesis"
    BOOK_HEBREW = "Bereshith"
    url = "https://www.crowndiamond.org/cd/genesis.html"
    numCorrDict = {'a': 1,
                   'b': 2,
                   'g': 3,
                   'd': 4,
                   'h': 5,
                   'w': 6,
                   'v': 6,
                   'z': 7,
                   'j': 8,
                   'f': 9,
                   'y': 10,
                   'i': 10,
                   'k': 20,
                   'l': 30,
                   'm': 40,
                   'n': 50,
                   's': 60,
                   'o': 70,
                   'u': 70,
                   '[': 70,
                   'p': 80,
                   'x': 90,
                   'q': 100,
                   'r': 200,
                   'c': 300,
                   't': 400}  # dictionary of Qabalistic Correspondences for each letter of the Hebrew alphabet (NOTE: some Hebrew letters have multiple English equivalents)

    text = getPage(url)  # get text from website
    lines = getLines(text)  # parse text into lines
    bookDict = fillBookDict(lines, BOOK, BOOK_HEBREW)  # fill dictionary for Book of Torah
    bookDictList = removeFooter(parseWords(bookDict))  # reformat dictionary
    bookDictNumeric = convertToNumeric(bookDictList, numCorrDict)  # apply Qabalistic correspondences to words
    bookDictParSums = sumParagraphs(bookDictNumeric)  # sum the paragraphs
    bookDictChpSums = sumChapters(bookDictParSums)  # sum the chapters

    # print chapter sums
    for chapter in bookDictChpSums:
        print bookDictChpSums[chapter]

if __name__ == '__main__': main()
