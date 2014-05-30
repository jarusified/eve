#!/usr/bin/python
# Simple Python text and image glyphinfo based on PDFlib TET
#
# $Id: glyphinfo.py,v 1.9 2012/01/19 07:36:10 rjs Exp $
#

import sys
from traceback import print_tb, print_exc
from PDFlib.TET import *

# global option list */
globaloptlist = "searchpath={{../data} {../../../resource/cmap}}"

# document-specific option list */
docoptlist = ""

# page-specific option list */
pageoptlist = "granularity=word"

# tet.char_info character types with real geometry info.
TET_CT__REAL	= 0
TET_CT_NORMAL	= 0
TET_CT_SEQ_START	= 1

# tet.char_info character types with artificial geometry info.
TET_CT__ARTIFICIAL	= 10
TET_CT_SEQ_CONT	= 10
TET_CT_INSERTED	= 12


# tet.char_info text rendering modes.
TET_TR_FILL	= 0	# fill text
TET_TR_STROKE	= 1	# stroke text (outline)
TET_TR_FILLSTROKE	= 2	# fill and stroke text
TET_TR_INVISIBLE	= 3	# invisible text
TET_TR_FILL_CLIP	= 4	# fill text and
                                        # add it to the clipping path
TET_TR_STROKE_CLIP	= 5	# stroke text and
                                        #  add it to the clipping path
TET_TR_FILLSTROKE_CLIP= 6# fill and stroke text and
                                        #  add it to the clipping path
TET_TR_CLIP	= 7	# add text to the clipping path

# tet.char_info attributes
TET_ATTR_NONE      = 0x00000000
TET_ATTR_SUB       = 0x00000001	# subscript
TET_ATTR_SUP       = 0x00000002	# superscript
TET_ATTR_DROPCAP   = 0x00000004	# initial large letter
TET_ATTR_SHADOW    = 0x00000008	# shadowed text
# character before hyphenation
TET_ATTR_DEHYPHENATION_PRE       = 0x00000010
# hyphenation artifact, i.e. the dash
TET_ATTR_DEHYPHENATION_ARTIFACT  = 0x00000020
# character after hyphenation
TET_ATTR_DEHYPHENATION_POST      = 0x00000040

import traceback
def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except KeyError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)


if len(sys.argv) != 3:
    raise Exception("usage: glyphinfo <infilename> <outfilename>\n")

try:
    try:

        tet = TET()

        if (sys.version_info[0] < 3):
            fp = open(sys.argv[2], 'w')
	    from ctypes import *
	    PyFile_SetEncoding = pythonapi.PyFile_SetEncoding
	    PyFile_SetEncoding.argtypes = (py_object, c_char_p)
	    PyFile_SetEncoding(fp, 'utf-8')
        else:
            fp = open(sys.argv[2], 'w', 2, 'utf-8')

        tet.set_option(globaloptlist)

        doc = tet.open_document(sys.argv[1], docoptlist)

        if (doc == -1):
            raise Exception("Error " + tet.get_errnum() + "in " \
                + tet.get_apiname() + "(): " + tet.get_errmsg())

        # get number of pages in the document */
        n_pages = tet.pcos_get_number(doc, "length:pages")

        # loop over pages in the document */
        for pageno in range(1, int(n_pages)+1):

            page = tet.open_page(doc, pageno, pageoptlist)

            if (page == -1):
                print("Error " + tet.get_errnum() + "in " \
                    + tet.get_apiname() + "(): " + tet.get_errmsg())
                continue                        # try next page */

	    # write UTF-8 BOM
	    print >>fp, ("%c%c%c" % (0xef, 0xbb, 0xbf));

	    # Administrative information
	    print >>fp, ("[ Document: '%s' ]" %
	                    tet.pcos_get_string(doc, "filename"))
	    print >>fp, ("[ Document options: '%s' ]" % docoptlist)
	    print >>fp, ("[ Page options: '%s' ]" % pageoptlist)
	    print >>fp, ("[ ----- Page %d ----- ]" % pageno)

            # Retrieve all text fragments
            text = tet.get_text(page)
            while (text):
                print >>fp, ("[%s]" % text)  # print the retrieved text

                # Loop over all characters */
                ci = tet.get_char_info(page)
                while (ci):
		    # Fetch the font name with pCOS (based on its ID)
                    fontname = tet.pcos_get_string(doc, \
                                "fonts[%d]/name" % ci["fontid"])

		    # Print the character */
		    print >>fp, ("U+%04X" % ci["uv"]),

		    # ...and its ASCII representation if appropriate */
		    print >>fp, (" '%s'" % unichr(ci["uv"])),

		    # Print font name, size, and position */
		    print >>fp, (" %s size=%.2f x=%.2f y=%.2f" % \
			(fontname, ci["fontsize"], ci["x"], ci["y"])),

		    # Examine the "type" member */
		    if (ci["type"] == TET_CT_SEQ_START):
			print >>fp, ( " ligature_start"),
		    elif (ci["type"] == TET_CT_SEQ_CONT):
			print >>fp, ( " ligature_cont"),
		    # Separators are only inserted for granularity > word */
		    elif (ci["type"] == TET_CT_INSERTED):
			print >>fp, ( " inserted"),

		    # Examine the bit flags in the "attributes" member */
		    if (ci["attributes"] != TET_ATTR_NONE):
			if (ci["attributes"] & TET_ATTR_SUB):
			    print >>fp, ( "/sub"),
			if (ci["attributes"] & TET_ATTR_SUP):
			    print >>fp, ( "/sup"),
			if (ci["attributes"] & TET_ATTR_DROPCAP):
			    print >>fp, ( "/dropcap"),
			if (ci["attributes"] & TET_ATTR_SHADOW):
			    print >>fp, ( "/shadow"),
			if (ci["attributes"] & TET_ATTR_DEHYPHENATION_PRE):
			    print >>fp, ( "/dehyphenation_pre"),
			if (ci["attributes"] & TET_ATTR_DEHYPHENATION_ARTIFACT):
			    print >>fp, ( "/dehyphenation_artifact")
			if (ci["attributes"] & TET_ATTR_DEHYPHENATION_POST):
			    print >>fp, ( "/dehyphenation_post"),

		    print >>fp
		    ci = tet.get_char_info(page)

		print >>fp
                text = tet.get_text(page)

            if (tet.get_errnum() != 0):
                raise Exception ("\nError " + repr(tet.get_errnum()) \
                    + "in " + tet.get_apiname() + "() on page " + \
                    repr(pageno) + ": " + tet.get_errmsg() + "\n")

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
