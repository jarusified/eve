#!/usr/bin/python
# Resource-based image extractor based on PDFlib TET
#
# $Id: image_resources.py,v 1.7 2012/02/16 14:28:00 rjs Exp $
#

from sys import *
from traceback import print_tb, print_exc
from PDFlib.TET import *

# global option list */
globaloptlist = "searchpath={{../data}}"

# document-specific option list */
docoptlist = ""

# page-specific option list */
pageoptlist = ""

# here you can insert basic image extract options (more below) */
baseimageoptlist = ""

if len(argv) != 2:
    raise Exception("usage: image_resources <filename>\n")

try:
    try:
        tet = TET()

        outfilebase = argv[1]

        tet.set_option(globaloptlist)

        doc = tet.open_document(argv[1], docoptlist)

        if (doc == -1):
            raise Exception("Error " + tet.get_errnum() + "in " \
                + tet.get_apiname() + "(): " + tet.get_errmsg())

        # Images will only be merged upon opening a page.
        # In order to enumerate all merged image resources
        # we open all pages before extracting the images.
        #/

        # get number of pages in the document */
        n_pages = tet.pcos_get_number(doc, "length:pages")

        # loop over pages in the document */
        for pageno in range(1, int(n_pages)+1):

            page = tet.open_page(doc, pageno, pageoptlist)

            if (page == -1):
                print("Error " + tet.get_errnum() + "in " \
                    + tet.get_apiname() + "(): " + tet.get_errmsg())
                continue                        # try next page */

            if (tet.get_errnum() != 0):
                raise Exception ("\nError " + repr(tet.get_errnum()) \
                    + "in " + tet.get_apiname() + "() on page " + \
                    repr(pageno) + ": " + tet.get_errmsg() + "\n")

            tet.close_page(page)


        # get number of image resources in the document */
        n_images = tet.pcos_get_number(doc, "length:images")

        # loop over image resources in the document */
        for imageid in range(0, int(n_images)):

            # examine image type
            mergetype = tet.pcos_get_number(doc,
                        "images[%d]/mergetype" % imageid)

            # skip images which have been consumed by merging
            if (mergetype == 0 or mergetype == 1):
                # Print the following information for each image:
                # - image number
                # - pCOS id (required for indexing the images[] array)
                # - physical size of the placed image on the page
                # - pixel size of the underlying PDF image
                # - number of components, bits per component, and colorspace
                # - mergetype if different from "normal", i.e. "artificial"
                #   (=merged) or "consumed"
                #
                width = tet.pcos_get_number(doc, \
                                "images[%d]/Width" % imageid)
                height = tet.pcos_get_number(doc, \
                                "images[%d]/Height" % imageid)
                bpc = tet.pcos_get_number(doc, \
                                "images[%d]/bpc" % imageid)
                cs = tet.pcos_get_number(doc, \
                                "images[%d]/colorspaceid" % imageid)

                txt = "image I%d: %dx%d pixel, " % (imageid, width, height);

                if (cs != -1):
                    txt = txt + "%dx" % tet.pcos_get_number(doc, \
                                "colorspaces[%d]/components" % cs) \
                        + "%d bit " % bpc \
                        + "%s" % tet.pcos_get_string(doc, \
                                "colorspaces[%d]/name" % cs)
                else:
                    # cs==-1 may happen for some JPEG 2000 images. bpc,
                    # colorspace name and number of components are not
                    # available in this case.
                    txt = txt + "JPEG2000"

                if (mergetype):
                    txt = txt + ", mergetype="
                    if (mergetype == 1):
                        txt = txt + "artificial"
                    else:
                        txt = txt + "consumed"

                print(txt)

                # Fetch the image data and write it to a disk file. The
                # output filenames are generated from the input filename
                # by appending page number and image number.
                #
                imageoptlist = "%s filename={%s_I%d}" % \
                    (baseimageoptlist, outfilebase, imageid)
                
                if (tet.write_image_file(doc, imageid, \
                                            imageoptlist) == -1):
                    print("\nError " + repr(tet.get_errnum()) + "in " + \
                        tet.get_apiname() + "():" + tet.get_errmsg())
                    continue                   # process next image */

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
