# It-ebooks unwatermark.

Tool for cleaning all watermarks from books dawnloaded from http://it-ebooks.info.
Based on https://gist.github.com/Daxda/9939745

Usage:
```sh
⇒  python unwatermark.py -h
usage: unwatermark.py [-h] -f [FILES [FILES ...]] [--no-backup] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -f [FILES [FILES ...]], --files [FILES [FILES ...]]
                        One or more PDF files to remove it-ebook's watermarks.
  --no-backup           Disables the creating of backups for the files which
                        are being processed.
  -v, --verbose         Verbose output.
```
