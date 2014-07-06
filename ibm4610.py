#!/usr/bin/python2

# example use: ibm4610.print_slip(printer, 220016, 310416376402461, 89014103233764024616, "Subscriber C")

#library for printing to an IBM 4610 in emulation mode

import random
import serial
from shadylogo import shadylogo

def get_printer(dev="/dev/ttyS0", baud=19200, timeout=3.0):
    return serial.Serial(dev, baudrate=baud, timeout=timeout)

def reset(printer):
    printer.write("\x10\x05\x40")

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
    printer.write("\x1D\x6B\x04{0}\x00".format(data))

def print_pdf417(printer, data):
    #limit 1000 characters
    printer.write("\x1D\x50{0}\x00".format(data))

def cut_paper(printer):
    printer.write("\x0C")

def print_logo(printer, logo, x, y, density="\x00"):
    printer.write("\x1B\x2A{0}{1}{2}{3}\x0A".format(density, chr(x/8), chr(y/8), logo))
    # The image!  It is bits in a line, opposite bit order (LSB is leftmost pixel), for lines.  Line widths are multiples of 8.
    # Then, you can print as many columns like that as you want.  But, alas, only so many characters in an image are supported (see manual).

def print_slip(printer, ext, imsi, iccid, name):
    set_codepage(printer, 1)
    print_logo(printer, shadylogo, 256, 184)
    set_charsize(printer, 4, 4)
    printer.write("\n")
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
    set_barcode_dimensions(printer, 50)
    print_code39_barcode(printer, ext)
    cut_paper(printer)
