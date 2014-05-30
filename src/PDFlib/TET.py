from tetlib_py import *

class TET(object):

    def __init__(self):
        self.__p = TET_new()
        TET_set_option(self.__p, "binding={python} objorient")

    # it is recommended not to use __del__ as it is not guaranteed
    # when this will be executed (see Python Esential Reference Page 94).
    # so we also implement a delete method and invalidate self.__p
    # whenever this will be called.
    def __del__(self):
        if (self.__p):
            TET_delete(self.__p)

    def delete(self):
        if (self.__p):
            TET_delete(self.__p)
        self.__p = 0

    def close_document(self, doc):
        TET_close_document(self.__p, doc)

    def close_page(self, page):
        TET_close_page(self.__p, page)

    def create_pvf(self, filename, data, optlist):
        TET_create_pvf(self.__p, filename, data, optlist)

    def delete_pvf(self, filename):
        return TET_delete_pvf(self.__p, filename)

    def get_apiname(self):
        return TET_get_apiname(self.__p)

    def get_char_info(self, page):
        return TET_get_char_info(self.__p, page)

    def get_errmsg(self):
        return TET_get_errmsg(self.__p)

    def get_errnum(self):
        return TET_get_errnum(self.__p)

    def get_image_data(self, doc, imageid, optlist):
        return TET_get_image_data(self.__p, doc, imageid, optlist)

    def get_image_info(self, page):
        return TET_get_image_info(self.__p, page)

    def get_text(self, page):
        return TET_get_text(self.__p, page)

    def info_pvf(self, filename, keyword):
        return TET_info_pvf(self.__p, filename, keyword)

    def open_document(self, filename, optlist):
        return TET_open_document(self.__p, filename, optlist)

    def open_document_mem(self, data, optlist):
        return TET_open_document_mem(self.__p, data, optlist)

    def open_page(self, doc, pagenumber, optlist):
        return TET_open_page(self.__p, doc, pagenumber, optlist)

    def pcos_get_number(self, doc, path):
        return TET_pcos_get_number(self.__p, doc, path)

    def pcos_get_string(self, doc, path):
        return TET_pcos_get_string(self.__p, doc, path)

    def pcos_get_stream(self, doc, optlist, path):
        return TET_pcos_get_stream(self.__p, doc, optlist, path)

    def set_option(self, optlist):
        TET_set_option(self.__p, optlist)

    def convert_to_unicode(self, inputformat, inputstring, optlist):
        return TET_convert_to_unicode(self.__p, inputformat, inputstring, optlist)

    def write_image_file(self, doc, imageid, optlist):
        return TET_write_image_file(self.__p, doc, imageid, optlist)

    def process_page(self, doc, pageno, optlist):
        return TET_process_page(self.__p, doc, pageno, optlist)

    def get_xml_data(self, doc, optlist):
        return TET_get_xml_data(self.__p, doc, optlist)

