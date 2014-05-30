#!/usr/bin/python
# Extract text from PDF and filter according to font name and size.
# This can be used to identify headings in the document and create a
# table of contents.
#
# $Id: fontfilter.py,v 1.11.2.1 2012/02/21 13:54:06 rjs Exp $
#/

import sys
from traceback import print_tb, print_exc
from PDFlib.TET import *


# global option list */
globaloptlist = "searchpath={{../data} {../../../resource/cmap}}"

# document-specific option list */
docoptlist = ""

# page-specific option list */
pageoptlist = "granularity=line"

# Search text with at least this size (use 0 to catch all sizes) */
fontsizetrigger = 10

# Catch text where the font name contains this string
# (use empty string to catch all font names)
#/
fontnametrigger = "Bold"

if len(sys.argv) != 2:
    raise Exception("usage: fontfilter <infilename>\n")

try:
    try:
        pageno = 0

        tet = TET()

        tet.set_option(globaloptlist)

        doc = tet.open_document(sys.argv[1], docoptlist)

        if (doc == -1):
            raise Exception("Error %d in %s(): %s\n" % \
                (tet.get_errnum(), tet.get_apiname(), \
                tet.get_errmsg()))

        # get number of pages in the document */
        n_pages = int(tet.pcos_get_number(doc, "length:pages"))

        # loop over pages in the document */
        for pageno in range(1, n_pages+1):
            page = tet.open_page(doc, pageno, pageoptlist)

            if (page == -1):
                print(("Error %d in %s() on page %d: %s\n" % \
                    (tet.get_errnum(), tet.get_apiname(), pageno, \
                     tet.get_errmsg())))
                continue                        # try next page */

            # Retrieve all text fragments for the page */
            text = tet.get_text(page)
            while (text):
                # Loop over all characters */
                ci = tet.get_char_info(page)
                while (ci):
                    # We need only the font name and size the text 
                    # position could be fetched from ci->x and ci->y.
                    #/
                    fontname = tet.pcos_get_string(doc, \
                                "fonts[%d]/name" % ci["fontid"])

                    # Check whether we found a match */
                    # C only: some versions of strstr don't allow empty
                    # strings, so we better check */
                    if (ci["fontsize"] >= fontsizetrigger and \
                                fontname.find(fontnametrigger) != -1):
                        # print the retrieved font name, size, and text */
                        print(("[%s %.2f] %s" % (fontname, ci["fontsize"], text)))
                    ci = tet.get_char_info(page)
                    # In this sample we check only the first character of
                    # each fragment.
                    #/
                    break
                text = tet.get_text(page)
            if (tet.get_errnum() != 0):
                raise Exception("Error %d in %s() on page %d: %s\n" % \
                    (tet.get_errnum(), tet.get_apiname(), pageno, \
                     tet.get_errmsg()))

            tet.close_page(page)

        tet.close_document(doc)


    except TETException:
        if (pageno == 0):
            print("TET exception occurred:\n[%d] in %s: %s" %
                ((tet.get_errnum()), tet.get_apiname(), 
                tet.get_errmsg()))
        else:
            print("TET exception occurred:\n[%d] in %s: %s() on page %d" %
                ((tet.get_errnum()), tet.get_apiname(), 
                tet.get_errmsg(), pageno))
        print_tb(exc_info()[2])

#    except Exception:
#        print("Exception occurred: %s" % (exc_info()[0]))
#       print_exc()

finally:
    tet.delete()
