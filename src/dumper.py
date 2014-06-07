# TET sample application for dumping PDF information with pCOS
#
# $Id: dumper.py,v 1.16.2.1 2012/02/21 13:54:32 rjs Exp $
#

from sys import *
from traceback import print_tb, print_exc
from PDFlib.TET import *

def yesno(arg):
    if (arg != 0):
        return "yes"
    return "no"


if len(argv) != 2:
    raise Exception("usage: dumper <filename>")

try:
    try:
        tet = TET()

        searchpath = "searchpath={{../data}}"
        docoptlist = "requiredmode=minimum"
        globaloptlist = ""

        tet.set_option(searchpath)
        tet.set_option(globaloptlist)

        doc = tet.open_document(argv[1], docoptlist)
        if doc  == -1:
            raise Exception("ERROR: %s\n" % tet.get_errmsg())

        # --------- general information (always available) */
        pcosmode = int(tet.pcos_get_number(doc, "pcosmode"))

        #print(("   File name: %s" % tet.pcos_get_string(doc, "filename")))

        #print((" PDF version: %s" % \
        #    tet.pcos_get_string(doc, "pdfversionstring")))

        #print(("  Encryption: %s" % \
        #    tet.pcos_get_string(doc, "encrypt/description")))

        #print(("   Master pw: %s" % \
        #    yesno(tet.pcos_get_number(doc, "encrypt/master"))))

        #print(("     User pw: %s" % \
        #    yesno(tet.pcos_get_number(doc, "encrypt/user"))))

        #print(("Text copying: %s" % \
        #    yesno(not tet.pcos_get_number(doc, "encrypt/nocopy"))))

        #print(("  Linearized: %s" % \
        #    yesno(tet.pcos_get_number(doc, "linearized"))))

        if (pcosmode == 0):
           # print("Minimum mode: no more information available\n")
            tet.close_document(doc)
            exit(0)

        # --------- more details (requires at least user password) */

       # print(("PDF/X status: %s" % tet.pcos_get_string(doc, "pdfx")))

        #print(("PDF/A status: %s" % tet.pcos_get_string(doc, "pdfa")))

        #print("    XFA data: %s" % \
         #   yesno(tet.pcos_get_number(doc, "type:/Root/AcroForm/XFA") != 0))

        #print(("  Tagged PDF: %s\n" % \
         #   yesno(tet.pcos_get_number(doc, "tagged"))))

        #print(("No. of pages: %d" % \
         #   int(tet.pcos_get_number(doc, "length:pages"))))

        #print((" Page 1 size: width=%g, height=%g" % \
         #   (tet.pcos_get_number(doc, "pages[%d]/width" % 0),
          #   tet.pcos_get_number(doc, "pages[%d]/height" % 0))))

        count = int(tet.pcos_get_number(doc, "length:fonts"))
        #print(("No. of fonts: %d" % count))

        for i in range(count):
            type = tet.pcos_get_string(doc, "fonts[%d]/type" % i)
            name = tet.pcos_get_string(doc, "fonts[%d]/name" % i)

          #  if (tet.pcos_get_number(doc, "fonts[%d]/embedded" % i)):
         #       print("embedded %s font %s" % (type, name))
           # else:
          #      print("unembedded %s font %s" % (type, name))

        #print()

        plainmetadata = \
                int(tet.pcos_get_number(doc, "encrypt/plainmetadata"))

        if (pcosmode == 1 and not plainmetadata and \
                int(tet.pcos_get_number(doc, "encrypt/nocopy"))):
            print("Restricted mode: no more information available\n")
            tet.close_document(doc)
            exit(0)

        # --------- document info keys and XMP metadata (requires master pw
        # or plaintext metadata)
        #

        count = int(tet.pcos_get_number(doc, "length:/Info"))

        for i in range(0, count):
            objtype = int(tet.pcos_get_number(doc, "type:/Info[%d]" % i))
            key = tet.pcos_get_string(doc, "/Info[%d].key" % i)

            # Info entries can be stored as string or name objects */
            # pcos_to_sting == 4; pcos_ot_name == 3
            #if (objtype == 4 or objtype == 3):
             #   print("%12s: '%10s'" % \
             #       (key, tet.pcos_get_string(doc, "/Info[%d]" % i)))
           # else:
            #    print("%12s: (%s object)" % \
#                    (key, tet.pcos_get_string(doc, "type:/Info[%d]" % i)))

        #print()

        objtype = int(tet.pcos_get_number(doc, "type:/Root/Metadata"))
        # pcos_ot_stream == 7
        if (objtype == 7):
            contents = tet.pcos_get_stream(doc, "", "/Root/Metadata")
            ustring = contents.decode('utf_8')
            #print("XMP meta data: %d bytes (%d Unicode characters)\n" % 
                #(len(contents), len(ustring)))
       # else:
        #    print("XMP meta data: not present\n")

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
