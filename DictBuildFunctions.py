import GematriaFunctions

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

def getWordsSet(book_dict_list):
    words_alpha = []
    # generate set of all words in book
    for chapter in book_dict_list:
        for par in book_dict_list[chapter]:
            for word in par:
                words_alpha.append(word)
    words_alpha = set(words_alpha)
    return words_alpha

def makeReportDicts(words_alpha, num_corr_dict, book_dict_list, book):
    alpha_dict = {}
    gematria_dict = {}
    numerology_dict = {}
    words_gematria = []
    words_numerology = []

    for word in sorted(words_alpha):
        gematria = GematriaFunctions.getWordscoreGematria(word, num_corr_dict)
        numerology = GematriaFunctions.getWordscoreNumerology(word, num_corr_dict)
        alpha_dict[word] = {'Gematria': gematria,
                            'Numerology': numerology,
                            'Locations': []}
        try:
            gematria_dict[gematria]['Words'].append(word)
            numerology_dict[numerology]['Words'].append(word)
        except KeyError:
            gematria_dict[gematria] = {'Words': []}
            gematria_dict[gematria]['Words'].append(word)
            numerology_dict[numerology] = {'Words': []}
            numerology_dict[numerology]['Words'].append(word)
        words_gematria.append(gematria)
        words_numerology.append(numerology)

    addLocations(alpha_dict, book_dict_list, book) # add locations of words

    return alpha_dict, gematria_dict, numerology_dict, words_gematria, words_numerology

def addLocations(alpha_dict, book_dict_list, book):
    # generate set of all words in book
    for i, chapter in enumerate(sorted(book_dict_list)):
        for j, par in enumerate(book_dict_list[chapter]):
            for k, word in enumerate(par):
                alpha_dict[word]['Locations'].append(book + ':' + str(i + 1) + ':' + str(j + 1) + ':' + str(k + 1))
    return alpha_dict