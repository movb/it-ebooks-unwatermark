import re
import shutil
import argparse
from os import path
from sys import stderr

#
#   Author: Daxda
#   Date:   02.04.2014
#   WTF:    This is a quick tool I've hacked together to easily remove the meta
#           information as well as the annoying link on each page of eBooks down-
#           loaded from it-ebooks.info. The modified file will hold the original
#           file name and the original file will be renamed to 'original.pdf.OLD'
#
#

# 'pattern' is the regex pattern which is used to remove the annotation elements,
# the rough structure of it looks like this:
#
#   obj
#   <<
#   /Type /Annot
#   /Subtype /Link
#   /Rect [ 264 91 348 79 ]   # The digits on this line will differ
#   /Border [ 0 0 0 ]         # The same goes for the digits on this line
#   /A <<
#   /Type /Action
#   /S /URI
#   /URI (http://www.it-ebooks.info/)
#   >>
#   >>
#   endobj
#

pattern = """0a2f54797065202f416e6e6f740a2f53756274797065202f4c696e6b0a2f526563
74205b20.*?205d0a2f426f7264657220.*?\n0a2f41203c3c0a2f54797065202f416374696f6e0
a2f53202f5552490a2f5552492028687474703a2f2f7777772e69742d65626f6f6b732e696e666f
2f290a3e3e""".replace("\n", "").strip()

def remove_evil_links(pdf_data):
    """ Removes all it-ebook's links and metadata from the passed PDF data. """
    pdf_data = pdf_data.encode("hex")
    # Remove each annotation element inside the PDF file (This removes the
    # "clickable" it-ebooks.info links)
    new_data = re.sub(pattern, "", pdf_data)
    # Remove the actual links (link elements which are assigned to the annotations)
    new_data = new_data.replace("www.it-ebooks.info".encode("hex"), "")
    return new_data.decode("hex")

def main(args):
    try:
        args.files = list(set(args.files))
        for file_path in args.files:
            if not file_path:
                continue
            if args.verbose:
                print("Processing: {0}".format(file_path))
            try:
                with open(file_path, "rb") as input_file:
                    pdf_data = input_file.read()
            except IOError as e:
                stderr.write("{0}: {1}\n".format(file_path, e.strerror))
                stderr.flush()
                continue

            # Backup the file with a different name
            if not args.no_backup:
                if args.verbose:
                    print("Creating backup: {0}.OLD".format(file_path))
                shutil.move(file_path, "{0}.OLD".format(file_path))

            # Modify the PDF file
            new_pdf_data = remove_evil_links(pdf_data)
            # Save the new file
            with open(file_path, "wb") as out_file:
                out_file.write(new_pdf_data)
            if args.verbose:
                print("Saving modified file: {0}".format(file_path))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files",
                        help="One or more PDF files to remove it-ebook's watermarks.",
                        nargs="*", required=True)
    parser.add_argument("--no-backup",
                        help="Disables the creating of backups for the files which"+\
                             " are being processed. ",
                        action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    main(args)