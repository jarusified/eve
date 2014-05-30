# TET sample application for dumping PDF information in the XML language TETML
#
# $Id: tetml.py,v 1.12 2012/01/19 07:36:10 rjs Exp $
#/

import sys
from traceback import *
from PDFlib.TET import *

# global option list */
globaloptlist = "searchpath={{../data} {../../../resource/cmap}}"

# document-specific option list */
basedocoptlist = ""

# page-specific option list */
# Remove the tetml= option if you don't need font and geometry information
pageoptlist = "granularity=word tetml={glyphdetails={all}}"

# set this to 1 to generate TETML output in memory */
inmemory = 0

if len(sys.argv) != 3:
    raise Exception("usage: tetml <pdffilename> <xmlfilename>\n")

try:
    try:
        pageno = 0
        tet = TET()

        tet.set_option(globaloptlist)

        if (inmemory):
            docoptlist =  "tetml={} %s" % basedocoptlist
        else:
            docoptlist =  "tetml={filename={%s}} %s" % \
                                (sys.argv[2], basedocoptlist)

        doc = tet.open_document(sys.argv[1], docoptlist)

        if (doc == -1):
            raise Exception("Error %d in %s(): %s" % \
               (tet.get_errnum(), tet.get_apiname(), tet.get_errmsg()))
        n_pages = int(tet.pcos_get_number(doc, "length:pages"))


        # loop over pages in the document */
        for pageno in range(1, n_pages+1):
            tet.process_page(doc, pageno, pageoptlist)

        # This could be combined with the last page-related call */
        tet.process_page(doc, 0, "tetml={trailer}")

        if (inmemory):
            fp = open(sys.argv[2], "wb")

            # Retrieve the generated TETML data from memory. Since we have
            # only a single call the result will contain the full TETML.
            #/

            tetml = tet.get_xml_data(doc, "")
            if (not tetml):
                raise Exception("tetml: couldn't retrieve XML data")

            fp.fwrite(tetml)
            fp.close()

        tet.close_document(doc)

    except TETException:
        print("TET exception occurred:\n[%d] %s: %s" %
            ((tet.get_errnum()), tet.get_apiname(),  tet.get_errmsg()))
        print_tb(exc_info()[2])

    except Exception:
        #print("Exception occurred: %s" % (exc_info()[0]))
        print_exc()

finally:
    tet.delete()
