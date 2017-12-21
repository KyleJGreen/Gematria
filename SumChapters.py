import random
from collections import OrderedDict

import sys

import DictBuildFunctions
import GematriaFunctions
import TemurahFunctions
import IOFunctions
from chained import Chain
import collections
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='For Gematria analysis of sacred texts.')
    parser.add_argument('book', nargs='?', help='Please specify the Book you want to analyze')
    args = parser.parse_args()

    # variables
    english_hebrew_correspondences = {"genesis" : "Bereshith", "exodus" : "Shemot", "leviticus" : "Vayikra",
                                      "numbers" : "Bemidbar", "deuteronomy" : "Devarim"}
    BOOK_HEBREW = english_hebrew_correspondences[args.book.lower()]
    books = ["genesis", "exodus", "leviticus", "numbers", "deuteronomy"]
    num_corr_dict = collections.OrderedDict([('a', 1),
    ('b', 2),
    ('g', 3),
    ('d', 4),
    ('h', 5),
    ('w', 6),
    ('z', 7),
    ('j', 8),
    ('f', 9),
    ('y', 10),
    ('k', 20),
    ('l', 30),
    ('m', 40),
    ('n', 50),
    ('s', 60),
    ('o', 70),
    ('[', 70),
    ('p', 80),
    ('x', 90),
    ('q', 100),
    ('r', 200),
    ('c', 300),
    ('t', 400)])  # dictionary of Qabalistic Correspondences for each letter of the...
    # Hebrew alphabet (NOTE: some Hebrew letters have multiple English equivalents)

    # INITIAL DICTIONARY
    lines = IOFunctions.getLines(IOFunctions.getBookFromText(args.book.lower()))  # parse text into lines
    book_dict = DictBuildFunctions.fillBookDict(lines, args.book, BOOK_HEBREW)  # fill dictionary for Book of Torah
    book_dict_list = DictBuildFunctions.parseWords(book_dict)  # reformat dictionary

    # FILL REPORT DICTIONARIES
    words_alpha = DictBuildFunctions.getWordsSet(book_dict_list)
    alpha_dict, gematria_dict, numerology_dict, words_gematria, words_numerology = \
        DictBuildFunctions.makeReportDicts(words_alpha, num_corr_dict, book_dict_list, args.book)

    # GEMATRIA
    book_dict_gematria = GematriaFunctions.convertToGematria(book_dict_list, num_corr_dict)  # apply Qabalistic # correspondences to words
    gematria_par_sums = GematriaFunctions.sumParagraphs(book_dict_gematria)  # sum the paragraphs
    gematria_chp_sums = GematriaFunctions.sumChapters(gematria_par_sums)  # sum the chapters
    book_gematira = GematriaFunctions.sumBook(gematria_chp_sums)  # sum the book

    # NUMEROLOGY
    book_dict_numerology = GematriaFunctions.convertToNumerological(book_dict_list, num_corr_dict)
    numerology_par_sums = GematriaFunctions.sumParagraphs(book_dict_numerology)  # sum the paragraphs
    numerology_chp_sums = GematriaFunctions.sumChapters(numerology_par_sums)  # sum the chapters
    book_numerology = GematriaFunctions.sumBook(numerology_chp_sums)  # sum the book

    # GENERATE REPORTS
    # pd.DataFrame(alpha_dict).T.to_excel('Reports/%s_Words-AlphabeticalReport.xls' %(args.book))
    # pd.DataFrame(gematria_dict).T.to_excel('Reports/%s_Words-GematriaReport.xls' %(args.book))
    # pd.DataFrame(numerology_dict).T.to_excel('Reports/%s_Words-NumerologyReport.xls' %(args.book))
    # pd.DataFrame(gematria_par_sums).T.to_excel('Reports/%s_GematriaParagraphsReportReport.xls' %(args.book))
    # pd.DataFrame(gematria_chp_sums).T.to_excel('Reports/%s_GematriaChapersReport.xls' %(args.book))
    # pd.DataFrame(numerology_par_sums).T.to_excel('Reports/%s_NumerologyParagraphsReport.xls' %(args.book))
    # pd.DataFrame(numerology_chp_sums).T.to_excel('Reports/%s_NumerologyChaptersReport.xls' %(args.book))

    for chapter in book_dict_gematria:
        # print(book_dict_gematria[chapter])

        for paragraph in book_dict_gematria[chapter]:
            text = str(paragraph).replace(',','').replace('[','').replace(']','')
            mychain = Chain(3)  # create an empty third order chain "mychain"
            mychain.addSequence(text)  # mychain will index characters in this string
            seq = mychain.getSequence()  # seq is now a list of characters generated from mychain
            seq_str = str(seq).replace('\', ', '').replace('\'', '')
            words_list = [gematria_dict[int(sum)]['Words'][random.randint(0,len(gematria_dict[int(sum)]['Words']) - 1)] for sum in seq_str[1:-1].split()]
            generated = str(seq).replace('\', ', '').replace('\'', '').replace('[', '').replace(']', '')
            if text != generated:
                print("Original : " + text)
                print("Generated : " + generated)
                print("Generated Words : " + str(words_list).replace('\', ', ' ').replace('\'', '').replace('[', '').replace(']', ''))

        sys.exit()

    print(GematriaFunctions.getDigitSums(book_gematira))
    print(GematriaFunctions.getDigitSums(book_numerology))

if __name__ == '__main__': main()
