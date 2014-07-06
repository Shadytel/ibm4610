#!/usr/bin/python2

#library for printing to an IBM 4610 in emulation mode

import random

def set_codepage(printer, page):
    # 0 CP437 USA
    # 1 CP858 Multilingual (default)
    # 5 Generic
    printer.write("\x1B\x74{0}".format(chr(page)))

def set_charsize(printer, width, height):
    # scale is multiplied by argument, from 1-8
    # in each dimension
    printer.write("\x1D\x21{0}".format(chr( ((width-1)<<4)+(height-1) )))

def set_barcode_dimensions(printer, height, width = 3):
    printer.write("\x1D\x68{0}".format(chr(height)))
    printer.write("\x1D\x77{0}".format(chr(width)))

def set_barcode_human_readable_text(printer, param):
    # 0 Suppress
    # 1 Above
    # 2 Below
    # 3 Both
    printer.write("\x1D\x48{0}".format(chr(param)))

def print_code39_barcode(printer, data):
    #data is constrained to [:digits:] in ASCII
    printer.write("\x1D\x6B\x04{}\x00".format(data))

def print_pdf417(printer, data):
    #limit 1000 characters
    printer.write("\x1D\x50{0}\x00".format(data))

def cut_paper(printer):
    printer.write("\x0C")

def print_slip(printer, ext, imsi, iccid, name):
    set_codepage(printer, 1)
    set_charsize(printer, 4, 4)
    printer.write("{0}".format(ext))
    set_charsize(printer, 1, 1)
    printer.write("\n\n")
    r = random.randrange(0, 99999)
    set_barcode_human_readable_text(printer, 0)
    print_pdf417(printer, "{0}/{1}/{2}/{3}/{4}".format(ext, imsi, iccid, name, r))
    printer.write("\n")
    printer.write(" IMSI: {0}\n".format(imsi))
    printer.write("ICCID: {0}\n".format(iccid))
    set_charsize(printer, 2, 2)
    printer.write(name)
    set_charsize(printer, 1, 1)
    printer.write("\n\n")
    set_barcode_dimensions(printer, 5)
    print_code39_barcode(printer, ext)
    cut_paper(printer)
