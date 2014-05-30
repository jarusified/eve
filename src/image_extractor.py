#!/usr/bin/python
# Simple Python image extractor based on PDFlib TET
#
# $Id: image_extractor.py,v 1.1 2013/05/13 15:18:03 rjs Exp $
#

from sys import *
from traceback import print_tb, print_exc
from PDFlib.TET import *

# global option list */
globaloptlist = "searchpath={{../data}}"

# document-specific option list */
docoptlist = ""

# page-specific option list */
pageoptlist = "granularity=page"

# here you can insert basic image extract options (more below)
baseimageoptlist = ""


if len(argv) != 2:
    raise Exception("usage: image_extractor <infilename>\n")

outfilebase = argv[1]
try:
    try:

        tet = TET()

        tet.set_option(globaloptlist)


        doc = tet.open_document(argv[1], docoptlist)

        if (doc == -1):
            raise Exception("Error " + tet.get_errnum() + "in " \
                + tet.get_apiname() + "(): " + tet.get_errmsg())

        # get number of pages in the document */
        n_pages = tet.pcos_get_number(doc, "length:pages")

        # loop over pages in the document */
        for pageno in range(1, int(n_pages)+1):
            imageno = -1

            page = tet.open_page(doc, pageno, pageoptlist)

            if (page == -1):
                print("Error " + tet.get_errnum() + "in " \
                    + tet.get_apiname() + "(): " + tet.get_errmsg())
                continue                        # try next page */

            # Retrieve all text fragments; This is actually not required
            # for granularity=page, but must be used for other granularities.
            #
            ti = tet.get_image_info(page)
            while (ti):
		# Report image geometry
		print("page %d: %.2fx%.2fpt, alpha=%.2f, beta=%.2f" %
		(pageno, ti["width"], ti["height"], ti["alpha"], ti["beta"]))

		# Retrieve additional image properties with pCOS
		print("   id=%d, %dx%d pixel" % ( ti["imageid"],
		    tet.pcos_get_number(doc, "images[%d]/Width" % ti["imageid"]),
		    tet.pcos_get_number(doc, "images[%d]/Height" % ti["imageid"])))
		cs =  tet.pcos_get_number(doc, "images[%d]/colorspaceid" % ti["imageid"])

		if (cs != -1):
		    print("   %dx%d bit %s" % (tet.pcos_get_number(doc, "colorspaces[%d]/components" % cs),
			tet.pcos_get_number(doc, "images[%d]/bpc" % ti["imageid"]), 
			tet.pcos_get_string(doc, "colorspaces[%d]/name" % cs )))

		else:
		    # cs==-1 may happen for some JPEG 2000 images. bpc,
		    # colorspace name and number of components are not
		    # available in this case.


		    print("JPEG2000")

		# Fetch image data and write it to a disk file. The
		# output filename is generated from the input filename,
		# page number and image ID.

		imageoptlist = baseimageoptlist + " filename {" + outfilebase + "_p" + repr(pageno) + "_I" + repr(ti["imageid"]) + "}"
		if (tet.write_image_file(doc, ti["imageid"], imageoptlist) == -1):
		    print("Error " + tet.get_errnum() + " in " +
			tet.get_apiname() + "(): " + tet.get_errmsg())
		ti = tet.get_image_info(page)


            if (tet.get_errnum() != 0):
                raise Exception ("Error " + repr(tet.get_errnum()) \
                    + "in " + tet.get_apiname() + "() on page " + \
                    repr(pageno) + ": " + tet.get_errmsg() )

            tet.close_page(page)

        tet.close_document(doc)

    except TETException:
        print("TET exception occurred:\n[%d] %s: %s" %
            ((tet.get_errnum()), tet.get_apiname(),  tet.get_errmsg()))
        print_tb(exc_info()[2])

    except Exception:
        print("Exception occurred: %s" % (exc_info()[0]))
        print_exc()

finally:
    tet.delete()
