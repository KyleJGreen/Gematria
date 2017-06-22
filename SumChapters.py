from collections import OrderedDict
import DictBuildFunctions
import GematriaFunctions
import TemurahFunctions
import IOFunctions
import collections
import pandas as pd

def main():
    # variables
    BOOK = "Genesis"
    BOOK_HEBREW = "Bereshith"
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
    lines = IOFunctions.getLines(IOFunctions.getBookFromText(books[0]))  # parse text into lines
    book_dict = DictBuildFunctions.fillBookDict(lines, BOOK, BOOK_HEBREW)  # fill dictionary for Book of Torah
    book_dict_list = DictBuildFunctions.parseWords(book_dict)  # reformat dictionary

    # FILL REPORT DICTIONARIES
    words_alpha = DictBuildFunctions.getWordsSet(book_dict_list)
    alpha_dict, gematria_dict, numerology_dict, words_gematria, words_numerology = \
        DictBuildFunctions.makeReportDicts(words_alpha, num_corr_dict, book_dict_list, BOOK)

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
    # pd.DataFrame(alpha_dict).T.to_excel('Reports/Words-AlphabeticalReport.xls')
    # pd.DataFrame(gematria_dict).T.to_excel('Reports/Words-GematriaReport.xls')
    # pd.DataFrame(numerology_dict).T.to_excel('Reports/Words-NumerologyReport.xls')
    # pd.DataFrame(gematria_par_sums).T.to_excel('Reports/GematriaParagraphsReportReport.xls')
    # pd.DataFrame(gematria_chp_sums).T.to_excel('Reports/GematriaChapersReport.xls')
    # pd.DataFrame(numerology_par_sums).T.to_excel('Reports/NumerologyParagraphsReport.xls')
    # pd.DataFrame(numerology_chp_sums).T.to_excel('Reports/NumerologyChaptersReport.xls')

    print(GematriaFunctions.getDigitSums(book_gematira))
    print(GematriaFunctions.getDigitSums(book_numerology))

if __name__ == '__main__': main()
