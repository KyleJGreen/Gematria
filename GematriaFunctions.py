def getWordscoreGematria(word, num_corr_dict):
    wordscore_gematria = 0
    # for each character in a word, compute its score and add it to the total for the word
    for char in word:
        wordscore_gematria += num_corr_dict[char.lower()]  # add char score to word total
    return wordscore_gematria

# apply Qabalistic correspondences to words in dictionary
def convertToGematria(book_dict_list, num_corr_dict):
    book_dict_gematria = {}  # new dictionary for storing words within paragraphs of chapters as numerical scores

    # for each paragraph in each chapter, convert each word to a numerical score give the Table of pg. 4 in Aleister
    # Crowley's 777
    for chapter in book_dict_list:
        chapter_lines = []  # to contain list of lines with scores for each word
        for par in book_dict_list[chapter]:
            par_lines = []
            for word in par:
                par_lines.insert(len(par_lines), getWordscoreGematria(word, num_corr_dict))  # insert word total to new list
            chapter_lines.insert(len(chapter_lines), par_lines)  # add new list to chapter lines
        book_dict_gematria[chapter] = chapter_lines  # populate dictionary

    return book_dict_gematria  # return the new dictionary

def getWordscoreNumerology(word, num_corr_dict):
    wordscore_numerology = 0
    # for each character in a word, compute its score and add it to the total for the word
    for char in word:
        wordscore_numerology += getNumerologicalValue(char.lower(), num_corr_dict)  # add char score to word total
    return wordscore_numerology

# apply Numerological correspondences to words in dictionary
def convertToNumerological(bookDictList, num_corr_dict):
    book_dict_numerology = {}  # new dictionary for storing words within paragraphs of chapters as numerical scores

    # for each paragraph in each chapter, convert each word to a numerical score given its position in the Hebrew
    # alphabet
    for chapter in bookDictList:
        chapter_lines = []  # to contain list of lines with scores for each word
        for par in bookDictList[chapter]:
            par_lines = []
            for word in par:
                par_lines.insert(len(par_lines), getWordscoreNumerology(word, num_corr_dict))  # insert word total to new list
            chapter_lines.insert(len(chapter_lines), par_lines)  # add new list to chapter lines
        book_dict_numerology[chapter] = chapter_lines  # populate dictionary

    return book_dict_numerology  # return the new dictionary

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

# sum the entire book
def sumBook(bookDictChpSums):
    sum = 0
    # sum all chapters
    for chapter in bookDictChpSums:
        sum += bookDictChpSums[chapter]

    return sum

# return the digit sums for a given word (helper function)
def getDigitSums(word):
    sums = []
    sums.append(word)
    sums =getDigitSum(word, sums)
    return sums

# recursive function for generating individual digit sums
def getDigitSum(word, sums):
    # base case
    if word <= 9:
        return sums
    else:
        sum = 0
        for digit in str(word):
            sum += int(digit)
        sums.append(sum)
        return (getDigitSum((sum), sums))

def getNumerologicalValue(letter, num_corr_dict):
    if num_corr_dict.keys().index(letter) <= 15:
        return num_corr_dict.keys().index(letter) + 1
    else:
        return num_corr_dict.keys().index(letter)